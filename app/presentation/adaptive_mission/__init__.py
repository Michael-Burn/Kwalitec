"""Founder diagnostics for Adaptive Mission Engine (AME-001).

These endpoints exist for architecture validation and debugging.
They are NOT part of the student-facing experience.
"""

from __future__ import annotations

from flask import Blueprint

adaptive_mission_diagnostics_bp = Blueprint(
    "adaptive_mission",
    __name__,
    url_prefix="/founder/missions",
)


def load_routes() -> None:
    """Import route modules so view functions register on the blueprint."""
    from app.presentation.adaptive_mission import routes as _routes  # noqa: F401
