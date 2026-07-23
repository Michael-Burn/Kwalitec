"""Mission Workspace Flask routes — thin HTTP glue over MissionController."""

from __future__ import annotations

from typing import Any

from flask import Blueprint, Flask, render_template, request

from adapters.flask.dashboard.dependency_provider import get_dependencies
from adapters.flask.mission.controller import MissionController
from adapters.flask.page_renderer import PageRenderer
from adapters.flask.template_mapper import MISSION_TEMPLATE

mission_bp = Blueprint(
    "eos_mission",
    __name__,
    url_prefix="/eos/mission",
)


@mission_bp.get("/")
def show_mission() -> Any:
    """Render the mission workspace surface from the live experience."""
    deps = get_dependencies()
    controller = MissionController(deps)
    student_id = (request.args.get("student_id") or "").strip() or None
    view_model = controller.show(student_id)
    experience = controller.current_experience(student_id)
    resolved = student_id or deps.student_id_resolver()
    context = PageRenderer().for_mission(view_model, student_id=resolved)
    if experience is not None:
        change = getattr(experience, "readiness_change", None)
        if change is not None and getattr(change, "changed", False):
            context["readiness_change_message"] = (
                getattr(change, "message", None) or ""
            ).strip() or None
    return render_template(MISSION_TEMPLATE, **context)


def register_mission(app: Flask | object) -> None:
    """Register the mission blueprint on a Flask application."""
    register = getattr(app, "register_blueprint", None)
    if register is None:
        raise TypeError("app must support register_blueprint")
    register(mission_bp)
