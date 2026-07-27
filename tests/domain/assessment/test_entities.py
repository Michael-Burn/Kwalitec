"""Entity invariant and session behaviour tests."""

from __future__ import annotations

import pytest

from domain.assessment import (
    AssessmentConfiguration,
    AssessmentMetadata,
    AssessmentObservation,
    AssessmentPurpose,
    AssessmentResult,
    AssessmentSession,
    AssessmentStatus,
    AssessmentType,
    AttemptOutcome,
    ConfidenceLevel,
    DuplicateQuestionReferenceError,
    EvidenceStrength,
    InstrumentId,
    InvalidAssessmentStateTransition,
    ItemType,
    LearningObjectiveId,
    LearningObjectiveReference,
    MissingLearningObjectiveError,
    ObservationId,
    ObservationKind,
    QuestionId,
    QuestionReference,
    ResultId,
    SessionId,
)
from domain.assessment.exceptions import (
    AssessmentInvariantViolation,
    InvalidObservationPayloadError,
)
from domain.assessment.factories import (
    AssessmentInstrumentFactory,
    AssessmentObservationFactory,
    AssessmentResultFactory,
)


def test_instrument_rejects_duplicate_questions(
    question_ref: QuestionReference, objective_ref: LearningObjectiveReference
) -> None:
    with pytest.raises(DuplicateQuestionReferenceError):
        AssessmentInstrumentFactory.create(
            instrument_id=InstrumentId("inst"),
            assessment_type=AssessmentType.SINGLE_ITEM,
            purpose=AssessmentPurpose.DIAGNOSTIC,
            questions=[question_ref, question_ref],
            learning_objectives=[objective_ref],
            metadata=AssessmentMetadata(version="1", title="Dup"),
        )


def test_instrument_requires_learning_objective(
    question_ref: QuestionReference,
) -> None:
    with pytest.raises(MissingLearningObjectiveError):
        AssessmentInstrumentFactory.create(
            instrument_id=InstrumentId("inst"),
            assessment_type=AssessmentType.SINGLE_ITEM,
            purpose=AssessmentPurpose.DIAGNOSTIC,
            questions=[question_ref],
            learning_objectives=[],
            metadata=AssessmentMetadata(version="1", title="Missing LO"),
        )


def test_session_lifecycle_and_commit(session: AssessmentSession) -> None:
    events = session.pull_events()
    assert any(type(e).__name__ == "AssessmentSessionConstructed" for e in events)
    assert session.status is AssessmentStatus.DRAFT

    session.mark_ready()
    session.start()
    assert session.status is AssessmentStatus.IN_PROGRESS

    attempt = session.commit_response(
        QuestionId("q-001"),
        response_payload={"selected": "B"},
        confidence=ConfidenceLevel(4),
        response_time_ms=1200,
        hints_used=0,
    )
    assert attempt.committed is True
    assert attempt.attempt_number.value == 1

    session.submit()
    assert session.status is AssessmentStatus.SUBMITTED
    session.mark_observed()
    session.mark_reasoned()
    session.close()
    assert session.status is AssessmentStatus.CLOSED


def test_session_rejects_invalid_transition(session: AssessmentSession) -> None:
    session.mark_ready()
    with pytest.raises(InvalidAssessmentStateTransition):
        session.mark_observed()


def test_commit_requires_in_progress(session: AssessmentSession) -> None:
    with pytest.raises(AssessmentInvariantViolation):
        session.commit_response(QuestionId("q-001"), response_payload={"a": 1})


def test_pause_resume_and_abandon(session: AssessmentSession) -> None:
    session.mark_ready()
    session.start()
    session.pause()
    assert session.status is AssessmentStatus.PAUSED
    session.resume()
    assert session.status is AssessmentStatus.IN_PROGRESS
    session.abandon()
    assert session.status is AssessmentStatus.ABANDONED


def test_observation_requires_question_for_answered(
    session: AssessmentSession,
) -> None:
    with pytest.raises(InvalidObservationPayloadError):
        AssessmentObservation(
            observation_id=ObservationId("obs-1"),
            session_id=session.session_id,
            kind=ObservationKind.QUESTION_ANSWERED,
        )


def test_record_observation_on_submitted_session(
    session: AssessmentSession,
) -> None:
    session.mark_ready()
    session.start()
    session.commit_response(QuestionId("q-001"), response_payload={"selected": "A"})
    session.submit()
    observation = AssessmentObservationFactory.create(
        observation_id=ObservationId("obs-1"),
        session_id=session.session_id,
        kind=ObservationKind.QUESTION_ANSWERED,
        question_id=QuestionId("q-001"),
        provenance={"assessment_session_id": session.session_id.value},
    )
    session.record_observation(observation)
    assert "obs-1" in session.observation_ids


def test_result_is_evidence_only() -> None:
    result = AssessmentResultFactory.create(
        result_id=ResultId("res-1"),
        session_id=SessionId("sess-1"),
        observation_ids=[ObservationId("obs-1")],
        correctness_counts={AttemptOutcome.CORRECT: 1, AttemptOutcome.INCORRECT: 0},
        evidence_strength=EvidenceStrength.thin(),
    )
    assert isinstance(result, AssessmentResult)
    assert result.correctness_count_map()[AttemptOutcome.CORRECT] == 1


def test_create_session_direct() -> None:
    objective = LearningObjectiveReference(
        objective_id=LearningObjectiveId("lo-x"),
    )
    question = QuestionReference(
        question_id=QuestionId("q-x"),
        item_type=ItemType.MULTIPLE_CHOICE,
        version="1",
        learning_objective=objective,
    )
    session = AssessmentSession.create(
        session_id=SessionId("s-direct"),
        student_id="student-1",
        instrument_id=InstrumentId("inst-x"),
        purpose=AssessmentPurpose.FORMATIVE_CHECKPOINT,
        assessment_type=AssessmentType.SINGLE_ITEM,
        questions=[question],
        configuration=AssessmentConfiguration(invite_confidence=False),
    )
    assert session.status is AssessmentStatus.DRAFT
