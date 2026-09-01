"""HTTP routes for the Learning Session Experience UI.

Thin Flask layer: auth → views → templates.
Educational authority stays in Session Experience application services.
"""

from __future__ import annotations

import logging

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.application.session_experience.exceptions import (
    PortUnavailable,
    ReflectionError,
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
    ChecklistItemForm,
    CompleteSessionForm,
    ContinueReflectionForm,
    FinishReviewForm,
    PauseSessionForm,
    ResumeSessionForm,
    SubmitAnswerForm,
)
from app.presentation.session.messages import FLASH_SUCCESS, FLASH_WARNING
from app.presentation.session.services.study_session_service import (
    StudySessionService,
)
from app.presentation.session.views import (
    advance_activity,
    begin_session,
    complete_and_return,
    continue_reflection,
    load_page,
    pause_session,
    request_finish,
    resume_redirect_if_needed,
    resume_session,
    submit_answer,
    update_checklist,
)

_study_session = StudySessionService()

logger = logging.getLogger(__name__)


def _guard_ownership(exc: SessionOwnershipError):
    logger.warning("Session ownership denied: %s", exc)
    abort(403)


def _missing_session_redirect(session_id: str, exc: SessionExperienceError):
    logger.warning("Session unavailable (%s): %s", session_id, exc)
    flash(FLASH_WARNING["missing"], "warning")
    return redirect(url_for("student.home"))


def _contention_redirect(session_id: str, exc: BaseException):
    """PX-B-008 — infra contention is never scored as educational failure."""
    logger.warning(
        "Session contention on %s (%s): %s",
        session_id,
        type(exc).__name__,
        exc,
    )
    flash(FLASH_WARNING["continue_contention"], "warning")
    return redirect(url_for("student.home"))


def _is_contention_error(exc: BaseException) -> bool:
    """True for optimistic-lock / transient DB contention classes."""
    name = type(exc).__name__
    if name in {"OptimisticLockError", "StaleDataError", "OperationalError"}:
        return True
    module = type(exc).__module__ or ""
    if "sqlalchemy" in module and name in {
        "OperationalError",
        "DBAPIError",
        "TimeoutError",
    }:
        return True
    try:
        from app.infrastructure.persistence.optimistic_locking import (
            OptimisticLockError,
        )

        if isinstance(exc, OptimisticLockError):
            return True
    except Exception:
        pass
    return False


@session_bp.errorhandler(Exception)
def _session_contention_boundary(exc: Exception):
    """Catch-all for session blueprint: map contention to calm recovery."""
    from flask import request

    if not _is_contention_error(exc):
        # Re-raise so the app 500 handler remains authoritative for real bugs.
        raise exc
    session_id = (request.view_args or {}).get("session_id", "")
    return _contention_redirect(str(session_id or ""), exc)


