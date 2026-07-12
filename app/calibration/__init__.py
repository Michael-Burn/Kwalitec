"""Student Calibration blueprint — Study Plan → Calibration product surface."""

from __future__ import annotations

from flask import Blueprint

calibration_bp = Blueprint("calibration", __name__, url_prefix="/calibration")

from app.calibration import routes as _routes  # noqa: E402, F401
