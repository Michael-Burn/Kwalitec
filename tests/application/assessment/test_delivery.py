"""Unit tests for assessment delivery strategies, sequencing, and lifecycle."""

from __future__ import annotations

import pytest

from application.assessment.commands.commands import (
    CommitAssessmentResponseCommand,
    CreateAssessmentSessionCommand,
    NavigateAssessmentSessionCommand,
    PauseAssessmentSessionCommand,
    ResumeAssessmentSessionCommand,
    StartAssessmentSessionCommand,
    SubmitAssessmentSessionCommand,
)
from application.assessment.delivery.exceptions import (
    DuplicateSubmissionError,
    ExpiredSessionError,
    InvalidResponseFormatError,
    SessionOwnershipError,
    SessionStateError,
)
from application.assessment.delivery.question_content import (
    ChoiceOption,
    QuestionContent,
)
from application.assessment.delivery.sequencing import compute_progress
from application.assessment.delivery.strategies import all_strategies, get_strategy
from domain.assessment.enums import ItemType
from infrastructure.assessment.composition import build_assessment_delivery


def test_all_item_types_have_strategies() -> None:
    strategies = {s.item_type for s in all_strategies()}
    assert strategies == set(ItemType)


@pytest.mark.parametrize(
    ("item_type", "raw", "ok"),
    [
        (ItemType.MULTIPLE_CHOICE, {"selected_option": "a"}, True),
        (ItemType.MULTIPLE_CHOICE, {"selected_option": "z"}, False),
        (ItemType.NUMERIC, {"entered_value": "0.02"}, True),
        (ItemType.NUMERIC, {"entered_value": "abc"}, False),
        (ItemType.CONFIDENCE_RATING, {"confidence": 3}, True),
        (ItemType.CONFIDENCE_RATING, {"confidence": 9}, False),
        (ItemType.REFLECTION, {"reflection_text": "Still shaky"}, True),
        (ItemType.REFLECTION, {"reflection_text": ""}, False),
    ],
)
def test_strategy_validation(item_type: ItemType, raw: dict, ok: bool) -> None:
    content = QuestionContent(
        question_id="q-x",
        item_type=item_type,
        stem="Stem",
        options=(
            ChoiceOption("a", "A"),
            ChoiceOption("b", "B"),
        ),
    )
    strategy = get_strategy(item_type)
    if ok:
        payload = strategy.map_response(raw, content)
        assert payload["item_type"] == item_type.value
    else:
        with pytest.raises(InvalidResponseFormatError):
            strategy.map_response(raw, content)


def test_compute_progress_navigation_flags() -> None:
    progress = compute_progress(
        question_ids=("q1", "q2", "q3"),
        answered_question_ids={"q1"},
        current_index=1,
        allow_previous=True,
        session_submitted=False,
    )
    assert progress.answered_count == 1
    assert progress.remaining_count == 2
    assert progress.can_go_previous is True
    assert progress.can_go_next is True
    assert progress.can_complete is False


def test_delivery_lifecycle_resume_and_complete() -> None:
    composition = build_assessment_delivery(seed=True)
    svc = composition.delivery_service
    student = "student-42"
    created = svc.create_session(
        CreateAssessmentSessionCommand(
            session_id="asess-life-1",
            student_id=student,
            instrument_id=composition.default_instrument_id,
        )
    )
    assert created.status == "ready"
    started = svc.start(
        StartAssessmentSessionCommand(session_id="asess-life-1"),
        student_id=student,
    )
    assert started.status == "in_progress"
    assert started.question is not None

    # Answer first MC
    svc.commit_response(
        CommitAssessmentResponseCommand(
            session_id="asess-life-1",
            question_id="q-mc-force",
            response_payload={"selected_option": "a"},
        ),
        student_id=student,
    )
    paused = svc.pause(
        PauseAssessmentSessionCommand(session_id="asess-life-1"),
        student_id=student,
    )
    assert paused.status == "paused"
    resumed = svc.resume(
        ResumeAssessmentSessionCommand(session_id="asess-life-1"),
        student_id=student,
    )
    assert resumed.status == "in_progress"

    # Remaining questions
    svc.commit_response(
        CommitAssessmentResponseCommand(
            session_id="asess-life-1",
            question_id="q-numeric-mu",
            response_payload={"entered_value": "0.02"},
        ),
        student_id=student,
    )
    svc.commit_response(
        CommitAssessmentResponseCommand(
            session_id="asess-life-1",
            question_id="q-confidence-mu",
            response_payload={"confidence": 4},
            confidence=4,
        ),
        student_id=student,
    )
    svc.commit_response(
        CommitAssessmentResponseCommand(
            session_id="asess-life-1",
            question_id="q-reflection-mu",
            response_payload={"reflection_text": "Need more practice on mu."},
        ),
        student_id=student,
    )

    delivery = svc.get_delivery("asess-life-1", student_id=student)
    assert delivery.progress.can_complete is True

    completed = svc.complete(
        SubmitAssessmentSessionCommand(session_id="asess-life-1"),
        student_id=student,
    )
    assert completed.status == "submitted"
    assert completed.result is not None
    assert completed.observation_count >= 4


