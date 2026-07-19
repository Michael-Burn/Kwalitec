"""Student Experience UI — Flask blueprint under ``/student``.

Thin renderer of Student Experience application snapshots.
Owns presentation, navigation chrome, and view-model formatting only.
"""

from __future__ import annotations

from flask import Blueprint

student_bp = Blueprint(
    "student",
    __name__,
    url_prefix="/student",
)


def load_routes() -> None:
    """Import route handlers (side-effect registration on ``student_bp``)."""
    from app.presentation.student import routes as _routes  # noqa: F401


__all__ = ["load_routes", "student_bp"]
