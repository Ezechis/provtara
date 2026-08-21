from __future__ import annotations

from phase1.ingest import BOARD_HOMES, BOARD_URLS, SOURCES, is_it_role, job_from_remotive, merge_jobs
from phase0.qualify import job_from_dict


def test_four_verified_boards_are_wired():
    assert set(SOURCES) == {"remotive", "arbeitnow", "remoteok", "jobicy"}
    assert set(BOARD_URLS) == set(SOURCES) == set(BOARD_HOMES)


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
