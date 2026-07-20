"""Curriculum Studio UI — Flask blueprint under ``/founder/studio``.

Thin renderer of Curriculum Studio application snapshots for Founders.
Owns presentation only — no educational math or publication policy.
"""

from __future__ import annotations

from flask import Blueprint

studio_bp = Blueprint(
    "curriculum_studio",
    __name__,
    url_prefix="/founder/studio",
)


def load_routes() -> None:
    """Import route handlers (side-effect registration on ``studio_bp``)."""
    from app.presentation.curriculum_studio import routes as _routes  # noqa: F401


__all__ = ["load_routes", "studio_bp"]
