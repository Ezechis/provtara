from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse

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


def test_confirm_page_shows_phone_profile_education_and_full_country(client):
    _register_and_login(client)
    client.post("/upload/sample", follow_redirects=True)
    page = client.get("/confirm").get_data(as_text=True)
    assert 'name="phone"' in page
    assert 'name="location"' not in page
    assert "Professional profile" in page
    assert "Work authorization / location" in page
    assert "Nigeria" in page
    assert ">NG<" not in page
    assert "Python" in page
    assert "Django" in page
    assert "Educational qualifications" in page
    assert "Certifications" in page
    assert "Not mandatory" in page
    saved = client.post(
        "/confirm",
        data={
            "confirm": "1",
            "name": "Jordan Hale",
            "email": "jordan.hale@example.com",
            "phone": "+234 801 000 0000",
            "profile": "Backend engineer shipping Django APIs.",
            "career_start": "2023-02-01",
            "work_authorization": "Lagos, Nigeria",
            "skills": "Python, Django, PostgreSQL, Docker",
            "education": "B.Sc Computer Science, University of Lagos",
            "certifications": "",
        },
        follow_redirects=True,
    )
    assert saved.status_code == 200
    assert "Your matches" in saved.get_data(as_text=True)
    assert "Harbor Ledger" in saved.get_data(as_text=True)
    pack = client.post("/jobs/yes-django-backend/pack", follow_redirects=True)
    text = client.get("/packs/yes-django-backend/resume.md").get_data(as_text=True)
    assert "+234 801 000 0000" in text
    assert "Nigeria" in text
    assert "Work authorization / location" in text
    assert "University of Lagos" in text
    assert "CERTIFICATIONS" not in text


def test_confirm_fields_stay_in_their_boxes(client):
    cv = """
Ezechi Kingsley
ezechi@example.com
+234 803 111 2222
Lagos, Nigeria
Results-driven IT professional, with eight years delivering network and cloud solutions for banks.

PROFESSIONAL SUMMARY
Network and backend engineer who ships Django APIs.

WORK EXPERIENCE
Network Engineer, MainOne, Jan 2020 – Present
- Designed Django REST APIs on PostgreSQL for the ops portal

EDUCATIONAL QUALIFICATIONS
B.Sc Computer Science, University of Lagos, 2014

CORE COMPETENCIES
Python, Django, PostgreSQL, Cisco

CERTIFICATIONS
CCNA
"""
    _register_and_login(client, email="qa-fields@example.com")
    r = client.post("/upload", data={"resume_text": cv}, follow_redirects=True)
    html = r.get_data(as_text=True)
    assert r.status_code == 200
    profile = re.search(r'name="profile"[^>]*>(.*?)</textarea>', html, re.S).group(1)
    auth = re.search(r'name="work_authorization"[^>]*value="([^"]*)"', html).group(1)
    skills = re.search(r'name="skills"[^>]*>(.*?)</textarea>', html, re.S).group(1)
    education = re.search(r'name="education"[^>]*>(.*?)</textarea>', html, re.S).group(1)
    certs = re.search(r'name="certifications"[^>]*>(.*?)</textarea>', html, re.S).group(1)
    assert "Network and backend engineer" in profile
    assert "Results-driven" not in auth
    assert "Nigeria" in auth
    assert "Lagos" in auth
    assert "Python" in skills
    assert "Cisco" in skills
    assert "University of Lagos" in education
    assert "CCNA" in certs


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
    assert "PROFESSIONAL SUMMARY" in text
    assert "Harbor Ledger" in text
    assert "SKILLS ALIGNED TO THIS ROLE" in text
    assert "NimbusPay" in text


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
    body = r.get_data(as_text=True)
    assert "Ready to send" in body
    assert "Continue this application" in body
    assert "Verified boards" not in body
    assert "You do not need board homepages" in body
    assert client.get("/packs/no-k8s-sre/resume.md").status_code == 404
    yes = client.get("/packs/yes-django-backend/resume.md")
    assert yes.status_code == 200
    assert b"Kubernetes" not in yes.data
    opened = client.post("/auto-apply/yes-django-backend/opened", follow_redirects=False)
    assert opened.status_code in (302, 303)
    assert "harbor-ledger" in (opened.headers.get("Location") or "")


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


def test_login_page_links_to_forgot_password(client):
    body = client.get("/login").get_data(as_text=True)
    assert 'href="/forgot"' in body
    assert "Forgot your password" in body


def test_forgot_unknown_email_does_not_reveal_missing_account(client):
    r = client.post("/forgot", data={"email": "nobody@example.com"}, follow_redirects=True)
    assert r.status_code == 200
    assert "If that address is registered" in r.get_data(as_text=True)
    assert not client.application.config.get("LAST_RESET_URL")


def test_forgot_password_email_path_sets_new_password(client):
    _register_and_login(client)
    client.post("/logout")
    sent = client.post("/forgot", data={"email": "ada@example.com"}, follow_redirects=True)
    assert sent.status_code == 200
    assert "If that address is registered" in sent.get_data(as_text=True)
    url = client.application.config.get("LAST_RESET_URL")
    assert url
    path = urlparse(url).path
    form = client.get(path)
    assert form.status_code == 200
    assert "Create a new password" in form.get_data(as_text=True)
    mismatch = client.post(
        path,
        data={"password": "new-password", "password_confirm": "other-one"},
        follow_redirects=True,
    )
    assert "did not match" in mismatch.get_data(as_text=True)
    saved = client.post(
        path,
        data={"password": "new-password", "password_confirm": "new-password"},
        follow_redirects=True,
    )
    assert saved.status_code == 200
    assert "Password updated" in saved.get_data(as_text=True)
    assert client.get(path, follow_redirects=False).status_code in (302, 303)
    old = client.post("/login", data={"email": "ada@example.com", "password": "correct-horse"})
    assert old.status_code == 401
    ok = client.post("/login", data={"email": "ada@example.com", "password": "new-password"})
    assert ok.status_code in (302, 303)


def test_bad_reset_token_asks_for_a_new_link(client):
    r = client.get("/reset/not-a-real-token", follow_redirects=True)
    assert r.status_code == 200
    body = r.get_data(as_text=True).lower()
    assert "invalid" in body or "expired" in body


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
