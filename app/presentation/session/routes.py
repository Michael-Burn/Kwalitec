"""HTTP routes for the Learning Session Experience UI.

Thin Flask layer: auth → views → templates.
Educational authority stays in Session Experience application services.
"""

from __future__ import annotations

import logging

from flask import abort, flash, redirect, render_template, url_for
from flask_login import login_required

from app.application.session_experience.exceptions import (
    PortUnavailable,
    SessionExperienceError,
    SessionNotFound,
    SessionOwnershipError,
    WorkspaceNotFound,
)
from app.domain.session_experience.session_workspace import SessionSurface
from app.presentation.session import session_bp
from app.presentation.session.forms import (
    AdvanceActivityForm,
    BeginSessionForm,
    CompleteSessionForm,
    ContinueReflectionForm,
    SubmitAnswerForm,
)
from app.presentation.session.messages import FLASH_SUCCESS, FLASH_WARNING
from app.presentation.session.views import (
    advance_activity,
    begin_session,
    complete_and_return,
    continue_reflection,
    load_page,
    resume_redirect_if_needed,
    submit_answer,
)

logger = logging.getLogger(__name__)


def _guard_ownership(exc: SessionOwnershipError):
    logger.warning("Session ownership denied: %s", exc)
    abort(403)


def _missing_session_redirect(session_id: str, exc: SessionExperienceError):
    logger.warning("Session unavailable (%s): %s", session_id, exc)
    flash(FLASH_WARNING["missing"], "warning")
    return redirect(url_for("student.home"))


@session_bp.get("/<session_id>/")
@session_bp.get("/<session_id>/overview")
@login_required
def overview(session_id: str):
    """Session Overview — today's objective and Begin Session."""
    try:
        resume = resume_redirect_if_needed(session_id, SessionSurface.OVERVIEW)
        if resume is not None:
            flash(FLASH_SUCCESS["resumed"], "success")
            return resume
        page = load_page(session_id, SessionSurface.OVERVIEW)
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except (SessionNotFound, WorkspaceNotFound) as exc:
        return _missing_session_redirect(session_id, exc)
    form = BeginSessionForm()
    form.session_id.data = session_id
    if page.overview and page.overview.mission_id:
        form.mission_id.data = page.overview.mission_id
    return render_template(
        "session/overview.html",
        title=page.shell.page_title,
        page=page,
        form=form,
    )


@session_bp.post("/<session_id>/begin")
@login_required
def begin(session_id: str):
    """Primary Overview CTA — begin the Session."""
    form = BeginSessionForm()
    if not form.validate_on_submit():
        flash(FLASH_WARNING["begin_invalid"], "warning")
        return redirect(url_for("session.overview", session_id=session_id))
    try:
        begin_session(session_id=session_id)
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except PortUnavailable:
        flash(FLASH_WARNING["begin_unavailable"], "warning")
        return redirect(url_for("session.overview", session_id=session_id))
    except SessionExperienceError as exc:
        logger.warning("Begin session failed: %s", exc)
        flash(FLASH_WARNING["begin_failed"], "warning")
        return redirect(url_for("session.overview", session_id=session_id))
    flash(FLASH_SUCCESS["begun"], "success")
    return redirect(url_for("session.activity", session_id=session_id))


@session_bp.get("/<session_id>/activity")
@login_required
def activity(session_id: str):
    """Learning Activity — question, answer, progress."""
    try:
        resume = resume_redirect_if_needed(session_id, SessionSurface.ACTIVITY)
        if resume is not None:
            return resume
        page = load_page(session_id, SessionSurface.ACTIVITY)
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except (SessionNotFound, WorkspaceNotFound) as exc:
        return _missing_session_redirect(session_id, exc)
    answer_form = SubmitAnswerForm()
    answer_form.session_id.data = session_id
    if page.activity:
        answer_form.activity_id.data = page.activity.activity_id
    advance_form = AdvanceActivityForm()
    advance_form.session_id.data = session_id
    return render_template(
        "session/activity.html",
        title=page.shell.page_title,
        page=page,
        answer_form=answer_form,
        advance_form=advance_form,
    )


@session_bp.post("/<session_id>/activity/answer")
@login_required
def answer(session_id: str):
    """Submit an activity response through the educational kernel ports."""
    form = SubmitAnswerForm()
    if not form.validate_on_submit():
        flash(FLASH_WARNING["answer_required"], "warning")
        return redirect(url_for("session.activity", session_id=session_id))
    try:
        submit_answer(
            session_id=session_id,
            activity_id=(form.activity_id.data or "").strip(),
            response=(form.response.data or "").strip(),
        )
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except PortUnavailable:
        flash(FLASH_WARNING["activity_unavailable"], "warning")
        return redirect(url_for("session.activity", session_id=session_id))
    except SessionExperienceError as exc:
        logger.warning("Submit answer failed: %s", exc)
        flash(FLASH_WARNING["answer_failed"], "warning")
        return redirect(url_for("session.activity", session_id=session_id))
    return redirect(url_for("session.activity", session_id=session_id))


