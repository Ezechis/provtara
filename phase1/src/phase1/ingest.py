from __future__ import annotations

import hashlib
import json
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import unescape

from phase0.models import Job
from phase0.qualify import job_from_dict
from phase0.truth import SKILL_CATALOG

UA = "Provtara/0.1 (honest IT job workshop; +https://github.com/Ezechis)"

IT_POSITIVE = (
    "engineer",
    "developer",
    "software",
    "backend",
    "front-end",
    "frontend",
    "full-stack",
    "fullstack",
    "devops",
    "sre",
    "site reliability",
    "data scientist",
    "data engineer",
    "machine learning",
    "security engineer",
    "qa engineer",
    "quality assurance",
    "sysadmin",
    "system administrator",
    "cloud",
    "platform engineer",
    "python",
    "java ",
    "javascript",
    "typescript",
    "golang",
    "kubernetes",
    "react",
    "ios",
    "android",
    "mobile engineer",
)

IT_NEGATIVE = (
    "sales manager",
    "account executive",
    "recruiter",
    "talent acquisition",
    "customer success",
    "business development",
    "marketing manager",
    "content writer",
    "copywriter",
    "graphic designer",
    "product support",
    "customer service",
    "erp consultant",
    "life sciences consulting",
)

_HTML = re.compile(r"<[^>]+>")
_YEARS = re.compile(r"(\d+)\s*\+?\s*years?", re.I)


def strip_html(text: str) -> str:
    return unescape(_HTML.sub(" ", text or ""))


def is_it_role(title: str, description: str, tags: list[str] | None = None) -> bool:
    blob = f"{title} {description} {' '.join(tags or [])}".lower()
    if any(n in blob for n in IT_NEGATIVE):
        return False
    return any(p in blob for p in IT_POSITIVE)


_NICE_SPLIT = re.compile(
    r"(?:nice\s+to\s+have|nices?\s*[-:]|plus\s*:|our\s+stack\s+also|"
    r"stack\s+(?:also\s+)?includes|technologies?\s+we\s+use|"
    r"bonus(?:\s+points)?(?:\s+if)?)",
    re.I,
)
_GO_LANG = re.compile(
    r"(?<![A-Za-z])(?:golang|go\s*lang(?:uage)?|"
    r"go\s+(?:developer|engineer|programmer|service|services|binary|module)s?)"
    r"(?![A-Za-z])|\b(?:in|using|with|written\s+in)\s+go\b",
    re.I,
)


def _skill_in_text(skill: str, text: str) -> bool:
    if not text:
        return False
    if skill.lower() == "go":
        return bool(_GO_LANG.search(text))
    return bool(
        re.search(r"(?<![A-Za-z0-9])" + re.escape(skill) + r"(?![A-Za-z0-9])", text, re.I)
    )


def _skills_from(text: str) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for skill in SKILL_CATALOG:
        if not _skill_in_text(skill, text):
            continue
        key = skill.lower()
        if key in seen:
            continue
        seen.add(key)
        found.append(skill)
    return found


def _first_index(skill: str, text: str) -> int:
    if skill.lower() == "go":
        m = _GO_LANG.search(text or "")
        return m.start() if m else 10**9
    m = re.search(
        r"(?<![A-Za-z0-9])" + re.escape(skill) + r"(?![A-Za-z0-9])",
        text or "",
        re.I,
    )
    return m.start() if m else 10**9


def _core_and_tail(description: str) -> tuple[str, str]:
    text = (description or "").strip()
    split = _NICE_SPLIT.split(text, maxsplit=1)
    head = split[0].strip()
    marked_tail = split[1].strip() if len(split) > 1 else ""
    sentences = re.split(r"(?<=[.!?])\s+", head) if head else []
    core = " ".join(sentences[:2]).strip() or head
    leftover = " ".join(sentences[2:]).strip()
    tail = " ".join(p for p in (leftover, marked_tail) if p)
    return core, tail


def listing_stack(title: str, description: str) -> tuple[list[str], list[str]]:
    """Must-haves from the role (title + opening), not catalog order."""
    title = title or ""
    description = description or ""
    core, tail = _core_and_tail(description)
    title_skills = _skills_from(title)
    core_skills = _skills_from(core)
    must: list[str] = []
    seen: set[str] = set()
    for skill in title_skills + sorted(core_skills, key=lambda s: _first_index(s, f"{title}\n{core}")):
        key = skill.lower()
        if key in seen:
            continue
        seen.add(key)
        must.append(skill)
        if len(must) >= 4:
            break
    if not must:
        ordered = sorted(
            _skills_from(f"{title}\n{description}"),
            key=lambda s: _first_index(s, f"{title}\n{description}"),
        )
        must = ordered[:4]
        seen = {s.lower() for s in must}
    rest: list[str] = []
    for skill in _skills_from(tail) + _skills_from(f"{title}\n{description}"):
        key = skill.lower()
        if key in seen:
            continue
        seen.add(key)
        rest.append(skill)
        if len(rest) >= 4:
            break
    return must, rest


