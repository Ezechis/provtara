from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage


def smtp_ready() -> bool:
    return bool(os.environ.get("SMTP_HOST") and os.environ.get("SMTP_FROM"))


def send_mail(to_addr: str, subject: str, body: str) -> bool:
    host = os.environ.get("SMTP_HOST") or ""
    from_addr = os.environ.get("SMTP_FROM") or ""
    if not host or not from_addr or not to_addr:
        return False
    port = int(os.environ.get("SMTP_PORT") or "587")
    user = os.environ.get("SMTP_USER") or ""
    password = os.environ.get("SMTP_PASS") or ""
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg.set_content(body)
    try:
        with smtplib.SMTP(host, port, timeout=20) as smtp:
            smtp.starttls()
            if user:
                smtp.login(user, password)
            smtp.send_message(msg)
        return True
    except (OSError, smtplib.SMTPException):
        return False


def qualified_digest(email: str, rows: list[dict], origin: str) -> tuple[str, str]:
    lines = [
        "Provtara found IT jobs that pass your confirmed résumé.",
        "We do not invent skills. We do not click Submit.",
        "",
    ]
    for row in rows:
        job = row["job"]
        lines.append(f"- {job.title} at {job.company}")
        lines.append(f"  {origin}/vacancies/{job.id}")
        lines.append(f"  Apply on the official listing: {job.apply_url}")
        lines.append("")
    lines.append("Turn alerts off: " + origin + "/account")
    return "Provtara — jobs you can actually do", "\n".join(lines)