@session_bp.post("/<session_id>/activity/advance")
@login_required
def advance(session_id: str):
    """Advance to the next activity or reflection."""
    form = AdvanceActivityForm()
    if not form.validate_on_submit():
        flash(FLASH_WARNING["continue_invalid"], "warning")
        return redirect(url_for("session.activity", session_id=session_id))
    try:
        nxt = advance_activity(session_id=session_id)
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except PortUnavailable:
        flash(FLASH_WARNING["activity_unavailable"], "warning")
        return redirect(url_for("session.activity", session_id=session_id))
    except SessionExperienceError as exc:
        logger.warning("Advance activity failed: %s", exc)
        flash(FLASH_WARNING["continue_failed"], "warning")
        return redirect(url_for("session.activity", session_id=session_id))
    if nxt is None:
        return redirect(url_for("session.reflection", session_id=session_id))
    return redirect(url_for("session.activity", session_id=session_id))


@session_bp.get("/<session_id>/reflection")
@login_required
def reflection(session_id: str):
    """Reflection checkpoint — educational guidance only."""
    try:
        resume = resume_redirect_if_needed(session_id, SessionSurface.REFLECTION)
        if resume is not None:
            return resume
        page = load_page(session_id, SessionSurface.REFLECTION)
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except (SessionNotFound, WorkspaceNotFound) as exc:
        return _missing_session_redirect(session_id, exc)
    form = ContinueReflectionForm()
    form.session_id.data = session_id
    return render_template(
        "session/reflection.html",
        title=page.shell.page_title,
        page=page,
        form=form,
    )


@session_bp.post("/<session_id>/reflection/continue")
@login_required
def reflection_continue(session_id: str):
    """Continue from reflection to session summary."""
    form = ContinueReflectionForm()
    if not form.validate_on_submit():
        flash(FLASH_WARNING["continue_invalid"], "warning")
        return redirect(url_for("session.reflection", session_id=session_id))
    try:
        continue_reflection(session_id=session_id)
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except PortUnavailable:
        flash(FLASH_WARNING["reflection_unavailable"], "warning")
        return redirect(url_for("session.reflection", session_id=session_id))
    except SessionExperienceError as exc:
        logger.warning("Reflection continue failed: %s", exc)
        flash(FLASH_WARNING["reflection_failed"], "warning")
        return redirect(url_for("session.reflection", session_id=session_id))

    from flask_login import current_user

    from app.services.presentation_telemetry_service import (
        EVENT_REFLECTION_COMPLETED,
        PresentationTelemetryService,
    )

    PresentationTelemetryService.record(
        EVENT_REFLECTION_COMPLETED,
        user_id=current_user.id,
        resource_type="session",
        resource_id=session_id,
        path=f"/session/{session_id}/reflection/continue",
    )
    return redirect(url_for("session.summary", session_id=session_id))


@session_bp.get("/<session_id>/summary")
@login_required
def summary(session_id: str):
    """Session Summary — outcomes and next recommendation."""
    try:
        resume = resume_redirect_if_needed(session_id, SessionSurface.SUMMARY)
        if resume is not None:
            return resume
        page = load_page(session_id, SessionSurface.SUMMARY)
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except (SessionNotFound, WorkspaceNotFound) as exc:
        return _missing_session_redirect(session_id, exc)
    form = CompleteSessionForm()
    form.session_id.data = session_id
    return render_template(
        "session/summary.html",
        title=page.shell.page_title,
        page=page,
        form=form,
    )


@session_bp.get("/<session_id>/complete")
@login_required
def complete(session_id: str):
    """Complete surface — return home CTA."""
    try:
        resume = resume_redirect_if_needed(session_id, SessionSurface.COMPLETE)
        if resume is not None:
            return resume
        page = load_page(session_id, SessionSurface.COMPLETE)
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except (SessionNotFound, WorkspaceNotFound) as exc:
        return _missing_session_redirect(session_id, exc)
    form = CompleteSessionForm()
    form.session_id.data = session_id
    return render_template(
        "session/complete.html",
        title=page.shell.page_title,
        page=page,
        form=form,
    )


@session_bp.post("/<session_id>/complete")
@login_required
def finish(session_id: str):
    """Complete the session and return to Student Home."""
    form = CompleteSessionForm()
    if not form.validate_on_submit():
        flash(FLASH_WARNING["complete_invalid"], "warning")
        return redirect(url_for("session.complete", session_id=session_id))
    try:
        complete_and_return(session_id=session_id)
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except PortUnavailable:
        flash(FLASH_WARNING["complete_unavailable"], "warning")
        return redirect(url_for("session.complete", session_id=session_id))
    except (SessionNotFound, WorkspaceNotFound) as exc:
        return _missing_session_redirect(session_id, exc)
    except SessionExperienceError as exc:
        logger.warning("Complete session failed: %s", exc)
        flash(FLASH_WARNING["complete_failed"], "warning")
        return redirect(url_for("session.complete", session_id=session_id))
    flash(FLASH_SUCCESS["completed"], "success")
    return redirect(url_for("student.home"))
