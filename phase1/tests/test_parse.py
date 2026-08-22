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


def test_propose_does_not_invent_a_bullet_to_ground_skills():
    text = "Ada Lovelace\nada@example.com\nSkills: Kubernetes, Terraform, Python"
    draft = propose_from_text(text)
    assert "Experience described in the uploaded résumé." not in str(draft)
    skills = {s.lower() for s in draft["skills"]}
    assert "kubernetes" not in skills
    assert "terraform" not in skills
    assert draft["experience"] == []


def test_propose_guesses_ng_auth_from_lagos_not_by_default():
    local = propose_from_text(
        "Chioma\nc@example.com\nLagos, Nigeria\nBuilt Django REST APIs on PostgreSQL."
    )
    assert "NG" in local["work_authorization"]
    remote = propose_from_text(
        "Alex\nalex@example.com\nBerlin\nBuilt Django REST APIs on PostgreSQL."
    )
    assert remote["work_authorization"] == []


def test_grounded_skills_drop_unevidenced_tokens():
    bullets = [
        {"text": "Shipped Django APIs on PostgreSQL.", "tags": ["Django", "PostgreSQL"]},
    ]
    skills = grounded_skills(["Django", "PostgreSQL", "Kubernetes"], bullets)
    assert "Kubernetes" not in skills
    assert "Django" in skills
