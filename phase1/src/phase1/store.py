from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from werkzeug.security import check_password_hash, generate_password_hash


def connect(path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL,
            plan TEXT NOT NULL DEFAULT 'free',
            currency TEXT NOT NULL DEFAULT 'usd',
            alerts_on INTEGER NOT NULL DEFAULT 1,
            last_alert_at TEXT,
            plan_requested TEXT
        );
        CREATE TABLE IF NOT EXISTS profiles (
            user_id INTEGER PRIMARY KEY,
            json TEXT NOT NULL,
            raw_text TEXT,
            confirmed_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS packs (
            user_id INTEGER NOT NULL,
            job_id TEXT NOT NULL,
            resume_text TEXT NOT NULL,
            letter_text TEXT NOT NULL,
            gap_markdown TEXT NOT NULL,
            created_at TEXT NOT NULL,
            PRIMARY KEY (user_id, job_id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS hidden (
            user_id INTEGER NOT NULL,
            job_id TEXT NOT NULL,
            PRIMARY KEY (user_id, job_id)
        );
        CREATE TABLE IF NOT EXISTS listings (
            id TEXT PRIMARY KEY,
            apply_url TEXT NOT NULL UNIQUE,
            source TEXT,
            json TEXT NOT NULL,
            fetched_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS apply_log (
            user_id INTEGER NOT NULL,
            job_id TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            PRIMARY KEY (user_id, job_id)
        );
        CREATE TABLE IF NOT EXISTS alerts_sent (
            user_id INTEGER NOT NULL,
            job_id TEXT NOT NULL,
            sent_at TEXT NOT NULL,
            PRIMARY KEY (user_id, job_id)
        );
        """
    )
    _ensure_column(conn, "users", "plan", "TEXT NOT NULL DEFAULT 'free'")
    _ensure_column(conn, "users", "currency", "TEXT NOT NULL DEFAULT 'usd'")
    _ensure_column(conn, "users", "alerts_on", "INTEGER NOT NULL DEFAULT 1")
    _ensure_column(conn, "users", "last_alert_at", "TEXT")
    _ensure_column(conn, "users", "plan_requested", "TEXT")
    conn.commit()


def _ensure_column(conn: sqlite3.Connection, table: str, name: str, spec: str) -> None:
    cols = {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}
    if name not in cols:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {name} {spec}")


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def create_user(
    conn: sqlite3.Connection,
    email: str,
    password: str,
    *,
    alerts_on: bool = True,
    currency: str = "usd",
) -> int:
    cur = conn.execute(
        """
        INSERT INTO users (email, password_hash, created_at, alerts_on, currency)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            email.lower().strip(),
            generate_password_hash(password),
            now(),
            1 if alerts_on else 0,
            "ngn" if currency.lower() == "ngn" else "usd",
        ),
    )
    conn.commit()
    return int(cur.lastrowid)


def get_user_by_email(conn: sqlite3.Connection, email: str):
    return conn.execute(
        "SELECT * FROM users WHERE email = ?", (email.lower().strip(),)
    ).fetchone()


def verify_user(conn: sqlite3.Connection, email: str, password: str):
    row = get_user_by_email(conn, email)
    if row is None:
        return None
    if not check_password_hash(row["password_hash"], password):
        return None
    return row


def save_profile(conn: sqlite3.Connection, user_id: int, data: dict, raw_text: str = "") -> None:
    conn.execute(
        """
        INSERT INTO profiles (user_id, json, raw_text, confirmed_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            json = excluded.json,
            raw_text = excluded.raw_text,
            confirmed_at = excluded.confirmed_at
        """,
        (user_id, json.dumps(data), raw_text, now()),
    )
    conn.commit()


def get_profile(conn: sqlite3.Connection, user_id: int) -> dict | None:
    row = conn.execute("SELECT json FROM profiles WHERE user_id = ?", (user_id,)).fetchone()
    if row is None:
        return None
    return json.loads(row["json"])


def save_pack(
    conn: sqlite3.Connection,
    user_id: int,
    job_id: str,
    resume_text: str,
    letter_text: str,
    gap_markdown: str,
) -> None:
    conn.execute(
        """
        INSERT INTO packs (user_id, job_id, resume_text, letter_text, gap_markdown, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id, job_id) DO UPDATE SET
            resume_text = excluded.resume_text,
            letter_text = excluded.letter_text,
            gap_markdown = excluded.gap_markdown,
            created_at = excluded.created_at
        """,
        (user_id, job_id, resume_text, letter_text, gap_markdown, now()),
    )
    conn.commit()


def get_pack(conn: sqlite3.Connection, user_id: int, job_id: str):
    return conn.execute(
        "SELECT * FROM packs WHERE user_id = ? AND job_id = ?",
        (user_id, job_id),
    ).fetchone()


def hide_job(conn: sqlite3.Connection, user_id: int, job_id: str) -> None:
    conn.execute(
        "INSERT OR IGNORE INTO hidden (user_id, job_id) VALUES (?, ?)",
        (user_id, job_id),
    )
    conn.commit()


def hidden_ids(conn: sqlite3.Connection, user_id: int) -> set[str]:
    rows = conn.execute("SELECT job_id FROM hidden WHERE user_id = ?", (user_id,)).fetchall()
    return {r["job_id"] for r in rows}


def save_listings(conn: sqlite3.Connection, jobs: list, source: str = "boards") -> int:
    from phase0.models import Job
    from phase1.ingest import job_source

    n = 0
    for job in jobs:
        if not isinstance(job, Job):
            continue
        origin = source if source != "boards" else job_source(job)
        payload = {
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "apply_url": job.apply_url,
            "remote": job.remote,
            "must_haves": list(job.must_haves),
            "nice_to_haves": list(job.nice_to_haves),
            "min_years": job.min_years,
            "work_authorization_any_of": list(job.work_authorization_any_of),
            "hook": job.hook,
            "description": job.description,
            "location": job.location,
        }
        conn.execute(
            """
            INSERT INTO listings (id, apply_url, source, json, fetched_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(apply_url) DO UPDATE SET
                json = excluded.json,
                source = excluded.source,
                fetched_at = excluded.fetched_at
            """,
            (job.id, job.apply_url, origin, json.dumps(payload), now()),
        )
        n += 1
    conn.commit()
    return n


def load_listings(conn: sqlite3.Connection) -> list:
    from phase0.qualify import job_from_dict

    rows = conn.execute("SELECT json FROM listings ORDER BY fetched_at DESC").fetchall()
    jobs = []
    for row in rows:
        try:
            jobs.append(job_from_dict(json.loads(row["json"])))
        except (KeyError, TypeError, json.JSONDecodeError):
            continue
    return jobs


def listing_count(conn: sqlite3.Connection) -> int:
    row = conn.execute("SELECT COUNT(*) AS n FROM listings").fetchone()
    return int(row["n"] if row else 0)


def last_fetched_at(conn: sqlite3.Connection) -> str | None:
    row = conn.execute("SELECT MAX(fetched_at) AS t FROM listings").fetchone()
    if row is None:
        return None
    return row["t"]


def refresh_is_stale(conn: sqlite3.Connection, seconds: int = 900) -> bool:
    stamp = last_fetched_at(conn)
    if not stamp:
        return True
    try:
        ts = datetime.fromisoformat(stamp)
    except ValueError:
        return True
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - ts).total_seconds() >= seconds


def log_apply(conn: sqlite3.Connection, user_id: int, job_id: str, status: str) -> None:
    conn.execute(
        """
        INSERT INTO apply_log (user_id, job_id, status, created_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id, job_id) DO UPDATE SET
            status = excluded.status,
            created_at = excluded.created_at
        """,
        (user_id, job_id, status, now()),
    )
    conn.commit()


def apply_status(conn: sqlite3.Connection, user_id: int) -> dict[str, str]:
    rows = conn.execute(
        "SELECT job_id, status FROM apply_log WHERE user_id = ?", (user_id,)
    ).fetchall()
    return {r["job_id"]: r["status"] for r in rows}


def get_user(conn: sqlite3.Connection, user_id: int):
    return conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


def set_alerts(conn: sqlite3.Connection, user_id: int, on: bool) -> None:
    conn.execute("UPDATE users SET alerts_on = ? WHERE id = ?", (1 if on else 0, user_id))
    conn.commit()


def set_plan_request(conn: sqlite3.Connection, user_id: int, plan: str, currency: str) -> None:
    conn.execute(
        "UPDATE users SET plan_requested = ?, currency = ? WHERE id = ?",
        (plan, currency, user_id),
    )
    conn.commit()


def set_plan(conn: sqlite3.Connection, user_id: int, plan: str) -> None:
    conn.execute("UPDATE users SET plan = ? WHERE id = ?", (plan, user_id))
    conn.commit()


def packs_this_month(conn: sqlite3.Connection, user_id: int) -> int:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-01T00:00:00+00:00")
    row = conn.execute(
        "SELECT COUNT(*) AS n FROM packs WHERE user_id = ? AND created_at >= ?",
        (user_id, stamp),
    ).fetchone()
    return int(row["n"] if row else 0)


def alert_users(conn: sqlite3.Connection):
    return conn.execute(
        "SELECT * FROM users WHERE alerts_on = 1"
    ).fetchall()


def mark_alert_sent(conn: sqlite3.Connection, user_id: int, job_id: str) -> None:
    conn.execute(
        "INSERT OR IGNORE INTO alerts_sent (user_id, job_id, sent_at) VALUES (?, ?, ?)",
        (user_id, job_id, now()),
    )
    conn.execute("UPDATE users SET last_alert_at = ? WHERE id = ?", (now(), user_id))
    conn.commit()


def alert_already_sent(conn: sqlite3.Connection, user_id: int, job_id: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM alerts_sent WHERE user_id = ? AND job_id = ?",
        (user_id, job_id),
    ).fetchone()
    return row is not None

