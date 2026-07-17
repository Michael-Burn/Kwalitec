"""Founder Dashboard blueprint — Founder Command Centre (IAHF-003 / POP-002).

Single Founder operational home under ``/founder``. Historical FOS-004
presentation lives under Operations; live Product Check-in ops under Feedback.
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
