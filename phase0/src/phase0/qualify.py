from __future__ import annotations

from datetime import date
from pathlib import Path

import yaml

from phase0.geo import auth_matches, country_label
from phase0.models import (
    Bullet,
    FitScore,
    GapRow,
    GateFailed,
    Job,
    Profile,
    QualifyResult,
    Role,
    canon,
)

MUST_WEIGHT = 80
NICE_WEIGHT = 20


def profile_from_dict(data: dict) -> Profile:
    roles = []
    for raw in data.get("experience") or []:
        bullets = tuple(
            Bullet(id=b["id"], text=b["text"], tags=tuple(b.get("tags") or []))
            for b in raw.get("bullets") or []
        )
        roles.append(
            Role(
                id=raw["id"],
                employer=raw["employer"],
                title=raw["title"],
                start=str(raw["start"]),
                end=str(raw["end"]),
                bullets=bullets,
            )
        )
    start = data["career_start"]
    if not isinstance(start, date):
        start = date.fromisoformat(str(start)[:10])
    return Profile(
        name=data["name"],
        email=data["email"],
        location=data["location"],
        remote_ok=bool(data.get("remote_ok")),
        work_authorization=tuple(data.get("work_authorization") or []),
        career_start=start,
        skills=tuple(data.get("skills") or []),
        employers=tuple(data.get("employers") or []),
        experience=tuple(roles),
        summary=data.get("summary") or "",
        education=tuple(data.get("education") or []),
        certifications=tuple(data.get("certifications") or []),
        phone=data.get("phone") or "",
    )


def profile_to_dict(profile: Profile) -> dict:
    return {
        "name": profile.name,
        "email": profile.email,
        "location": profile.location,
        "remote_ok": profile.remote_ok,
        "work_authorization": list(profile.work_authorization),
        "career_start": profile.career_start.isoformat(),
        "skills": list(profile.skills),
        "employers": list(profile.employers),
        "summary": profile.summary,
        "education": list(profile.education),
        "certifications": list(profile.certifications),
        "phone": profile.phone,
        "experience": [
            {
                "id": role.id,
                "employer": role.employer,
                "title": role.title,
                "start": role.start,
                "end": role.end,
                "bullets": [
                    {"id": b.id, "text": b.text, "tags": list(b.tags)}
                    for b in role.bullets
                ],
            }
            for role in profile.experience
        ],
    }


def load_profile(path: Path | str) -> Profile:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return profile_from_dict(data)


def job_from_dict(data: dict) -> Job:
    return Job(
        id=str(data["id"]),
        title=data["title"],
        company=data["company"],
        apply_url=data.get("apply_url") or "",
        remote=bool(data.get("remote")),
        must_haves=tuple(data.get("must_haves") or []),
        nice_to_haves=tuple(data.get("nice_to_haves") or []),
        min_years=int(data.get("min_years") or 0),
        work_authorization_any_of=tuple(data.get("work_authorization_any_of") or []),
        hook=data.get("hook") or "",
        description=data.get("description") or "",
        location=data.get("location") or "",
    )


def load_job(path: Path | str) -> Job:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return job_from_dict(data)


def _evidence_for(profile: Profile, requirement: str) -> list[str]:
    want = canon(requirement)
    hits: list[str] = []
    if want in profile.skill_set:
        for role in profile.experience:
            for bullet in role.bullets:
                if want in {canon(t) for t in bullet.tags}:
                    hits.append(bullet.id)
    return hits


