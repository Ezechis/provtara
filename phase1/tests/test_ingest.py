from __future__ import annotations

from phase1.ingest import (
    BOARD_HOMES,
    BOARD_URLS,
    SOURCES,
    keep_listing,
    is_it_role,
    job_from_remotive,
    merge_jobs,
)
from phase0.qualify import job_from_dict
from phase1.catalog import all_jobs


def test_verified_boards_are_wired():
    expected = {"remotive", "arbeitnow", "remoteok", "jobicy", "himalayas", "hnjobs"}
    assert set(SOURCES) == expected
    assert set(BOARD_URLS) == set(SOURCES) == set(BOARD_HOMES)
    assert "wwr" not in SOURCES
    assert "We Work Remotely" not in SOURCES.values()


def _sample_job(**overrides):
    data = {
        "id": "remotive-abc",
        "title": "Backend Engineer",
        "company": "Acme",
        "apply_url": "https://example.com/jobs/1",
        "remote": True,
        "must_haves": ["Python"],
        "nice_to_haves": [],
        "min_years": 2,
        "work_authorization_any_of": ["ANY"],
        "hook": "h",
        "description": "Python Django",
    }
    data.update(overrides)
    return job_from_dict(data)


def test_we_work_remotely_listings_are_dropped():
    wwr = _sample_job(
        id="wwr-deadbeef",
        apply_url="https://weworkremotely.com/remote-jobs/acme-backend",
    )
    via_other_board = _sample_job(
        id="remotive-deadbeef",
        apply_url="https://www.weworkremotely.com/remote-jobs/acme-backend",
    )
    copilot = _sample_job(
        id="himalayas-deadbeef",
        apply_url="https://jobcopilot.com/apply/xyz",
    )
    ok = _sample_job()
    assert keep_listing(wwr) is False
    assert keep_listing(via_other_board) is False
    assert keep_listing(copilot) is False
    assert keep_listing(ok) is True
    kept = all_jobs("/no/such/provtara-jobs-dir", [wwr, via_other_board, copilot, ok])
    ids = {j.id for j in kept}
    assert "wwr-deadbeef" not in ids
    assert "remotive-deadbeef" not in ids
    assert "himalayas-deadbeef" not in ids
    assert "remotive-abc" in ids


def test_rejects_sales_roles():
    assert is_it_role("Account Executive", "Sell our SaaS", []) is False
    assert is_it_role("Technical Recruiter", "Source engineers", ["recruiting"]) is False


def test_accepts_software_engineer():
    assert is_it_role("Backend Engineer", "Python Django APIs", ["python"]) is True


def test_map_remotive_software_job():
    item = {
        "id": 99,
        "url": "https://example.com/jobs/99",
        "title": "Python Developer",
        "company_name": "Acme",
        "category": "software-dev",
        "candidate_required_location": "Anywhere",
        "description": "<p>Build Django services with PostgreSQL and Docker.</p>",
    }
    job = job_from_remotive(item)
    assert job is not None
    assert job.title == "Python Developer"
    assert job.company == "Acme"
    assert job.remote is True
    assert "Django" in job.must_haves or "Python" in job.must_haves
    assert "Kubernetes" not in job.must_haves or "django" in job.description.lower()


def test_live_listing_uses_role_skills_not_catalog_order():
    item = {
        "id": 100,
        "url": "https://example.com/jobs/100",
        "title": "Backend Engineer",
        "company_name": "Acme",
        "category": "software-dev",
        "description": (
            "We are hiring a Backend Engineer. You will work with Python and Django. "
            "Our stack also includes AWS, Java, Kubernetes, Terraform, Kafka, Docker, "
            "PostgreSQL, Git, and Linux. Nice to have: TensorFlow, FastAPI. 3+ years."
        ),
    }
    job = job_from_remotive(item)
    assert job is not None
    assert "Python" in job.must_haves
    assert "Django" in job.must_haves
    assert "Kubernetes" not in job.must_haves
    assert "TensorFlow" not in job.must_haves
    assert "FastAPI" not in job.must_haves


def test_english_go_is_not_a_must_have():
    item = {
        "id": 101,
        "url": "https://example.com/jobs/101",
        "title": "Backend Engineer",
        "company_name": "Acme",
        "category": "software-dev",
        "description": (
            "<p>You will go to production with Python and Django. "
            "Docker and PostgreSQL.</p>"
        ),
    }
    job = job_from_remotive(item)
    assert job is not None
    assert "Go" not in job.must_haves
    assert "Golang" not in job.must_haves
    assert "Python" in job.must_haves or "Django" in job.must_haves


def test_map_remotive_skips_design_category():
    item = {
        "id": 2,
        "url": "https://example.com/design",
        "title": "Senior Graphic Designer",
        "company_name": "Acme",
        "category": "design",
        "description": "Figma and software branding.",
    }
    assert job_from_remotive(item) is None


def test_map_remotive_skips_non_it():
    item = {
        "id": 1,
        "url": "https://example.com/sales",
        "title": "Sales Manager",
        "company_name": "Acme",
        "category": "sales",
        "description": "Hit quota",
    }
    assert job_from_remotive(item) is None


def test_merge_dedupes_by_apply_url():
    a = job_from_dict(
        {
            "id": "a",
            "title": "A",
            "company": "X",
            "apply_url": "https://ex.com/1",
            "remote": True,
            "must_haves": ["Python"],
            "nice_to_haves": [],
            "min_years": 2,
            "work_authorization_any_of": ["ANY"],
            "hook": "h",
            "description": "d",
        }
    )
    b = job_from_dict(
        {
            "id": "b",
            "title": "B",
            "company": "Y",
            "apply_url": "https://ex.com/1",
            "remote": True,
            "must_haves": ["Python"],
            "nice_to_haves": [],
            "min_years": 2,
            "work_authorization_any_of": ["ANY"],
            "hook": "h",
            "description": "d",
        }
    )
    merged = merge_jobs([a], [b])
    assert len(merged) == 1
    assert merged[0].id == "a"
