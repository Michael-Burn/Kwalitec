"""Tests for EvidenceValidationPolicy and EvidenceNormalisationPolicy."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from domain.education.educational_evidence import (
    EvidenceContext,
    EvidenceId,
    EvidenceMetadata,
    EvidenceNormalisationPolicy,
    EvidenceTimestamp,
    EvidenceType,
    EvidenceValidationPolicy,
    EvidenceWeight,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from tests.domain.education.educational_evidence.conftest import (
    make_context,
    make_environment,
    make_source,
)


class TestBasicAssertions:
    def test_assert_identity_accepts_valid(self) -> None:
        evidence_id = EvidenceId("e1")
        assert EvidenceValidationPolicy.assert_identity(evidence_id) is evidence_id

    def test_assert_identity_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_identity("e1")  # type: ignore[arg-type]

    def test_assert_student_id_strips_whitespace(self) -> None:
        assert EvidenceValidationPolicy.assert_student_id("  s1  ") == "s1"

    def test_assert_student_id_rejects_blank(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_student_id("   ")

    def test_assert_evidence_type_accepts_valid(self) -> None:
        assert (
            EvidenceValidationPolicy.assert_evidence_type(
                EvidenceType.QUESTION_ANSWERED
            )
            is EvidenceType.QUESTION_ANSWERED
        )

    def test_assert_evidence_type_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_evidence_type("question_answered")  # type: ignore[arg-type]

    def test_assert_timestamp_accepts_valid(self) -> None:
        ts = EvidenceTimestamp.of(datetime(2026, 1, 1, tzinfo=UTC))
        assert EvidenceValidationPolicy.assert_timestamp(ts) is ts

    def test_assert_timestamp_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_timestamp(
                datetime(2026, 1, 1, tzinfo=UTC)  # type: ignore[arg-type]
            )

    def test_assert_source_accepts_valid(self) -> None:
        source = make_source()
        assert EvidenceValidationPolicy.assert_source(source) is source

    def test_assert_source_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_source("student_action")  # type: ignore[arg-type]

    def test_assert_context_accepts_valid(self) -> None:
        context = make_context()
        assert EvidenceValidationPolicy.assert_context(context) is context

    def test_assert_context_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_context(None)  # type: ignore[arg-type]

    def test_assert_weight_accepts_valid(self) -> None:
        weight = EvidenceWeight.of(0.5)
        assert EvidenceValidationPolicy.assert_weight(weight) is weight

    def test_assert_weight_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_weight(0.5)  # type: ignore[arg-type]

    def test_assert_metadata_accepts_valid(self) -> None:
        metadata = EvidenceMetadata.empty()
        assert EvidenceValidationPolicy.assert_metadata(metadata) is metadata

    def test_assert_metadata_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_metadata({})  # type: ignore[arg-type]


class TestContextMatchesType:
    @pytest.mark.parametrize(
        "evidence_type,field_name",
        [
            (EvidenceType.QUESTION_ANSWERED, "competency_id"),
            (EvidenceType.QUESTION_INCORRECT, "competency_id"),
            (EvidenceType.MISSION_COMPLETED, "mission_id"),
            (EvidenceType.MISSION_ABANDONED, "mission_id"),
            (EvidenceType.STUDY_SESSION_STARTED, "learning_episode_id"),
            (EvidenceType.STUDY_SESSION_COMPLETED, "learning_episode_id"),
            (EvidenceType.HINT_REQUESTED, "competency_id"),
            (EvidenceType.REVIEW_COMPLETED, "competency_id"),
            (EvidenceType.CHECKPOINT_REACHED, "checkpoint_id"),
            (EvidenceType.SUBJECT_VISITED, "subject_id"),
            (EvidenceType.COMPETENCY_PRACTISED, "competency_id"),
        ],
    )
    def test_missing_required_field_is_rejected(
        self, evidence_type: EvidenceType, field_name: str
    ) -> None:
        context = EvidenceContext.of(make_environment())
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_context_matches_type(
                evidence_type, context
            )

    @pytest.mark.parametrize(
        "evidence_type,kwargs",
        [
            (EvidenceType.QUESTION_ANSWERED, {"competency_id": "algebra"}),
            (EvidenceType.MISSION_COMPLETED, {"mission_id": "mission-1"}),
            (
                EvidenceType.STUDY_SESSION_STARTED,
                {"learning_episode_id": "episode-1"},
            ),
            (EvidenceType.CHECKPOINT_REACHED, {"checkpoint_id": "checkpoint-1"}),
            (EvidenceType.SUBJECT_VISITED, {"subject_id": "math"}),
        ],
    )
    def test_required_field_present_is_accepted(
        self, evidence_type: EvidenceType, kwargs: dict
    ) -> None:
        base_kwargs = {"competency_id": None}
        base_kwargs.update(kwargs)
        context = make_context(**base_kwargs)
        EvidenceValidationPolicy.assert_context_matches_type(evidence_type, context)

    def test_confidence_reported_requires_subject_or_competency(self) -> None:
        context = EvidenceContext.of(make_environment())
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_context_matches_type(
                EvidenceType.CONFIDENCE_REPORTED, context
            )

    def test_confidence_reported_accepts_subject_only(self) -> None:
        context = make_context(competency_id=None, subject_id="math")
        EvidenceValidationPolicy.assert_context_matches_type(
            EvidenceType.CONFIDENCE_REPORTED, context
        )

    def test_confidence_reported_accepts_competency_only(self) -> None:
        context = make_context(competency_id="algebra")
        EvidenceValidationPolicy.assert_context_matches_type(
            EvidenceType.CONFIDENCE_REPORTED, context
        )

    def test_unrestricted_type_accepts_empty_context(self) -> None:
        context = EvidenceContext.of(make_environment())
        EvidenceValidationPolicy.assert_context_matches_type(
            EvidenceType.TIME_INVESTED, context
        )


class TestMetadataMatchesType:
    def test_is_correct_required_for_question_answered(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_metadata_matches_type(
                EvidenceType.QUESTION_ANSWERED, EvidenceMetadata.empty()
            )

    def test_is_correct_must_be_bool(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_metadata_matches_type(
                EvidenceType.QUESTION_ANSWERED,
                EvidenceMetadata.of(is_correct="yes"),
            )

    def test_is_correct_contradiction_is_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_metadata_matches_type(
                EvidenceType.QUESTION_ANSWERED,
                EvidenceMetadata.of(is_correct=False),
            )
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_metadata_matches_type(
                EvidenceType.QUESTION_INCORRECT,
                EvidenceMetadata.of(is_correct=True),
            )

    def test_is_correct_consistent_is_accepted(self) -> None:
        EvidenceValidationPolicy.assert_metadata_matches_type(
            EvidenceType.QUESTION_ANSWERED, EvidenceMetadata.of(is_correct=True)
        )
        EvidenceValidationPolicy.assert_metadata_matches_type(
            EvidenceType.QUESTION_INCORRECT, EvidenceMetadata.of(is_correct=False)
        )

    def test_completed_required_for_mission_types(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_metadata_matches_type(
                EvidenceType.MISSION_COMPLETED, EvidenceMetadata.empty()
            )

    def test_completed_must_be_bool(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_metadata_matches_type(
                EvidenceType.MISSION_COMPLETED,
                EvidenceMetadata.of(completed="yes"),
            )

    def test_completed_contradiction_is_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_metadata_matches_type(
                EvidenceType.MISSION_COMPLETED,
                EvidenceMetadata.of(completed=False),
            )
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_metadata_matches_type(
                EvidenceType.MISSION_ABANDONED,
                EvidenceMetadata.of(completed=True),
            )

    def test_completed_consistent_is_accepted(self) -> None:
        EvidenceValidationPolicy.assert_metadata_matches_type(
            EvidenceType.MISSION_COMPLETED, EvidenceMetadata.of(completed=True)
        )
        EvidenceValidationPolicy.assert_metadata_matches_type(
            EvidenceType.MISSION_ABANDONED, EvidenceMetadata.of(completed=False)
        )

    def test_duration_seconds_required_and_positive(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_metadata_matches_type(
                EvidenceType.TIME_INVESTED, EvidenceMetadata.empty()
            )
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_metadata_matches_type(
                EvidenceType.TIME_INVESTED,
                EvidenceMetadata.of(duration_seconds=0),
            )
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_metadata_matches_type(
                EvidenceType.TIME_INVESTED,
                EvidenceMetadata.of(duration_seconds=True),
            )
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_metadata_matches_type(
                EvidenceType.TIME_INVESTED,
                EvidenceMetadata.of(duration_seconds="60"),
            )
        EvidenceValidationPolicy.assert_metadata_matches_type(
            EvidenceType.TIME_INVESTED, EvidenceMetadata.of(duration_seconds=60.0)
        )

    def test_hint_count_required_and_at_least_one(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_metadata_matches_type(
                EvidenceType.HINT_REQUESTED, EvidenceMetadata.empty()
            )
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_metadata_matches_type(
                EvidenceType.HINT_REQUESTED, EvidenceMetadata.of(hint_count=0)
            )
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_metadata_matches_type(
                EvidenceType.HINT_REQUESTED, EvidenceMetadata.of(hint_count=True)
            )
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_metadata_matches_type(
                EvidenceType.HINT_REQUESTED, EvidenceMetadata.of(hint_count=1.5)
            )
        EvidenceValidationPolicy.assert_metadata_matches_type(
            EvidenceType.HINT_REQUESTED, EvidenceMetadata.of(hint_count=1)
        )

    def test_confidence_level_required_and_known(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_metadata_matches_type(
                EvidenceType.CONFIDENCE_REPORTED, EvidenceMetadata.empty()
            )
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_metadata_matches_type(
                EvidenceType.CONFIDENCE_REPORTED,
                EvidenceMetadata.of(confidence_level="unknown"),
            )
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_metadata_matches_type(
                EvidenceType.CONFIDENCE_REPORTED,
                EvidenceMetadata.of(confidence_level=3),
            )
        EvidenceValidationPolicy.assert_metadata_matches_type(
            EvidenceType.CONFIDENCE_REPORTED,
            EvidenceMetadata.of(confidence_level="high"),
        )

    def test_goal_id_required_and_non_empty(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_metadata_matches_type(
                EvidenceType.GOAL_ACHIEVED, EvidenceMetadata.empty()
            )
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_metadata_matches_type(
                EvidenceType.GOAL_ACHIEVED, EvidenceMetadata.of(goal_id="   ")
            )
        EvidenceValidationPolicy.assert_metadata_matches_type(
            EvidenceType.GOAL_ACHIEVED, EvidenceMetadata.of(goal_id="goal-1")
        )

    def test_reflection_text_required_and_non_empty(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_metadata_matches_type(
                EvidenceType.REFLECTION_RECORDED, EvidenceMetadata.empty()
            )
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_metadata_matches_type(
                EvidenceType.REFLECTION_RECORDED,
                EvidenceMetadata.of(reflection_text="   "),
            )
        EvidenceValidationPolicy.assert_metadata_matches_type(
            EvidenceType.REFLECTION_RECORDED,
            EvidenceMetadata.of(reflection_text="It was hard"),
        )

    def test_unrestricted_type_accepts_empty_metadata(self) -> None:
        EvidenceValidationPolicy.assert_metadata_matches_type(
            EvidenceType.CHECKPOINT_REACHED, EvidenceMetadata.empty()
        )


class TestEvidenceNormalisationPolicy:
    def test_normalise_metadata_is_idempotent(self) -> None:
        metadata = EvidenceMetadata.of(b=2, a=1)
        normalised = EvidenceNormalisationPolicy.normalise_metadata(metadata)
        assert normalised == metadata
        assert (
            EvidenceNormalisationPolicy.normalise_metadata(normalised) == normalised
        )

    def test_normalise_weight_is_idempotent(self) -> None:
        weight = EvidenceWeight.of(0.123456)
        normalised = EvidenceNormalisationPolicy.normalise_weight(weight)
        assert normalised == weight
        assert EvidenceNormalisationPolicy.normalise_weight(normalised) == normalised

    def test_is_metadata_normalised_true_for_canonical_metadata(self) -> None:
        assert EvidenceNormalisationPolicy.is_metadata_normalised(
            EvidenceMetadata.of(a=1, b=2)
        )

    def test_is_weight_normalised_true_for_canonical_weight(self) -> None:
        assert EvidenceNormalisationPolicy.is_weight_normalised(EvidenceWeight.of(0.5))
