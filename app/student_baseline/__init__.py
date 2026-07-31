"""SB-001A Student Baseline presentation — progressive educational origin."""

from __future__ import annotations

from flask import Blueprint

student_baseline_bp = Blueprint(
    "student_baseline",
    __name__,
    url_prefix="/baseline",
)

from app.student_baseline import routes as _routes  # noqa: E402, F401
