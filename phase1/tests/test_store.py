from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

from phase1.store import BOARD_REFRESH_SECONDS, connect, init_db, refresh_is_stale


def test_board_refresh_interval_is_four_hours():
    assert BOARD_REFRESH_SECONDS == 4 * 60 * 60


def test_refresh_is_stale_when_empty_or_older_than_four_hours(tmp_path: Path):
    conn = connect(tmp_path / "listings.db")
    init_db(conn)
    assert refresh_is_stale(conn) is True
    now = datetime.now(timezone.utc)
    conn.execute(
        "INSERT INTO listings (id, apply_url, source, json, fetched_at) VALUES (?,?,?,?,?)",
        ("fresh", "https://example.com/fresh", "test", "{}", now.isoformat()),
    )
    conn.commit()
    assert refresh_is_stale(conn) is False
    conn.execute(
        "UPDATE listings SET fetched_at = ? WHERE id = ?",
        ((now - timedelta(hours=3, minutes=50)).isoformat(), "fresh"),
    )
    conn.commit()
    assert refresh_is_stale(conn) is False
    conn.execute(
        "UPDATE listings SET fetched_at = ? WHERE id = ?",
        ((now - timedelta(hours=4, minutes=1)).isoformat(), "fresh"),
    )
    conn.commit()
    assert refresh_is_stale(conn) is True
