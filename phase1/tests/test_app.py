from __future__ import annotations

from pathlib import Path

import pytest

from phase1.plans import pack_budget, get_plan
from phase1.web import create_app

PHASE0 = Path(__file__).resolve().parents[2] / "phase0"
PROFILE = PHASE0 / "fixtures" / "profile.yaml"


@pytest.fixture
def client(tmp_path):
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test",
            "DATABASE": str(tmp_path / "test.db"),
            "JOBS_DIR": str(PHASE0 / "fixtures" / "jobs"),
        }
    )
    return app.test_client()


def _register_and_login(client, email="ada@example.com", password="correct-horse"):
    client.post("/register", data={"email": email, "password": password}, follow_redirects=True)
    return client.post("/login", data={"email": email, "password": password}, follow_redirects=True)


def test_landing_states_the_promise(client):
    r = client.get("/")
    assert r.status_code == 200
    body = r.get_data(as_text=True).lower()
    assert "nothing invented" in body or "never" in body
    assert "submit" in body.lower() or "you submit" in body.lower()
    assert "verified" in body
    assert 'href="/boards"' in r.get_data(as_text=True)
    assert "apply directly" in body
    assert "auto-apply" in body
    home = r.get_data(as_text=True)
    assert "Nigerian IT Vacancies" in home
    assert "Web3 IT Vacancies" in home
    assert "Upload Your Resume" in home
    assert "On-Site Jobs" in home
    assert "Work From Anywhere" in home
    assert 'name="q"' in home
    assert ">Vacancies<" not in home
    assert ">Confirm<" not in home
    assert ">Jobs you can do<" not in home
    for name in ("Remotive", "Arbeitnow", "RemoteOK", "Jobicy"):
        assert name not in home


def test_pricing_page_lists_naira_and_dollars(client):
    r = client.get("/pricing?currency=ngn")
    assert r.status_code == 200
    body = r.get_data(as_text=True).replace(",", "")
    assert "5000" in body
    assert "Basic" in r.get_data(as_text=True)
    assert "Premium" in r.get_data(as_text=True)
    usd = client.get("/pricing?currency=usd").get_data(as_text=True)
    assert "$9" in usd
    assert "$19" in usd


def test_pack_budget_never_exceeds_monthly_cap():
    free = get_plan("free")
    basic = get_plan("basic")
    assert pack_budget(free, 0) == free["auto_batch"]
    assert pack_budget(free, free["packs_month"]) == 0
    assert pack_budget(basic, basic["packs_month"] - 2) == 2
    assert pack_budget(basic, 0) == basic["auto_batch"]


def test_register_required_before_upload(client):
    r = client.get("/upload", follow_redirects=False)
    assert r.status_code in (302, 303)
    assert "/login" in r.headers["Location"]


def test_sample_profile_then_qualified_job_not_sre(client):
    _register_and_login(client)
    r = client.post("/upload/sample", follow_redirects=True)
    assert r.status_code == 200
    r = client.post("/confirm", data={"confirm": "1"}, follow_redirects=True)
    assert r.status_code == 200
    jobs = r.get_data(as_text=True)
    assert "Harbor Ledger" in jobs
    assert "Your matches" in jobs
    assert "Prepare" in jobs
    # SRE role is a long shot, not a prepare target
    r2 = client.get("/jobs/no-k8s-sre")
    page = r2.get_data(as_text=True)
    assert "Prepare application" not in page
    assert "not met" in page.lower() or "Not a fit" in page or "long shot" in page.lower()


def test_pack_download_has_no_kubernetes(client):
    _register_and_login(client)
    client.post("/upload/sample", follow_redirects=True)
    client.post("/confirm", data={"confirm": "1"}, follow_redirects=True)
    r = client.post("/jobs/yes-django-backend/pack", follow_redirects=True)
    assert r.status_code == 200
    page = r.get_data(as_text=True)
    assert "Harbor Ledger" in page
    dl = client.get("/packs/yes-django-backend/resume.md")
    assert dl.status_code == 200
    text = dl.get_data(as_text=True)
    assert "Kubernetes" not in text
    assert "Django" in text


def test_vacancies_are_public(client):
    r = client.get("/vacancies")
    assert r.status_code == 200
    body = r.get_data(as_text=True)
    assert "Harbor Ledger" in body
    assert "Apply directly" in body
    assert "Auto-apply" in body
    assert 'href="/boards"' in body
    assert "IT jobs published from verified" in body
    for name in ("Remotive", "Arbeitnow", "RemoteOK", "Jobicy"):
        assert f">{name}<" not in body


def test_boards_page_lists_verified_sources(client):
    r = client.get("/boards")
    assert r.status_code == 200
    body = r.get_data(as_text=True)
    assert "Remotive" in body
    assert "Arbeitnow" in body
    assert "RemoteOK" in body
    assert "Jobicy" in body
    assert "Himalayas" in body
    assert "We Work Remotely" in body
    assert "Hacker News Jobs" in body
    assert "https://remotive.com" in body
    assert "https://remoteok.com" in body
    assert "https://himalayas.app" in body


