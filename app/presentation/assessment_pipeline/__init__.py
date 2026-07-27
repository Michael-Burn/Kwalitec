"""Founder diagnostics for Assessment & Learning Feedback Pipeline (AP-001).

These endpoints exist for architecture validation and debugging.
They are NOT part of the student-facing experience.
"""

from __future__ import annotations

from flask import Blueprint

assessment_pipeline_diagnostics_bp = Blueprint(
    "assessment_pipeline",
    __name__,
    url_prefix="/founder/assessment",
)


def load_routes() -> None:
    """Import route modules so view functions register on the blueprint."""
    from app.presentation.assessment_pipeline import routes as _routes  # noqa: F401
