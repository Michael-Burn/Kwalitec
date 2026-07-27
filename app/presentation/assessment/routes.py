"""HTTP routes for Assessment Delivery.

Thin Flask layer: auth → views → templates.
No Twin updates, Reasoning, Mission adaptation, or Tutor interpretation.
"""

from __future__ import annotations

import logging

from flask import abort, flash, redirect, render_template, url_for
from flask_login import login_required

from app.presentation.assessment import assessment_bp
from app.presentation.assessment.forms import (
    BeginAssessmentForm,
    CancelAssessmentForm,
    CompleteAssessmentForm,
    HintAssessmentForm,
    NavigateAssessmentForm,
    PauseAssessmentForm,
    RespondAssessmentForm,
    ResumeAssessmentForm,
    StartAssessmentForm,
)
from app.presentation.assessment.messages import FLASH_SUCCESS, FLASH_WARNING
from app.presentation.assessment.views import (
    begin_session,
    cancel_session,
    commit_response,
    complete_session,
    load_page,
    navigate,
    pause_session,
    payload_from_form,
    request_hint,
    resume_session,
    start_new_session,
)
from application.assessment.delivery.exceptions import (
    AssessmentDeliveryError,
    DuplicateSubmissionError,
    ExpiredSessionError,
    InvalidResponseFormatError,
    QuestionUnavailableError,
    SessionNotFoundError,
    SessionOwnershipError,
    SessionStateError,
)

logger = logging.getLogger(__name__)


def _guard_ownership(exc: SessionOwnershipError):
    logger.warning("Assessment ownership denied: %s", exc)
    abort(403)


def _missing_redirect(exc: AssessmentDeliveryError):
    logger.warning("Assessment unavailable: %s", exc)
    flash(FLASH_WARNING["missing"], "warning")
    return redirect(url_for("assessment.entry"))


@assessment_bp.get("/")
@login_required
def entry():
    """Entry — explain purpose and start a learning check."""
    form = StartAssessmentForm()
    return render_template(
        "student/assessment/entry.html",
        title="Learning Check",
        form=form,
    )


@assessment_bp.post("/start")
@login_required
def start():
    form = StartAssessmentForm()
    if not form.validate_on_submit():
        flash(FLASH_WARNING["invalid"], "warning")
        return redirect(url_for("assessment.entry"))
    try:
        page = start_new_session(instrument_id=form.instrument_id.data or None)
    except AssessmentDeliveryError as exc:
        logger.warning("Start assessment failed: %s", exc)
        flash(FLASH_WARNING["state"], "warning")
        return redirect(url_for("assessment.entry"))
    flash(FLASH_SUCCESS["started"], "success")
    return redirect(
        url_for("assessment.overview", session_id=page.shell.session_id)
    )


@assessment_bp.get("/<session_id>/")
@assessment_bp.get("/<session_id>/overview")
@login_required
def overview(session_id: str):
    try:
        page = load_page(session_id)
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except SessionNotFoundError as exc:
        return _missing_redirect(exc)

    if page.shell.status == "in_progress":
        return redirect(url_for("assessment.item", session_id=session_id))
    if page.shell.status == "paused":
        resume_form = ResumeAssessmentForm()
        resume_form.session_id.data = session_id
        cancel_form = CancelAssessmentForm()
        cancel_form.session_id.data = session_id
        return render_template(
            "student/assessment/overview.html",
            title=page.shell.page_title,
            page=page,
            resume_form=resume_form,
            cancel_form=cancel_form,
            begin_form=None,
        )
    if page.progress.is_complete or page.shell.status in {
        "submitted",
        "abandoned",
        "closed",
    }:
        return redirect(url_for("assessment.complete_page", session_id=session_id))

    begin_form = BeginAssessmentForm()
    begin_form.session_id.data = session_id
    cancel_form = CancelAssessmentForm()
    cancel_form.session_id.data = session_id
    return render_template(
        "student/assessment/overview.html",
        title=page.shell.page_title,
        page=page,
        begin_form=begin_form,
        cancel_form=cancel_form,
        resume_form=None,
    )


