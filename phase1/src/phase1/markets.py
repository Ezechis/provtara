from __future__ import annotations

import re

from phase0.models import Job

MARKETS: tuple[dict, ...] = (
    {"id": "ng", "label": "Nigerian IT Vacancies", "featured": True},
    {"id": "us", "label": "US IT Vacancies", "featured": False},
    {"id": "ca", "label": "Canadian IT Vacancies", "featured": False},
    {"id": "uk", "label": "UK IT Vacancies", "featured": False},
    {"id": "ke", "label": "Kenya IT Vacancies", "featured": False},
    {"id": "gh", "label": "Ghana IT Vacancies", "featured": False},
    {"id": "za", "label": "S-Africa IT Vacancies", "featured": False},
    {"id": "eu", "label": "European IT Vacancies", "featured": False},
    {"id": "row", "label": "Rest Of The World", "featured": False},
)

WORK_MODES: tuple[dict, ...] = (
    {"id": "onsite", "label": "On-Site Jobs"},
    {"id": "remote", "label": "Remote Jobs"},
    {"id": "anywhere", "label": "Work From Anywhere"},
)

_MARKET_WORDS: dict[str, tuple[str, ...]] = {
    "ng": (
        "nigeria",
        "lagos",
        "abuja",
        "port harcourt",
        "ibadan",
        "enugu",
        "kano",
        "kaduna",
        "warri",
        "phc",
    ),
    "ke": ("kenya", "nairobi", "mombasa", "kisumu"),
    "gh": ("ghana", "accra", "kumasi", "tema"),
    "za": (
        "south africa",
        "south-africa",
        "johannesburg",
        "cape town",
        "durban",
        "pretoria",
        "gauteng",
        "soweto",
    ),
    "uk": (
        "united kingdom",
        "uk",
        "london",
        "manchester",
        "edinburgh",
        "britain",
        "england",
        "scotland",
        "wales",
        "birmingham",
    ),
    "us": (
        "united states",
        "usa",
        "u.s.",
        "new york",
        "san francisco",
        "seattle",
        "austin",
        "chicago",
        "boston",
        "denver",
        "atlanta",
        "california",
        "remote us",
    ),
    "ca": ("canada", "toronto", "vancouver", "montreal", "calgary", "ottawa"),
    "eu": (
        "europe",
        "european union",
        "germany",
        "france",
        "netherlands",
        "spain",
        "ireland",
        "sweden",
        "berlin",
        "amsterdam",
        "paris",
        "dublin",
        "munich",
        "lisbon",
        "poland",
        "portugal",
        "belgium",
        "italy",
        "schengen",
    ),
}

_ANYWHERE = (
    "work from anywhere",
    "anywhere in the world",
    "remote worldwide",
    "any timezone",
    "any time zone",
)

_MARKET_ORDER = ("ng", "ke", "gh", "za", "uk", "us", "ca", "eu")


def _blob(job: Job) -> str:
    return f"{job.location} {job.hook} {job.description} {job.title} {job.company}".lower()


def _has_word(blob: str, word: str) -> bool:
    return re.search(r"(?<![a-z0-9])" + re.escape(word) + r"(?![a-z0-9])", blob) is not None


def market_id(job: Job) -> str:
    blob = _blob(job)
    for mid in _MARKET_ORDER:
        if any(_has_word(blob, w) for w in _MARKET_WORDS[mid]):
            return mid
    return "row"


def work_mode(job: Job) -> str:
    loc = (job.location or "").strip().lower()
    if loc in {"anywhere", "worldwide", "world", "remote worldwide"}:
        return "anywhere"
    blob = f"{job.location} {job.hook}".lower()
    if any(token in blob for token in _ANYWHERE):
        return "anywhere"
    if job.remote:
        return "remote"
    return "onsite"


def market_label(mid: str) -> str:
    for item in MARKETS:
        if item["id"] == mid:
            return item["label"]
    return "IT Vacancies"


def filter_jobs(
    jobs: list[Job],
    *,
    region: str = "",
    mode: str = "",
    q: str = "",
) -> list[Job]:
    needle = " ".join((q or "").lower().split())
    out: list[Job] = []
    for job in jobs:
        if region and market_id(job) != region:
            continue
        if mode and work_mode(job) != mode:
            continue
        if needle:
            hay = f"{job.title} {job.company} {job.location} {job.hook} {job.description}".lower()
            if needle not in hay:
                continue
        out.append(job)
    return out
