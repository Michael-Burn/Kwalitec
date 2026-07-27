"""Assessment Delivery UI — Flask blueprint under ``/assessment``.

Thin renderer of Assessment Delivery application snapshots.
Educational authority stays in application/assessment. No Twin / Reasoning.
"""

from __future__ import annotations

from flask import Blueprint

assessment_bp = Blueprint(
    "assessment",
    __name__,
    url_prefix="/assessment",
)


def load_routes() -> None:
    """Import route handlers (side-effect registration on ``assessment_bp``)."""
    from app.presentation.assessment import routes as _routes  # noqa: F401


__all__ = ["assessment_bp", "load_routes"]
