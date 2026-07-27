"""Founder diagnostics for Learning Graph (SDT-003).

These endpoints exist for architecture validation and debugging.
They are NOT part of the student-facing experience.
"""

from __future__ import annotations

from flask import Blueprint

learning_graph_diagnostics_bp = Blueprint(
    "learning_graph",
    __name__,
    url_prefix="/founder/learning-graph",
)


def load_routes() -> None:
    """Import route modules so view functions register on the blueprint."""
    from app.presentation.learning_graph import routes as _routes  # noqa: F401
