"""Qualification gate: only eminently qualified jobs get a pack."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase0.qualify import GateFailed, gap_table, load_job, load_profile, qualify, score_fit

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
PROFILE = FIXTURES / "profile.yaml"


@pytest.fixture
def profile():
    return load_profile(PROFILE)


def test_yes_job_passes_the_gate(profile):
    job = load_job(FIXTURES / "jobs" / "yes-django-backend.yaml")
    result = qualify(profile, job)
    assert result.passed is True
    assert result.failed_must_haves == []


def test_no_job_fails_the_gate(profile):
    job = load_job(FIXTURES / "jobs" / "no-k8s-sre.yaml")
    result = qualify(profile, job)
    assert result.passed is False
    assert "Kubernetes" in result.failed_must_haves
    assert "Go" in result.failed_must_haves


def test_near_miss_fails_without_exception(profile):
    job = load_job(FIXTURES / "jobs" / "near-miss-k8s.yaml")
    result = qualify(profile, job)
    assert result.passed is False
    assert result.failed_must_haves == ["Kubernetes"]


def test_near_miss_passes_with_exception(profile):
    job = load_job(FIXTURES / "jobs" / "near-miss-k8s.yaml")
    result = qualify(profile, job, exception_for=["Kubernetes"])
    assert result.passed is True
    assert result.exceptions == ["Kubernetes"]


def test_gap_table_marks_missing_skill_not_met(profile):
    job = load_job(FIXTURES / "jobs" / "near-miss-k8s.yaml")
    rows = gap_table(profile, job)
    k8s = next(r for r in rows if r.requirement == "Kubernetes")
    assert k8s.verdict == "not met"
    assert k8s.evidence == []


def test_gap_table_marks_python_met(profile):
    job = load_job(FIXTURES / "jobs" / "yes-django-backend.yaml")
    rows = gap_table(profile, job)
    python = next(r for r in rows if r.requirement == "Python")
    assert python.verdict == "met"
    assert python.evidence


def test_years_requirement_uses_profile_dates_not_padding(profile):
    job = load_job(FIXTURES / "jobs" / "no-k8s-sre.yaml")
    rows = gap_table(profile, job)
    years = next(r for r in rows if "years" in r.requirement.lower())
    assert years.verdict == "not met"


def test_prepare_pack_refuses_failed_gate(profile):
    from phase0.pack import prepare_pack

    job = load_job(FIXTURES / "jobs" / "no-k8s-sre.yaml")
    with pytest.raises(GateFailed):
        prepare_pack(profile, job)


def test_harbor_ledger_is_a_full_evidenced_fit(profile):
    job = load_job(FIXTURES / "jobs" / "yes-django-backend.yaml")
    fit = score_fit(profile, job)
    assert fit.percent == 100
    assert fit.must_met == fit.must_total
    assert fit.nice_met == fit.nice_total
    assert qualify(profile, job).fit.percent == 100


def test_near_miss_scores_high_but_still_fails_the_gate(profile):
    job = load_job(FIXTURES / "jobs" / "near-miss-k8s.yaml")
    fit = score_fit(profile, job)
    assert fit.percent == 84
    assert qualify(profile, job).passed is False


def test_sre_role_scores_low_without_k8s_go_or_us_auth(profile):
    job = load_job(FIXTURES / "jobs" / "no-k8s-sre.yaml")
    fit = score_fit(profile, job)
    assert fit.percent == 29
    assert fit.percent < 50


def test_confirmed_skill_counts_without_bullet_tag(profile):
    from dataclasses import replace

    job = load_job(FIXTURES / "jobs" / "yes-django-backend.yaml")
    new_roles = []
    for role in profile.experience:
        bullets = tuple(
            replace(b, tags=tuple(t for t in b.tags if t.lower() != "python"))
            for b in role.bullets
        )
        new_roles.append(replace(role, bullets=bullets))
    stripped = replace(profile, experience=tuple(new_roles))
    assert "python" in stripped.skill_set
    result = qualify(stripped, job)
    python = next(r for r in result.gaps if r.requirement == "Python")
    assert python.verdict == "met"
    assert result.passed is True


def test_skill_absent_from_resume_does_not_count(profile):
    from dataclasses import replace

    job = load_job(FIXTURES / "jobs" / "near-miss-k8s.yaml")
    assert "kubernetes" not in profile.skill_set
    assert qualify(profile, job).passed is False
    padded = replace(profile, skills=profile.skills + ("Kubernetes",))
    assert "kubernetes" in padded.skill_set
    assert qualify(padded, job).passed is True
