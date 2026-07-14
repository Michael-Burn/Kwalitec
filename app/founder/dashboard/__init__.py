"""Founder Dashboard blueprint (FOS-004).

Version 1 presentation layer over Knowledge Engine, Capability Archive,
and Internal Alpha Pipeline outputs.
"""

from __future__ import annotations

from flask import Blueprint

founder_dashboard_bp = Blueprint(
    "founder_dashboard",
    __name__,
    url_prefix="/founder",
    template_folder="templates",
    static_folder="static",
    static_url_path="/static",
)

from app.founder.dashboard import routes as _routes  # noqa: E402, F401

__all__ = ["founder_dashboard_bp"]
