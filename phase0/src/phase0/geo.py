from __future__ import annotations

import re

LABELS = {
    "NG": "Nigeria",
    "KE": "Kenya",
    "GH": "Ghana",
    "ZA": "South Africa",
    "US": "United States",
    "GB": "United Kingdom",
    "CA": "Canada",
    "IN": "India",
    "DE": "Germany",
    "NL": "Netherlands",
    "IE": "Ireland",
    "FR": "France",
    "AE": "United Arab Emirates",
    "AU": "Australia",
    "RW": "Rwanda",
    "UG": "Uganda",
    "TZ": "Tanzania",
    "EG": "Egypt",
    "ANY": "ANY",
}

_ALIASES = {
    "nigeria": "NG",
    "ng": "NG",
    "naija": "NG",
    "kenya": "KE",
    "ke": "KE",
    "ghana": "GH",
    "gh": "GH",
    "south africa": "ZA",
    "za": "ZA",
    "rsa": "ZA",
    "united states": "US",
    "united states of america": "US",
    "usa": "US",
    "us": "US",
    "united kingdom": "GB",
    "uk": "GB",
    "gb": "GB",
    "britain": "GB",
    "england": "GB",
    "canada": "CA",
    "ca": "CA",
    "india": "IN",
    "in": "IN",
    "germany": "DE",
    "de": "DE",
    "netherlands": "NL",
    "holland": "NL",
    "ireland": "IE",
    "ie": "IE",
    "france": "FR",
    "fr": "FR",
    "united arab emirates": "AE",
    "uae": "AE",
    "ae": "AE",
    "australia": "AU",
    "au": "AU",
    "rwanda": "RW",
    "uganda": "UG",
    "tanzania": "TZ",
    "egypt": "EG",
    "any": "ANY",
}

_CITIES = {
    "lagos": "NG",
    "abuja": "NG",
    "port harcourt": "NG",
    "ibadan": "NG",
    "kano": "NG",
    "enugu": "NG",
    "nairobi": "KE",
    "mombasa": "KE",
    "accra": "GH",
    "kumasi": "GH",
    "johannesburg": "ZA",
    "cape town": "ZA",
    "durban": "ZA",
    "london": "GB",
    "dublin": "IE",
    "berlin": "DE",
    "amsterdam": "NL",
}


def country_code(value: str) -> str:
    raw = " ".join((value or "").lower().split()).strip(" .,")
    if not raw:
        return ""
    if raw in _ALIASES:
        return _ALIASES[raw]
    upper = raw.upper()
    if upper in LABELS:
        return upper
    if raw in _CITIES:
        return _CITIES[raw]
    for name, code in sorted(_ALIASES.items(), key=lambda kv: -len(kv[0])):
        if len(name) > 3 and name in raw:
            return code
    for city, code in _CITIES.items():
        if city in raw:
            return code
    return ""


def country_label(value: str) -> str:
    code = country_code(value)
    if code and code != "ANY":
        return LABELS.get(code, value.strip())
    if code == "ANY":
        return "ANY"
    text = (value or "").strip()
    return text


def auth_codes(values: list[str] | tuple[str, ...]) -> set[str]:
    codes: set[str] = set()
    for value in values or []:
        code = country_code(value)
        if code:
            codes.add(code)
        elif (value or "").strip().upper() == "ANY":
            codes.add("ANY")
    return codes


def auth_matches(have: list[str] | tuple[str, ...], allowed: list[str] | tuple[str, ...]) -> bool:
    want = auth_codes(allowed)
    if not want or "ANY" in want:
        return True
    return bool(want & auth_codes(have))


def split_auth_location(text: str) -> tuple[list[str], str]:
    raw = " ".join((text or "").split()).strip(" ,")
    if not raw:
        return [], ""
    labels: list[str] = []
    seen: set[str] = set()
    for part in [p.strip() for p in raw.split(",") if p.strip()]:
        label = country_label(part)
        code = country_code(part)
        if code and code != "ANY" and label not in seen:
            seen.add(label)
            labels.append(label)
    if not labels:
        code = country_code(raw)
        if code and code != "ANY":
            labels.append(country_label(raw))
    location = raw
    for code, name in LABELS.items():
        if code != "ANY":
            location = location.replace(code, name) if location == code else location
    if location.upper() in LABELS:
        location = LABELS[location.upper()]
    elif country_code(location) and location.upper() == country_code(location):
        location = country_label(location)
    return labels, location


def looks_like_place(value: str) -> bool:
    text = (value or "").strip()
    if not text or text.lower() in {"not specified"}:
        return False
    if len(text) > 70 or text.count(",") > 3 or len(text.split()) > 8:
        return False
    if re.search(
        r"\b(university|college|polytechnic|institute|bachelor|master|diploma|hnd|b\.?\s*sc|m\.?\s*sc)\b",
        text,
        re.I,
    ):
        return False
    return bool(country_code(text))


def auth_location_display(draft: dict) -> str:
    loc = (draft.get("location") or "").strip()
    names = []
    for item in draft.get("work_authorization") or []:
        label = country_label(item)
        if label and label not in {"ANY"} and label not in names:
            names.append(label)
    if loc and looks_like_place(loc):
        loc_l = loc.lower()
        extra = [n for n in names if n.lower() not in loc_l]
        if extra:
            return loc + ", " + ", ".join(extra)
        if loc.upper() in LABELS:
            return LABELS[loc.upper()]
        if country_code(loc) and loc.upper() == country_code(loc):
            return country_label(loc)
        return loc
    return ", ".join(names)
