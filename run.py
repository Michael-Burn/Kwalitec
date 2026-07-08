"""Local entry point for the Kwalitec application."""

from app import create_app
from app.models import User  # noqa: F401 - imported so Flask-Migrate sees models

app = create_app()


if __name__ == "__main__":
    app.run()
