"""Learning Session Experience UI — Flask blueprint under ``/session``.

Thin renderer of Session Experience application snapshots.
Owns presentation, minimal chrome, and view-model formatting only.
"""

from __future__ import annotations

from flask import Blueprint

session_bp = Blueprint(
    "session",
    __name__,
    url_prefix="/session",
)


def load_routes() -> None:
    """Import route handlers (side-effect registration on ``session_bp``)."""
    from app.presentation.session import routes as _routes  # noqa: F401


__all__ = ["load_routes", "session_bp"]
