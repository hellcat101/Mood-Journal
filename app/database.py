"""Database utilities for the Mood Journal application."""
import sqlite3
from flask import Flask, g

_SCHEMA = """
    CREATE TABLE IF NOT EXISTS entries (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        mood       TEXT    NOT NULL,
        emoji      TEXT    NOT NULL,
        note       TEXT,
        created_at TEXT    NOT NULL DEFAULT (datetime('now'))
    )
"""


def get_db() -> sqlite3.Connection:
    """Return (or open) the per-request DB connection, creating schema if needed."""
    from flask import current_app
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row
        g.db.execute(_SCHEMA)
        g.db.commit()
    return g.db


def close_db(e=None) -> None:
    """Close the DB connection at the end of the request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app: Flask) -> None:
    """Register the teardown handler (schema creation is lazy via get_db)."""
    app.teardown_appcontext(close_db)
