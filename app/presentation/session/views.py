"""View helpers for Learning Session Experience routes."""

from __future__ import annotations

import logging
from dataclasses import replace

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

logger = logging.getLogger(__name__)


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
    page = page_from_flow(flow)
    return _apply_ri001_session_briefing(page)


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
    snap = service().submit_response(
        student_id(),
        session_id=session_id,
        activity_id=activity_id,
        response=response,
    )
    _vp001_record_evidence(
        session_id=session_id,
        activity_id=activity_id,
        event="practice_attempt",
    )
    return snap


def advance_activity(*, session_id: str) -> ActivitySnapshot | None:
    assert_session_owned(session_id)
    return service().advance_activity(student_id(), session_id=session_id)


def continue_reflection(
    *, session_id: str, note: str | None = None
) -> ReflectionSnapshot:
    assert_session_owned(session_id)
    return service().continue_from_reflection(
        student_id(), session_id=session_id, note=note
    )


def complete_and_return(*, session_id: str) -> CompletionSnapshot:
    """Complete the V2 session and close the Mission commitment lifecycle.

    RR-001.1 / JR-01: V2 ``session.finish`` must call
    ``RecommendationCommitmentService.mark_completed`` so Home reflection
    chrome and the journal completion arc appear on the canonical Alpha path
    (legacy mission finish already did this).
    """
    assert_session_owned(session_id)
    snap = service().complete_session(student_id(), session_id=session_id)
    _vp001_record_evidence(
        session_id=session_id,
        event="study_session",
        metadata={"topics": list(getattr(snap, "topics_completed", ()) or ())},
    )
    _link_commitment_completion(
        int(current_user.id),
        session_id=session_id,
        session_topic=_session_topic_hint(snap),
    )
    return snap


def _session_topic_hint(snap: CompletionSnapshot) -> str:
    """Best-effort topic label from completion projection (fail-open)."""
    topics = getattr(snap, "topics_completed", ()) or ()
    if topics:
        return str(topics[0])
    next_rec = getattr(snap, "next_recommendation", "") or ""
    return str(next_rec).strip()


def _apply_ri001_session_briefing(
    page: SessionPageViewModel,
) -> SessionPageViewModel:
    """Overlay Study Session Experience Model framing when Preferred Authority wins."""
    if page.overview is None:
        return page
    briefing = _ri001_session_briefing(int(current_user.id))
    if not briefing:
        return page
    why = str(
        briefing.get("educational_why")
        or briefing.get("why_studying")
        or briefing.get("summary")
        or ""
    ).strip()
    objective = str(
        briefing.get("expected_outcome")
        or briefing.get("learning_objective")
        or briefing.get("briefing_title")
        or ""
    ).strip()
    title = str(briefing.get("briefing_title") or briefing.get("title") or "").strip()
    overview = page.overview
    if why:
        overview = replace(overview, why_studying=why)
    if objective:
        overview = replace(
            overview,
            objective=objective,
            learning_goal=objective or overview.learning_goal,
        )
    shell = page.shell
    if title:
        shell = replace(shell, topic_title=title)
    return replace(page, overview=overview, shell=shell)


def _ri001_session_briefing(user_id: int) -> dict | None:
    """Return Study Session Experience adapter when Preferred Authority wins."""
    try:
        from app.application.runtime_integration import (
            AuthoritySource,
            build_runtime_integration_service,
            map_session_briefing,
        )
        from app.application.runtime_integration.dto import IntegrationSurface

        result = build_runtime_integration_service().resolve_for_surface(
            user_id,
            IntegrationSurface.STUDY_SESSION,
            runtime_a_fallback=lambda _sid, _surface: None,
        )
        if result.authority is not AuthoritySource.EDUCATIONAL_INTELLIGENCE:
            return None
        if result.experience is None:
            return None
        return map_session_briefing(result.experience.surfaces.session_briefing)
    except Exception:  # noqa: BLE001 — Temporary compatibility
        logger.debug(
            "VP-001 session Preferred Authority unavailable for user=%s",
            user_id,
            exc_info=True,
        )
        return None


def _vp001_record_evidence(
    *,
    session_id: str,
    activity_id: str | None = None,
    event: str = "practice_attempt",
    metadata: dict | None = None,
) -> None:
    """Fail-open LP-001 evidence refresh after session activity."""
    try:
        from app.infrastructure.adapters.learner_lifecycle import (
            record_session_evidence,
        )

        record_session_evidence(
            student_id=int(current_user.id),
            session_id=session_id,
            activity_id=activity_id,
            event=event,
            metadata=metadata,
        )
    except Exception:  # noqa: BLE001 — never break session UX
        logger.debug(
            "VP-001 session evidence hook failed session=%s",
            session_id,
            exc_info=True,
        )


def _link_commitment_completion(
    user_id: int,
    *,
    session_id: str,
    session_topic: str = "",
) -> None:
    """EP-008.3 / RR-001.1: link V2 session completion to commitment (preference)."""
    try:
        from app.application.student_experience.recommendation_commitment import (
            RecommendationCommitmentService,
        )
        from app.services.recommendation_service import RecommendationService

        tip = RecommendationService.get_dashboard_today_recommendation(user_id)
        if not isinstance(tip, dict):
            tip = {"title": session_topic} if session_topic else {}
        RecommendationCommitmentService.mark_completed(
            user_id,
            tip=tip,
            session_id=session_id,
            session_topic=session_topic,
        )
    except Exception:
        logger.debug(
            "EP-008.3 commitment completion link failed for user %s",
            user_id,
            exc_info=True,
        )
