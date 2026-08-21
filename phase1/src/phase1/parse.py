from __future__ import annotations

import io
import re
from datetime import date

from phase0.truth import SKILL_CATALOG

_EMAIL = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)
_YEAR = re.compile(r"\b(20\d{2})\b")


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
    for ln in lines[:8]:
        if "," in ln and "@" not in ln and ln != name:
            location = ln
            break
    years = [int(y) for y in _YEAR.findall(text)]
    career_start = f"{min(years)}-01-01" if years else "2023-01-01"
    skills = _skills_in(text)
    bullets = []
    for i, ln in enumerate(lines):
        if len(ln) < 40:
            continue
        tags = _skills_in(ln)
        if not tags:
            continue
        bullets.append({"id": f"u.{i}", "text": ln, "tags": tags})
    if not bullets and skills:
        bullets.append(
            {
                "id": "u.0",
                "text": "Experience described in the uploaded résumé.",
                "tags": skills[:6],
            }
        )
    employers = []
    return {
        "name": name[:80],
        "email": email,
        "location": location or "Not specified",
        "remote_ok": True,
        "work_authorization": ["NG"],
        "career_start": career_start,
        "skills": grounded_skills(skills, bullets),
        "employers": employers,
        "summary": f"IT candidate since {career_start[:4]}.",
        "experience": [
            {
                "id": "from-resume",
                "employer": "From résumé",
                "title": "Roles as stated",
                "start": career_start[:7],
                "end": "present",
                "bullets": bullets,
            }
        ]
        if bullets
        else [],
    }
