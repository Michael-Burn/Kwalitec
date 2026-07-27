"""Founder diagnostics for Student Digital Twin (SDT-001).

These endpoints exist for architecture validation and debugging.
They are NOT part of the student-facing experience.
"""

from __future__ import annotations

from flask import Blueprint

twin_diagnostics_bp = Blueprint(
    "student_digital_twin",
    __name__,
    url_prefix="/founder/twin",
)


def load_routes() -> None:
    """Import route modules so view functions register on the blueprint."""
    from app.presentation.student_digital_twin import routes as _routes  # noqa: F401