@assessment_bp.post("/<session_id>/begin")
@login_required
def begin(session_id: str):
    form = BeginAssessmentForm()
    if not form.validate_on_submit():
        flash(FLASH_WARNING["invalid"], "warning")
        return redirect(url_for("assessment.overview", session_id=session_id))
    try:
        begin_session(session_id=session_id)
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except ExpiredSessionError:
        flash(FLASH_WARNING["expired"], "warning")
        return redirect(url_for("assessment.entry"))
    except (SessionStateError, SessionNotFoundError) as exc:
        logger.warning("Begin failed: %s", exc)
        flash(FLASH_WARNING["state"], "warning")
        return redirect(url_for("assessment.overview", session_id=session_id))
    flash(FLASH_SUCCESS["begun"], "success")
    return redirect(url_for("assessment.item", session_id=session_id))


@assessment_bp.get("/<session_id>/item")
@login_required
def item(session_id: str):
    try:
        page = load_page(session_id)
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except SessionNotFoundError as exc:
        return _missing_redirect(exc)

    if page.shell.status == "ready":
        return redirect(url_for("assessment.overview", session_id=session_id))
    if page.shell.status == "paused":
        return redirect(url_for("assessment.overview", session_id=session_id))
    if page.progress.is_complete or page.shell.status == "submitted":
        return redirect(url_for("assessment.complete_page", session_id=session_id))

    respond_form = RespondAssessmentForm()
    respond_form.session_id.data = session_id
    if page.question:
        respond_form.question_id.data = page.question.question_id
        if page.question.options:
            choices = [(o["option_id"], o["label"]) for o in page.question.options]
            respond_form.selected_options.choices = choices
            respond_form.linked_concepts.choices = choices

    nav_next = NavigateAssessmentForm()
    nav_next.session_id.data = session_id
    nav_next.direction.data = "next"
    nav_prev = NavigateAssessmentForm()
    nav_prev.session_id.data = session_id
    nav_prev.direction.data = "previous"
    pause_form = PauseAssessmentForm()
    pause_form.session_id.data = session_id
    complete_form = CompleteAssessmentForm()
    complete_form.session_id.data = session_id
    hint_form = HintAssessmentForm()
    hint_form.session_id.data = session_id
    if page.question:
        hint_form.question_id.data = page.question.question_id

    return render_template(
        "student/assessment/item.html",
        title=page.shell.page_title,
        page=page,
        respond_form=respond_form,
        nav_next=nav_next,
        nav_prev=nav_prev,
        pause_form=pause_form,
        complete_form=complete_form,
        hint_form=hint_form,
    )


@assessment_bp.post("/<session_id>/respond")
@login_required
def respond(session_id: str):
    form = RespondAssessmentForm()
    # Dynamic choices for multi-select validation
    try:
        page = load_page(session_id)
        if page.question and page.question.options:
            choices = [(o["option_id"], o["label"]) for o in page.question.options]
            form.selected_options.choices = choices
            form.linked_concepts.choices = choices
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except SessionNotFoundError as exc:
        return _missing_redirect(exc)

    if not form.validate_on_submit():
        flash(FLASH_WARNING["invalid"], "warning")
        return redirect(url_for("assessment.item", session_id=session_id))

    response_time_ms = None
    if form.response_time_ms.data:
        try:
            response_time_ms = int(form.response_time_ms.data)
        except ValueError:
            response_time_ms = None

    try:
        commit_response(
            session_id=session_id,
            question_id=form.question_id.data,
            response_payload=payload_from_form(form),
            confidence=form.confidence.data,
            response_time_ms=response_time_ms,
        )
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except InvalidResponseFormatError:
        flash(FLASH_WARNING["invalid"], "warning")
        return redirect(url_for("assessment.item", session_id=session_id))
    except DuplicateSubmissionError:
        flash(FLASH_WARNING["duplicate"], "warning")
        return redirect(url_for("assessment.item", session_id=session_id))
    except ExpiredSessionError:
        flash(FLASH_WARNING["expired"], "warning")
        return redirect(url_for("assessment.entry"))
    except (
        SessionStateError,
        QuestionUnavailableError,
        SessionNotFoundError,
    ) as exc:
        logger.warning("Respond failed: %s", exc)
        flash(FLASH_WARNING["state"], "warning")
        return redirect(url_for("assessment.item", session_id=session_id))

    flash(FLASH_SUCCESS["saved"], "success")
    return redirect(url_for("assessment.item", session_id=session_id))


@assessment_bp.post("/<session_id>/navigate")
@login_required
def navigate_route(session_id: str):
    form = NavigateAssessmentForm()
    if not form.validate_on_submit():
        flash(FLASH_WARNING["invalid"], "warning")
        return redirect(url_for("assessment.item", session_id=session_id))
    try:
        navigate(session_id=session_id, direction=form.direction.data)
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except (SessionStateError, SessionNotFoundError) as exc:
        logger.warning("Navigate failed: %s", exc)
        flash(FLASH_WARNING["state"], "warning")
    return redirect(url_for("assessment.item", session_id=session_id))


