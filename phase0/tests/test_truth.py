"""Truth firewall: output may not contain skills absent from the profile."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase0.pack import prepare_pack
from phase0.qualify import load_job, load_profile
from phase0.truth import check_text

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
PROFILE = FIXTURES / "profile.yaml"


def test_checker_flags_skill_not_in_profile():
    profile = load_profile(PROFILE)
    lying = "Built production Kubernetes clusters on EKS using Go."
    violations = check_text(profile, lying)
    rules = {v.rule for v in violations}
    assert "ungrounded_skill" in rules
    excerpts = " ".join(v.excerpt.lower() for v in violations)
    assert "kubernetes" in excerpts


def test_checker_allows_skills_in_profile():
    profile = load_profile(PROFILE)
    honest = "Shipped Django APIs on PostgreSQL, containerised with Docker."
    assert check_text(profile, honest) == []


def test_yes_pack_contains_no_ungrounded_skill():
    profile = load_profile(PROFILE)
    job = load_job(FIXTURES / "jobs" / "yes-django-backend.yaml")
    pack = prepare_pack(profile, job)
    assert check_text(profile, pack.resume_text) == []
    assert check_text(profile, pack.letter_text) == []
    assert "kubernetes" not in pack.resume_text.lower()
    assert "django" in pack.resume_text.lower()


def test_exception_pack_names_gap_in_letter_not_on_resume():
    profile = load_profile(PROFILE)
    job = load_job(FIXTURES / "jobs" / "near-miss-k8s.yaml")
    pack = prepare_pack(profile, job, exception_for=["Kubernetes"])
    assert "kubernetes" not in pack.resume_text.lower()
    assert "kubernetes" in pack.letter_text.lower()
    assert check_text(profile, pack.resume_text) == []
    # Letter may name a missing skill as a gap; that is not a claim of possession.
    letter_violations = check_text(profile, pack.letter_text, allow_gap_mentions=["Kubernetes"])
    assert letter_violations == []


def test_prepare_pack_refuses_to_emit_if_resume_would_lie():
    """If generation stuffed a missing skill into the resume, emit is blocked."""
    from phase0 import pack as pack_mod

    profile = load_profile(PROFILE)
    job = load_job(FIXTURES / "jobs" / "yes-django-backend.yaml")

    original = pack_mod._render_resume

    def poisoned(profile, job, selection):
        text = original(profile, job, selection)
        return text + "\n- Production Kubernetes (EKS)\n"

    pack_mod._render_resume = poisoned
    try:
        from phase0.truth import TruthFailed

        with pytest.raises(TruthFailed):
            pack_mod.prepare_pack(profile, job)
    finally:
        pack_mod._render_resume = original
