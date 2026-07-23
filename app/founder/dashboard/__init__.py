"""Kwalitec Console blueprint — operational portal (CONSOLE-001).

Primary entry under ``/console``. Legacy ``/founder`` URLs redirect here.
Historical FOS-004 presentation lives under System Operations; live Product
Check-in ops under Support.
"""

from __future__ import annotations

from flask import Blueprint

founder_dashboard_bp = Blueprint(
    "founder_dashboard",
    __name__,
    url_prefix="/console",
    template_folder="templates",
    static_folder="static",
    static_url_path="/static",
)

from app.founder.dashboard import routes as _routes  # noqa: E402, F401

__all__ = ["founder_dashboard_bp"]
