"""Founder diagnostics for Evidence-Backed Intelligent Tutor (TUTOR-001).

These endpoints exist for architecture validation and debugging.
They are NOT part of the student-facing experience redesign.
"""

from __future__ import annotations

from flask import Blueprint

intelligent_tutor_diagnostics_bp = Blueprint(
    "intelligent_tutor",
    __name__,
    url_prefix="/founder/tutor",
)


def load_routes() -> None:
    """Import route modules so view functions register on the blueprint."""
    from app.presentation.intelligent_tutor import routes as _routes  # noqa: F401
