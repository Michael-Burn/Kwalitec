"""Tests for the EducationalEvidence aggregate's record_* factories."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from domain.education.educational_evidence import (
    CheckpointId,
    EducationalEvidence,
    EvidenceSnapshot,
    EvidenceType,
    EvidenceWeight,
    LearningEnvironmentKind,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from tests.domain.education.educational_evidence.conftest import (
    make_environment,
    make_evidence_id,
    make_source,
)

OCCURRED_AT = datetime(2026, 7, 21, 12, 0, tzinfo=UTC)
STUDENT_ID = "student-ada"


class TestRecordQuestionAnswer:
    def test_produces_question_answered_for_correct(self) -> None:
        evidence = EducationalEvidence.record_question_answer(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            competency_id="algebra",
            is_correct=True,
        )
        assert evidence.evidence_type is EvidenceType.QUESTION_ANSWERED
        assert evidence.metadata.get("is_correct") is True
        assert evidence.references_competency("algebra")

    def test_produces_question_incorrect_for_incorrect(self) -> None:
        evidence = EducationalEvidence.record_question_answer(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            competency_id="algebra",
            is_correct=False,
        )
        assert evidence.evidence_type is EvidenceType.QUESTION_INCORRECT
        assert evidence.metadata.get("is_correct") is False

    def test_requires_competency_id(self) -> None:
        with pytest.raises(TypeError):
            EducationalEvidence.record_question_answer(  # type: ignore[call-arg]
                make_evidence_id(),
                STUDENT_ID,
                OCCURRED_AT,
                make_source(),
                learning_environment=make_environment(),
                is_correct=True,
            )

    def test_accepts_optional_subject_and_episode(self) -> None:
        evidence = EducationalEvidence.record_question_answer(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            competency_id="algebra",
            is_correct=True,
            subject_id="math",
            learning_episode_id="episode-1",
        )
        assert evidence.references_subject("math")
        assert evidence.references_learning_episode("episode-1")

    def test_extra_metadata_cannot_override_reserved_key(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EducationalEvidence.record_question_answer(
                make_evidence_id(),
                STUDENT_ID,
                OCCURRED_AT,
                make_source(),
                learning_environment=make_environment(),
                competency_id="algebra",
                is_correct=True,
                extra_metadata={"is_correct": False},
            )

    def test_extra_metadata_is_merged(self) -> None:
        evidence = EducationalEvidence.record_question_answer(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            competency_id="algebra",
            is_correct=True,
            extra_metadata={"attempt_number": 2},
        )
        assert evidence.metadata.get("attempt_number") == 2

    def test_default_weight_differs_by_outcome(self) -> None:
        correct = EducationalEvidence.record_question_answer(
            make_evidence_id("a"),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            competency_id="algebra",
            is_correct=True,
        )
        incorrect = EducationalEvidence.record_question_answer(
            make_evidence_id("b"),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            competency_id="algebra",
            is_correct=False,
        )
        assert correct.weight.magnitude != incorrect.weight.magnitude

    def test_explicit_weight_override(self) -> None:
        evidence = EducationalEvidence.record_question_answer(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            competency_id="algebra",
            is_correct=True,
            weight=EvidenceWeight.of(0.9),
        )
        assert evidence.weight.magnitude == 0.9

    def test_explicit_weight_override_as_float(self) -> None:
        evidence = EducationalEvidence.record_question_answer(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            competency_id="algebra",
            is_correct=True,
            weight=0.42,
        )
        assert evidence.weight.magnitude == 0.42

    def test_invalid_weight_type_is_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EducationalEvidence.record_question_answer(
                make_evidence_id(),
                STUDENT_ID,
                OCCURRED_AT,
                make_source(),
                learning_environment=make_environment(),
                competency_id="algebra",
                is_correct=True,
                weight="high",  # type: ignore[arg-type]
            )

    def test_accepts_evidence_timestamp_directly(self) -> None:
        from domain.education.educational_evidence import EvidenceTimestamp

        evidence = EducationalEvidence.record_question_answer(
            make_evidence_id(),
            STUDENT_ID,
            EvidenceTimestamp.of(OCCURRED_AT),
            make_source(),
            learning_environment=make_environment(),
            competency_id="algebra",
            is_correct=True,
        )
        assert evidence.occurred_at.occurred_at == OCCURRED_AT


class TestRecordReflection:
    def test_produces_reflection_recorded(self) -> None:
        evidence = EducationalEvidence.record_reflection(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(
                LearningEnvironmentKind.REFLECTION_PROMPT
            ),
            reflection_text="I found derivatives hard today.",
        )
        assert evidence.evidence_type is EvidenceType.REFLECTION_RECORDED
        assert evidence.metadata.get("reflection_text") == (
            "I found derivatives hard today."
        )

    def test_context_is_optional(self) -> None:
        evidence = EducationalEvidence.record_reflection(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            reflection_text="General reflection",
        )
        assert evidence.context.learning_context.is_empty()

    def test_rejects_blank_reflection_text(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EducationalEvidence.record_reflection(
                make_evidence_id(),
                STUDENT_ID,
                OCCURRED_AT,
                make_source(),
                learning_environment=make_environment(),
                reflection_text="   ",
            )


class TestRecordSessionLifecycle:
    def test_record_session_start(self) -> None:
        evidence = EducationalEvidence.record_session_start(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(
                LearningEnvironmentKind.STUDY_SESSION
            ),
            learning_episode_id="episode-1",
        )
        assert evidence.evidence_type is EvidenceType.STUDY_SESSION_STARTED
        assert evidence.references_learning_episode("episode-1")

    def test_record_session_completion(self) -> None:
        evidence = EducationalEvidence.record_session_completion(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(
                LearningEnvironmentKind.STUDY_SESSION
            ),
            learning_episode_id="episode-1",
        )
        assert evidence.evidence_type is EvidenceType.STUDY_SESSION_COMPLETED

    def test_session_requires_learning_episode(self) -> None:
        with pytest.raises(TypeError):
            EducationalEvidence.record_session_start(  # type: ignore[call-arg]
                make_evidence_id(),
                STUDENT_ID,
                OCCURRED_AT,
                make_source(),
                learning_environment=make_environment(),
            )


class TestRecordMissionCompletion:
    def test_produces_mission_completed(self) -> None:
        evidence = EducationalEvidence.record_mission_completion(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            mission_id="mission-1",
            completed=True,
        )
        assert evidence.evidence_type is EvidenceType.MISSION_COMPLETED
        assert evidence.metadata.get("completed") is True
        assert evidence.references_mission("mission-1")

    def test_produces_mission_abandoned(self) -> None:
        evidence = EducationalEvidence.record_mission_completion(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            mission_id="mission-1",
            completed=False,
        )
        assert evidence.evidence_type is EvidenceType.MISSION_ABANDONED
        assert evidence.metadata.get("completed") is False


class TestRecordHintRequest:
    def test_default_hint_count_is_one(self) -> None:
        evidence = EducationalEvidence.record_hint_request(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            competency_id="algebra",
        )
        assert evidence.evidence_type is EvidenceType.HINT_REQUESTED
        assert evidence.metadata.get("hint_count") == 1

    def test_explicit_hint_count(self) -> None:
        evidence = EducationalEvidence.record_hint_request(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            competency_id="algebra",
            hint_count=3,
        )
        assert evidence.metadata.get("hint_count") == 3

    def test_rejects_zero_hint_count(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EducationalEvidence.record_hint_request(
                make_evidence_id(),
                STUDENT_ID,
                OCCURRED_AT,
                make_source(),
                learning_environment=make_environment(),
                competency_id="algebra",
                hint_count=0,
            )


class TestRecordCheckpoint:
    def test_produces_checkpoint_reached(self) -> None:
        evidence = EducationalEvidence.record_checkpoint(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(
                LearningEnvironmentKind.CHECKPOINT_GATE
            ),
            checkpoint_id="checkpoint-1",
        )
        assert evidence.evidence_type is EvidenceType.CHECKPOINT_REACHED
        assert evidence.references_checkpoint("checkpoint-1")


class TestRecordConfidence:
    def test_produces_confidence_reported_with_subject(self) -> None:
        evidence = EducationalEvidence.record_confidence(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            confidence_level="high",
            subject_id="math",
        )
        assert evidence.evidence_type is EvidenceType.CONFIDENCE_REPORTED
        assert evidence.metadata.get("confidence_level") == "high"

    def test_produces_confidence_reported_with_competency(self) -> None:
        evidence = EducationalEvidence.record_confidence(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            confidence_level="low",
            competency_id="algebra",
        )
        assert evidence.evidence_type is EvidenceType.CONFIDENCE_REPORTED

    def test_requires_a_target(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EducationalEvidence.record_confidence(
                make_evidence_id(),
                STUDENT_ID,
                OCCURRED_AT,
                make_source(),
                learning_environment=make_environment(),
                confidence_level="high",
            )

    def test_rejects_unknown_confidence_level(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EducationalEvidence.record_confidence(
                make_evidence_id(),
                STUDENT_ID,
                OCCURRED_AT,
                make_source(),
                learning_environment=make_environment(),
                confidence_level="unknown",
                subject_id="math",
            )


class TestRecordTimeInvested:
    def test_produces_time_invested(self) -> None:
        evidence = EducationalEvidence.record_time_invested(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            duration_seconds=900,
        )
        assert evidence.evidence_type is EvidenceType.TIME_INVESTED
        assert evidence.metadata.get("duration_seconds") == 900

    def test_rejects_non_positive_duration(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EducationalEvidence.record_time_invested(
                make_evidence_id(),
                STUDENT_ID,
                OCCURRED_AT,
                make_source(),
                learning_environment=make_environment(),
                duration_seconds=0,
            )


class TestRecordReviewCompletion:
    def test_produces_review_completed(self) -> None:
        evidence = EducationalEvidence.record_review_completion(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(LearningEnvironmentKind.REVIEW),
            competency_id="algebra",
        )
        assert evidence.evidence_type is EvidenceType.REVIEW_COMPLETED


class TestRecordGoalAchievement:
    def test_produces_goal_achieved(self) -> None:
        evidence = EducationalEvidence.record_goal_achievement(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(LearningEnvironmentKind.GOAL_TRACKING),
            goal_id="goal-1",
        )
        assert evidence.evidence_type is EvidenceType.GOAL_ACHIEVED
        assert evidence.metadata.get("goal_id") == "goal-1"

    def test_rejects_blank_goal_id(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EducationalEvidence.record_goal_achievement(
                make_evidence_id(),
                STUDENT_ID,
                OCCURRED_AT,
                make_source(),
                learning_environment=make_environment(),
                goal_id="   ",
            )


class TestRecordSubjectVisit:
    def test_produces_subject_visited(self) -> None:
        evidence = EducationalEvidence.record_subject_visit(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(LearningEnvironmentKind.FREE_PRACTICE),
            subject_id="math",
        )
        assert evidence.evidence_type is EvidenceType.SUBJECT_VISITED
        assert evidence.references_subject("math")


class TestRecordCompetencyPractice:
    def test_produces_competency_practised(self) -> None:
        evidence = EducationalEvidence.record_competency_practice(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(LearningEnvironmentKind.FREE_PRACTICE),
            competency_id="algebra",
        )
        assert evidence.evidence_type is EvidenceType.COMPETENCY_PRACTISED
        assert evidence.references_competency("algebra")


class TestQueryHelpers:
    def test_is_type(self) -> None:
        evidence = EducationalEvidence.record_subject_visit(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            subject_id="math",
        )
        assert evidence.is_type(EvidenceType.SUBJECT_VISITED)
        assert not evidence.is_type(EvidenceType.GOAL_ACHIEVED)

    def test_reference_helpers_accept_typed_ids(self) -> None:
        evidence = EducationalEvidence.record_checkpoint(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            checkpoint_id=CheckpointId("checkpoint-1"),
        )
        assert evidence.references_checkpoint(CheckpointId("checkpoint-1"))
        assert not evidence.references_checkpoint("other-checkpoint")

    def test_reference_helpers_return_false_when_absent(self) -> None:
        evidence = EducationalEvidence.record_time_invested(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            duration_seconds=60,
        )
        assert not evidence.references_subject("math")
        assert not evidence.references_competency("algebra")
        assert not evidence.references_mission("mission-1")
        assert not evidence.references_checkpoint("checkpoint-1")
        assert not evidence.references_learning_episode("episode-1")


class TestSnapshot:
    def test_produce_snapshot_mirrors_evidence(self) -> None:
        evidence = EducationalEvidence.record_subject_visit(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            subject_id="math",
        )
        snapshot = evidence.produce_snapshot()
        assert isinstance(snapshot, EvidenceSnapshot)
        assert snapshot.evidence_id == evidence.evidence_id
        assert snapshot.student_id == evidence.student_id
        assert snapshot.evidence_type == evidence.evidence_type
        assert snapshot.occurred_at == evidence.occurred_at
        assert snapshot.source == evidence.source
        assert snapshot.context == evidence.context
        assert snapshot.weight == evidence.weight
        assert snapshot.metadata == evidence.metadata


class TestEqualityHashRepr:
    def test_equal_evidence_compares_equal(self) -> None:
        first = EducationalEvidence.record_subject_visit(
            make_evidence_id("same"),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            subject_id="math",
        )
        second = EducationalEvidence.record_subject_visit(
            make_evidence_id("same"),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            subject_id="math",
        )
        assert first == second
        assert hash(first) == hash(second)

    def test_different_content_is_not_equal(self) -> None:
        first = EducationalEvidence.record_subject_visit(
            make_evidence_id("same"),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            subject_id="math",
        )
        second = EducationalEvidence.record_subject_visit(
            make_evidence_id("same"),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            subject_id="physics",
        )
        assert first != second

    def test_equality_against_foreign_type_is_not_implemented(self) -> None:
        evidence = EducationalEvidence.record_subject_visit(
            make_evidence_id(),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            subject_id="math",
        )
        assert evidence != "not-evidence"
        assert evidence == evidence  # identity shortcut

    def test_repr_contains_key_fields(self) -> None:
        evidence = EducationalEvidence.record_subject_visit(
            make_evidence_id("ev-x"),
            STUDENT_ID,
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            subject_id="math",
        )
        text = repr(evidence)
        assert "ev-x" in text
        assert "SUBJECT_VISITED" in text or "subject_visited" in text
