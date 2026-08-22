from __future__ import annotations

import io
import re
from datetime import date

from phase0.truth import SKILL_CATALOG

_EMAIL = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)
_YEAR = re.compile(r"\b(20\d{2})\b")
_PHONE = re.compile(r"(?:\+\d{1,3}[\s-]?)?(?:\(?\d{3,4}\)?[\s.-]?)\d{3}[\s.-]?\d{3,4}")
_MONTHS = r"jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?"
_DATE_SPAN = re.compile(
    rf"(?P<a>(?:(?:{_MONTHS})\.?\s+)?(?:19|20)\d{{2}})"
    rf"\s*[–\-—to]+\s*"
    rf"(?P<b>present|current|now|(?:(?:{_MONTHS})\.?\s+)?(?:19|20)\d{{2}})",
    re.I,
)
_SECTION = re.compile(
    r"^(experience|work (?:history|experience)|employment|professional experience|"
    r"education|academic|skills|technical skills|technologies|tech stack|"
    r"summary|profile|objective|projects|certifications)\s*:?$",
    re.I,
)
_TITLE_HINT = re.compile(
    r"\b(engineer|developer|analyst|manager|administrator|designer|scientist|"
    r"architect|specialist|consultant|intern|officer|lead|head of|director)\b",
    re.I,
)


def _skills_in(text: str) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for skill in SKILL_CATALOG:
        if re.search(r"(?<![A-Za-z0-9])" + re.escape(skill) + r"(?![A-Za-z0-9])", text, re.I):
            key = skill.lower()
            if key in seen:
                continue
            seen.add(key)
            found.append(skill)
    return found


def normalize_career_start(raw: str, fallback: str = "2023-01-01") -> str:
    value = (raw or "").strip()
    if re.fullmatch(r"\d{4}", value):
        value = f"{value}-01-01"
    elif re.fullmatch(r"\d{4}-\d{2}", value):
        value = f"{value}-01"
    try:
        parsed = date.fromisoformat(value[:10])
    except ValueError:
        return fallback
    this_year = date.today().year
    if parsed.year < 1990 or parsed.year > this_year:
        return fallback
    return parsed.isoformat()


def guess_work_authorization(text: str) -> list[str]:
    blob = (text or "").lower()
    found: list[str] = []
    if any(k in blob for k in ("nigeria", "lagos", "abuja", "port harcourt", "naija")):
        found.append("NG")
    return found


def grounded_skills(listed: list[str], bullets: list[dict]) -> list[str]:
    from phase0.models import canon

    evidenced: set[str] = set()
    for b in bullets:
        for tag in b.get("tags") or []:
            evidenced.add(canon(tag))
        evidenced.update(canon(s) for s in _skills_in(b.get("text") or ""))
    keep = []
    seen = set()
    for s in listed:
        c = canon(s)
        if c in evidenced and c not in seen:
            seen.add(c)
            keep.append(s)
    return keep


def extract_docx(data: bytes) -> str:
    from docx import Document

    doc = Document(io.BytesIO(data))
    parts = [p.text for p in doc.paragraphs if p.text]
    for table in doc.tables:
        for row in table.rows:
            parts.append(" ".join(c.text for c in row.cells))
    return "\n".join(parts)


def extract_pdf(data: bytes) -> str:
    text = ""
    try:
        from pypdf import PdfReader

        reader = PdfReader(io.BytesIO(data))
        chunks: list[str] = []
        for page in reader.pages:
            chunks.append(page.extract_text() or "")
        text = "\n".join(chunks)
    except Exception:
        text = ""
    if len(text.strip()) < 40:
        strings = re.findall(rb"\(([^)]{3,})\)", data)
        extra = "\n".join(s.decode("latin-1", "replace") for s in strings)
        text = f"{text}\n{extra}".strip()
    return text


def _looks_like_role_header(ln: str) -> bool:
    if len(ln) > 140:
        return False
    if _DATE_SPAN.search(ln) and _TITLE_HINT.search(ln):
        return True
    if _DATE_SPAN.search(ln) and re.search(r"[,|@]| at ", ln):
        return True
    if _TITLE_HINT.search(ln) and re.search(r"\s(at|,|\||—|-)\s", ln) and len(ln) < 100:
        return True
    return False


def _split_role_header(ln: str) -> tuple[str, str, str, str]:
    start, end = "", "present"
    span = _DATE_SPAN.search(ln)
    rest = ln
    if span:
        start = re.sub(r"\s+", " ", span.group("a")).strip()
        end = re.sub(r"\s+", " ", span.group("b")).strip()
        rest = (ln[: span.start()] + " " + ln[span.end() :]).strip(" ,|–—-")
    rest = re.sub(r"[()]", " ", rest)
    rest = re.sub(r"\s+", " ", rest).strip(" ,|-")
    at = re.search(r"\bat\s+(.+)$", rest, re.I)
    if at:
        title = rest[: at.start()].strip(" ,|-") or "Role"
        employer = at.group(1).strip(" ,|-") or "Employer"
        return title[:80], employer[:80], start or "—", end
    parts = [p.strip() for p in re.split(r"\s*[|,]\s*", rest) if p.strip()]
    title = parts[0] if parts else "Role"
    employer = parts[1] if len(parts) > 1 else (parts[0] if parts else "Employer")
    if len(parts) == 1:
        employer = "Employer"
    return title[:80], employer[:80], start or "—", end


