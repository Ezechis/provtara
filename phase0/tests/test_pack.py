from __future__ import annotations

from pathlib import Path

from phase0.pack import prepare_pack
from phase0.qualify import load_job, load_profile

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
PROFILE = FIXTURES / "profile.yaml"


def test_harbor_pack_is_a_full_job_specific_resume():
    profile = load_profile(PROFILE)
    job = load_job(FIXTURES / "jobs" / "yes-django-backend.yaml")
    pack = prepare_pack(profile, job)
    resume = pack.resume_text
    letter = pack.letter_text
    assert "Kubernetes" not in resume
    assert "Kubernetes" not in letter
    assert "Harbor Ledger" in resume
    assert "Backend Engineer" in resume
    assert "NimbusPay" in resume
    assert "Coastline Labs" in resume
    assert "PROFESSIONAL SUMMARY" in resume
    assert "SKILLS MATCHED TO THIS VACANCY" in resume
    assert resume.index("Django") < resume.index("Linux")
    assert "Matched to this vacancy" in resume
    assert "targeting" in resume.lower()
    assert "Harbor Ledger" in resume
    assert "Every bullet is taken from" not in resume
    assert "I am applying for the Backend Engineer role at Harbor Ledger" in letter
    assert "auto-apply" not in letter.lower()
    assert "Django REST APIs" in letter


def test_exception_letter_still_names_the_gap_not_the_resume():
    profile = load_profile(PROFILE)
    job = load_job(FIXTURES / "jobs" / "near-miss-k8s.yaml")
    pack = prepare_pack(profile, job, exception_for=["Kubernetes"])
    assert "kubernetes" not in pack.resume_text.lower()
    assert "kubernetes" in pack.letter_text.lower()
    assert "gap" in pack.letter_text.lower()
