# Moodly 🌱 — Mood Journal

A minimal daily mood tracker built with Flask, SQLite, and vanilla JS.

## Features

- Log your daily mood (5 options) with an optional note
- Dashboard with a weekly mood bar chart and recent entries
- Full history with delete support
- REST API with 4 endpoints
- SQLite database (zero config)
- Docker support

## Project Structure

```
mood-journal/
├── app/
│   ├── __init__.py       # App factory
│   ├── database.py       # SQLite helpers
│   ├── models.py         # Entry dataclass + mood options
│   ├── routes.py         # Flask blueprints (pages + API)
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/           # main.js, log.js, dashboard.js, history.js
│   └── templates/        # base.html, index.html, dashboard.html, history.html
├── tests/
│   └── test_routes.py    # pytest test suite
├── run.py                # Entry point
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .gitignore
```

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/api/entries` | List all entries |
| POST | `/api/entries` | Create a new entry |
| DELETE | `/api/entries/<id>` | Delete an entry |
| GET | `/api/stats` | Mood counts (last 7 days) |

**POST `/api/entries` body:**
```json
{ "mood": "happy", "note": "Great day!" }
```
Valid moods: `amazing`, `happy`, `neutral`, `sad`, `awful`

## Running Locally

```bash
# 1. Create virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python run.py
# Visit http://localhost:5000
```

## Running with Docker

```bash
docker-compose up --build
# Visit http://localhost:5000
```

## Running Tests

```bash
pytest tests/ -v
```
