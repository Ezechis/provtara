from __future__ import annotations

import hmac
import hashlib
import json
from datetime import datetime, timedelta, timezone

from phase1.billing import (
    amount_for,
    paid_until_iso,
    paystack_signature,
    stripe_signature,
    verify_paystack_signature,
    verify_stripe_signature,
)
from phase1.web import create_app
from phase1.plans import get_plan
from phase1.store import (
    activate_payment,
    connect,
    create_payment,
    create_user,
    effective_plan_id,
    get_payment,
    get_user,
    get_user_by_email,
    init_db,
)


def test_amount_for_ngn_and_usd_month_and_year():
    basic = get_plan("basic")
    kobo, ccy = amount_for(basic, "ngn", "month")
    assert ccy == "NGN"
    assert kobo == 5000 * 100
    naira_year, _ = amount_for(basic, "ngn", "year")
    assert naira_year == 50000 * 100
    cents, usd = amount_for(basic, "usd", "month")
    assert usd == "USD"
    assert cents == 9 * 100
    year_cents, _ = amount_for(get_plan("pro"), "usd", "year")
    assert year_cents == 190 * 100


def test_paystack_and_stripe_signatures_round_trip():
    body = b'{"event":"charge.success"}'
    ps = paystack_signature("sk_test", body)
    assert verify_paystack_signature("sk_test", body, ps)
    assert not verify_paystack_signature("sk_other", body, ps)
    st = stripe_signature("whsec_test", body, ts="123")
    header = f"t=123,v1={st}"
    assert verify_stripe_signature("whsec_test", body, header)
    assert not verify_stripe_signature("whsec_other", body, header)


def test_payment_webhook_activates_plan_and_is_idempotent(tmp_path):
    conn = connect(tmp_path / "bill.db")
    init_db(conn)
    uid = create_user(conn, "ada@example.com", "correct-horse")
    create_payment(
        conn,
        user_id=uid,
        provider="paystack",
        reference="ref-1",
        plan="pro",
        currency="ngn",
        period="month",
        amount=1200000,
    )
    first = activate_payment(conn, "ref-1")
    second = activate_payment(conn, "ref-1")
    assert first is True
    assert second is False
    row = get_user(conn, uid)
    assert row["plan"] == "pro"
    assert row["currency"] == "ngn"
    until = datetime.fromisoformat(row["paid_until"])
    if until.tzinfo is None:
        until = until.replace(tzinfo=timezone.utc)
    assert until > datetime.now(timezone.utc) + timedelta(days=20)
    pay = get_payment(conn, "ref-1")
    assert pay["status"] == "paid"


def test_expired_paid_until_falls_back_to_free(tmp_path):
    conn = connect(tmp_path / "exp.db")
    init_db(conn)
    uid = create_user(conn, "ada@example.com", "correct-horse")
    past = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(timespec="seconds")
    conn.execute(
        "UPDATE users SET plan = ?, paid_until = ? WHERE id = ?",
        ("premium", past, uid),
    )
    conn.commit()
    row = get_user(conn, uid)
    assert effective_plan_id(row) == "free"


PHASE0 = __import__("pathlib").Path(__file__).resolve().parents[2] / "phase0"


def _app(tmp_path, **extra):
    cfg = {
        "TESTING": True,
        "SECRET_KEY": "test",
        "DATABASE": str(tmp_path / "pay.db"),
        "JOBS_DIR": str(PHASE0 / "fixtures" / "jobs"),
        "PAYSTACK_SECRET_KEY": "sk_test_paystack",
        "STRIPE_SECRET_KEY": "sk_test_stripe",
        "STRIPE_WEBHOOK_SECRET": "whsec_test",
    }
    cfg.update(extra)
    return create_app(cfg)


def test_checkout_requires_login(tmp_path):
    client = _app(tmp_path).test_client()
    r = client.post(
        "/billing/checkout",
        data={"plan": "basic", "currency": "ngn", "period": "month"},
        follow_redirects=False,
    )
    assert r.status_code in (302, 303)
    assert "/login" in (r.headers.get("Location") or "")


def test_ngn_checkout_without_key_stays_on_pricing(tmp_path):
    app = _app(tmp_path, PAYSTACK_SECRET_KEY="")
    client = app.test_client()
    client.post("/register", data={"email": "ada@example.com", "password": "correct-horse"}, follow_redirects=True)
    client.post("/login", data={"email": "ada@example.com", "password": "correct-horse"}, follow_redirects=True)
    r = client.post(
        "/billing/checkout",
        data={"plan": "basic", "currency": "ngn", "period": "month"},
        follow_redirects=True,
    )
    body = r.get_data(as_text=True)
    assert "PAYSTACK_SECRET_KEY" in body
    conn = connect(app.config["DATABASE"])
    init_db(conn)
    row = get_user_by_email(conn, "ada@example.com")
    assert effective_plan_id(row) == "free"


def test_paystack_webhook_upgrades_logged_in_user(tmp_path):
    app = _app(tmp_path)
    client = app.test_client()
    client.post("/register", data={"email": "ada@example.com", "password": "correct-horse"}, follow_redirects=True)
    client.post("/login", data={"email": "ada@example.com", "password": "correct-horse"}, follow_redirects=True)
    conn = connect(app.config["DATABASE"])
    init_db(conn)
    uid = get_user_by_email(conn, "ada@example.com")["id"]
    create_payment(
        conn,
        user_id=uid,
        provider="paystack",
        reference="ref-live",
        plan="basic",
        currency="ngn",
        period="month",
        amount=500000,
    )
    body = json.dumps(
        {"event": "charge.success", "data": {"status": "success", "reference": "ref-live"}}
    ).encode()
    sig = paystack_signature("sk_test_paystack", body)
    r = client.post(
        "/billing/paystack/webhook",
        data=body,
        headers={"X-Paystack-Signature": sig, "Content-Type": "application/json"},
    )
    assert r.status_code == 200
    row = get_user(conn, uid)
    assert row["plan"] == "basic"
    assert effective_plan_id(row) == "basic"


def test_stripe_webhook_upgrades_user(tmp_path):
    app = _app(tmp_path)
    client = app.test_client()
    client.post("/register", data={"email": "ada@example.com", "password": "correct-horse"}, follow_redirects=True)
    conn = connect(app.config["DATABASE"])
    init_db(conn)
    uid = get_user_by_email(conn, "ada@example.com")["id"]
    body = json.dumps(
        {
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "id": "cs_test_1",
                    "client_reference_id": str(uid),
                    "metadata": {
                        "user_id": str(uid),
                        "plan": "premium",
                        "period": "year",
                        "reference": "prv_stripe_1",
                    },
                }
            },
        }
    ).encode()
    sig = stripe_signature("whsec_test", body, ts="111")
    r = client.post(
        "/billing/stripe/webhook",
        data=body,
        headers={"Stripe-Signature": f"t=111,v1={sig}", "Content-Type": "application/json"},
    )
    assert r.status_code == 200
    row = get_user(conn, uid)
    assert row["plan"] == "premium"
    assert row["currency"] == "usd"


def test_pricing_shows_pay_buttons_when_logged_in(tmp_path):
    client = _app(tmp_path).test_client()
    client.post("/register", data={"email": "ada@example.com", "password": "correct-horse"}, follow_redirects=True)
    client.post("/login", data={"email": "ada@example.com", "password": "correct-horse"}, follow_redirects=True)
    body = client.get("/pricing?currency=usd").get_data(as_text=True)
    assert "Pay $9 / month" in body or "Pay $9" in body
    assert 'name="period" value="year"' in body
    assert "/billing/checkout" in body
