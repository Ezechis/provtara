from __future__ import annotations

from pathlib import Path

import pytest

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
    for name in ("Remotive", "Arbeitnow", "RemoteOK", "Jobicy"):
        assert name not in r.get_data(as_text=True)


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
    assert "https://remotive.com" in body
    assert "https://remoteok.com" in body


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


def test_cannot_pack_failed_gate(client):
    _register_and_login(client)
    client.post("/upload/sample", follow_redirects=True)
    client.post("/confirm", data={"confirm": "1"}, follow_redirects=True)
    r = client.post("/jobs/no-k8s-sre/pack", follow_redirects=True)
    assert r.status_code == 200
    assert b"GATE" in r.data or b"gate" in r.data or b"not invent" in r.data
    dl = client.get("/packs/no-k8s-sre/resume.md")
    assert dl.status_code == 404
