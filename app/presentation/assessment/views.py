"""View helpers for Assessment Delivery routes."""

from __future__ import annotations

import uuid
from typing import Any

from flask_login import current_user

from app.presentation.assessment.factory import get_assessment_delivery_service
from app.presentation.assessment.view_models import (
    AssessmentPageViewModel,
    page_from_delivery,
)
from application.assessment.commands.commands import (
    CancelAssessmentSessionCommand,
    CommitAssessmentResponseCommand,
    CreateAssessmentSessionCommand,
    NavigateAssessmentSessionCommand,
    PauseAssessmentSessionCommand,
    RequestAssessmentHintCommand,
    ResumeAssessmentSessionCommand,
    StartAssessmentSessionCommand,
    SubmitAssessmentSessionCommand,
)
from application.assessment.delivery.delivery_service import AssessmentDeliveryService
from application.assessment.delivery.exceptions import SessionOwnershipError
from application.assessment.dto.models import AssessmentAttemptDTO


def student_id() -> str:
    return str(current_user.id)


def service() -> AssessmentDeliveryService:
    return get_assessment_delivery_service()


def assert_session_owned(session_id: str) -> None:
    delivery = service().get_delivery(session_id, student_id=student_id())
    if delivery.session.student_id != student_id():
        raise SessionOwnershipError(
            f"session {session_id} is not owned by student {student_id()}"
        )


def load_page(session_id: str) -> AssessmentPageViewModel:
    assert_session_owned(session_id)
    delivery = service().get_delivery(session_id, student_id=student_id())
    return page_from_delivery(delivery)


def start_new_session(*, instrument_id: str | None = None) -> AssessmentPageViewModel:
    svc = service()
    iid = instrument_id or svc.default_instrument_id
    if not iid:
        raise RuntimeError("no default assessment instrument configured")
    session_id = f"asess-{uuid.uuid4().hex[:12]}"
    delivery = svc.create_session(
        CreateAssessmentSessionCommand(
            session_id=session_id,
            student_id=student_id(),
            instrument_id=iid,
        )
    )
    return page_from_delivery(delivery)


def begin_session(*, session_id: str) -> AssessmentPageViewModel:
    delivery = service().start(
        StartAssessmentSessionCommand(session_id=session_id),
        student_id=student_id(),
    )
    return page_from_delivery(delivery)


def pause_session(*, session_id: str) -> AssessmentPageViewModel:
    delivery = service().pause(
        PauseAssessmentSessionCommand(session_id=session_id),
        student_id=student_id(),
    )
    return page_from_delivery(delivery)


def resume_session(*, session_id: str) -> AssessmentPageViewModel:
    delivery = service().resume(
        ResumeAssessmentSessionCommand(session_id=session_id),
        student_id=student_id(),
    )
    return page_from_delivery(delivery)


def cancel_session(*, session_id: str) -> AssessmentPageViewModel:
    delivery = service().cancel(
        CancelAssessmentSessionCommand(session_id=session_id),
        student_id=student_id(),
    )
    return page_from_delivery(delivery)


def navigate(*, session_id: str, direction: str) -> AssessmentPageViewModel:
    delivery = service().navigate(
        NavigateAssessmentSessionCommand(
            session_id=session_id, direction=direction
        ),
        student_id=student_id(),
    )
    return page_from_delivery(delivery)


def request_hint(*, session_id: str, question_id: str) -> AssessmentPageViewModel:
    delivery = service().request_hint(
        RequestAssessmentHintCommand(
            session_id=session_id, question_id=question_id
        ),
        student_id=student_id(),
    )
    return page_from_delivery(delivery)


def commit_response(
    *,
    session_id: str,
    question_id: str,
    response_payload: dict[str, Any],
    confidence: int | None = None,
    response_time_ms: int | None = None,
) -> AssessmentAttemptDTO:
    return service().commit_response(
        CommitAssessmentResponseCommand(
            session_id=session_id,
            question_id=question_id,
            response_payload=response_payload,
            confidence=confidence,
            response_time_ms=response_time_ms,
        ),
        student_id=student_id(),
    )


def complete_session(*, session_id: str) -> AssessmentPageViewModel:
    delivery = service().complete(
        SubmitAssessmentSessionCommand(session_id=session_id),
        student_id=student_id(),
    )
    return page_from_delivery(delivery)


def payload_from_form(form) -> dict[str, Any]:
    """Extract strategy-facing raw fields from RespondAssessmentForm."""
    payload: dict[str, Any] = {}
    if form.selected_option.data:
        payload["selected_option"] = form.selected_option.data
    if form.selected_options.data:
        payload["selected_options"] = list(form.selected_options.data)
    if form.linked_concepts.data:
        payload["linked_concepts"] = list(form.linked_concepts.data)
    if form.entered_value.data:
        payload["entered_value"] = form.entered_value.data
    if form.entered_expression.data:
        payload["entered_expression"] = form.entered_expression.data
    if form.entered_text.data:
        payload["entered_text"] = form.entered_text.data
    if form.entered_steps.data:
        payload["entered_steps"] = form.entered_steps.data
    if form.reflection_text.data:
        payload["reflection_text"] = form.reflection_text.data
    if form.confidence.data is not None:
        payload["confidence"] = form.confidence.data
    return payload
