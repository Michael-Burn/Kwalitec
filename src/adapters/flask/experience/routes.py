"""Experience surface Flask routes — Home / Journey / Readiness / Coach."""

from __future__ import annotations

from typing import Any

from flask import Blueprint, Flask, render_template, request

from adapters.flask.dashboard.dependency_provider import get_dependencies
from adapters.flask.experience.controller import ExperienceSurfaceController
from adapters.flask.page_renderer import PageRenderer
from adapters.flask.template_mapper import (
    DASHBOARD_TEMPLATE,
    EXPERIENCE_SURFACE_TEMPLATE,
    MISSION_TEMPLATE,
)
from application.student_experience.integration.enums import JourneySurface

experience_bp = Blueprint(
    "eos_experience",
    __name__,
    url_prefix="/eos",
)


def _student_id() -> str | None:
    return (request.args.get("student_id") or "").strip() or None


@experience_bp.get("/home/")
def show_home() -> Any:
    """Render Home — live experience decision screen."""
    deps = get_dependencies()
    view_model, experience = ExperienceSurfaceController(deps).show_home(
        _student_id()
    )
    resolved = _student_id() or deps.student_id_resolver()
    context = PageRenderer().for_dashboard(
        view_model,
        student_id=resolved,
        from_surface=(request.args.get("from") or "").strip() or None,
        updated=(request.args.get("updated") or "").strip() or None,
        readiness_change_message=_readiness_change(experience),
        experience_success_message=_success(experience),
    )
    return render_template(DASHBOARD_TEMPLATE, **context)


@experience_bp.get("/journey/")
def show_journey() -> Any:
    """Render Learning Journey from the shared experience snapshot."""
    return _render_surface(JourneySurface.JOURNEY)


@experience_bp.get("/readiness/")
def show_readiness() -> Any:
    """Render Exam Readiness from the shared experience snapshot."""
    return _render_surface(JourneySurface.READINESS)


@experience_bp.get("/coach/")
def show_coach() -> Any:
    """Render Learning Coach from the shared experience snapshot."""
    return _render_surface(JourneySurface.COACH)


@experience_bp.get("/workspace/")
def show_workspace() -> Any:
    """Render Study Workspace — alias of mission with shared experience."""
    deps = get_dependencies()
    view_model, experience = ExperienceSurfaceController(deps).show_workspace(
        _student_id()
    )
    resolved = _student_id() or deps.student_id_resolver()
    context = PageRenderer().for_mission(view_model, student_id=resolved)
    context["readiness_change_message"] = _readiness_change(experience)
    context["experience_success_message"] = _success(experience)
    return render_template(MISSION_TEMPLATE, **context)


def _render_surface(surface: JourneySurface) -> Any:
    deps = get_dependencies()
    view, experience = ExperienceSurfaceController(deps).show_surface(
        surface, _student_id()
    )
    resolved = _student_id() or deps.student_id_resolver()
    context = PageRenderer().for_experience_surface(
        view,
        student_id=resolved,
        readiness_change_message=_readiness_change(experience),
        experience_success_message=_success(experience) or view.success_message,
    )
    return render_template(EXPERIENCE_SURFACE_TEMPLATE, **context)


def _readiness_change(experience: object | None) -> str | None:
    if experience is None:
        return None
    change = getattr(experience, "readiness_change", None)
    if change is None or not getattr(change, "changed", False):
        return None
    return (getattr(change, "message", None) or "").strip() or None


def _success(experience: object | None) -> str | None:
    if experience is None:
        return None
    for state in getattr(experience, "surface_states", ()) or ():
        message = (getattr(state, "success_message", None) or "").strip()
        if message:
            return message
    celebrations = getattr(experience, "celebrations", None)
    moments = getattr(celebrations, "moments", ()) or ()
    if moments:
        first = moments[0]
        return (
            getattr(first, "message", None)
            or getattr(first, "title", None)
            or ""
        ).strip() or None
    return None


def register_experience(app: Flask | object) -> None:
    """Register experience surface blueprints on a Flask application."""
    register = getattr(app, "register_blueprint", None)
    if register is None:
        raise TypeError("app must support register_blueprint")
    register(experience_bp)
