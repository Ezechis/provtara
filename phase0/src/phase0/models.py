from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True)
class Bullet:
    id: str
    text: str
    tags: tuple[str, ...]


@dataclass(frozen=True)
class Role:
    id: str
    employer: str
    title: str
    start: str
    end: str
    bullets: tuple[Bullet, ...]


@dataclass(frozen=True)
class Profile:
    name: str
    email: str
    location: str
    remote_ok: bool
    work_authorization: tuple[str, ...]
    career_start: date
    skills: tuple[str, ...]
    employers: tuple[str, ...]
    experience: tuple[Role, ...]
    summary: str
    education: tuple[str, ...] = ()
    phone: str = ""
    as_of: date = date(2026, 8, 20)

    @property
    def years_experience(self) -> float:
        days = (self.as_of - self.career_start).days
        return round(days / 365.25, 1)

    @property
    def skill_set(self) -> set[str]:
        return {canon(s) for s in self.skills}


@dataclass(frozen=True)
class Job:
    id: str
    title: str
    company: str
    apply_url: str
    remote: bool
    must_haves: tuple[str, ...]
    nice_to_haves: tuple[str, ...]
    min_years: int
    work_authorization_any_of: tuple[str, ...]
    hook: str
    description: str
    location: str = ""


@dataclass(frozen=True)
class GapRow:
    requirement: str
    evidence: list[str]
    verdict: str  # "met" | "not met"


@dataclass(frozen=True)
class FitScore:
    """Honest fit 0–100. Must-haves dominate; keyword stuffing does not count."""

    percent: int
    must_met: int
    must_total: int
    nice_met: int
    nice_total: int

    @property
    def band(self) -> str:
        if self.percent >= 80:
            return "high"
        if self.percent >= 50:
            return "mid"
        return "low"


@dataclass(frozen=True)
class QualifyResult:
    passed: bool
    failed_must_haves: list[str]
    exceptions: list[str]
    gaps: list[GapRow]
    fit: FitScore


@dataclass(frozen=True)
class Pack:
    resume_text: str
    letter_text: str
    gaps: list[GapRow]
    job_id: str


class GateFailed(Exception):
    """Job did not pass the qualification gate."""


class TruthFailed(Exception):
    """Generated text contained claims not in the evidence profile."""


ALIASES = {
    "postgres": "postgresql",
    "postgresql": "postgresql",
    "k8s": "kubernetes",
    "kubernetes": "kubernetes",
    "golang": "go",
    "go": "go",
    "rest apis": "rest",
    "rest api": "rest",
    "amazon eks": "eks",
}


def canon(name: str) -> str:
    key = " ".join(name.lower().strip().split())
    return ALIASES.get(key, key)
