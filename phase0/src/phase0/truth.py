from __future__ import annotations

import re
from dataclasses import dataclass

from phase0.models import Profile, TruthFailed, canon

# Closed catalog of IT tokens we will never let through unless the profile has them.
# A claim like "Fluent in Rust" still fails if Rust is in this list and not in the profile.
SKILL_CATALOG = (
    "Kubernetes",
    "k8s",
    "Go",
    "Golang",
    "Terraform",
    "TensorFlow",
    "FastAPI",
    "EKS",
    "Kafka",
    "Rust",
    "Scala",
    "Ruby",
    "Rails",
    "Java",
    "Spring",
    "C++",
    "AWS",
    "GCP",
    "Azure",
    "Helm",
    "Istio",
    "Ansible",
    "Pulumi",
    "Spark",
    "Hadoop",
    "PyTorch",
    "Ragas",
    "TruLens",
    "GraphQL",
    "MongoDB",
    "Cassandra",
    "Snowflake",
    "Airflow",
    "Python",
    "Django",
    "PostgreSQL",
    "Postgres",
    "Docker",
    "Linux",
    "Git",
    "REST",
    "pytest",
    "Redis",
    "Celery",
    "JavaScript",
    "TypeScript",
    "React",
    "Node",
    "Solidity",
    "Ethereum",
    "Foundry",
    "Hardhat",
    "EVM",
)


@dataclass(frozen=True)
class Violation:
    rule: str
    line_no: int
    excerpt: str
    detail: str


def _allowed(profile: Profile) -> set[str]:
    allowed = set(profile.skill_set)
    for role in profile.experience:
        for bullet in role.bullets:
            allowed.update(canon(t) for t in bullet.tags)
    return allowed


def check_text(
    profile: Profile,
    text: str,
    allow_gap_mentions: list[str] | None = None,
) -> list[Violation]:
    allowed = _allowed(profile)
    skip = {canon(s) for s in (allow_gap_mentions or [])}
    violations: list[Violation] = []
    lines = text.splitlines() or [text]

    for i, line in enumerate(lines, start=1):
        for skill in SKILL_CATALOG:
            pattern = r"(?<![A-Za-z0-9])" + re.escape(skill) + r"(?![A-Za-z0-9])"
            if not re.search(pattern, line, flags=re.IGNORECASE):
                continue
            key = canon(skill)
            if key in allowed or key in skip:
                continue
            violations.append(
                Violation(
                    rule="ungrounded_skill",
                    line_no=i,
                    excerpt=skill,
                    detail=f"{skill!r} is not in the evidence profile",
                )
            )

        for m in re.finditer(r"\b(\d+)\s*\+?\s*years?\b", line, flags=re.IGNORECASE):
            n = int(m.group(1))
            if n > int(profile.years_experience) + 1:
                violations.append(
                    Violation(
                        rule="date_inflation",
                        line_no=i,
                        excerpt=m.group(0),
                        detail=f"profile has {profile.years_experience} years (started {profile.career_start})",
                    )
                )

    # de-dupe identical ungrounded hits on the same line
    seen: set[tuple] = set()
    unique: list[Violation] = []
    for v in violations:
        key = (v.rule, v.line_no, v.excerpt.lower())
        if key in seen:
            continue
        seen.add(key)
        unique.append(v)
    return unique


def require_clean(profile: Profile, text: str, *, kind: str, allow_gap_mentions: list[str] | None = None) -> None:
    hits = check_text(profile, text, allow_gap_mentions=allow_gap_mentions)
    if hits:
        detail = "; ".join(f"{v.excerpt} ({v.rule})" for v in hits)
        raise TruthFailed(f"{kind} failed truth check: {detail}")
