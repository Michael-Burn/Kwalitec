"""View helpers for Learning Session Experience routes."""

from __future__ import annotations

from flask import redirect, url_for
from flask_login import current_user
from werkzeug.wrappers import Response

from app.application.session_experience.dto.activity_snapshot import ActivitySnapshot
from app.application.session_experience.dto.completion_snapshot import (
    CompletionSnapshot,
)
from app.application.session_experience.dto.overview_snapshot import OverviewSnapshot
from app.application.session_experience.dto.reflection_snapshot import (
    ReflectionSnapshot,
)
from app.application.session_experience.exceptions import SessionOwnershipError
from app.application.session_experience.facade import SessionExperienceService
from app.domain.session_experience.session_workspace import (
    SessionSurface,
    surface_index,
)
from app.presentation.session.factory import get_session_experience_service
from app.presentation.session.navigation import SURFACE_ENDPOINTS
from app.presentation.session.view_models import SessionPageViewModel, page_from_flow


def student_id() -> str:
    """Stable student identity for the authenticated user."""
    return str(current_user.id)


def service() -> SessionExperienceService:
    return get_session_experience_service()


def assert_session_owned(session_id: str) -> None:
    """Raise when the session belongs to a different student (IDOR guard)."""
    sid = student_id()
    sess = session_id.strip()
    svc = service()
    workspace = svc.registry.get_workspace_for_session(sess)
    if workspace is not None and workspace.student_id != sid:
        raise SessionOwnershipError(
            f"session {sess} is not owned by student {sid}"
        )


def resume_redirect_if_needed(
    session_id: str, requested: SessionSurface | str
) -> Response | None:
    """Redirect to the active surface when URL would rewind or skip ahead.

    Interrupt → resume must restore the workspace position rather than
    silently resetting to Overview when the student re-enters the session.
    """
    assert_session_owned(session_id)
    svc = service()
    workspace = svc.registry.get_workspace_for_session(session_id)
    if workspace is None:
        svc.open_session(student_id(), session_id=session_id)
        workspace = svc.registry.get_workspace_for_session(session_id)
    if workspace is None:
        return None
    if workspace.student_id != student_id():
        raise SessionOwnershipError(
            f"session {session_id} is not owned by student {student_id()}"
        )
    target = SessionSurface(str(requested).strip().lower())
    active = workspace.active_surface
    if surface_index(target) != surface_index(active):
        endpoint = SURFACE_ENDPOINTS[active]
        return redirect(url_for(endpoint, session_id=session_id))
    return None


def load_page(
    session_id: str, surface: SessionSurface | str
) -> SessionPageViewModel:
    """Load a session surface page for the current student.

    Does not rewind or skip the workspace via URL. Callers should use
    ``resume_redirect_if_needed`` first so interrupt/resume restores the
    active surface correctly.
    """
    _ = surface  # Enforced by resume_redirect_if_needed before render.
    assert_session_owned(session_id)
    svc = service()
    workspace = svc.registry.get_workspace_for_session(session_id)
    if workspace is None:
        svc.open_session(student_id(), session_id=session_id)
        workspace = svc.registry.get_workspace_for_session(session_id)
    if workspace is not None and workspace.student_id != student_id():
        raise SessionOwnershipError(
            f"session {session_id} is not owned by student {student_id()}"
        )
    flow = svc.get_flow(student_id(), session_id=session_id)
    return page_from_flow(flow)


def open_overview(
    *, session_id: str | None = None, mission_id: str | None = None
) -> OverviewSnapshot:
    """Open Session Overview after Student Home Start Session."""
    return service().open_session(
        student_id(), session_id=session_id, mission_id=mission_id
    )


def begin_session(*, session_id: str) -> OverviewSnapshot:
    assert_session_owned(session_id)
    return service().begin_session(student_id(), session_id=session_id)


def submit_answer(
    *, session_id: str, activity_id: str, response: str
) -> ActivitySnapshot:
    assert_session_owned(session_id)
    return service().submit_response(
        student_id(),
        session_id=session_id,
        activity_id=activity_id,
        response=response,
    )


def advance_activity(*, session_id: str) -> ActivitySnapshot | None:
    assert_session_owned(session_id)
    return service().advance_activity(student_id(), session_id=session_id)


def continue_reflection(*, session_id: str) -> ReflectionSnapshot:
    assert_session_owned(session_id)
    return service().continue_from_reflection(student_id(), session_id=session_id)


def complete_and_return(*, session_id: str) -> CompletionSnapshot:
    assert_session_owned(session_id)
    return service().complete_session(student_id(), session_id=session_id)
