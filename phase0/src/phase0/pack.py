from __future__ import annotations

import re
from pathlib import Path

from phase0.models import Job, Pack, Profile, Role, canon
from phase0.qualify import require_gate
from phase0.truth import TruthFailed, require_clean


def _fit_score(tags: tuple[str, ...], text: str, job: Job) -> int:
    tagset = {canon(t) for t in tags}
    blob = text.lower()
    score = 0
    for req in job.must_haves:
        key = canon(req)
        if key in tagset or re.search(r"(?<![a-z0-9])" + re.escape(key) + r"(?![a-z0-9])", blob):
            score += 3
    for req in job.nice_to_haves:
        key = canon(req)
        if key in tagset or re.search(r"(?<![a-z0-9])" + re.escape(key) + r"(?![a-z0-9])", blob):
            score += 1
    return score


def _score_bullet(tags: tuple[str, ...], job: Job) -> int:
    return _fit_score(tags, "", job)


def select_bullets(profile: Profile, job: Job) -> list[str]:
    ranked: list[tuple[int, str, str]] = []
    rest: list[tuple[int, str, str]] = []
    for role in profile.experience:
        for bullet in role.bullets:
            s = _fit_score(bullet.tags, bullet.text, job)
            item = (s, role.id, bullet.id)
            if s > 0:
                ranked.append(item)
            else:
                rest.append(item)
    ranked.sort(key=lambda x: (-x[0], x[1], x[2]))
    rest.sort(key=lambda x: (x[1], x[2]))
    return [b_id for _, _, b_id in ranked] + [b_id for _, _, b_id in rest]


def _bullet_by_id(profile: Profile, bullet_id: str):
    for role in profile.experience:
        for bullet in role.bullets:
            if bullet.id == bullet_id:
                return role, bullet
    raise KeyError(bullet_id)


def _recent_title(profile: Profile) -> str:
    for role in profile.experience:
        title = (role.title or "").strip()
        if title and title.lower() not in {"roles as stated", "role", "from résumé", "from resume"}:
            return title
    return "Software engineer"


def _overlap_skills(profile: Profile, job: Job) -> list[str]:
    have = profile.skill_set
    out: list[str] = []
    seen: set[str] = set()
    for req in (*job.must_haves, *job.nice_to_haves):
        key = canon(req)
        if key in have and key not in seen:
            seen.add(key)
            out.append(req)
    return out


def _ordered_skills(profile: Profile, job: Job) -> tuple[list[str], list[str]]:
    have = profile.skill_set
    lead: list[str] = []
    seen: set[str] = set()
    for req in (*job.must_haves, *job.nice_to_haves):
        key = canon(req)
        if key in have and key not in seen:
            seen.add(key)
            lead.append(req)
    extra = []
    for skill in profile.skills:
        key = canon(skill)
        if key not in seen:
            seen.add(key)
            extra.append(skill)
    return lead, extra


def _years_phrase(profile: Profile) -> str:
    years = int(profile.years_experience)
    if years < 1:
        return "early-career professional experience"
    if years == 1:
        return "1 year of professional experience"
    return f"{years} years of professional experience"


def _tailored_summary(profile: Profile, job: Job) -> str:
    overlap = _overlap_skills(profile, job)
    title = _recent_title(profile)
    employer = ""
    for role in profile.experience:
        if role.employer and role.employer.lower() not in {"from résumé", "from resume", "employer"}:
            employer = role.employer
            break
    bits = [
        f"{title} with {_years_phrase(profile)}"
        + (f", most recently at {employer}" if employer else "")
        + f", applying for {job.title} at {job.company}."
    ]
    if overlap:
        if len(overlap) == 1:
            lead = overlap[0]
        else:
            lead = ", ".join(overlap[:-1]) + ", and " + overlap[-1]
        bits.append(f"This version leads with evidenced {lead} — the tools this vacancy names that the confirmed résumé actually supports.")
    strongest = None
    best = -1
    for role in profile.experience:
        for bullet in role.bullets:
            s = _fit_score(bullet.tags, bullet.text, job)
            if s > best:
                best = s
                strongest = bullet.text.rstrip(".")
    if strongest:
        bits.append(f"Signature work: {strongest}.")
    original = (profile.summary or "").strip()
    if original and not original.lower().startswith("it candidate"):
        if original[-1] not in ".!?":
            original += "."
        if original.lower() not in " ".join(bits).lower():
            bits.append(original)
    return " ".join(bits)


