from dataclasses import dataclass
from typing import Optional


MOOD_OPTIONS: dict[str, str] = {
    "amazing": "🌟",
    "happy": "😊",
    "neutral": "😐",
    "sad": "😔",
    "awful": "😢",
}


@dataclass
class Entry:
    """Represents a single mood journal entry."""
    id: int
    mood: str
    emoji: str
    note: Optional[str]
    created_at: str

    def to_dict(self) -> dict:
        """Serialize entry to a JSON-friendly dictionary."""
        return {
            "id": self.id,
            "mood": self.mood,
            "emoji": self.emoji,
            "note": self.note,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_row(row) -> "Entry":
        """Create an Entry instance from a sqlite3.Row object."""
        return Entry(
            id=row["id"],
            mood=row["mood"],
            emoji=row["emoji"],
            note=row["note"],
            created_at=row["created_at"],
        )
