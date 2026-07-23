"""Internal Alpha operational surfaces — ALPHA-001.

Onboarding, lightweight feedback, telemetry ingest, and support/help.
Does not implement educational features or modify Education OS.
"""

from __future__ import annotations

from flask import Blueprint

alpha_bp = Blueprint("alpha", __name__, url_prefix="/alpha")

from app.alpha import routes as _routes  # noqa: E402, F401
