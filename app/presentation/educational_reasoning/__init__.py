"""Founder diagnostics for Educational Reasoning Engine (SDT-002).

These endpoints exist for architecture validation and debugging.
They are NOT part of the student-facing experience.
"""

from __future__ import annotations

from flask import Blueprint

reasoning_diagnostics_bp = Blueprint(
    "educational_reasoning",
    __name__,
    url_prefix="/founder/reasoning",
)


def load_routes() -> None:
    """Import route modules so view functions register on the blueprint."""
    from app.presentation.educational_reasoning import routes as _routes  # noqa: F401