def gap_table(profile: Profile, job: Job) -> list[GapRow]:
    rows: list[GapRow] = []
    for req in job.must_haves:
        ev = _evidence_for(profile, req)
        rows.append(GapRow(requirement=req, evidence=ev, verdict="met" if ev else "not met"))
    if job.min_years:
        ok = profile.years_experience + 0.05 >= float(job.min_years)
        rows.append(
            GapRow(
                requirement=f"{job.min_years}+ years",
                evidence=[f"{profile.years_experience} years since {profile.career_start.isoformat()}"]
                if ok
                else [],
                verdict="met" if ok else "not met",
            )
        )
    if job.work_authorization_any_of:
        ok = auth_matches(profile.work_authorization, job.work_authorization_any_of)
        names = [country_label(a) for a in job.work_authorization_any_of if country_label(a) != "ANY"]
        if any(str(a).upper() == "ANY" or country_label(a) == "ANY" for a in job.work_authorization_any_of):
            names.append("any")
        label = "Work authorization / location: " + " / ".join(names or ["any"])
        evidence = [country_label(a) for a in profile.work_authorization] if ok else []
        if profile.location:
            evidence = [profile.location] + [e for e in evidence if e.lower() not in profile.location.lower()]
        rows.append(
            GapRow(
                requirement=label,
                evidence=evidence,
                verdict="met" if ok else "not met",
            )
        )
    return rows


def _must_item_scores(profile: Profile, job: Job) -> list[float]:
    scores: list[float] = []
    for req in job.must_haves:
        scores.append(1.0 if _evidence_for(profile, req) else 0.0)
    if job.min_years:
        need = float(job.min_years)
        have = profile.years_experience
        if have + 0.05 >= need:
            scores.append(1.0)
        else:
            scores.append(min(1.0, max(0.0, have / need)))
    if job.work_authorization_any_of:
        scores.append(1.0 if auth_matches(profile.work_authorization, job.work_authorization_any_of) else 0.0)
    return scores


def _nice_item_scores(profile: Profile, job: Job) -> list[float]:
    return [1.0 if _evidence_for(profile, req) else 0.0 for req in job.nice_to_haves]


def score_fit(profile: Profile, job: Job) -> FitScore:
    """Percent of how far the evidenced profile covers this job.

    Must-haves, years, and work authorization are 80% of the score.
    Nice-to-haves are the remaining 20%. A skill with no tagged bullet
    is 0 — listing it on the résumé is not enough. The pack gate is
    still pass/fail; a high percent with a missing must-have is a long shot.
    """
    musts = _must_item_scores(profile, job)
    nices = _nice_item_scores(profile, job)
    if not musts and not nices:
        percent = 0
    elif not musts:
        percent = round((sum(nices) / len(nices)) * 100)
    else:
        must_avg = sum(musts) / len(musts)
        nice_avg = (sum(nices) / len(nices)) if nices else 1.0
        percent = round(must_avg * MUST_WEIGHT + nice_avg * NICE_WEIGHT)
    percent = max(0, min(100, percent))
    return FitScore(
        percent=percent,
        must_met=sum(1 for s in musts if s >= 1.0),
        must_total=len(musts),
        nice_met=sum(1 for s in nices if s >= 1.0),
        nice_total=len(nices),
    )


def qualify(
    profile: Profile,
    job: Job,
    exception_for: list[str] | None = None,
) -> QualifyResult:
    exceptions = list(exception_for or [])
    exception_set = {canon(x) for x in exceptions}
    gaps = gap_table(profile, job)
    failed: list[str] = []
    for row in gaps:
        if row.verdict == "met":
            continue
        # years / auth rows use the full requirement string; skills use the must-have name
        key = row.requirement
        if canon(key) in exception_set or key in exceptions:
            continue
        # "Kubernetes" must-have is the requirement string as listed
        if any(canon(key) == canon(x) for x in exceptions):
            continue
        failed.append(key)
    return QualifyResult(
        passed=not failed,
        failed_must_haves=failed,
        exceptions=exceptions,
        gaps=gaps,
        fit=score_fit(profile, job),
    )


def require_gate(profile: Profile, job: Job, exception_for: list[str] | None = None) -> QualifyResult:
    result = qualify(profile, job, exception_for=exception_for)
    if not result.passed:
        miss = ", ".join(result.failed_must_haves) or "requirements"
        raise GateFailed(f"{job.id} did not pass the gate: {miss}")
    return result
