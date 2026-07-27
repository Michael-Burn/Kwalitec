"""Enum behaviour tests."""

from __future__ import annotations

from domain.assessment import (
    AssessmentPurpose,
    AssessmentStatus,
    AssessmentType,
    AttemptOutcome,
    ConfidenceBand,
    DifficultyBand,
    EvidenceSource,
    EvidenceStrengthBand,
    ItemType,
    ObservationKind,
)


def test_assessment_purpose_values_match_design_intents() -> None:
    values = {member.value for member in AssessmentPurpose}
    assert "diagnostic" in values
    assert "formative_checkpoint" in values
    assert "mastery_verification" in values
    assert "revision_stability" in values


def test_assessment_status_includes_lifecycle_states() -> None:
    values = {member.value for member in AssessmentStatus}
    for expected in (
        "draft",
        "ready",
        "in_progress",
        "paused",
        "submitted",
        "observed",
        "reasoned",
        "closed",
        "abandoned",
        "invalidated",
    ):
        assert expected in values


def test_item_types_cover_question_model() -> None:
    values = {member.value for member in ItemType}
    assert "multiple_choice" in values
    assert "formula" in values
    assert "concept_linking" in values


def test_observation_and_evidence_enums() -> None:
    assert ObservationKind.QUESTION_ANSWERED.value == "question_answered"
    assert AttemptOutcome.PARTIAL.value == "partial"
    assert EvidenceSource.ASSESSMENT_ENGINE.value == "assessment_engine"
    assert ConfidenceBand.HIGH.value == "high"
    assert DifficultyBand.STRETCH.value == "stretch"
    assert EvidenceStrengthBand.THIN.value == "thin"
    assert AssessmentType.QUIZ_BUNDLE.value == "quiz_bundle"
