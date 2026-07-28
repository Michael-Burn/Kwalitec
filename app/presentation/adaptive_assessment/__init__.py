"""Adaptive Assessment presentation — Flask blueprint (ILE-001B).

Mission-embedded Quick Check learner experience. Thin HTTP only.
Educational authority remains outside this package.
"""

from __future__ import annotations

from flask import Blueprint

adaptive_assessment_bp = Blueprint(
    "adaptive_assessment",
    __name__,
    url_prefix="/adaptive-assessment",
)


def load_routes() -> None:
    """Import route handlers (side-effect registration)."""
    from app.presentation.adaptive_assessment import routes as _routes  # noqa: F401


__all__ = ["adaptive_assessment_bp", "load_routes"]
