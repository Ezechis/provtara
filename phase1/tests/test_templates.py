from __future__ import annotations

from phase1.templates_catalog import ROLES, get_role, grouped_roles, letter_markdown, resume_markdown
from phase1.web import create_app


def test_role_ids_are_unique():
    ids = [r.id for r in ROLES]
    assert len(ids) == len(set(ids))
    assert len(ROLES) >= 70


def test_families_cover_the_asked_fields():
    names = {fam for fam, _ in grouped_roles()}
    assert "Networking & infrastructure" in names
    assert "Programming" in names
    assert "DevOps & cloud" in names
    assert "AI / ML" in names
    assert "Data" in names


def test_resume_is_a_template_not_a_fake_job():
    role = get_role("backend-engineer")
    assert role is not None
    text = resume_markdown(role)
    assert "[Your name]" in text
    assert "Backend Engineer" in text
    assert "Acme" not in text
    assert "I invented" not in text.lower()


def test_letter_names_the_gap_rule():
    role = get_role("machine-learning-engineer")
    assert role is not None
    text = letter_markdown(role)
    assert text.startswith("Dear hiring team")
    assert "leave it off the résumé" in text


def test_templates_index_and_rail(tmp_path):
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test",
            "DATABASE": str(tmp_path / "t.db"),
        }
    )
    client = app.test_client()
    home = client.get("/")
    assert home.status_code == 200
    body = home.get_data(as_text=True)
    assert "CV &amp; letter templates" in body or "CV & letter templates" in body
    assert "Network Engineer" in body
    assert "résumé" in body
    assert href_ok(body, "/templates/backend-engineer")
    idx = client.get("/templates")
    assert idx.status_code == 200
    assert "Data Engineer" in idx.get_data(as_text=True)
    page = client.get("/templates/devops-engineer")
    assert page.status_code == 200
    html = page.get_data(as_text=True)
    assert "DevOps Engineer" in html
    assert "[Your name]" in html
    dl = client.get("/templates/devops-engineer/resume.md")
    assert dl.status_code == 200
    assert b"[Your name]" in dl.data
    letter = client.get("/templates/network-engineer/letter.md")
    assert letter.status_code == 200
    assert b"Network Engineer" in letter.data
    assert client.get("/templates/not-a-real-role").status_code == 404


def href_ok(body: str, path: str) -> bool:
    return path in body
