"""WSGI entry point for production servers."""

from app import create_app
from app.models import User  # noqa: F401 - imported so Flask-Migrate sees models

app = create_app()
