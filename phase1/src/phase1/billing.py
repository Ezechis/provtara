from __future__ import annotations

import hashlib
import hmac
import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

from phase1.plans import get_plan


class BillingError(Exception):
    """Provider refused the checkout or returned an unexpected payload."""


def amount_for(plan: dict, currency: str, period: str) -> tuple[int, str]:
    currency = (currency or "usd").lower()
    period = "year" if period == "year" else "month"
    if currency == "ngn":
        naira = int(plan["ngn_year"] if period == "year" else plan["ngn_month"])
        return naira * 100, "NGN"
    dollars = int(plan["usd_year"] if period == "year" else plan["usd_month"])
    return dollars * 100, "USD"


def paid_until_iso(period: str, *, now: datetime | None = None) -> str:
    start = now or datetime.now(timezone.utc)
    days = 365 if period == "year" else 31
    return (start + timedelta(days=days)).isoformat(timespec="seconds")


def paystack_signature(secret: str, body: bytes) -> str:
    return hmac.new(secret.encode("utf-8"), body, hashlib.sha512).hexdigest()


def verify_paystack_signature(secret: str, body: bytes, header: str | None) -> bool:
    if not secret or not header:
        return False
    expect = paystack_signature(secret, body)
    return hmac.compare_digest(expect, header.strip())


def stripe_signature(secret: str, body: bytes, ts: str = "0") -> str:
    signed = ts.encode("utf-8") + b"." + body
    return hmac.new(secret.encode("utf-8"), signed, hashlib.sha256).hexdigest()


def verify_stripe_signature(secret: str, body: bytes, header: str | None) -> bool:
    if not secret or not header:
        return False
    parts = {}
    for item in header.split(","):
        if "=" in item:
            key, val = item.split("=", 1)
            parts[key.strip()] = val.strip()
    ts = parts.get("t")
    v1 = parts.get("v1")
    if not ts or not v1:
        return False
    expect = stripe_signature(secret, body, ts=ts)
    return hmac.compare_digest(expect, v1)


def start_paystack(
    *,
    secret: str,
    email: str,
    amount: int,
    reference: str,
    callback_url: str,
    metadata: dict,
) -> dict:
    payload = {
        "email": email,
        "amount": amount,
        "currency": "NGN",
        "reference": reference,
        "callback_url": callback_url,
        "metadata": metadata,
    }
    data = _json_request(
        "https://api.paystack.co/transaction/initialize",
        secret=secret,
        body=payload,
    )
    if not data.get("status"):
        raise BillingError(str(data.get("message") or "Paystack initialize failed"))
    inner = data.get("data") or {}
    url = inner.get("authorization_url")
    if not url:
        raise BillingError("Paystack did not return a checkout URL")
    return {"url": url, "reference": inner.get("reference") or reference}


def verify_paystack_reference(*, secret: str, reference: str) -> dict:
    data = _json_request(
        "https://api.paystack.co/transaction/verify/" + urllib.parse.quote(reference),
        secret=secret,
        method="GET",
    )
    inner = data.get("data") or {}
    if not data.get("status") or (inner.get("status") or "").lower() != "success":
        raise BillingError("Paystack payment is not successful")
    meta = inner.get("metadata") or {}
    return {
        "reference": inner.get("reference") or reference,
        "user_id": _intish(meta.get("user_id")),
        "plan": meta.get("plan"),
        "period": meta.get("period") or "month",
        "currency": "ngn",
    }


def start_stripe(
    *,
    secret: str,
    email: str,
    amount: int,
    success_url: str,
    cancel_url: str,
    metadata: dict,
    label: str,
) -> dict:
    fields = {
        "mode": "payment",
        "success_url": success_url,
        "cancel_url": cancel_url,
        "customer_email": email,
        "client_reference_id": str(metadata.get("user_id") or ""),
        "line_items[0][quantity]": "1",
        "line_items[0][price_data][currency]": "usd",
        "line_items[0][price_data][unit_amount]": str(amount),
        "line_items[0][price_data][product_data][name]": label,
        "metadata[plan]": str(metadata.get("plan") or ""),
        "metadata[period]": str(metadata.get("period") or "month"),
        "metadata[user_id]": str(metadata.get("user_id") or ""),
        "metadata[reference]": str(metadata.get("reference") or ""),
        "payment_intent_data[metadata][reference]": str(metadata.get("reference") or ""),
    }
    data = _form_request("https://api.stripe.com/v1/checkout/sessions", secret=secret, fields=fields)
    url = data.get("url")
    if not url:
        raise BillingError("Stripe did not return a checkout URL")
    return {"url": url, "reference": metadata.get("reference") or data.get("id")}


def retrieve_stripe_session(*, secret: str, session_id: str) -> dict:
    data = _form_request(
        "https://api.stripe.com/v1/checkout/sessions/" + urllib.parse.quote(session_id),
        secret=secret,
        method="GET",
    )
    if (data.get("payment_status") or "") != "paid" and (data.get("status") or "") != "complete":
        raise BillingError("Stripe session is not paid")
    meta = data.get("metadata") or {}
    return {
        "reference": meta.get("reference") or data.get("id"),
        "user_id": _intish(meta.get("user_id") or data.get("client_reference_id")),
        "plan": meta.get("plan"),
        "period": meta.get("period") or "month",
        "currency": "usd",
        "session_id": data.get("id"),
    }


def paystack_event_reference(payload: dict) -> str | None:
    event = (payload.get("event") or "").lower()
    if event not in {"charge.success", "transaction.success"}:
        return None
    data = payload.get("data") or {}
    if (data.get("status") or "").lower() not in {"success", "successful"}:
        return None
    return data.get("reference")


def stripe_event_session_id(payload: dict) -> str | None:
    if (payload.get("type") or "") != "checkout.session.completed":
        return None
    obj = payload.get("data", {}).get("object") or {}
    return obj.get("id")


def checkout_label(plan_id: str, period: str) -> str:
    plan = get_plan(plan_id)
    when = "year" if period == "year" else "month"
    return f"Provtara {plan['label']} ({when})"


def _intish(value) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _json_request(url: str, *, secret: str, body: dict | None = None, method: str = "POST") -> dict:
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {secret}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    return _read_json(req)


def _form_request(url: str, *, secret: str, fields: dict | None = None, method: str = "POST") -> dict:
    data = None if fields is None else urllib.parse.urlencode(fields).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {secret}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
    )
    return _read_json(req)


def _read_json(req: urllib.request.Request) -> dict:
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        raise BillingError(raw[:300] or str(exc)) from exc
    except urllib.error.URLError as exc:
        raise BillingError(str(exc.reason or exc)) from exc
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise BillingError("Provider returned non-JSON") from exc
    if not isinstance(payload, dict):
        raise BillingError("Provider returned an unexpected payload")
    return payload
