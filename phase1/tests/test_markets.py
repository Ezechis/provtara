from __future__ import annotations

from pathlib import Path

from phase1.catalog import load_jobs
from phase1.markets import ecosystem_id, filter_jobs, market_id, work_mode
from phase0.qualify import job_from_dict

JOBS = Path(__file__).resolve().parents[1] / "data" / "jobs"


def test_seeded_african_markets_exist():
    jobs = load_jobs(JOBS)
    markets = {market_id(j) for j in jobs}
    assert "ng" in markets
    assert "ke" in markets
    assert "gh" in markets
    assert "za" in markets
    ng = [j for j in jobs if market_id(j) == "ng"]
    assert any(work_mode(j) == "onsite" for j in ng)
    assert any("Lagos" in (j.location or "") for j in ng)
    web3 = [j for j in jobs if ecosystem_id(j) == "web3"]
    assert web3
    assert filter_jobs(jobs, ecosystem="web3")


def test_filter_region_and_search():
    jobs = load_jobs(JOBS)
    ng = filter_jobs(jobs, region="ng")
    assert ng
    assert all(market_id(j) == "ng" for j in ng)
    pythonish = filter_jobs(jobs, q="backend")
    assert any("Backend" in j.title for j in pythonish)


def test_anywhere_vs_onsite():
    remote = job_from_dict(
        {
            "id": "t-remote",
            "title": "Engineer",
            "company": "X",
            "apply_url": "https://example.com/a",
            "remote": True,
            "must_haves": ["Python"],
            "location": "Worldwide",
            "hook": "Work from anywhere.",
            "description": "Work from anywhere on the team.",
            "min_years": 1,
            "work_authorization_any_of": ["ANY"],
        }
    )
    onsite = job_from_dict(
        {
            "id": "t-lagos",
            "title": "Engineer",
            "company": "Y",
            "apply_url": "https://example.com/b",
            "remote": False,
            "must_haves": ["Python"],
            "location": "Lagos, Nigeria",
            "hook": "Office in Lagos.",
            "description": "On-site in Lagos.",
            "min_years": 1,
            "work_authorization_any_of": ["NG"],
        }
    )
    assert work_mode(remote) == "anywhere"
    assert work_mode(onsite) == "onsite"
    assert market_id(onsite) == "ng"
