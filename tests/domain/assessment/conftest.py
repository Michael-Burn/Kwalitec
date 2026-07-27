"""Shared fixtures for assessment domain unit tests."""

from __future__ import annotations

import pytest

from domain.assessment import (
    AssessmentConfiguration,
    AssessmentMetadata,
    AssessmentPurpose,
    AssessmentType,
    DifficultyBand,
    DifficultyLevel,
    InstrumentId,
    ItemType,
    LearningObjectiveId,
    LearningObjectiveReference,
    QuestionId,
    QuestionReference,
    SessionId,
)
from domain.assessment.factories import (
    AssessmentInstrumentFactory,
    AssessmentSessionFactory,
)


@pytest.fixture
def objective_ref() -> LearningObjectiveReference:
    return LearningObjectiveReference(
        objective_id=LearningObjectiveId("lo-force-mortality"),
        label="Force of mortality",
    )


@pytest.fixture
def question_ref(objective_ref: LearningObjectiveReference) -> QuestionReference:
    return QuestionReference(
        question_id=QuestionId("q-001"),
        item_type=ItemType.MULTIPLE_CHOICE,
        version="1",
        learning_objective=objective_ref,
        curriculum_entity_id="topic-cm1-01",
        difficulty=DifficultyLevel(band=DifficultyBand.STANDARD),
        estimated_time_seconds=90,
    )


@pytest.fixture
def second_question_ref(
    objective_ref: LearningObjectiveReference,
) -> QuestionReference:
    return QuestionReference(
        question_id=QuestionId("q-002"),
        item_type=ItemType.NUMERIC,
        version="1",
        learning_objective=objective_ref,
        estimated_time_seconds=60,
    )


@pytest.fixture
def instrument(
    question_ref: QuestionReference,
    objective_ref: LearningObjectiveReference,
):
    return AssessmentInstrumentFactory.create(
        instrument_id=InstrumentId("inst-diag-001"),
        assessment_type=AssessmentType.QUIZ_BUNDLE,
        purpose=AssessmentPurpose.DIAGNOSTIC,
        questions=[question_ref],
        learning_objectives=[objective_ref],
        metadata=AssessmentMetadata(
            version="1",
            title="Diagnostic check — force of mortality",
            description="Short diagnostic probe",
        ),
        configuration=AssessmentConfiguration(),
    )


@pytest.fixture
def session(instrument):
    return AssessmentSessionFactory.create_from_instrument(
        session_id=SessionId("sess-001"),
        student_id="student-42",
        instrument=instrument,
        twin_id="twin-42",
    )
