from __future__ import annotations

from phase1.parse import propose_from_text, grounded_skills


def test_propose_finds_django_not_kubernetes():
    text = """Jordan Hale
jordan.hale@example.com
Lagos, Nigeria

Backend engineer. Python, Django, PostgreSQL, Docker.
Built Django REST APIs on PostgreSQL at NimbusPay.
"""
    draft = propose_from_text(text)
    skills = {s.lower() for s in draft["skills"]}
    assert "python" in skills
    assert "django" in skills
    assert "kubernetes" not in skills
    assert "go" not in skills


def test_grounded_skills_drop_unevidenced_tokens():
    bullets = [
        {"text": "Shipped Django APIs on PostgreSQL.", "tags": ["Django", "PostgreSQL"]},
    ]
    skills = grounded_skills(["Django", "PostgreSQL", "Kubernetes"], bullets)
    assert "Kubernetes" not in skills
    assert "Django" in skills