def _clean_bullet(ln: str) -> str:
    return re.sub(r"^[\-•–*—]\s*", "", ln).strip()


def extract_upload(file_storage) -> str:
    name = (getattr(file_storage, "filename", None) or "").lower()
    data = file_storage.read()
    if hasattr(file_storage, "seek"):
        try:
            file_storage.seek(0)
        except Exception:
            pass
    if name.endswith(".docx"):
        return extract_docx(data)
    if name.endswith(".pdf"):
        return extract_pdf(data)
    if name.endswith(".txt") or name.endswith(".md") or name.endswith(".rtf"):
        return data.decode("utf-8", "replace")
    raise ValueError("Upload a PDF or DOCX, or paste the résumé text.")


def propose_from_text(text: str) -> dict:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    email_m = _EMAIL.search(text)
    email = email_m.group(0) if email_m else ""
    name = lines[0] if lines and "@" not in lines[0] else "Candidate"
    location = ""
    for ln in lines[:10]:
        if ln == name or "@" in ln:
            continue
        if _PHONE.fullmatch(re.sub(r"\s+", " ", ln)):
            continue
        if "," in ln and not _looks_like_role_header(ln):
            location = ln
            break
    phone = ""
    ph = _PHONE.search(text)
    if ph:
        phone = ph.group(0).strip()
    this_year = date.today().year
    years = [int(y) for y in _YEAR.findall(text) if 1995 <= int(y) <= this_year]
    career_start = normalize_career_start(f"{min(years)}-01-01" if years else "2023-01-01")
    listed_skills = _skills_in(text)

    section = ""
    roles: list[dict] = []
    education: list[str] = []
    summary_bits: list[str] = []
    loose: list[dict] = []
    current: dict | None = None

    def flush() -> None:
        nonlocal current
        if current is None:
            return
        if current["bullets"] or current["title"] not in {"Role"}:
            roles.append(current)
        current = None

    for ln in lines:
        if ln in {name, email, phone, location}:
            continue
        heading = _SECTION.match(ln)
        if heading:
            key = heading.group(1).lower()
            flush()
            if key.startswith("edu") or key == "academic":
                section = "edu"
            elif "skill" in key or "tech" in key:
                section = "skills"
            elif key in {"summary", "profile", "objective"}:
                section = "sum"
            elif "experience" in key or key == "employment":
                section = "exp"
            else:
                section = key
            continue
        if section == "edu":
            if len(ln) > 8:
                education.append(ln)
            continue
        if section == "sum":
            if len(ln) > 20:
                summary_bits.append(_clean_bullet(ln))
            continue
        if section == "skills":
            continue
        if _looks_like_role_header(ln):
            flush()
            title, employer, start, end = _split_role_header(ln)
            current = {
                "id": f"r.{len(roles)}",
                "title": title,
                "employer": employer,
                "start": start,
                "end": end,
                "bullets": [],
            }
            section = "exp"
            continue
        cleaned = _clean_bullet(ln)
        if re.match(r"(?i)^(skills|technologies|tech stack|tools|competenc)\b", cleaned):
            continue
        tags = _skills_in(cleaned)
        is_bullet = bool(re.match(r"^[\-•–*—]\s+", ln)) or len(cleaned) >= 28
        if current is not None and is_bullet:
            current["bullets"].append(
                {
                    "id": f"r.{len(roles)}.{len(current['bullets'])}",
                    "text": cleaned,
                    "tags": tags,
                }
            )
            continue
        if is_bullet and (tags or len(cleaned) >= 40):
            loose.append({"id": f"u.{len(loose)}", "text": cleaned, "tags": tags})

    flush()
    if not roles and loose:
        roles.append(
            {
                "id": "from-resume",
                "employer": "From résumé",
                "title": "Roles as stated",
                "start": career_start[:7],
                "end": "present",
                "bullets": loose,
            }
        )
    bullets = [b for role in roles for b in role["bullets"]]
    employers = []
    for role in roles:
        emp = role.get("employer") or ""
        if emp and emp not in employers and emp.lower() not in {"employer", "from résumé", "from resume"}:
            employers.append(emp)
    summary = " ".join(summary_bits).strip()
    if not summary:
        for b in bullets[:2]:
            summary_bits.append(b["text"].rstrip("."))
        if summary_bits:
            summary = ". ".join(summary_bits) + "."
    return {
        "name": name[:80],
        "email": email,
        "location": location or "Not specified",
        "phone": phone,
        "remote_ok": True,
        "work_authorization": guess_work_authorization(text),
        "career_start": career_start,
        "skills": grounded_skills(listed_skills, bullets),
        "employers": employers,
        "summary": summary[:400],
        "education": education[:8],
        "experience": roles,
    }
