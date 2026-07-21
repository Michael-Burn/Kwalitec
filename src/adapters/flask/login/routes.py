"""Student login Flask routes — identity only, no educational logic."""

from __future__ import annotations

from typing import Any

from flask import Blueprint, Flask, redirect, render_template, request, session

from adapters.flask.dashboard.dependency_provider import STUDENT_SESSION_KEY
from adapters.flask.navigation import DASHBOARD_PATH, with_query
from adapters.flask.template_mapper import LOGIN_TEMPLATE, TemplateMapper

login_bp = Blueprint(
    "eos_login",
    __name__,
    url_prefix="/eos/login",
)


@login_bp.get("/")
def show_login() -> Any:
    """Render the student identity form."""
    student_id = (request.args.get("student_id") or "").strip()
    context = TemplateMapper.for_login(student_id=student_id)
    return render_template(LOGIN_TEMPLATE, **context)


@login_bp.post("/")
def submit_login() -> Any:
    """Store student identity in the Flask session and open the dashboard."""
    student_id = (request.form.get("student_id") or "").strip()
    if not student_id:
        context = TemplateMapper.for_login(error="Student ID is required.")
        return render_template(LOGIN_TEMPLATE, **context), 400
    session[STUDENT_SESSION_KEY] = student_id
    return redirect(with_query(DASHBOARD_PATH, student_id=student_id))


def register_login(app: Flask | object) -> None:
    """Register the login blueprint on a Flask application."""
    register = getattr(app, "register_blueprint", None)
    if register is None:
        raise TypeError("app must support register_blueprint")
    register(login_bp)
