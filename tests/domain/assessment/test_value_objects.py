"""Value object validation tests for the assessment domain."""

from __future__ import annotations

import pytest

from domain.assessment import (
    AssessmentConfiguration,
    AssessmentId,
    AttemptNumber,
    ConfidenceLevel,
    DifficultyBand,
    DifficultyLevel,
    EvidenceDimensions,
    EvidenceStrength,
    EvidenceStrengthBand,
    HintPolicy,
    InvalidConfidenceRangeError,
    ItemType,
    LearningObjectiveId,
    LearningObjectiveReference,
    QuestionId,
    QuestionReference,
    RetryPolicy,
    SessionId,
)
from domain.assessment.enums import AttemptOutcome
from domain.assessment.exceptions import AssessmentInvariantViolation
from domain.education.foundation.errors import EducationalInvariantViolation


def test_identity_value_objects_reject_blank() -> None:
    with pytest.raises(EducationalInvariantViolation):
        AssessmentId("  ")
    with pytest.raises(EducationalInvariantViolation):
        SessionId("")


def test_attempt_number_requires_positive_int() -> None:
    assert AttemptNumber(1).value == 1
    assert AttemptNumber(1).next().value == 2
    with pytest.raises(AssessmentInvariantViolation):
        AttemptNumber(0)
    with pytest.raises(AssessmentInvariantViolation):
        AttemptNumber(True)  # type: ignore[arg-type]


def test_confidence_level_range() -> None:
    assert ConfidenceLevel(3).band.value == "medium"
    with pytest.raises(InvalidConfidenceRangeError):
        ConfidenceLevel(0)
    with pytest.raises(InvalidConfidenceRangeError):
        ConfidenceLevel(6)


def test_difficulty_and_evidence_strength() -> None:
    level = DifficultyLevel(band=DifficultyBand.INTRODUCTORY)
    assert level.band is DifficultyBand.INTRODUCTORY
    assert EvidenceStrength.thin().band is EvidenceStrengthBand.THIN
    assert EvidenceStrength.strong().band is EvidenceStrengthBand.STRONG
    with pytest.raises(AssessmentInvariantViolation):
        EvidenceStrength(band="thin")  # type: ignore[arg-type]


def test_question_reference_requires_learning_objective() -> None:
    objective = LearningObjectiveReference(
        objective_id=LearningObjectiveId("lo-1"),
    )
    ref = QuestionReference(
        question_id=QuestionId("q-1"),
        item_type=ItemType.REFLECTION,
        version="1",
        learning_objective=objective,
    )
    assert ref.question_id.value == "q-1"
    with pytest.raises(AssessmentInvariantViolation):
        QuestionReference(
            question_id=QuestionId("q-1"),
            item_type=ItemType.REFLECTION,
            version="1",
            learning_objective="lo-1",  # type: ignore[arg-type]
        )


def test_configuration_invariants() -> None:
    cfg = AssessmentConfiguration(
        hint_policy=HintPolicy.NONE,
        retry_policy=RetryPolicy.NONE,
        max_retries=None,
    )
    assert cfg.allow_pause is True
    with pytest.raises(AssessmentInvariantViolation):
        AssessmentConfiguration(require_confidence=True, invite_confidence=False)
    with pytest.raises(AssessmentInvariantViolation):
        AssessmentConfiguration(retry_policy=RetryPolicy.LIMITED, max_retries=None)


def test_evidence_dimensions_validation() -> None:
    dims = EvidenceDimensions(
        correctness=AttemptOutcome.CORRECT,
        confidence=ConfidenceLevel(4),
        hints_used=1,
        retries=0,
        misconception_tags=("mis-rate",),
        evidence_strength=EvidenceStrength.moderate(),
    )
    assert dims.hints_used == 1
    with pytest.raises(AssessmentInvariantViolation):
        EvidenceDimensions(hints_used=-1)
