from __future__ import annotations

from pathlib import Path

from phase0.models import Job, Pack, Profile, canon
from phase0.qualify import qualify, require_gate
from phase0.truth import TruthFailed, require_clean


def _score_bullet(tags: tuple[str, ...], job: Job) -> int:
    tagset = {canon(t) for t in tags}
    score = 0
    for req in job.must_haves:
        if canon(req) in tagset:
            score += 2
    for req in job.nice_to_haves:
        if canon(req) in tagset:
            score += 1
    return score


def select_bullets(profile: Profile, job: Job) -> list[str]:
    ranked: list[tuple[int, str, str]] = []
    for role in profile.experience:
        for bullet in role.bullets:
            s = _score_bullet(bullet.tags, job)
            if s > 0:
                ranked.append((s, role.id, bullet.id))
    ranked.sort(key=lambda x: (-x[0], x[1], x[2]))
    return [b_id for _, _, b_id in ranked[:8]]


def _bullet_by_id(profile: Profile, bullet_id: str):
    for role in profile.experience:
        for bullet in role.bullets:
            if bullet.id == bullet_id:
                return role, bullet
    raise KeyError(bullet_id)


def _render_resume(profile: Profile, job: Job, selection: list[str]) -> str:
    skill_line = ", ".join(profile.skills)
    lines = [
        profile.name,
        f"{profile.email} · {profile.location}",
        f"Work authorization: {', '.join(profile.work_authorization)}",
        "",
        "SUMMARY",
        profile.summary,
        "",
        "SKILLS",
        skill_line,
        "",
        "EXPERIENCE",
    ]
    by_role: dict[str, list[str]] = {}
    role_meta: dict[str, str] = {}
    for bid in selection:
        role, bullet = _bullet_by_id(profile, bid)
        by_role.setdefault(role.id, []).append(bullet.text)
        role_meta[role.id] = f"{role.title}, {role.employer} ({role.start} – {role.end})"
    for role in profile.experience:
        if role.id not in by_role:
            continue
        lines.append(role_meta[role.id])
        for text in by_role[role.id]:
            lines.append(f"- {text}")
        lines.append("")
    lines.append(f"Prepared for: {job.title} at {job.company}")
    lines.append("Every bullet is taken from the confirmed evidence profile. None were invented.")
    return "\n".join(lines).strip() + "\n"


def _render_letter(profile: Profile, job: Job, selection: list[str], exceptions: list[str]) -> str:
    evid = []
    for bid in selection[:3]:
        _, bullet = _bullet_by_id(profile, bid)
        evid.append(bullet.text.rstrip("."))
    evidence_block = ". ".join(evid) + "."
    parts = [
        f"Dear {job.company} hiring team,",
        "",
        job.hook + " I can help with that using work I have already shipped — not a stack I am pretending to have.",
        "",
        evidence_block,
        "",
    ]
    if exceptions:
        missing = ", ".join(exceptions)
        parts.append(
            f"I do not have production {missing} experience. That is a real gap. "
            f"This letter names it instead of putting {missing} on the résumé. "
            "If you need that on day one, I am not the hire."
        )
        parts.append("")
    parts.extend(
        [
            f"I am based in {profile.location} and available for remote work.",
            "",
            "I will submit this pack myself. Please do not treat this as an auto-apply.",
            "",
            f"{profile.name}",
            profile.email,
        ]
    )
    return "\n".join(parts).strip() + "\n"


def prepare_pack(
    profile: Profile,
    job: Job,
    exception_for: list[str] | None = None,
) -> Pack:
    result = require_gate(profile, job, exception_for=exception_for)
    selection = select_bullets(profile, job)
    resume = _render_resume(profile, job, selection)
    letter = _render_letter(profile, job, selection, result.exceptions)
    require_clean(profile, resume, kind="resume")
    require_clean(
        profile,
        letter,
        kind="cover_letter",
        allow_gap_mentions=result.exceptions,
    )
    return Pack(resume_text=resume, letter_text=letter, gaps=result.gaps, job_id=job.id)


def write_pack(pack: Pack, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "resume.md").write_text(pack.resume_text, encoding="utf-8")
    (out_dir / "cover_letter.md").write_text(pack.letter_text, encoding="utf-8")
    gap_lines = ["| Requirement | Evidence | Verdict |", "|---|---|---|"]
    for row in pack.gaps:
        ev = ", ".join(row.evidence) if row.evidence else "—"
        gap_lines.append(f"| {row.requirement} | {ev} | {row.verdict} |")
    (out_dir / "gap_table.md").write_text("\n".join(gap_lines) + "\n", encoding="utf-8")