def test_auto_apply_requires_login(client):
    r = client.get("/auto-apply?job=yes-django-backend", follow_redirects=False)
    assert r.status_code in (302, 303)
    assert "/login" in r.headers["Location"]
    assert "auto-apply" in r.headers["Location"]


def test_auto_apply_skips_failed_gate(client):
    _register_and_login(client)
    client.post("/upload/sample", follow_redirects=True)
    client.post("/confirm", data={"confirm": "1"}, follow_redirects=True)
    r = client.post(
        "/auto-apply",
        data={"job_id": ["no-k8s-sre", "yes-django-backend"]},
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert client.get("/packs/no-k8s-sre/resume.md").status_code == 404
    yes = client.get("/packs/yes-django-backend/resume.md")
    assert yes.status_code == 200
    assert b"Kubernetes" not in yes.data


def test_jobs_rank_by_evidenced_fit_percent(client):
    _register_and_login(client)
    client.post("/upload/sample", follow_redirects=True)
    r = client.post("/confirm", data={"confirm": "1"}, follow_redirects=True)
    body = r.get_data(as_text=True)
    assert "Harbor Ledger" in body
    assert "100 percent evidenced fit" in body
    assert "84 percent evidenced fit" in body
    assert "29 percent evidenced fit" in body
    assert body.index("Harbor Ledger") < body.index("Quayline") < body.index("Northpeak")
    assert body.index("100 percent evidenced fit") < body.index("84 percent evidenced fit")
    assert body.index("84 percent evidenced fit") < body.index("29 percent evidenced fit")
    assert 'href="/jobs"' in body
    assert "Your matches" in body
    detail = client.get("/jobs/yes-django-backend").get_data(as_text=True)
    assert "100 percent evidenced fit" in detail
    assert "Gate pass" in detail
    near = client.get("/jobs/near-miss-k8s").get_data(as_text=True)
    assert "84 percent evidenced fit" in near
    assert "Gate failed" in near


def test_vacancies_bump_qualified_after_resume(client):
    public = client.get("/vacancies").get_data(as_text=True)
    assert "percent evidenced fit" not in public
    _register_and_login(client)
    client.post("/upload/sample", follow_redirects=True)
    client.post("/confirm", data={"confirm": "1"}, follow_redirects=True)
    body = client.get("/vacancies").get_data(as_text=True)
    assert "100 percent evidenced fit" in body
    assert body.index("Harbor Ledger") < body.index("Northpeak Cloud")
    assert "sorted by evidenced fit" in body.lower()


def test_register_and_login_have_show_password(client):
    for path in ("/register", "/login"):
        body = client.get(path).get_data(as_text=True)
        assert 'type="password"' in body
        assert "secret-toggle" in body
        assert "Show" in body


def test_resume_draft_stays_out_of_the_session_cookie(client):
    _register_and_login(client)
    blob = (
        "Jordan Hale\njordan.hale@example.com\nLagos, Nigeria\n"
        + ("Built Django REST APIs on PostgreSQL with Docker and pytest.\n" * 80)
    )
    r = client.post("/upload", data={"resume_text": blob}, follow_redirects=True)
    assert r.status_code == 200
    assert ">Confirm<" in r.get_data(as_text=True) or "Confirm" in r.get_data(as_text=True)
    with client.session_transaction() as sess:
        assert "draft" not in sess
        assert "raw_text" not in sess
    confirmed = client.post("/confirm", data={"confirm": "1"}, follow_redirects=True)
    assert confirmed.status_code == 200
    assert "Your matches" in confirmed.get_data(as_text=True)


def test_stale_login_does_not_500_on_upload(client):
    _register_and_login(client)
    with client.session_transaction() as sess:
        sess["user_id"] = 99999
        sess["email"] = "ghost@example.com"
    r = client.post("/upload/sample", follow_redirects=False)
    assert r.status_code != 500
    assert r.status_code in (302, 303)
    assert "/login" in r.headers["Location"]
    r2 = client.post(
        "/upload",
        data={"resume_text": "Ada\nada@example.com\nBuilt Django REST APIs on PostgreSQL."},
        follow_redirects=False,
    )
    assert r2.status_code != 500
    assert r2.status_code in (302, 303)


def test_cannot_pack_failed_gate(client):
    _register_and_login(client)
    client.post("/upload/sample", follow_redirects=True)
    client.post("/confirm", data={"confirm": "1"}, follow_redirects=True)
    r = client.post("/jobs/no-k8s-sre/pack", follow_redirects=True)
    assert r.status_code == 200
    assert b"GATE" in r.data or b"gate" in r.data or b"not invent" in r.data
    dl = client.get("/packs/no-k8s-sre/resume.md")
    assert dl.status_code == 404
