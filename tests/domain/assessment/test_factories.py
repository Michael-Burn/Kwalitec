"""Factory behaviour tests."""

from __future__ import annotations

from domain.assessment import (
    AssessmentMetadata,
    AssessmentPurpose,
    AssessmentStatus,
    AssessmentType,
    InstrumentId,
    LearningObjectiveReference,
    QuestionReference,
    SessionId,
)
from domain.assessment.factories import (
    AssessmentInstrumentFactory,
    AssessmentSessionFactory,
)


def test_instrument_factory_builds_catalogue_entry(
    question_ref: QuestionReference, objective_ref: LearningObjectiveReference
) -> None:
    instrument = AssessmentInstrumentFactory.create(
        instrument_id=InstrumentId("inst-f"),
        assessment_type=AssessmentType.QUIZ_BUNDLE,
        purpose=AssessmentPurpose.RECOVERY_CHECK,
        questions=[question_ref],
        learning_objectives=[objective_ref],
        metadata=AssessmentMetadata(version="2", title="Recovery check"),
    )
    assert instrument.question_count() == 1
    assert instrument.purpose is AssessmentPurpose.RECOVERY_CHECK


def test_session_factory_copies_instrument_shape(instrument) -> None:
    session = AssessmentSessionFactory.create_from_instrument(
        session_id=SessionId("sess-f"),
        student_id="student-9",
        instrument=instrument,
        mission_id="mission-1",
    )
    assert session.status is AssessmentStatus.DRAFT
    assert session.instrument_id == instrument.instrument_id
    assert session.purpose == instrument.purpose
    assert len(session.questions) == instrument.question_count()
    assert session.mission_id == "mission-1"