def _min_years(text: str) -> int:
    nums = [int(n) for n in _YEARS.findall(text or "")]
    if not nums:
        return 2
    return min(max(nums), 8)


def _id_for(url: str, prefix: str) -> str:
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}-{digest}"


def _job(
    *,
    source: str,
    title: str,
    company: str,
    url: str,
    description: str,
    location: str = "",
    remote: bool = True,
) -> Job | None:
    if not title or not url:
        return None
    desc = strip_html(description)[:4000]
    if not is_it_role(title, desc):
        return None
    must, nice = listing_stack(title, desc)
    if not must and not nice:
        return None
    hook = desc.split(".")[0].strip()[:180] or f"{company} is hiring for {title}."
    return job_from_dict(
        {
            "id": _id_for(url, source),
            "title": title.strip()[:120],
            "company": (company or "Company").strip()[:80],
            "apply_url": url.strip(),
            "remote": remote,
            "must_haves": must,
            "nice_to_haves": nice,
            "min_years": _min_years(desc),
            "work_authorization_any_of": ["ANY"],
            "hook": hook,
            "description": desc[:1500],
            "location": location[:80],
        }
    )


def job_from_remotive(item: dict) -> Job | None:
    cat = (item.get("category") or "").lower()
    if cat and cat not in {"software-dev", "data", "devops", "qa"} and "software" not in cat:
        return None
    return _job(
        source="remotive",
        title=item.get("title") or "",
        company=item.get("company_name") or "",
        url=item.get("url") or item.get("short_url") or "",
        description=item.get("description") or "",
        location=item.get("candidate_required_location") or "Remote",
        remote=True,
    )


def job_from_arbeitnow(item: dict) -> Job | None:
    tags = item.get("tags") or []
    if isinstance(tags, str):
        tags = [tags]
    return _job(
        source="arbeitnow",
        title=item.get("title") or "",
        company=item.get("company_name") or "",
        url=item.get("url") or "",
        description=item.get("description") or "",
        location=item.get("location") or "",
        remote=bool(item.get("remote", True)),
    )


def job_from_remoteok(item: dict) -> Job | None:
    if not item.get("position") and not item.get("title"):
        return None
    tags = item.get("tags") or []
    return _job(
        source="remoteok",
        title=item.get("position") or item.get("title") or "",
        company=item.get("company") or "",
        url=item.get("url") or item.get("apply_url") or "",
        description=item.get("description") or " ".join(str(t) for t in tags),
        location=item.get("location") or "Remote",
        remote=True,
    )


def job_from_jobicy(item: dict) -> Job | None:
    return _job(
        source="jobicy",
        title=item.get("jobTitle") or item.get("title") or "",
        company=item.get("companyName") or item.get("company") or "",
        url=item.get("url") or item.get("jobPermalink") or "",
        description=item.get("jobDescription") or item.get("jobExcerpt") or "",
        location=item.get("jobGeo") or "Remote",
        remote=True,
    )


def job_from_himalayas(item: dict) -> Job | None:
    locs = item.get("locationRestrictions") or []
    names = []
    for loc in locs if isinstance(locs, list) else []:
        if isinstance(loc, dict):
            names.append(loc.get("name") or loc.get("alpha2") or "")
        elif isinstance(loc, str):
            names.append(loc)
    location = ", ".join(n for n in names if n) or "Worldwide"
    return _job(
        source="himalayas",
        title=item.get("title") or "",
        company=item.get("companyName") or item.get("company") or "",
        url=item.get("applicationLink") or item.get("guid") or "",
        description=item.get("description") or item.get("excerpt") or "",
        location=location,
        remote=True,
    )


def _rss_items(raw: bytes) -> list[dict]:
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return []
    out = []
    for item in root.iter("item"):
        out.append(
            {
                "title": (item.findtext("title") or "").strip(),
                "url": (item.findtext("link") or "").strip(),
                "description": (item.findtext("description") or "").strip(),
            }
        )
    return out


def job_from_wwr(item: dict) -> Job | None:
    title = item.get("title") or ""
    company = "Company"
    if ": " in title:
        company, title = title.split(": ", 1)
    return _job(
        source="wwr",
        title=title.strip(),
        company=company.strip(),
        url=item.get("url") or "",
        description=item.get("description") or "",
        location="Remote",
        remote=True,
    )


