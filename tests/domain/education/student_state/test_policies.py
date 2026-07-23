"""Tests for StateValidationPolicy."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import LearningEpisodeId
from domain.education.student_state import (
    StateValidationPolicy,
    StudentEducationalStateId,
)
from tests.domain.education.student_state.conftest import (
    make_checkpoint_reference,
    make_competency_state,
    make_confidence_summary,
    make_educational_health,
    make_mastery_summary,
    make_mission_reference,
    make_subject_state,
    make_timeline_reference,
)


class TestIdentityAndStudentId:
    def test_assert_identity_accepts_valid_id(self) -> None:
        state_id = StudentEducationalStateId("s1")
        assert StateValidationPolicy.assert_identity(state_id) is state_id

    def test_assert_identity_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            StateValidationPolicy.assert_identity("s1")  # type: ignore[arg-type]

    def test_assert_student_id_strips_whitespace(self) -> None:
        assert StateValidationPolicy.assert_student_id("  student-1  ") == "student-1"

    def test_assert_student_id_rejects_blank(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            StateValidationPolicy.assert_student_id("   ")

    def test_assert_student_id_rejects_whitespace_inside(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            StateValidationPolicy.assert_student_id("student one")


class TestCollectionAssertions:
    def test_assert_subject_states_accepts_unique(self) -> None:
        items = [
            make_subject_state(subject_id="math"),
            make_subject_state(subject_id="physics"),
        ]
        result = StateValidationPolicy.assert_subject_states(items)
        assert len(result) == 2

    def test_assert_subject_states_rejects_duplicates(self) -> None:
        items = [
            make_subject_state(subject_id="math"),
            make_subject_state(subject_id="math"),
        ]
        with pytest.raises(EducationalInvariantViolation):
            StateValidationPolicy.assert_subject_states(items)

    def test_assert_subject_states_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            StateValidationPolicy.assert_subject_states(["not-a-subject-state"])  # type: ignore[list-item]

    def test_assert_competency_states_accepts_unique(self) -> None:
        items = [
            make_competency_state(competency_id="algebra"),
            make_competency_state(competency_id="calculus"),
        ]
        result = StateValidationPolicy.assert_competency_states(items)
        assert len(result) == 2

    def test_assert_competency_states_rejects_duplicates(self) -> None:
        items = [
            make_competency_state(competency_id="algebra"),
            make_competency_state(competency_id="algebra"),
        ]
        with pytest.raises(EducationalInvariantViolation):
            StateValidationPolicy.assert_competency_states(items)

    def test_assert_competency_states_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            StateValidationPolicy.assert_competency_states([object()])  # type: ignore[list-item]


class TestSummaryAssertions:
    def test_assert_mastery_summary_accepts_valid(self) -> None:
        summary = make_mastery_summary()
        assert StateValidationPolicy.assert_mastery_summary(summary) is summary

    def test_assert_mastery_summary_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            StateValidationPolicy.assert_mastery_summary(None)  # type: ignore[arg-type]

    def test_assert_confidence_summary_accepts_valid(self) -> None:
        summary = make_confidence_summary()
        assert StateValidationPolicy.assert_confidence_summary(summary) is summary

    def test_assert_confidence_summary_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            StateValidationPolicy.assert_confidence_summary("bad")  # type: ignore[arg-type]

    def test_assert_educational_health_accepts_valid(self) -> None:
        health = make_educational_health()
        assert StateValidationPolicy.assert_educational_health(health) is health

    def test_assert_educational_health_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            StateValidationPolicy.assert_educational_health(42)  # type: ignore[arg-type]


class TestReferenceAssertions:
    def test_assert_active_learning_episode_accepts_none(self) -> None:
        assert StateValidationPolicy.assert_active_learning_episode(None) is None

    def test_assert_active_learning_episode_accepts_valid(self) -> None:
        episode_id = LearningEpisodeId("episode-1")
        assert (
            StateValidationPolicy.assert_active_learning_episode(episode_id)
            is episode_id
        )

    def test_assert_active_learning_episode_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            StateValidationPolicy.assert_active_learning_episode("episode-1")  # type: ignore[arg-type]

    def test_assert_current_mission_accepts_none(self) -> None:
        assert StateValidationPolicy.assert_current_mission(None) is None

    def test_assert_current_mission_accepts_valid(self) -> None:
        ref = make_mission_reference()
        assert StateValidationPolicy.assert_current_mission(ref) is ref

    def test_assert_current_mission_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            StateValidationPolicy.assert_current_mission("mission-1")  # type: ignore[arg-type]

    def test_assert_current_checkpoint_accepts_none(self) -> None:
        assert StateValidationPolicy.assert_current_checkpoint(None) is None

    def test_assert_current_checkpoint_accepts_valid(self) -> None:
        ref = make_checkpoint_reference()
        assert StateValidationPolicy.assert_current_checkpoint(ref) is ref

    def test_assert_current_checkpoint_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            StateValidationPolicy.assert_current_checkpoint("checkpoint-1")  # type: ignore[arg-type]

    def test_assert_educational_timeline_accepts_none(self) -> None:
        assert StateValidationPolicy.assert_educational_timeline(None) is None

    def test_assert_educational_timeline_accepts_valid(self) -> None:
        ref = make_timeline_reference()
        assert StateValidationPolicy.assert_educational_timeline(ref) is ref

    def test_assert_educational_timeline_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            StateValidationPolicy.assert_educational_timeline("timeline-1")  # type: ignore[arg-type]


class TestTimestampAssertion:
    def test_assert_last_updated_at_accepts_none(self) -> None:
        assert StateValidationPolicy.assert_last_updated_at(None) is None

    def test_assert_last_updated_at_accepts_datetime(self) -> None:
        now = datetime(2026, 1, 1, tzinfo=UTC)
        assert StateValidationPolicy.assert_last_updated_at(now) == now

    def test_assert_last_updated_at_rejects_non_datetime(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            StateValidationPolicy.assert_last_updated_at("2026-01-01")  # type: ignore[arg-type]
