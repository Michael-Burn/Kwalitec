"""Reflection Flask routes — thin HTTP glue over ReflectionController."""

from __future__ import annotations

from typing import Any

from flask import Blueprint, Flask, redirect, render_template, request

from adapters.flask.dashboard.dependency_provider import get_dependencies
from adapters.flask.navigation import DASHBOARD_PATH, with_query
from adapters.flask.page_renderer import PageRenderer
from adapters.flask.reflection.controller import ReflectionController
from adapters.flask.session.controller import SessionController
from adapters.flask.template_mapper import REFLECTION_TEMPLATE

reflection_bp = Blueprint(
    "eos_reflection",
    __name__,
    url_prefix="/eos/reflection",
)


def _ids() -> tuple[str | None, str | None]:
    student_id = (request.args.get("student_id") or "").strip() or None
    session_id = (request.args.get("session_id") or "").strip() or None
    return student_id, session_id


@reflection_bp.get("/")
def show_reflection() -> Any:
    """Render the reflection workspace for the current / requested session."""
    deps = get_dependencies()
    student_id, session_id = _ids()
    session_vm = SessionController(deps).show(student_id, session_id=session_id)
    view_model = ReflectionController(deps).show(
        session_vm,
        confidence=(request.args.get("confidence") or "").strip() or None,
        difficulty=(request.args.get("difficulty") or "").strip() or None,
        weak_concept=(request.args.get("weak_concept") or "").strip() or None,
        student_notes=(request.args.get("student_notes") or "").strip() or None,
    )
    resolved = student_id or deps.student_id_resolver()
    context = PageRenderer().for_reflection(
        view_model, student_id=resolved, session_id=session_id or ""
    )
    return render_template(REFLECTION_TEMPLATE, **context)


@reflection_bp.post("/")
def submit_reflection() -> Any:
    """Capture reflection evidence, update storage, optionally redirect."""
    deps = get_dependencies()
    form = request.form
    student_id = (
        form.get("student_id") or request.args.get("student_id") or ""
    ).strip()
    session_id = (
        form.get("session_id") or request.args.get("session_id") or ""
    ).strip()
    session_vm = SessionController(deps).show(
        student_id or None,
        session_id=session_id or None,
    )
    result = ReflectionController(deps).submit(
        session_vm,
        student_id=student_id or None,
        mission_id=(form.get("mission_id") or "").strip() or None,
        confidence=(form.get("confidence") or "").strip() or None,
        difficulty=(form.get("difficulty") or "").strip() or None,
        weak_concept=(form.get("weak_concept") or "").strip() or None,
        student_notes=(form.get("student_notes") or "").strip() or None,
    )
    if (form.get("redirect") or "").strip().lower() in {"1", "true", "yes"}:
        return redirect(with_query(DASHBOARD_PATH, student_id=student_id or None))
    context = PageRenderer().for_reflection(
        result.view_model,
        student_id=student_id,
        session_id=session_id,
        evidence_updated=result.update_result is not None,
    )
    return render_template(REFLECTION_TEMPLATE, **context)


def register_reflection(app: Flask | object) -> None:
    """Register the reflection blueprint on a Flask application."""
    register = getattr(app, "register_blueprint", None)
    if register is None:
        raise TypeError("app must support register_blueprint")
    register(reflection_bp)
