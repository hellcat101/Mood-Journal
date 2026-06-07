"""Mood Journal Flask App Initialization."""
from flask import Flask
from .database import init_db


def create_app() -> Flask:
    """Application factory for the Mood Journal Flask app."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret-key-change-in-production"
    app.config["DATABASE"] = "mood_journal.db"

    init_db(app)

    from .routes import main_bp, api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
