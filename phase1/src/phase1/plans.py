from __future__ import annotations

PLANS: dict[str, dict] = {
    "free": {
        "id": "free",
        "label": "Free",
        "usd_month": 0,
        "usd_year": 0,
        "ngn_month": 0,
        "ngn_year": 0,
        "profiles": 1,
        "packs_month": 2,
        "auto_batch": 1,
        "docx": False,
        "pdf": False,
        "alerts": "weekly3",
        "stylist": False,
        "blurb": "Try the honest loop. Two packs a month. You still click Submit.",
    },
    "basic": {
        "id": "basic",
        "label": "Basic",
        "usd_month": 9,
        "usd_year": 90,
        "ngn_month": 5000,
        "ngn_year": 50000,
        "profiles": 1,
        "packs_month": 10,
        "auto_batch": 5,
        "docx": True,
        "pdf": False,
        "alerts": "daily_ng",
        "stylist": False,
        "blurb": "A real hunt: ten packs, Word download, Nigerian jobs that pass your gate.",
    },
    "pro": {
        "id": "pro",
        "label": "Pro",
        "usd_month": 19,
        "usd_year": 190,
        "ngn_month": 12000,
        "ngn_year": 120000,
        "profiles": 2,
        "packs_month": 30,
        "auto_batch": 10,
        "docx": True,
        "pdf": True,
        "alerts": "pro",
        "stylist": True,
        "blurb": "Nigeria, Web3, and one extra market. PDF. Optional rewrite when an API key exists.",
    },
    "premium": {
        "id": "premium",
        "label": "Premium",
        "usd_month": 39,
        "usd_year": 390,
        "ngn_month": 25000,
        "ngn_year": 250000,
        "profiles": 5,
        "packs_month": 80,
        "auto_batch": 10,
        "docx": True,
        "pdf": True,
        "alerts": "fast",
        "stylist": True,
        "blurb": "Volume and faster alerts. Still no fake skills. Still you click Submit.",
    },
}

ORDER = ("free", "basic", "pro", "premium")


def get_plan(plan_id: str | None) -> dict:
    return PLANS.get((plan_id or "free").lower(), PLANS["free"])


def pack_budget(plan: dict, used: int) -> int:
    """How many packs this run may write. Never exceed the monthly cap."""
    remain = max(0, int(plan["packs_month"]) - max(0, int(used)))
    return min(int(plan["auto_batch"]), remain)


def money(plan: dict, currency: str) -> tuple[str, str]:
    if (currency or "usd").lower() == "ngn":
        return f"₦{plan['ngn_month']:,}", f"₦{plan['ngn_year']:,}"
    return f"${plan['usd_month']}", f"${plan['usd_year']}"
