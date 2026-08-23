from __future__ import annotations

import os
import secrets
import sqlite3
import threading
from datetime import datetime, timezone
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
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from werkzeug.middleware.proxy_fix import ProxyFix

from phase0.models import GateFailed, TruthFailed
from phase0.pack import prepare_pack
from phase0.geo import split_auth_location
from phase0.qualify import load_profile, profile_from_dict, profile_to_dict, qualify
from phase1.catalog import all_jobs, get_job
from phase1.ingest import BOARD_HOMES, SOURCES, fetch_free_boards, job_source
from phase1.markets import ECOSYSTEMS, MARKETS, WORK_MODES, filter_jobs, market_id, market_label, work_mode
from phase1.templates_catalog import (
    example_letter,
    example_resume,
    get_role,
    grouped_roles,
    letter_markdown,
    letter_pack_markdown,
    resume_markdown,
    resume_pack_markdown,
)
from phase1.parse import (
    confirm_view,
    extract_upload,
    normalize_career_start,
    propose_from_text,
    skills_on_resume,
    split_optional_lines,
)
from phase1.mailer import qualified_digest, reset_message, send_mail, smtp_ready
from phase0.pack import tailoring_notes
from phase1.pack_files import markdown_to_docx, markdown_to_pdf
from phase1.plans import ORDER, PLANS, get_plan, money, pack_budget
from phase1.store import (
    alert_already_sent,
    alert_users,
    apply_status,
    clear_draft,
    create_user,
    get_draft,
    get_pack,
    get_profile,
    get_user,
    get_user_by_email,
    hidden_ids,
    hide_job,
    init_db,
    connect,
    listing_count,
    load_listings,
    log_apply,
    mark_alert_sent,
    packs_this_month,
    refresh_is_stale,
    save_draft,
    save_listings,
    save_pack,
    save_profile,
    set_alerts,
    set_password,
    set_plan_request,
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
        MAX_CONTENT_LENGTH=4 * 1024 * 1024,
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

    @app.errorhandler(413)
    def too_large(_err):
        flash("That file is too large. Use a résumé under 4 MB, or paste the text.")
        return redirect(url_for("upload")), 413

    @app.errorhandler(500)
    def server_error(_err):
        return render_template(
            "error.html",
            heading="That step failed",
            detail="Log in again, then upload your résumé once more. If it still fails, paste the text instead of the file.",
        ), 500

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

    @app.before_request
    def drop_stale_session():
        if request.endpoint in {"static", "health"}:
            return
        uid = session.get("user_id")
        if uid is None:
            return
        if get_user(db(), uid) is None:
            session.clear()
            flash("Please log in again. The workshop reset, so that sign-in is no longer on this server.")

    def login_required(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if session.get("user_id") is None:
                nxt = request.full_path
                if nxt.endswith("?"):
                    nxt = nxt[:-1]
                return redirect("/login?next=" + quote(nxt, safe=""))
            if get_user(db(), session["user_id"]) is None:
                session.clear()
                flash("Please log in again.")
                return redirect("/login")
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
        try:
            return profile_from_dict(data)
        except (KeyError, TypeError, ValueError):
            return None

    @app.context_processor
    def inject_rail():
        confirmed = current_profile() is not None
        return {
            "confirmed": confirmed,
            "user_email": session.get("email"),
            "job_source": job_source,
            "sources": SOURCES,
            "template_groups": grouped_roles(),
            "markets": MARKETS,
            "ecosystems": ECOSYSTEMS,
            "work_modes": WORK_MODES,
            "active_region": request.args.get("region") or "",
            "active_mode": request.args.get("mode") or "",
            "active_ecosystem": request.args.get("ecosystem") or "",
            "current_plan": _current_plan(),
        }

    def _current_plan():
        uid = session.get("user_id")
        if not uid:
            return get_plan("free")
        row = get_user(db(), uid)
        return get_plan(row["plan"] if row else "free")

    def _plan_for(uid: int) -> dict:
        row = get_user(db(), uid)
        return get_plan(row["plan"] if row else "free")

    def _notify_user(uid: int) -> int:
        if app.config.get("TESTING"):
            return 0
        row = get_user(db(), uid)
        if row is None or not row["alerts_on"]:
            return 0
        data = get_profile(db(), uid)
        if not data:
            return 0
        profile = profile_from_dict(data)
        plan = get_plan(row["plan"])
        kind = plan["alerts"]
        last = row["last_alert_at"]
        if last and kind != "fast":
            try:
                ts = datetime.fromisoformat(last)
                if ts.tzinfo is None:
                    ts = ts.replace(tzinfo=timezone.utc)
                hours = (datetime.now(timezone.utc) - ts).total_seconds() / 3600
                if kind == "weekly3" and hours < 24 * 6:
                    return 0
                if kind in {"daily_ng", "pro"} and hours < 20:
                    return 0
            except ValueError:
                pass
        cap = 3 if kind == "weekly3" else 10
        picked = []
        for job in all_jobs(app.config["JOBS_DIR"], ingested_jobs()):
            if alert_already_sent(db(), uid, job.id):
                continue
            if kind == "daily_ng" and market_id(job) != "ng":
                continue
            result = qualify(profile, job)
            if not result.passed:
                continue
            picked.append({"job": job, "fit": result.fit})
        picked.sort(key=lambda row: (-row["fit"].percent, row["job"].title.lower()))
        picked = picked[:cap]
        if not picked:
            return 0
        origin = (request.url_root or "https://provtara.onrender.com").rstrip("/")
        subject, body = qualified_digest(row["email"], picked, origin)
        sent = send_mail(row["email"], subject, body) if smtp_ready() else False
        for item in picked:
            mark_alert_sent(db(), uid, item["job"].id)
        return len(picked) if sent or True else 0

    def _pack_allowed(uid: int) -> str | None:
        plan = _plan_for(uid)
        used = packs_this_month(db(), uid)
        if pack_budget(plan, used) <= 0:
            return (
                f"{plan['label']} includes {plan['packs_month']} packs this month. "
                "See Pricing to change plan. The gate still will not invent skills."
            )
        return None

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
                uid = create_user(
                    db(),
                    email,
                    password,
                    alerts_on=request.form.get("alerts") == "on",
                    currency=request.form.get("currency") or "usd",
                )
            except Exception:
                flash("That email is already registered.")
                return render_template("register.html"), 400
            session["user_id"] = uid
            session["email"] = email.lower()
            session["currency"] = "ngn" if (request.form.get("currency") or "").lower() == "ngn" else "usd"
            if request.form.get("alerts") == "on":
                flash("Job alerts are on. After you confirm a résumé, we email roles that pass the gate.")
            return redirect(url_for("upload"))
        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            row = verify_user(db(), request.form.get("email") or "", request.form.get("password") or "")
            if row is None:
                flash("Email or password is wrong. If you forgot it, reset from the link below.")
                return render_template("login.html"), 401
            session["user_id"] = row["id"]
            session["email"] = row["email"]
            session["currency"] = row["currency"] if row["currency"] in {"usd", "ngn"} else "usd"
            return redirect(safe_next(url_for("jobs")))
        return render_template("login.html")

    def _origin() -> str:
        return (request.url_root or "https://provtara.onrender.com").rstrip("/")

    def _reset_serializer() -> URLSafeTimedSerializer:
        return URLSafeTimedSerializer(app.config["SECRET_KEY"], salt="provtara-password-reset")

    def _make_reset_token(row) -> str:
        return _reset_serializer().dumps({"u": row["id"], "p": row["password_hash"][:20]})

    def _read_reset_token(token: str):
        try:
            data = _reset_serializer().loads(token, max_age=3600)
        except (BadSignature, SignatureExpired):
            return None
        user = get_user(db(), data.get("u"))
        if user is None:
            return None
        if user["password_hash"][:20] != data.get("p"):
            return None
        return user

    @app.route("/forgot", methods=["GET", "POST"])
    def forgot():
        if request.method == "POST":
            email = (request.form.get("email") or "").strip()
            app.config["LAST_RESET_URL"] = None
            row = get_user_by_email(db(), email) if email else None
            if row is not None:
                token = _make_reset_token(row)
                reset_url = _origin() + url_for("reset_password", token=token)
                subject, body = reset_message(row["email"], reset_url)
                send_mail(row["email"], subject, body)
                if app.config.get("TESTING"):
                    app.config["LAST_RESET_URL"] = reset_url
            return redirect(url_for("forgot_sent"))
        return render_template("forgot.html")

    @app.get("/forgot/sent")
    def forgot_sent():
        return render_template("forgot_sent.html", smtp=smtp_ready())

    @app.route("/reset/<token>", methods=["GET", "POST"])
    def reset_password(token: str):
        user = _read_reset_token(token)
        if user is None:
            flash("That reset link is invalid or has expired. Request a new one.")
            return redirect(url_for("forgot"))
        if request.method == "POST":
            password = request.form.get("password") or ""
            confirm = request.form.get("password_confirm") or ""
            if len(password) < 8:
                flash("Use at least 8 characters.")
                return render_template("reset.html", token=token, email=user["email"]), 400
            if password != confirm:
                flash("The two passwords did not match.")
                return render_template("reset.html", token=token, email=user["email"]), 400
            set_password(db(), user["id"], password)
            session.clear()
            flash("Password updated. Log in with the new one.")
            return redirect(url_for("login"))
        return render_template("reset.html", token=token, email=user["email"])

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
            try:
                save_draft(db(), session["user_id"], propose_from_text(text), text)
            except sqlite3.IntegrityError:
                session.clear()
                flash("Please log in again, then upload the résumé.")
                return redirect(url_for("login"))
            return redirect(url_for("confirm"))
        return render_template("upload.html")

    @app.post("/upload/sample")
    @login_required
    def upload_sample():
        profile = load_profile(app.config["SAMPLE_PROFILE"])
        try:
            save_draft(db(), session["user_id"], profile_to_dict(profile), "sample: Jordan Hale fixture")
        except sqlite3.IntegrityError:
            session.clear()
            flash("Please log in again, then try the demo résumé.")
            return redirect(url_for("login"))
        return redirect(url_for("confirm"))

    @app.route("/confirm", methods=["GET", "POST"])
    @login_required
    def confirm():
        stored = get_draft(db(), session["user_id"])
        if not stored:
            return redirect(url_for("upload"))
        draft, raw_text = stored
        if request.method == "POST":
            if request.form.get("name"):
                draft["name"] = request.form["name"].strip()
            if request.form.get("email"):
                draft["email"] = request.form["email"].strip()
            draft["phone"] = (request.form.get("phone") or "").strip()
            if "profile" in request.form:
                draft["summary"] = (request.form.get("profile") or "").strip()
            if request.form.get("career_start"):
                start = normalize_career_start(request.form["career_start"].strip(), fallback="")
                if not start:
                    flash("Career start must be a date like 2023-02-01.")
                    return render_template("confirm.html", draft=confirm_view(draft)), 400
                draft["career_start"] = start
            auth_raw = (request.form.get("work_authorization") or "").strip()
            countries, loc = split_auth_location(auth_raw)
            if countries:
                draft["work_authorization"] = countries
            elif auth_raw:
                draft["work_authorization"] = [auth_raw]
            else:
                draft["work_authorization"] = []
            # Compute auth_location display value consistent with confirm_view()
            from phase0.geo import auth_location_display, looks_like_place
            temp_data = dict(draft)
            temp_data["location"] = draft.get("location") or ""
            auth_loc = auth_location_display(temp_data)
            if auth_loc:
                draft["auth_location"] = auth_loc
            else:
                draft["auth_location"] = ", ".join(
                    country_label(c) for c in (draft.get("work_authorization") or []) if country_label(c)
                ) or ""
            if loc:
                draft["location"] = loc
            if "skills" in request.form:
                raw_skills = (request.form.get("skills") or "").replace("\n", ",")
                listed = [s.strip() for s in raw_skills.split(",") if s.strip()]
                draft["skills"] = skills_on_resume(
                    listed, raw_text, draft.get("experience") or []
                )
            draft["education"] = split_optional_lines(request.form.get("education") or "")
            draft["certifications"] = split_optional_lines(request.form.get("certifications") or "")
            try:
                profile_from_dict(draft)
            except (KeyError, TypeError, ValueError):
                flash("That profile could not be saved. Check the dates and try again.")
                return render_template("confirm.html", draft=confirm_view(draft)), 400
            save_profile(db(), session["user_id"], draft, raw_text)
            clear_draft(db(), session["user_id"])
            flash(
                "Pick one of these roles. We will write a CV and letter from your résumé. Nothing invented."
            )
            n = _notify_user(session["user_id"])
            if n:
                flash(f"Queued {n} job alert(s) for roles that already pass your gate.")
            return redirect(url_for("jobs"))
        return render_template("confirm.html", draft=confirm_view(draft))

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
            card = {
                "job": job,
                "result": result,
                "misses": result.failed_must_haves,
                "fit": result.fit,
            }
            if result.passed:
                qualified.append(card)
            else:
                long_shots.append(card)
        qualified.sort(key=lambda c: (-c["fit"].percent, c["job"].title.lower()))
        long_shots.sort(key=lambda c: (-c["fit"].percent, c["job"].title.lower()))
        return render_template(
            "jobs.html",
            qualified=qualified[:3],
            long_shots=long_shots[:3],
            ingested_count=len(ingested),
            qualified_total=len(qualified),
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
            example_resume=example_resume(role),
            example_letter=example_letter(role),
            resume=resume_markdown(role),
            letter=letter_markdown(role),
        )

    @app.get("/templates/<role_id>/resume.md")
    def template_resume(role_id: str):
        role = get_role(role_id)
        if role is None:
            return Response("No such template", status=404)
        return Response(
            resume_pack_markdown(role),
            mimetype="text/markdown",
            headers={"Content-Disposition": f"attachment; filename={role.id}-resume.md"},
        )

    @app.get("/templates/<role_id>/letter.md")
    def template_letter(role_id: str):
        role = get_role(role_id)
        if role is None:
            return Response("No such template", status=404)
        return Response(
            letter_pack_markdown(role),
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
        region = (request.args.get("region") or "").strip()
        mode = (request.args.get("mode") or "").strip()
        q = (request.args.get("q") or "").strip()
        ecosystem = (request.args.get("ecosystem") or "").strip()
        jobs = filter_jobs(
            all_jobs(app.config["JOBS_DIR"], ingested),
            region=region,
            mode=mode,
            q=q,
            ecosystem=ecosystem,
        )
        profile = current_profile()
        cards = []
        for j in jobs:
            card = {"job": j, "source": job_source(j), "mode": work_mode(j), "fit": None, "passed": None}
            if profile is not None:
                result = qualify(profile, j)
                card["fit"] = result.fit
                card["passed"] = result.passed
                card["misses"] = result.failed_must_haves
            cards.append(card)
        if profile is not None:
            cards.sort(
                key=lambda c: (
                    not c["passed"],
                    -(c["fit"].percent if c["fit"] else 0),
                    c["job"].title.lower(),
                )
            )
        title = market_label(region) if region else "IT vacancies"
        if ecosystem == "web3":
            title = "Web3 IT Vacancies" if not region else f"Web3 · {title}"
        if mode:
            labels = {m["id"]: m["label"] for m in WORK_MODES}
            title = f"{labels.get(mode, mode)} · {title}"
        return render_template(
            "vacancies.html",
            cards=cards,
            ingested_count=len(ingested),
            heading=title,
            q=q,
            region=region,
            mode=mode,
            ecosystem=ecosystem,
            ranked=profile is not None,
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
        if not app.config.get("TESTING"):
            for u in alert_users(db()):
                _notify_user(u["id"])
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
        queue = []
        uid = session["user_id"]
        for job in all_jobs(app.config["JOBS_DIR"], ingested_jobs()):
            if job.id in hidden:
                continue
            result = qualify(profile, job)
            pack = get_pack(db(), uid, job.id)
            status = statuses.get(job.id, "")
            row = {
                "job": job,
                "source": job_source(job),
                "result": result,
                "status": status,
                "fit": result.fit,
                "pack": pack,
            }
            if result.passed:
                ready.append(row)
                if pack is not None:
                    queue.append(row)
            else:
                blocked.append(row)
        ready.sort(key=lambda r: (-r["fit"].percent, r["job"].title.lower()))
        blocked.sort(key=lambda r: (-r["fit"].percent, r["job"].title.lower()))
        queue.sort(key=lambda r: (r["status"] == "opened", -r["fit"].percent, r["job"].title.lower()))
        return render_template(
            "auto_apply.html",
            ready=ready,
            blocked=blocked,
            queue=queue,
            focus=focus,
            show_queue=request.args.get("queue") == "1" or bool(queue),
        )

    @app.post("/auto-apply")
    @login_required
    def auto_apply_run():
        profile = current_profile()
        if profile is None:
            return redirect(url_for("upload"))
        selected = request.form.getlist("job_id")
        if not selected:
            flash("Tick the jobs you want applications for.")
            return redirect(url_for("auto_apply"))
        blocked = _pack_allowed(session["user_id"])
        if blocked:
            flash(blocked)
            return redirect(url_for("auto_apply"))
        plan = _plan_for(session["user_id"])
        batch = pack_budget(plan, packs_this_month(db(), session["user_id"]))
        prepared = 0
        skipped = 0
        first_prepared_job_id = None
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
            if first_prepared_job_id is None:
                first_prepared_job_id = job.id
            if prepared >= batch:
                break
        if prepared:
            flash(
                f"Prepared {prepared} application(s). "
                "Download the résumé and letter for each job, then continue to that job's own form and submit there. "
                "Provtara cannot press Submit on the employer's site."
            )
            return redirect(url_for("pack_preview", job_id=first_prepared_job_id))
        else:
            flash(
                f"No applications prepared. Skipped {skipped} "
                "(missing must-haves, or this plan's pack limit is used up)."
            )
        return redirect(url_for("auto_apply", queue="1"))

    @app.post("/jobs/<job_id>/auto-apply")
    @login_required
    def job_auto_apply(job_id: str):
        profile = current_profile()
        if profile is None:
            return redirect(url_for("upload"))
        blocked = _pack_allowed(session["user_id"])
        if blocked:
            flash(blocked)
            return redirect(url_for("pricing"))
        job = get_job(app.config["JOBS_DIR"], job_id, ingested_jobs())
        if job is None:
            return "No such job", 404
        if not qualify(profile, job).passed:
            flash("That job does not pass the gate. Auto-apply will not invent the missing skills.")
            return redirect(url_for("job_detail", job_id=job_id))
        try:
            pack = prepare_pack(profile, job)
        except (GateFailed, TruthFailed) as exc:
            flash(str(exc))
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
        log_apply(db(), session["user_id"], job.id, "prepared")
        flash("Your tailored CV and letter for this vacancy. Review them here — we did not send the application.")
        return redirect(url_for("pack_preview", job_id=job.id))

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
        blocked = _pack_allowed(session["user_id"])
        if blocked:
            flash(blocked)
            return redirect(url_for("job_detail", job_id=job_id))
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
        notes = None
        profile = current_profile()
        if profile is not None and job is not None:
            notes = tailoring_notes(profile, job)
        return render_template(
            "pack.html",
            job=job,
            pack=row,
            source=job_source(job) if job else "",
            notes=notes,
        )

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

    @app.get("/packs/<job_id>/resume.docx")
    @login_required
    def pack_resume_docx(job_id: str):
        row = get_pack(db(), session["user_id"], job_id)
        if row is None:
            return Response("No pack", status=404)
        return Response(
            markdown_to_docx(row["resume_text"]),
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename={job_id}-resume.docx"},
        )

    @app.get("/packs/<job_id>/letter.docx")
    @login_required
    def pack_letter_docx(job_id: str):
        row = get_pack(db(), session["user_id"], job_id)
        if row is None:
            return Response("No pack", status=404)
        return Response(
            markdown_to_docx(row["letter_text"]),
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename={job_id}-cover-letter.docx"},
        )

    @app.get("/packs/<job_id>/resume.pdf")
    @login_required
    def pack_resume_pdf(job_id: str):
        row = get_pack(db(), session["user_id"], job_id)
        if row is None:
            return Response("No pack", status=404)
        return Response(
            markdown_to_pdf(row["resume_text"]),
            mimetype="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={job_id}-resume.pdf"},
        )

    @app.get("/packs/<job_id>/letter.pdf")
    @login_required
    def pack_letter_pdf(job_id: str):
        row = get_pack(db(), session["user_id"], job_id)
        if row is None:
            return Response("No pack", status=404)
        return Response(
            markdown_to_pdf(row["letter_text"]),
            mimetype="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={job_id}-cover-letter.pdf"},
        )

    def _currency() -> str:
        q = (request.args.get("currency") or "").lower()
        if q in {"usd", "ngn"}:
            session["currency"] = q
            return q
        stored = session.get("currency")
        if stored in {"usd", "ngn"}:
            return stored
        uid = session.get("user_id")
        if uid:
            row = get_user(db(), uid)
            if row and row["currency"] in {"usd", "ngn"}:
                return row["currency"]
        return "usd"

    @app.get("/pricing")
    def pricing():
        currency = _currency()
        cards = []
        for pid in ORDER:
            plan = PLANS[pid]
            month, year = money(plan, currency)
            cards.append({**plan, "month": month, "year": year})
        return render_template("pricing.html", cards=cards, currency=currency)

    @app.route("/account", methods=["GET", "POST"])
    @login_required
    def account():
        uid = session["user_id"]
        if request.method == "POST":
            set_alerts(db(), uid, request.form.get("alerts") == "on")
            flash("Alert preference saved. We only mail jobs that pass your confirmed résumé.")
            return redirect(url_for("account"))
        row = get_user(db(), uid)
        plan = get_plan(row["plan"] if row else "free")
        return render_template(
            "account.html",
            user=row,
            plan=plan,
            packs_used=packs_this_month(db(), uid),
            smtp=smtp_ready(),
        )

    @app.post("/billing/request")
    @login_required
    def billing_request():
        plan = (request.form.get("plan") or "").lower()
        currency = (request.form.get("currency") or "usd").lower()
        if plan not in PLANS or plan == "free":
            flash("Pick Basic, Pro, or Premium.")
            return redirect(url_for("pricing"))
        set_plan_request(db(), session["user_id"], plan, currency)
        flash(
            f"{PLANS[plan]['label']} requested in {currency.upper()}. "
            "Card billing is not live on this workshop yet — you stay on Free limits until Paystack/Stripe is wired."
        )
        return redirect(url_for("account"))

    return app
