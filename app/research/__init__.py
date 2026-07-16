"""Research Intelligence blueprint — product check-in (RIP-001)."""

from __future__ import annotations

from flask import Blueprint

research_bp = Blueprint("research", __name__, url_prefix="/research")

from app.research import routes as _routes  # noqa: E402, F401
