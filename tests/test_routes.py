"""
Tests for the Mood Journal API routes.
"""
import json
import os
import tempfile
import pytest
from app import create_app


@pytest.fixture()
def app():
    """Create a test app backed by a temporary file database."""
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    test_app = create_app()
    test_app.config.update({
        "TESTING": True,
        "DATABASE": db_path,
    })
    yield test_app
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture()
def client(app):
    return app.test_client()


class TestPages:
    def test_index_loads(self, client) -> None:
        res = client.get("/")
        assert res.status_code == 200
        assert b"Moodly" in res.data

    def test_dashboard_loads(self, client) -> None:
        res = client.get("/dashboard")
        assert res.status_code == 200

    def test_history_loads(self, client) -> None:
        res = client.get("/history")
        assert res.status_code == 200


class TestEntriesAPI:
    def test_get_entries_empty(self, client) -> None:
        res = client.get("/api/entries")
        assert res.status_code == 200
        assert res.get_json() == []

    def test_create_entry_valid(self, client) -> None:
        payload = {"mood": "happy", "note": "Great day!"}
        res = client.post(
            "/api/entries",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert res.status_code == 201
        data = res.get_json()
        assert data["mood"] == "happy"
        assert data["emoji"] == "😊"
        assert data["note"] == "Great day!"

    def test_create_entry_invalid_mood(self, client) -> None:
        payload = {"mood": "ecstatic"}
        res = client.post(
            "/api/entries",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert res.status_code == 400
        assert "error" in res.get_json()

    def test_create_entry_no_note(self, client) -> None:
        payload = {"mood": "neutral"}
        res = client.post(
            "/api/entries",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert res.status_code == 201
        assert res.get_json()["note"] is None

    def test_delete_entry(self, client) -> None:
        create_res = client.post(
            "/api/entries",
            data=json.dumps({"mood": "sad"}),
            content_type="application/json",
        )
        entry_id = create_res.get_json()["id"]
        del_res = client.delete(f"/api/entries/{entry_id}")
        assert del_res.status_code == 200

    def test_delete_nonexistent_entry(self, client) -> None:
        res = client.delete("/api/entries/99999")
        assert res.status_code == 404

    def test_entries_list_after_create(self, client) -> None:
        client.post(
            "/api/entries",
            data=json.dumps({"mood": "amazing", "note": "Wonderful!"}),
            content_type="application/json",
        )
        res = client.get("/api/entries")
        entries = res.get_json()
        assert len(entries) >= 1
        assert entries[0]["mood"] == "amazing"


class TestStatsAPI:
    def test_stats_empty(self, client) -> None:
        res = client.get("/api/stats")
        assert res.status_code == 200
        assert res.get_json() == []

    def test_stats_after_entries(self, client) -> None:
        for mood in ["happy", "happy", "sad"]:
            client.post(
                "/api/entries",
                data=json.dumps({"mood": mood}),
                content_type="application/json",
            )
        res = client.get("/api/stats")
        stats = res.get_json()
        happy_stat = next((s for s in stats if s["mood"] == "happy"), None)
        assert happy_stat is not None
        assert happy_stat["count"] == 2
