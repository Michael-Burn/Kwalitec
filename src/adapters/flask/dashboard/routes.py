"""Student Dashboard Flask routes — thin HTTP glue over DashboardController."""

from __future__ import annotations

from typing import Any

from flask import Blueprint, Flask, render_template, request

from adapters.flask.dashboard.controller import DashboardController
from adapters.flask.dashboard.dependency_provider import get_dependencies
from adapters.flask.page_renderer import PageRenderer
from adapters.flask.template_mapper import DASHBOARD_TEMPLATE

dashboard_bp = Blueprint(
    "eos_dashboard",
    __name__,
    url_prefix="/eos/dashboard",
)


@dashboard_bp.get("/")
def show_dashboard() -> Any:
    """Render the Student Dashboard 2.0 surface."""
    deps = get_dependencies()
    student_id = (request.args.get("student_id") or "").strip() or None
    view_model = DashboardController(deps).show(student_id)
    resolved = student_id or deps.student_id_resolver()
    context = PageRenderer().for_dashboard(view_model, student_id=resolved)
    return render_template(DASHBOARD_TEMPLATE, **context)


def register_dashboard(app: Flask | object) -> None:
    """Register the dashboard blueprint on a Flask application."""
    register = getattr(app, "register_blueprint", None)
    if register is None:
        raise TypeError("app must support register_blueprint")
    register(dashboard_bp)