def test_delivery_navigation_previous_next() -> None:
    composition = build_assessment_delivery(seed=True)
    svc = composition.delivery_service
    student = "student-nav"
    svc.create_session(
        CreateAssessmentSessionCommand(
            session_id="asess-nav-1",
            student_id=student,
            instrument_id=composition.default_instrument_id,
        )
    )
    svc.start(
        StartAssessmentSessionCommand(session_id="asess-nav-1"),
        student_id=student,
    )
    nxt = svc.navigate(
        NavigateAssessmentSessionCommand(
            session_id="asess-nav-1", direction="next"
        ),
        student_id=student,
    )
    assert nxt.progress.current_index == 1
    prev = svc.navigate(
        NavigateAssessmentSessionCommand(
            session_id="asess-nav-1", direction="previous"
        ),
        student_id=student,
    )
    assert prev.progress.current_index == 0


def test_delivery_ownership_guard() -> None:
    composition = build_assessment_delivery(seed=True)
    svc = composition.delivery_service
    svc.create_session(
        CreateAssessmentSessionCommand(
            session_id="asess-own-1",
            student_id="owner",
            instrument_id=composition.default_instrument_id,
        )
    )
    with pytest.raises(SessionOwnershipError):
        svc.get_delivery("asess-own-1", student_id="other")


def test_duplicate_submission_when_retries_none() -> None:
    composition = build_assessment_delivery(seed=True)
    svc = composition.delivery_service
    student = "student-dup"
    svc.create_session(
        CreateAssessmentSessionCommand(
            session_id="asess-dup-1",
            student_id=student,
            instrument_id=composition.default_instrument_id,
        )
    )
    svc.start(
        StartAssessmentSessionCommand(session_id="asess-dup-1"),
        student_id=student,
    )
    svc.commit_response(
        CommitAssessmentResponseCommand(
            session_id="asess-dup-1",
            question_id="q-mc-force",
            response_payload={"selected_option": "a"},
        ),
        student_id=student,
    )
    # max_retries=1 allows attempt 2; attempt 3 should fail
    svc.commit_response(
        CommitAssessmentResponseCommand(
            session_id="asess-dup-1",
            question_id="q-mc-force",
            response_payload={"selected_option": "b"},
            retries=1,
        ),
        student_id=student,
    )
    with pytest.raises((DuplicateSubmissionError, SessionStateError)):
        svc.commit_response(
            CommitAssessmentResponseCommand(
                session_id="asess-dup-1",
                question_id="q-mc-force",
                response_payload={"selected_option": "c"},
                retries=2,
            ),
            student_id=student,
        )


def test_expired_session_blocks_start() -> None:
    from datetime import UTC, datetime, timedelta

    from application.assessment.delivery.delivery_service import (
        AssessmentDeliveryService,
    )

    composition = build_assessment_delivery(seed=True)
    now = datetime(2026, 7, 27, 12, 0, tzinfo=UTC)

    def clock() -> datetime:
        return now

    svc = AssessmentDeliveryService(
        sessions=composition.sessions,
        instruments=composition.instruments,
        observations=composition.observations,
        results=composition.results,
        question_content=composition.question_content,
        delivery_state=composition.delivery_state,
        session_builder=composition.session_builder,
        default_instrument_id=composition.default_instrument_id,
        clock=clock,
    )
    svc.create_session(
        CreateAssessmentSessionCommand(
            session_id="asess-exp-1",
            student_id="student-exp",
            instrument_id=composition.default_instrument_id,
        )
    )
    state = composition.delivery_state.get("asess-exp-1")
    assert state is not None
    state.expires_at = now - timedelta(seconds=1)
    composition.delivery_state.save(state)
    with pytest.raises(ExpiredSessionError):
        svc.start(
            StartAssessmentSessionCommand(session_id="asess-exp-1"),
            student_id="student-exp",
        )


def test_delivery_does_not_call_reasoning_or_twin() -> None:
    """Regression: complete path packages result only — no Twin/Reasoning imports."""
    import application.assessment.delivery.delivery_service as mod

    source = open(mod.__file__, encoding="utf-8").read()
    assert "StudentReasoningService" not in source
    assert "StudentDigitalTwin" not in source
    assert "MissionEngine" not in source
