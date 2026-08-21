from __future__ import annotations

import os
import secrets
import threading
from functools import wraps
from pathlib import Path
from urllib.parse import quote

from flask import (
    Flask,
    Response,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.middleware.proxy_fix import ProxyFix

from phase0.models import GateFailed, TruthFailed
from phase0.pack import prepare_pack
from phase0.qualify import load_profile, profile_from_dict, profile_to_dict, qualify
from phase1.catalog import all_jobs, get_job
from phase1.ingest import BOARD_HOMES, SOURCES, fetch_free_boards, job_source
from phase1.templates_catalog import (
    get_role,
    grouped_roles,
    letter_markdown,
    resume_markdown,
)
from phase1.parse import extract_upload, grounded_skills, propose_from_text
from phase1.store import (
    apply_status,
    create_user,
    get_pack,
    get_profile,
    hidden_ids,
    hide_job,
    init_db,
    connect,
    listing_count,
    load_listings,
    log_apply,
    refresh_is_stale,
    save_listings,
    save_pack,
    save_profile,
    verify_user,
)

HERE = Path(__file__).resolve().parent
PHASE1_ROOT = HERE.parents[1]
JOB_PORTAL = PHASE1_ROOT.parent
DEFAULT_JOBS = PHASE1_ROOT / "data" / "jobs"
SAMPLE_PROFILE = JOB_PORTAL / "phase0" / "fixtures" / "profile.yaml"
TEMPLATE_DIR = PHASE1_ROOT / "templates"
STATIC_DIR = PHASE1_ROOT / "static"


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(
        __name__,
        template_folder=str(TEMPLATE_DIR),
        static_folder=str(STATIC_DIR),
    )
    instance = PHASE1_ROOT / "instance"
    instance.mkdir(exist_ok=True)
    secret = os.environ.get("SECRET_KEY")
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    if not secret or secret == "dev-change-me":
        secret = "dev-change-me" if debug else secrets.token_hex(32)
    app.config.from_mapping(
        SECRET_KEY=secret,
        DATABASE=str(instance / "workshop.db"),
        JOBS_DIR=str(DEFAULT_JOBS),
        SAMPLE_PROFILE=str(SAMPLE_PROFILE),
    )
    if not debug:
        app.config.update(
            SESSION_COOKIE_SECURE=True,
            SESSION_COOKIE_HTTPONLY=True,
            SESSION_COOKIE_SAMESITE="Lax",
            PREFERRED_URL_SCHEME="https",
        )
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
    if test_config:
        app.config.update(test_config)

    def db():
        if "db" not in g:
            g.db = connect(app.config["DATABASE"])
            init_db(g.db)
        return g.db

    @app.teardown_appcontext
    def close_db(_exc):
        conn = g.pop("db", None)
        if conn is not None:
            conn.close()

    def login_required(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if session.get("user_id") is None:
                nxt = request.full_path
                if nxt.endswith("?"):
                    nxt = nxt[:-1]
                return redirect("/login?next=" + quote(nxt, safe=""))
            return view(*args, **kwargs)

        return wrapped

    def safe_next(default: str) -> str:
        nxt = request.args.get("next") or request.form.get("next") or default
        if not nxt.startswith("/") or nxt.startswith("//"):
            return default
        return nxt

    def current_profile():
        uid = session.get("user_id")
        if not uid:
            return None
        data = get_profile(db(), uid)
        if not data:
            return None
        return profile_from_dict(data)

    @app.context_processor
    def inject_rail():
        confirmed = current_profile() is not None
        return {
            "confirmed": confirmed,
            "user_email": session.get("email"),
            "job_source": job_source,
            "sources": SOURCES,
            "template_groups": grouped_roles(),
        }

    def ingested_jobs():
        return load_listings(db())

    ingest_lock = threading.Lock()

    def maybe_ingest():
        if app.config.get("TESTING"):
            return
        if listing_count(db()) > 0:
            return
        if not ingest_lock.acquire(blocking=False):
            return
        db_path = app.config["DATABASE"]

        def work():
            try:
                fetched, _errors = fetch_free_boards()
                conn = connect(db_path)
                try:
                    init_db(conn)
                    save_listings(conn, fetched)
                finally:
                    conn.close()
            finally:
                ingest_lock.release()

        threading.Thread(target=work, daemon=True, name="provtara-ingest").start()

    def pull_boards():
        fetched, errors = fetch_free_boards()
        n = save_listings(db(), fetched)
        msg = f"Pulled {n} IT jobs from verified boards."
        if errors:
            msg += " Some boards failed: " + ", ".join(f"{k} ({v})" for k, v in errors.items())
        return n, errors, msg

    @app.get("/")
    def landing():
        maybe_ingest()
        return render_template("landing.html", vacancy_count=listing_count(db()))

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            email = (request.form.get("email") or "").strip()
            password = request.form.get("password") or ""
            if not email or not password or len(password) < 8:
                flash("Email and a password of at least 8 characters are required.")
                return render_template("register.html"), 400
            try:
                uid = create_user(db(), email, password)
            except Exception:
                flash("That email is already registered.")
                return render_template("register.html"), 400
            session["user_id"] = uid
            session["email"] = email.lower()
            return redirect(url_for("upload"))
        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            row = verify_user(db(), request.form.get("email") or "", request.form.get("password") or "")
            if row is None:
                flash("Email or password is wrong.")
                return render_template("login.html"), 401
            session["user_id"] = row["id"]
            session["email"] = row["email"]
            return redirect(safe_next(url_for("jobs")))
        return render_template("login.html")

    @app.post("/logout")
    def logout():
        session.clear()
        return redirect(url_for("landing"))

    @app.route("/upload", methods=["GET", "POST"])
    @login_required
    def upload():
        if request.method == "POST":
            text = (request.form.get("resume_text") or "").strip()
            uploaded = request.files.get("resume_file")
            if uploaded and uploaded.filename:
                try:
                    extracted = extract_upload(uploaded)
                except ValueError as exc:
                    flash(str(exc))
                    return render_template("upload.html"), 400
                except Exception:
                    flash("Could not read that file. Try DOCX, or paste the text.")
                    return render_template("upload.html"), 400
                text = (extracted + "\n" + text).strip()
            if not text:
                flash("Upload a PDF or DOCX, or paste the résumé text.")
                return render_template("upload.html"), 400
            session["draft"] = propose_from_text(text)
            session["raw_text"] = text
            return redirect(url_for("confirm"))
        return render_template("upload.html")

    @app.post("/upload/sample")
    @login_required
    def upload_sample():
        profile = load_profile(app.config["SAMPLE_PROFILE"])
        session["draft"] = profile_to_dict(profile)
        session["raw_text"] = "sample: Jordan Hale fixture"
        return redirect(url_for("confirm"))

    @app.route("/confirm", methods=["GET", "POST"])
    @login_required
    def confirm():
        draft = session.get("draft")
        if not draft:
            return redirect(url_for("upload"))
        if request.method == "POST":
            if request.form.get("name"):
                draft["name"] = request.form["name"].strip()
            if request.form.get("email"):
                draft["email"] = request.form["email"].strip()
            if request.form.get("location"):
                draft["location"] = request.form["location"].strip()
            if request.form.get("career_start"):
                draft["career_start"] = request.form["career_start"].strip()
            if request.form.get("work_authorization"):
                draft["work_authorization"] = [
                    a.strip() for a in request.form["work_authorization"].split(",") if a.strip()
                ]
            if request.form.get("skills"):
                draft["skills"] = [s.strip() for s in request.form["skills"].split(",") if s.strip()]
            bullets = []
            for role in draft.get("experience") or []:
                bullets.extend(role.get("bullets") or [])
            listed = draft.get("skills") or []
            draft["skills"] = grounded_skills(listed, bullets)
            save_profile(db(), session["user_id"], draft, session.get("raw_text") or "")
            session.pop("draft", None)
            flash("Profile confirmed. Skills without a bullet were struck.")
            return redirect(url_for("jobs"))
        return render_template("confirm.html", draft=draft)

    @app.get("/jobs")
    @login_required
    def jobs():
        profile = current_profile()
        if profile is None:
            return redirect(url_for("upload"))
        maybe_ingest()
        hidden = hidden_ids(db(), session["user_id"])
        ingested = ingested_jobs()
        qualified = []
        long_shots = []
        for job in all_jobs(app.config["JOBS_DIR"], ingested):
            if job.id in hidden:
                continue
            result = qualify(profile, job)
            card = {"job": job, "result": result, "misses": result.failed_must_haves}
            if result.passed:
                qualified.append(card)
            else:
                long_shots.append(card)
        return render_template(
            "jobs.html",
            qualified=qualified,
            long_shots=long_shots,
            ingested_count=len(ingested),
        )

    @app.get("/jobs/<job_id>")
    @login_required
    def job_detail(job_id: str):
        profile = current_profile()
        if profile is None:
            return redirect(url_for("upload"))
        job = get_job(app.config["JOBS_DIR"], job_id, ingested_jobs())
        if job is None:
            return "No such job", 404
        result = qualify(profile, job)
        return render_template("job.html", job=job, result=result, source=job_source(job))

    @app.get("/health")
    def health():
        maybe_ingest()
        return {"ok": True, "listings": listing_count(db())}

    @app.get("/templates")
    def templates_index():
        return render_template("templates_index.html")

    @app.get("/templates/<role_id>")
    def template_detail(role_id: str):
        role = get_role(role_id)
        if role is None:
            return "No such template", 404
        return render_template(
            "template.html",
            role=role,
            resume=resume_markdown(role),
            letter=letter_markdown(role),
        )

    @app.get("/templates/<role_id>/resume.md")
    def template_resume(role_id: str):
        role = get_role(role_id)
        if role is None:
            return Response("No such template", status=404)
        return Response(
            resume_markdown(role),
            mimetype="text/markdown",
            headers={"Content-Disposition": f"attachment; filename={role.id}-resume.md"},
        )

    @app.get("/templates/<role_id>/letter.md")
    def template_letter(role_id: str):
        role = get_role(role_id)
        if role is None:
            return Response("No such template", status=404)
        return Response(
            letter_markdown(role),
            mimetype="text/markdown",
            headers={"Content-Disposition": f"attachment; filename={role.id}-cover-letter.md"},
        )

    @app.get("/boards")
    def boards():
        items = [
            {"id": key, "name": SOURCES[key], "url": BOARD_HOMES[key]}
            for key in SOURCES
        ]
        return render_template("boards.html", boards=items)

    @app.get("/vacancies")
    def vacancies():
        maybe_ingest()
        ingested = ingested_jobs()
        jobs = all_jobs(app.config["JOBS_DIR"], ingested)
        cards = [{"job": j, "source": job_source(j)} for j in jobs]
        return render_template(
            "vacancies.html",
            cards=cards,
            ingested_count=len(ingested),
        )

    @app.get("/vacancies/<job_id>")
    def vacancy_detail(job_id: str):
        maybe_ingest()
        job = get_job(app.config["JOBS_DIR"], job_id, ingested_jobs())
        if job is None:
            return "No such job", 404
        profile = current_profile()
        result = qualify(profile, job) if profile else None
        return render_template(
            "vacancy.html",
            job=job,
            source=job_source(job),
            result=result,
        )

    @app.post("/jobs/refresh")
    def jobs_refresh():
        if app.config.get("TESTING"):
            flash("Live board pull is skipped in tests.")
            return redirect(safe_next(url_for("vacancies")))
        if listing_count(db()) > 0 and not refresh_is_stale(db()):
            flash("Boards were pulled recently. Apply directly on a listing, or wait a few minutes to refresh.")
            return redirect(safe_next(url_for("vacancies")))
        _n, _errors, msg = pull_boards()
        flash(msg)
        return redirect(safe_next(url_for("vacancies")))

    @app.get("/auto-apply")
    @login_required
    def auto_apply():
        profile = current_profile()
        if profile is None:
            return redirect(url_for("upload"))
        maybe_ingest()
        statuses = apply_status(db(), session["user_id"])
        hidden = hidden_ids(db(), session["user_id"])
        focus = request.args.get("job") or ""
        ready = []
        blocked = []
        for job in all_jobs(app.config["JOBS_DIR"], ingested_jobs()):
            if job.id in hidden:
                continue
            result = qualify(profile, job)
            row = {
                "job": job,
                "source": job_source(job),
                "result": result,
                "status": statuses.get(job.id, ""),
            }
            if result.passed:
                ready.append(row)
            else:
                blocked.append(row)
        return render_template("auto_apply.html", ready=ready, blocked=blocked, focus=focus)

    @app.post("/auto-apply")
    @login_required
    def auto_apply_run():
        profile = current_profile()
        if profile is None:
            return redirect(url_for("upload"))
        selected = request.form.getlist("job_id")[:10]
        prepared = 0
        skipped = 0
        for job_id in selected:
            job = get_job(app.config["JOBS_DIR"], job_id, ingested_jobs())
            if job is None:
                skipped += 1
                continue
            result = qualify(profile, job)
            if not result.passed:
                skipped += 1
                continue
            try:
                pack = prepare_pack(profile, job)
            except (GateFailed, TruthFailed):
                skipped += 1
                continue
            gaps = ["| Requirement | Evidence | Verdict |", "|---|---|---|"]
            for row in pack.gaps:
                ev = ", ".join(row.evidence) if row.evidence else "—"
                gaps.append(f"| {row.requirement} | {ev} | {row.verdict} |")
            save_pack(
                db(),
                session["user_id"],
                job.id,
                pack.resume_text,
                pack.letter_text,
                "\n".join(gaps) + "\n",
            )
            log_apply(db(), session["user_id"], job.id, "prepared")
            prepared += 1
        flash(
            f"Auto-apply prepared {prepared} pack(s). "
            f"Skipped {skipped} (failed gate or truth check). "
            "Open each official listing to apply. Provtara does not log into ATS or click Submit."
        )
        return redirect(url_for("auto_apply"))

    @app.post("/auto-apply/<job_id>/opened")
    @login_required
    def auto_apply_opened(job_id: str):
        log_apply(db(), session["user_id"], job_id, "opened")
        job = get_job(app.config["JOBS_DIR"], job_id, ingested_jobs())
        if job is None or not job.apply_url:
            return redirect(url_for("auto_apply"))
        return redirect(job.apply_url)

    @app.post("/jobs/<job_id>/hide")
    @login_required
    def job_hide(job_id: str):
        hide_job(db(), session["user_id"], job_id)
        return redirect(url_for("jobs"))

    @app.post("/jobs/<job_id>/pack")
    @login_required
    def job_pack(job_id: str):
        profile = current_profile()
        if profile is None:
            return redirect(url_for("upload"))
        job = get_job(app.config["JOBS_DIR"], job_id, ingested_jobs())
        if job is None:
            return "No such job", 404
        exceptions = [e for e in request.form.getlist("exception") if e]
        try:
            pack = prepare_pack(profile, job, exception_for=exceptions or None)
        except GateFailed as exc:
            flash(str(exc) + " No pack written. The system does not invent missing skills.")
            return redirect(url_for("job_detail", job_id=job_id))
        except TruthFailed as exc:
            flash(str(exc) + " Fix the claim, never the checker.")
            return redirect(url_for("job_detail", job_id=job_id))
        gaps = ["| Requirement | Evidence | Verdict |", "|---|---|---|"]
        for row in pack.gaps:
            ev = ", ".join(row.evidence) if row.evidence else "—"
            gaps.append(f"| {row.requirement} | {ev} | {row.verdict} |")
        save_pack(
            db(),
            session["user_id"],
            job.id,
            pack.resume_text,
            pack.letter_text,
            "\n".join(gaps) + "\n",
        )
        return redirect(url_for("pack_preview", job_id=job.id))

    @app.get("/packs/<job_id>")
    @login_required
    def pack_preview(job_id: str):
        row = get_pack(db(), session["user_id"], job_id)
        if row is None:
            return "No pack", 404
        job = get_job(app.config["JOBS_DIR"], job_id, ingested_jobs())
        return render_template("pack.html", job=job, pack=row, source=job_source(job) if job else "")

    def _pack_file(job_id: str, field: str, filename: str, mime: str):
        row = get_pack(db(), session["user_id"], job_id)
        if row is None:
            return Response("No pack", status=404)
        return Response(
            row[field],
            mimetype=mime,
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )

    @app.get("/packs/<job_id>/resume.md")
    @login_required
    def pack_resume(job_id: str):
        return _pack_file(job_id, "resume_text", "resume.md", "text/markdown")

    @app.get("/packs/<job_id>/cover_letter.md")
    @login_required
    def pack_letter(job_id: str):
        return _pack_file(job_id, "letter_text", "cover_letter.md", "text/markdown")

    @app.get("/packs/<job_id>/gap_table.md")
    @login_required
    def pack_gaps(job_id: str):
        return _pack_file(job_id, "gap_markdown", "gap_table.md", "text/markdown")

    return app
