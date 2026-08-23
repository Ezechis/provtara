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
    assert "kubernetes" in skills
    assert "python" in skills
    assert draft["experience"] == []


def test_propose_guesses_ng_auth_from_lagos_not_by_default():
    local = propose_from_text(
        "Chioma\nc@example.com\nLagos, Nigeria\nBuilt Django REST APIs on PostgreSQL."
    )
    assert "Nigeria" in local["work_authorization"]
    assert "NG" not in local["work_authorization"]
    remote = propose_from_text(
        "Alex\nalex@example.com\nOslo\nBuilt Django REST APIs on PostgreSQL."
    )
    assert remote["work_authorization"] == []


def test_propose_keeps_real_roles_education_and_untagged_bullets():
    text = """
Chioma Okeke
chioma@example.com
Lagos, Nigeria
+234 801 234 5678

SUMMARY
Backend engineer shipping payments APIs in production.

EXPERIENCE
Backend Engineer, Paystack, Jan 2024 – Present
- Designed Django REST APIs for checkout, backed by PostgreSQL
- Cut reconciliation time by rewriting the nightly batch as an idempotent worker
Software Engineer, Andela, Feb 2023 – Dec 2023
- Shipped internal admin tools and Git-based release notes

EDUCATION
B.Sc Computer Science, University of Lagos, 2022

SKILLS
Python, Django, PostgreSQL, Docker, Kubernetes
"""
    draft = propose_from_text(text)
    titles = [r["title"] for r in draft["experience"]]
    employers = [r["employer"] for r in draft["experience"]]
    assert "Backend Engineer" in titles
    assert "Paystack" in employers
    assert "Andela" in employers
    assert any("reconciliation" in b["text"] for r in draft["experience"] for b in r["bullets"])
    assert any("University of Lagos" in row for row in draft["education"])
    assert "+234" in draft["phone"]
    skills = {s.lower() for s in draft["skills"]}
    assert "django" in skills
    assert "python" in skills
    assert "docker" in skills
    assert "kubernetes" in skills
    assert "payments APIs" in draft["summary"]


def test_profile_skills_education_not_muddled_into_location():
    text = """
Ezechi Kingsley
ezechi@example.com
+234 803 111 2222
Results-driven IT professional, with eight years delivering network and cloud solutions for banks.

WORK EXPERIENCE
Network Engineer, MainOne, Jan 2020 – Present
- Designed Django REST APIs on PostgreSQL for the ops portal

EDUCATIONAL QUALIFICATIONS
B.Sc Computer Science, University of Lagos, 2014
HND Electrical Engineering, Yaba College of Technology, 2011

CORE COMPETENCIES
Python, Django, PostgreSQL, Networking, Cisco, Cloud

CERTIFICATIONS
CCNA
"""
    draft = propose_from_text(text)
    assert "Results-driven" in (draft["summary"] or "")
    loc = (draft["location"] or "").lower()
    assert "results-driven" not in loc
    assert "Nigeria" in draft["work_authorization"]
    assert draft["career_start"].startswith("2020")
    skills = {s.lower() for s in draft["skills"]}
    assert "python" in skills
    assert "django" in skills
    assert "cisco" in skills
    assert "networking" in skills
    edu = " ".join(draft["education"]).lower()
    assert "university of lagos" in edu
    assert "b.sc" in edu or "computer science" in edu
    assert any("ccna" in c.lower() for c in draft["certifications"])


def test_education_and_certs_stay_in_separate_boxes():
    text = """
Ada Okafor
ada@example.com
Lagos, Nigeria

EDUCATIONAL QUALIFICATIONS
WAEC Senior School Certificate, 2010
B.Sc Computer Science, University of Lagos, 2014
CCNA

CERTIFICATIONS
AWS Certified Cloud Practitioner
"""
    draft = propose_from_text(text)
    edu = " ".join(draft["education"]).lower()
    cert = " ".join(draft["certifications"]).lower()
    assert "university of lagos" in edu
    assert "waec" in edu
    assert "ccna" in cert
    assert "aws" in cert
    assert "ccna" not in edu
    assert "university" not in cert


def test_combined_education_and_certification_heading_splits():
    text = """
Ada
ada@example.com
Lagos, Nigeria

EDUCATION AND CERTIFICATIONS
B.Eng Electrical Engineering, University of Nigeria, 2016
WAEC Senior School Certificate, 2010
Cisco Certified Network Associate
PMP
"""
    draft = propose_from_text(text)
    edu = " ".join(draft["education"]).lower()
    cert = " ".join(draft["certifications"]).lower()
    assert "university of nigeria" in edu
    assert "waec" in edu
    assert "cisco" in cert or "ccna" in cert or "certified" in cert
    assert "pmp" in cert
    assert "pmp" not in edu
    assert "university" not in cert


def test_skills_section_fills_confirm_list():
    text = """Ada Okafor
ada@example.com
Lagos, Nigeria

EXPERIENCE
Backend Engineer, Paystack, Jan 2024 – Present
- Designed checkout APIs

SKILLS
Python, Django, PostgreSQL, Docker, SQL, Excel
"""
    draft = propose_from_text(text)
    skills = {s.lower() for s in draft["skills"]}
    assert skills
    for need in ("python", "django", "postgresql", "docker", "sql", "excel"):
        assert need in skills


def test_skills_on_resume_keep_listed_and_tagged_drop_inventions():
    from phase1.parse import skills_on_resume

    experience = [
        {
            "bullets": [
                {"text": "Shipped Django APIs on PostgreSQL.", "tags": ["Django", "PostgreSQL"]},
            ]
        }
    ]
    raw = "Jordan Hale\nSKILLS\nPython, Django, PostgreSQL\n"
    kept = skills_on_resume(
        ["Python", "Django", "PostgreSQL", "Kubernetes"],
        raw,
        experience,
    )
    assert "Kubernetes" not in kept
    assert "Python" in kept
    assert "Django" in kept


def test_grounded_skills_drop_unevidenced_tokens():
    bullets = [
        {"text": "Shipped Django APIs on PostgreSQL.", "tags": ["Django", "PostgreSQL"]},
    ]
    skills = grounded_skills(["Django", "PostgreSQL", "Kubernetes"], bullets)
    assert "Kubernetes" not in skills
    assert "Django" in skills