@session_bp.get("/<session_id>/")
@session_bp.get("/<session_id>/overview")
@login_required
def overview(session_id: str):
    """Session Overview — today's objective and Start Session."""
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
    quick_check_embed = None
    try:
        from app.presentation.adaptive_assessment.mission_embed import (
            build_mission_quick_check_embed,
        )

        mission_ref = str(
            (page.overview.mission_id if page.overview else None)
            or session_id
        )
        quick_check_embed = build_mission_quick_check_embed(
            mission_ref=mission_ref,
            return_endpoint="session.overview",
            return_session_id=session_id,
        )
    except Exception:
        logger.debug(
            "Quick Check embed unavailable for session %s",
            session_id,
            exc_info=True,
        )
    study = _study_session.build_page(page)
    return render_template(
        "session/overview.html",
        title=study.page_title,
        page=page,
        study=study,
        form=form,
        quick_check_embed=quick_check_embed,
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
    return redirect(url_for("session.activity", session_id=session_id))


@session_bp.post("/<session_id>/pause")
@login_required
def pause(session_id: str):
    """Pause Study Session — safe leave; progress retained for resume."""
    form = PauseSessionForm()
    if not form.validate_on_submit():
        flash(FLASH_WARNING["pause_failed"], "warning")
        return redirect(url_for("session.activity", session_id=session_id))
    try:
        pause_session(session_id=session_id)
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except PortUnavailable:
        flash(FLASH_WARNING["pause_failed"], "warning")
        return redirect(url_for("session.activity", session_id=session_id))
    except SessionExperienceError as exc:
        logger.warning("Pause session failed: %s", exc)
        flash(FLASH_WARNING["pause_failed"], "warning")
        return redirect(url_for("session.activity", session_id=session_id))
    flash(FLASH_SUCCESS["paused"], "success")
    return redirect(url_for("student.home"))


@session_bp.post("/<session_id>/resume")
@login_required
def resume(session_id: str):
    """Resume a paused Study Session at the persisted surface."""
    form = ResumeSessionForm()
    if not form.validate_on_submit():
        flash(FLASH_WARNING["resume_failed"], "warning")
        return redirect(url_for("session.overview", session_id=session_id))
    try:
        resume_session(session_id=session_id)
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except PortUnavailable:
        flash(FLASH_WARNING["resume_failed"], "warning")
        return redirect(url_for("session.overview", session_id=session_id))
    except SessionExperienceError as exc:
        logger.warning("Resume session failed: %s", exc)
        flash(FLASH_WARNING["resume_failed"], "warning")
        return redirect(url_for("session.overview", session_id=session_id))
    flash(FLASH_SUCCESS["resumed"], "success")
    return redirect(url_for("session.activity", session_id=session_id))


@session_bp.post("/<session_id>/checklist")
@login_required
def checklist(session_id: str):
    """Toggle a plan-checklist item (session progress only)."""
    form = ChecklistItemForm()
    if not form.validate_on_submit():
        return redirect(url_for("session.overview", session_id=session_id))
    try:
        update_checklist(
            session_id=session_id,
            item_id=(form.item_id.data or "").strip(),
            done=str(form.done.data or "").strip() in {"1", "true", "yes", "on"},
        )
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except SessionExperienceError as exc:
        logger.warning("Checklist update failed: %s", exc)
        return redirect(url_for("session.overview", session_id=session_id))
    flash(FLASH_SUCCESS["checklist_updated"], "success")
    return redirect(url_for("session.overview", session_id=session_id))


@session_bp.post("/<session_id>/finish/start")
@login_required
def finish_start(session_id: str):
    """Enter Ready to Finish — Finish Review required before close."""
    try:
        request_finish(session_id=session_id)
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except PortUnavailable:
        flash(FLASH_WARNING["complete_unavailable"], "warning")
        return redirect(url_for("session.activity", session_id=session_id))
    except SessionExperienceError as exc:
        logger.warning("Request finish failed: %s", exc)
        flash(FLASH_WARNING["complete_failed"], "warning")
        return redirect(url_for("session.activity", session_id=session_id))
    return redirect(url_for("session.summary", session_id=session_id))


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
    if page.activity and page.activity.next_action_label:
        advance_form.submit.label.text = page.activity.next_action_label
    # CQ-004: keep Quick Check on Overview only — Activity stays focused practice.
    study = _study_session.build_page(page)
    return render_template(
        "session/activity.html",
        title=study.page_title,
        page=page,
        study=study,
        answer_form=answer_form,
        advance_form=advance_form,
        quick_check_embed=None,
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
            response=form.resolved_response(),
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
    flash(FLASH_SUCCESS["answer_recorded"], "success")
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
    except ReflectionError as exc:
        logger.warning("Reflection load failed: %s", exc)
        flash(FLASH_WARNING["reflection_unavailable"], "warning")
        return redirect(url_for("session.activity", session_id=session_id))
    except SessionExperienceError as exc:
        logger.warning("Reflection page failed: %s", exc)
        flash(FLASH_WARNING["reflection_unavailable"], "warning")
        return redirect(url_for("session.activity", session_id=session_id))
    form = ContinueReflectionForm()
    form.session_id.data = session_id
    study = _study_session.build_page(page)
    return render_template(
        "session/reflection.html",
        title=study.page_title,
        page=page,
        study=study,
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
        continue_reflection(
            session_id=session_id,
            note=form.reflection_note.data,
            confidence_rating=form.resolved_confidence_rating(),
        )
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
    """Session Summary / Finish Review — Yes / Partially / No when P2 ON."""
    try:
        resume = resume_redirect_if_needed(session_id, SessionSurface.SUMMARY)
        if resume is not None:
            return resume
        page = load_page(session_id, SessionSurface.SUMMARY)
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except (SessionNotFound, WorkspaceNotFound) as exc:
        return _missing_session_redirect(session_id, exc)
    from app.application.config.v2_flags import resolve_v2_feature_flags

    product = bool(resolve_v2_feature_flags().SR_SESSION_COMPLETION_PRODUCT)
    if product:
        form = FinishReviewForm()
    else:
        form = CompleteSessionForm()
    form.session_id.data = session_id
    study = _study_session.build_page(page)
    return render_template(
        "session/summary.html",
        title=study.page_title,
        page=page,
        study=study,
        form=form,
        finish_review_required=product,
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
    study = _study_session.build_page(page)
    subject_code = ""
    if page.overview and page.overview.subject_code:
        subject_code = page.overview.subject_code
    study = _study_session.enrich_completion(
        study,
        user_id=int(current_user.id),
        topic_id="",
        subject_code=subject_code,
    )
    return render_template(
        "session/complete.html",
        title=study.page_title,
        page=page,
        study=study,
        form=form,
        finish_review_required=False,
    )


@session_bp.post("/<session_id>/complete")
@login_required
def finish(session_id: str):
    """Complete the session after Finish Review (P2) or return-home (rollback)."""
    from app.application.config.v2_flags import resolve_v2_feature_flags

    product = bool(resolve_v2_feature_flags().SR_SESSION_COMPLETION_PRODUCT)
    if product:
        form = FinishReviewForm()
        if not form.validate_on_submit():
            flash(FLASH_WARNING["finish_review_required"], "warning")
            return redirect(url_for("session.summary", session_id=session_id))
        verdict = (form.completion_status.data or "").strip().lower()
        notes = form.notes.data
        redirect_surface = "session.summary"
    else:
        form = CompleteSessionForm()
        if not form.validate_on_submit():
            flash(FLASH_WARNING["complete_invalid"], "warning")
            return redirect(url_for("session.complete", session_id=session_id))
        verdict = None
        notes = None
        redirect_surface = "session.complete"
    try:
        complete_and_return(
            session_id=session_id,
            finish_verdict=verdict,
            finish_notes=notes,
        )
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except PortUnavailable:
        flash(FLASH_WARNING["complete_unavailable"], "warning")
        return redirect(url_for(redirect_surface, session_id=session_id))
    except (SessionNotFound, WorkspaceNotFound) as exc:
        return _missing_session_redirect(session_id, exc)
    except SessionExperienceError as exc:
        logger.warning("Complete session failed: %s", exc)
        message = str(exc).lower()
        if "finish review" in message:
            flash(FLASH_WARNING["finish_review_required"], "warning")
            return redirect(url_for("session.summary", session_id=session_id))
        if "evidence" in message or "practice" in message or "reading" in message:
            # Prefer the honest Authority explanation when present.
            detail = str(exc).strip()
            flash(
                detail if detail else FLASH_WARNING["evidence_rejected"],
                "warning",
            )
            return redirect(url_for("session.summary", session_id=session_id))
        flash(FLASH_WARNING["complete_failed"], "warning")
        return redirect(url_for(redirect_surface, session_id=session_id))
    return redirect(url_for("session.complete", session_id=session_id))


@session_bp.post("/<session_id>/finish")
@login_required
def finish_review(session_id: str):
    """Alias POST for Finish Review form on the Summary surface."""
    return finish(session_id)