@assessment_bp.post("/<session_id>/hint")
@login_required
def hint(session_id: str):
    form = HintAssessmentForm()
    if not form.validate_on_submit():
        flash(FLASH_WARNING["invalid"], "warning")
        return redirect(url_for("assessment.item", session_id=session_id))
    try:
        request_hint(session_id=session_id, question_id=form.question_id.data)
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except (SessionStateError, SessionNotFoundError) as exc:
        logger.warning("Hint failed: %s", exc)
        flash(FLASH_WARNING["state"], "warning")
        return redirect(url_for("assessment.item", session_id=session_id))
    flash(FLASH_SUCCESS["hint"], "success")
    return redirect(url_for("assessment.item", session_id=session_id))


@assessment_bp.post("/<session_id>/pause")
@login_required
def pause(session_id: str):
    form = PauseAssessmentForm()
    if not form.validate_on_submit():
        flash(FLASH_WARNING["invalid"], "warning")
        return redirect(url_for("assessment.item", session_id=session_id))
    try:
        pause_session(session_id=session_id)
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except (SessionStateError, SessionNotFoundError) as exc:
        logger.warning("Pause failed: %s", exc)
        flash(FLASH_WARNING["state"], "warning")
        return redirect(url_for("assessment.item", session_id=session_id))
    flash(FLASH_SUCCESS["paused"], "success")
    return redirect(url_for("assessment.overview", session_id=session_id))


@assessment_bp.post("/<session_id>/resume")
@login_required
def resume(session_id: str):
    form = ResumeAssessmentForm()
    if not form.validate_on_submit():
        flash(FLASH_WARNING["invalid"], "warning")
        return redirect(url_for("assessment.overview", session_id=session_id))
    try:
        resume_session(session_id=session_id)
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except ExpiredSessionError:
        flash(FLASH_WARNING["expired"], "warning")
        return redirect(url_for("assessment.entry"))
    except (SessionStateError, SessionNotFoundError) as exc:
        logger.warning("Resume failed: %s", exc)
        flash(FLASH_WARNING["state"], "warning")
        return redirect(url_for("assessment.overview", session_id=session_id))
    flash(FLASH_SUCCESS["resumed"], "success")
    return redirect(url_for("assessment.item", session_id=session_id))


@assessment_bp.post("/<session_id>/complete")
@login_required
def complete(session_id: str):
    form = CompleteAssessmentForm()
    if not form.validate_on_submit():
        flash(FLASH_WARNING["invalid"], "warning")
        return redirect(url_for("assessment.item", session_id=session_id))
    try:
        complete_session(session_id=session_id)
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except ExpiredSessionError:
        flash(FLASH_WARNING["expired"], "warning")
        return redirect(url_for("assessment.entry"))
    except (SessionStateError, SessionNotFoundError) as exc:
        logger.warning("Complete failed: %s", exc)
        flash(FLASH_WARNING["state"], "warning")
        return redirect(url_for("assessment.item", session_id=session_id))
    flash(FLASH_SUCCESS["completed"], "success")
    return redirect(url_for("assessment.complete_page", session_id=session_id))


@assessment_bp.get("/<session_id>/complete")
@login_required
def complete_page(session_id: str):
    try:
        page = load_page(session_id)
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except SessionNotFoundError as exc:
        return _missing_redirect(exc)
    return render_template(
        "student/assessment/complete.html",
        title="Check complete",
        page=page,
    )


@assessment_bp.post("/<session_id>/cancel")
@login_required
def cancel(session_id: str):
    form = CancelAssessmentForm()
    if not form.validate_on_submit():
        flash(FLASH_WARNING["invalid"], "warning")
        return redirect(url_for("assessment.overview", session_id=session_id))
    try:
        cancel_session(session_id=session_id)
    except SessionOwnershipError as exc:
        return _guard_ownership(exc)
    except (SessionStateError, SessionNotFoundError) as exc:
        logger.warning("Cancel failed: %s", exc)
        flash(FLASH_WARNING["state"], "warning")
        return redirect(url_for("assessment.overview", session_id=session_id))
    flash(FLASH_SUCCESS["cancelled"], "success")
    return redirect(url_for("assessment.entry"))
