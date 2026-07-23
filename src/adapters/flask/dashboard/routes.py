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


def _experience_messages(experience: object | None) -> tuple[str | None, str | None]:
    if experience is None:
        return None, None
    readiness = None
    change = getattr(experience, "readiness_change", None)
    if change is not None and getattr(change, "changed", False):
        readiness = (getattr(change, "message", None) or "").strip() or None
    success = None
    for state in getattr(experience, "surface_states", ()) or ():
        message = (getattr(state, "success_message", None) or "").strip()
        if message:
            success = message
            break
    return readiness, success


@dashboard_bp.get("/")
def show_dashboard() -> Any:
    """Render the Student Dashboard 2.0 surface from the live experience."""
    deps = get_dependencies()
    student_id = (request.args.get("student_id") or "").strip() or None
    controller = DashboardController(deps)
    view_model = controller.show(student_id)
    experience = controller.current_experience(student_id)
    resolved = student_id or deps.student_id_resolver()
    readiness, success = _experience_messages(experience)
    context = PageRenderer().for_dashboard(
        view_model,
        student_id=resolved,
        from_surface=(request.args.get("from") or "").strip() or None,
        updated=(request.args.get("updated") or "").strip() or None,
        readiness_change_message=readiness,
        experience_success_message=success,
    )
    return render_template(DASHBOARD_TEMPLATE, **context)


def register_dashboard(app: Flask | object) -> None:
    """Register the dashboard blueprint on a Flask application."""
    register = getattr(app, "register_blueprint", None)
    if register is None:
        raise TypeError("app must support register_blueprint")
    register(dashboard_bp)