def _ordered_role_bullets(role: Role, job: Job) -> list[str]:
    scored = [
        (_fit_score(b.tags, b.text, job), i, b.text)
        for i, b in enumerate(role.bullets)
    ]
    scored.sort(key=lambda x: (-x[0], x[1]))
    return [text for _, _, text in scored]


def _render_resume(profile: Profile, job: Job, selection: list[str]) -> str:
    selected = set(selection)
    lead, extra = _ordered_skills(profile, job)
    contact = [profile.email, profile.location]
    if profile.phone:
        contact.insert(1, profile.phone)
    auth = ", ".join(profile.work_authorization)
    lines = [
        profile.name,
        _recent_title(profile) + "  ·  " + job.title + ", " + job.company,
        " · ".join(p for p in contact if p),
    ]
    if auth:
        lines.append("Work authorization: " + auth)
    lines.extend(
        [
            "",
            "PROFESSIONAL SUMMARY",
            _tailored_summary(profile, job),
            "",
            "SKILLS ALIGNED TO THIS ROLE",
        ]
    )
    if lead:
        lines.append("Core for this vacancy: " + ", ".join(lead))
    if extra:
        lines.append("Also evidenced: " + ", ".join(extra))
    if not lead and not extra:
        lines.append("See confirmed résumé.")
    lines.extend(["", "EXPERIENCE"])
    for role in profile.experience:
        kept = [b for b in role.bullets if b.id in selected]
        if not kept:
            kept = list(role.bullets)
        texts = _ordered_role_bullets(
            Role(
                id=role.id,
                employer=role.employer,
                title=role.title,
                start=role.start,
                end=role.end,
                bullets=tuple(kept),
            ),
            job,
        )
        if not texts:
            continue
        lines.append(f"{role.title}, {role.employer} ({role.start} – {role.end})")
        for text in texts:
            lines.append(f"- {text}")
        lines.append("")
    if profile.education:
        lines.append("EDUCATION")
        for row in profile.education:
            lines.append(f"- {row}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def _render_letter(profile: Profile, job: Job, selection: list[str], exceptions: list[str]) -> str:
    overlap = _overlap_skills(profile, job)
    evid: list[str] = []
    for bid in selection:
        if len(evid) >= 4:
            break
        _, bullet = _bullet_by_id(profile, bid)
        evid.append(bullet.text.rstrip("."))
    title = _recent_title(profile)
    hook = (job.hook or "").strip()
    openers = [
        f"Dear {job.company} hiring team,",
        "",
        f"I am applying for the {job.title} role at {job.company}.",
    ]
    if hook:
        openers.append(
            f"{hook.rstrip('.')} I can contribute to that with work I have already shipped — not a stack I am borrowing for this letter."
        )
    elif overlap:
        openers.append(
            f"The vacancy calls for {', '.join(overlap[:4])}. Those are on the confirmed résumé, with bullets to match."
        )
    parts = openers + [""]
    if evid:
        if len(evid) == 1:
            parts.append(evid[0] + ".")
        else:
            body = ". ".join(evid) + "."
            parts.append(body)
        parts.append("")
    parts.append(
        f"I work as a {title.lower()} with {_years_phrase(profile)}, based in {profile.location}"
        + (" and available for remote work" if profile.remote_ok else "")
        + "."
    )
    parts.append("")
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
            "I would welcome the chance to take this further with your team.",
            "",
            profile.name,
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
    (out_dir / "gap_table.md").write_text("\n".join(gap_lines).strip() + "\n", encoding="utf-8")
