import sqlite3
from datetime import datetime, timedelta

import pytest

from DataAccess.Matches.MatchesDB import MatchesDB


def test_init_matches_table_creates_matchcache_table():
    conn = sqlite3.connect(":memory:")
    db = MatchesDB(conn)

    db.initMatchesTable()

    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='MatchCache';"
    )

    assert cursor.fetchone() == ("MatchCache",)


def test_add_matches_and_get_matches_round_trip():
    conn = sqlite3.connect(":memory:")
    db = MatchesDB(conn)

    db.initMatchesTable()

    match_id = "match-123"
    end_time = int(datetime.utcnow().timestamp())
    data = '{"winner":"blue"}'

    db.addMatches(match_id, end_time, data)

    rows = db.getMatches()

    assert rows == [(match_id, end_time, data)]


def test_clear_past_days_uses_parameter_tuple(monkeypatch):
    conn = sqlite3.connect(":memory:")
    db = MatchesDB(conn)

    captured = {}

    def fake_send_void_command(self, query, args=None):
        captured["query"] = query
        captured["args"] = args

    monkeypatch.setattr(MatchesDB.__base__, "sendVoidCommand", fake_send_void_command)

    db.clearPastDays(7)

    assert captured["query"] == "DELETE FROM MatchCache WHERE EndTimeSecondsPastEpoch < ?;"
    assert isinstance(captured["args"], int)