def job_from_hnjobs(item: dict) -> Job | None:
    return _job(
        source="hnjobs",
        title=item.get("title") or "",
        company=(item.get("title") or "Hiring company").split(" is hiring")[0][:80],
        url=item.get("url") or "",
        description=item.get("description") or item.get("title") or "",
        location="Remote",
        remote=True,
    )


SOURCES = {
    "remotive": "Remotive",
    "arbeitnow": "Arbeitnow",
    "remoteok": "RemoteOK",
    "jobicy": "Jobicy",
    "himalayas": "Himalayas",
    "wwr": "We Work Remotely",
    "hnjobs": "Hacker News Jobs",
}

BOARD_HOMES = {
    "remotive": "https://remotive.com",
    "arbeitnow": "https://www.arbeitnow.com",
    "remoteok": "https://remoteok.com",
    "jobicy": "https://jobicy.com",
    "himalayas": "https://himalayas.app",
    "wwr": "https://weworkremotely.com",
    "hnjobs": "https://news.ycombinator.com/jobs",
}


def job_source(job: Job) -> str:
    prefix = (job.id or "").split("-", 1)[0]
    return SOURCES.get(prefix, "Provtara")


def merge_jobs(primary: list[Job], extra: list[Job]) -> list[Job]:
    seen: set[str] = set()
    out: list[Job] = []
    for job in [*primary, *extra]:
        key = (job.apply_url or job.id).rstrip("/").lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(job)
    return out


BOARD_URLS = {
    "remotive": "https://remotive.com/api/remote-jobs?category=software-dev",
    "arbeitnow": "https://www.arbeitnow.com/api/job-board-api",
    "remoteok": "https://remoteok.com/api",
    "jobicy": "https://jobicy.com/api/v2/remote-jobs?count=50&tag=software",
    "himalayas": "https://himalayas.app/jobs/api?limit=20",
    "wwr": "https://weworkremotely.com/categories/remote-programming-jobs.rss",
    "hnjobs": "https://hnrss.org/jobs",
}
RSS_BOARDS = {"wwr", "hnjobs"}
PER_BOARD_CAP = 40
FETCH_TIMEOUT = 12


def _get_bytes(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": UA, "Accept": "application/json, application/rss+xml, text/xml, */*"},
    )
    with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT) as resp:
        return resp.read()


def _get_json(url: str) -> object:
    return json.loads(_get_bytes(url).decode("utf-8", "replace"))


def _extract_remotive(payload):
    items = payload.get("jobs", payload) if isinstance(payload, dict) else payload
    return [job_from_remotive(x) for x in items or []]


def _extract_arbeitnow(payload):
    items = payload.get("data", payload) if isinstance(payload, dict) else payload
    return [job_from_arbeitnow(x) for x in items or []]


def _extract_remoteok(payload):
    items = payload if isinstance(payload, list) else []
    return [job_from_remoteok(x) for x in items if isinstance(x, dict)]


def _extract_jobicy(payload):
    items = payload.get("jobs", []) if isinstance(payload, dict) else []
    return [job_from_jobicy(x) for x in items]


def _extract_himalayas(payload):
    items = payload.get("jobs", payload.get("data", payload)) if isinstance(payload, dict) else payload
    return [job_from_himalayas(x) for x in items or [] if isinstance(x, dict)]


_EXTRACTORS = {
    "remotive": _extract_remotive,
    "arbeitnow": _extract_arbeitnow,
    "remoteok": _extract_remoteok,
    "jobicy": _extract_jobicy,
    "himalayas": _extract_himalayas,
}


def _fetch_one(name: str, url: str) -> tuple[str, list[Job], str | None]:
    try:
        if name in RSS_BOARDS:
            items = _rss_items(_get_bytes(url))
            mapper = job_from_wwr if name == "wwr" else job_from_hnjobs
            batch = [j for j in (mapper(x) for x in items) if j is not None][:PER_BOARD_CAP]
            return name, batch, None
        payload = _get_json(url)
        batch = [j for j in _EXTRACTORS[name](payload) if j is not None][:PER_BOARD_CAP]
        return name, batch, None
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError, TypeError, ValueError, ET.ParseError) as exc:
        return name, [], str(exc)[:200]


def fetch_free_boards() -> tuple[list[Job], dict[str, str]]:
    """Pull IT jobs from no-key public boards in parallel. Errors are per-source."""
    jobs: list[Job] = []
    errors: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=7) as pool:
        futs = [pool.submit(_fetch_one, name, url) for name, url in BOARD_URLS.items()]
        for fut in as_completed(futs):
            name, batch, err = fut.result()
            jobs.extend(batch)
            if err:
                errors[name] = err
    return merge_jobs([], jobs), errors
