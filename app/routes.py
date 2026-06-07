"""Defines the routes for the Mood Journal application."""
from flask import (
    Blueprint,
    jsonify,
    render_template,
    request,
)
from .database import get_db
from .models import Entry, MOOD_OPTIONS

main_bp = Blueprint("main", __name__)
api_bp = Blueprint("api", __name__)


# Page Routes 

@main_bp.route("/")
def index():
    """Home page: mood entry form."""
    return render_template("index.html", moods=MOOD_OPTIONS)


@main_bp.route("/dashboard")
def dashboard():
    """Dashboard page: weekly mood chart and recent entries."""
    return render_template("dashboard.html")


@main_bp.route("/history")
def history():
    """History page: all entries, newest first."""
    db = get_db()
    rows = db.execute(
        "SELECT * FROM entries ORDER BY created_at DESC"
    ).fetchall()
    entries = [Entry.from_row(r) for r in rows]
    return render_template("history.html", entries=entries)


# API Routes

@api_bp.route("/entries", methods=["GET"])
def get_entries():
    """Return all journal entries as JSON."""
    db = get_db()
    rows = db.execute(
        "SELECT * FROM entries ORDER BY created_at DESC"
    ).fetchall()
    return jsonify([Entry.from_row(r).to_dict() for r in rows])


@api_bp.route("/entries", methods=["POST"])
def create_entry():
    """Create a new mood entry. Expects JSON body."""
    data: dict = request.get_json(silent=True) or {}
    mood: str = data.get("mood", "").strip().lower()
    note: str = data.get("note", "").strip()

    if mood not in MOOD_OPTIONS:
        return jsonify({"error": f"Invalid mood. Choose from: {list(MOOD_OPTIONS)}"}), 400

    emoji = MOOD_OPTIONS[mood]
    db = get_db()
    cursor = db.execute(
        "INSERT INTO entries (mood, emoji, note) VALUES (?, ?, ?)",
        (mood, emoji, note or None),
    )
    db.commit()

    row = db.execute(
        "SELECT * FROM entries WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    return jsonify(Entry.from_row(row).to_dict()), 201


@api_bp.route("/entries/<int:entry_id>", methods=["DELETE"])
def delete_entry(entry_id: int):
    """Delete a journal entry by ID."""
    db = get_db()
    existing = db.execute(
        "SELECT id FROM entries WHERE id = ?", (entry_id,)
    ).fetchone()

    if existing is None:
        return jsonify({"error": "Entry not found"}), 404

    db.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
    db.commit()
    return jsonify({"message": "Entry deleted"}), 200


@api_bp.route("/stats", methods=["GET"])
def get_stats():
    """Return mood frequency stats for the last 7 days."""
    db = get_db()
    rows = db.execute("""
        SELECT mood, emoji, COUNT(*) as count
        FROM entries
        WHERE created_at >= datetime('now', '-7 days')
        GROUP BY mood
        ORDER BY count DESC
    """).fetchall()

    stats = [{"mood": r["mood"], "emoji": r["emoji"], "count": r["count"]} for r in rows]
    return jsonify(stats)
