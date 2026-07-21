"""Study Session Flask routes — thin HTTP glue over SessionController."""

from __future__ import annotations

from typing import Any

from flask import Blueprint, Flask, redirect, render_template, request, session

from adapters.flask.checkpoint_store import MappingCheckpointStore
from adapters.flask.dashboard.dependency_provider import get_dependencies
from adapters.flask.page_renderer import PageRenderer
from adapters.flask.session.controller import SessionController
from adapters.flask.template_mapper import SESSION_TEMPLATE

session_bp = Blueprint(
    "eos_session",
    __name__,
    url_prefix="/eos/session",
)


def _store():
    deps = get_dependencies()
    return deps.checkpoint_store or MappingCheckpointStore(session)


def _render(
    controller: SessionController,
    student_id: str | None,
    session_id: str | None,
):
    runtime = controller.load_runtime(
        student_id, session_id=session_id, store=_store()
    )
    resolved = student_id or get_dependencies().student_id_resolver()
    context = PageRenderer().for_session(
        runtime.view_model,
        student_id=resolved,
        session_id=runtime.state.session_id,
        stage=runtime.state.stage.value,
        paused=runtime.state.paused,
    )
    return render_template(SESSION_TEMPLATE, **context)


@session_bp.get("/")
def show_session() -> Any:
    """Render the guided study-session surface."""
    deps = get_dependencies()
    controller = SessionController(deps)
    student_id = (request.args.get("student_id") or "").strip() or None
    session_id = (request.args.get("session_id") or "").strip() or None
    return _render(controller, student_id, session_id)


@session_bp.get("/<session_id>")
def show_session_by_id(session_id: str) -> Any:
    """Render a study session addressed by path identity."""
    deps = get_dependencies()
    controller = SessionController(deps)
    student_id = (request.args.get("student_id") or "").strip() or None
    return _render(controller, student_id, session_id)


@session_bp.post("/action")
def session_action() -> Any:
    """Apply a Session Runtime lifecycle action and re-render or redirect."""
    deps = get_dependencies()
    controller = SessionController(deps)
    form = request.form
    student_id = (
        form.get("student_id") or request.args.get("student_id") or ""
    ).strip()
    session_id = (
        form.get("session_id") or request.args.get("session_id") or ""
    ).strip()
    result = controller.apply_action(
        form.get("action") or "",
        student_id or None,
        session_id=session_id or None,
        store=_store(),
    )
    if result.redirect_path:
        return redirect(result.redirect_path)
    return _render(controller, student_id or None, result.state.session_id)


def register_session(app: Flask | object) -> None:
    """Register the session blueprint on a Flask application."""
    register = getattr(app, "register_blueprint", None)
    if register is None:
        raise TypeError("app must support register_blueprint")
    register(session_bp)
