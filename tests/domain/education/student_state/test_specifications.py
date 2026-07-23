"""Tests for StudentEducationalState specifications."""

from __future__ import annotations

from datetime import UTC

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.student_state import (
    EducationalStateSnapshot,
    SnapshotReflectsStateSpecification,
    StudentEducationalStateIsConsistentSpecification,
)
from tests.domain.education.student_state.conftest import (
    make_checkpoint_reference,
    make_competency_state,
    make_confidence_summary,
    make_educational_health,
    make_episode_id,
    make_mastery_summary,
    make_mission_reference,
    make_state,
    make_subject_state,
    make_timeline_reference,
)


class TestStudentEducationalStateIsConsistentSpecification:
    def test_satisfied_for_fresh_state(self) -> None:
        state = make_state()
        spec = StudentEducationalStateIsConsistentSpecification()
        assert spec.is_satisfied_by(state)
        spec.assert_satisfied_by(state)

    def test_satisfied_after_updates(self) -> None:
        state = make_state()
        state.update_subject_state(make_subject_state(subject_id="math"))
        state.update_competency(make_competency_state(competency_id="algebra"))
        spec = StudentEducationalStateIsConsistentSpecification()
        assert spec.is_satisfied_by(state)

    def test_assert_satisfied_by_raises_when_unsatisfied(self) -> None:
        state = make_state()
        state._student_id = ""  # simulate corrupted internal state
        spec = StudentEducationalStateIsConsistentSpecification()
        assert not spec.is_satisfied_by(state)
        with pytest.raises(EducationalInvariantViolation):
            spec.assert_satisfied_by(state)

    def test_unsatisfied_when_mastery_summary_missing(self) -> None:
        state = make_state()
        state._mastery_summary = None
        assert not StudentEducationalStateIsConsistentSpecification().is_satisfied_by(
            state
        )

    def test_unsatisfied_when_confidence_summary_missing(self) -> None:
        state = make_state()
        state._confidence_summary = None
        assert not StudentEducationalStateIsConsistentSpecification().is_satisfied_by(
            state
        )

    def test_unsatisfied_when_educational_health_missing(self) -> None:
        state = make_state()
        state._educational_health = None
        assert not StudentEducationalStateIsConsistentSpecification().is_satisfied_by(
            state
        )

    def test_unsatisfied_when_subject_ids_duplicated_internally(self) -> None:
        state = make_state()
        state._subject_states = [
            make_subject_state(subject_id="math"),
            make_subject_state(subject_id="math"),
        ]
        assert not StudentEducationalStateIsConsistentSpecification().is_satisfied_by(
            state
        )

    def test_unsatisfied_when_competency_ids_duplicated_internally(self) -> None:
        state = make_state()
        state._competency_states = [
            make_competency_state(competency_id="algebra"),
            make_competency_state(competency_id="algebra"),
        ]
        assert not StudentEducationalStateIsConsistentSpecification().is_satisfied_by(
            state
        )


class TestSnapshotReflectsStateSpecification:
    def test_satisfied_for_freshly_produced_snapshot(self) -> None:
        state = make_state()
        state.update_subject_state(make_subject_state(subject_id="math"))
        snapshot = state.produce_snapshot()
        spec = SnapshotReflectsStateSpecification()
        assert spec.is_satisfied_by(state, snapshot)
        spec.assert_satisfied_by(state, snapshot)

    def test_unsatisfied_after_state_mutates_past_snapshot(self) -> None:
        state = make_state()
        snapshot = state.produce_snapshot()
        state.update_subject_state(make_subject_state(subject_id="math"))
        spec = SnapshotReflectsStateSpecification()
        assert not spec.is_satisfied_by(state, snapshot)
        with pytest.raises(EducationalInvariantViolation):
            spec.assert_satisfied_by(state, snapshot)

    def test_unsatisfied_for_snapshot_from_different_state(self) -> None:
        state_a = make_state(state_id="s1", student_id="student-a")
        state_b = make_state(state_id="s2", student_id="student-b")
        snapshot_a = state_a.produce_snapshot()
        spec = SnapshotReflectsStateSpecification()
        assert not spec.is_satisfied_by(state_b, snapshot_a)

    def test_snapshot_type_is_educational_state_snapshot(self) -> None:
        state = make_state()
        snapshot = state.produce_snapshot()
        assert isinstance(snapshot, EducationalStateSnapshot)

    @pytest.mark.parametrize(
        "mutate",
        [
            lambda s: s.update_subject_state(make_subject_state(subject_id="new")),
            lambda s: s.update_competency(
                make_competency_state(competency_id="new")
            ),
            lambda s: s.update_mastery_summary(make_mastery_summary()),
            lambda s: s.update_confidence_summary(make_confidence_summary()),
            lambda s: s.update_educational_health(make_educational_health()),
            lambda s: s.attach_learning_episode(make_episode_id()),
            lambda s: s.attach_current_mission(make_mission_reference()),
            lambda s: s.attach_checkpoint(make_checkpoint_reference()),
            lambda s: s.attach_educational_timeline(make_timeline_reference()),
        ],
    )
    def test_unsatisfied_for_every_field_drift(self, mutate) -> None:
        state = make_state()
        snapshot = state.produce_snapshot()
        mutate(state)
        spec = SnapshotReflectsStateSpecification()
        assert not spec.is_satisfied_by(state, snapshot)

    def test_unsatisfied_when_last_updated_at_drifts_in_isolation(self) -> None:
        from datetime import datetime

        state = make_state()
        snapshot = state.produce_snapshot()
        # Simulate only the timestamp drifting, isolating this specific check
        # from every other field comparison in the specification.
        state._last_updated_at = datetime(2026, 5, 1, tzinfo=UTC)
        spec = SnapshotReflectsStateSpecification()
        assert not spec.is_satisfied_by(state, snapshot)

    def test_unsatisfied_when_student_id_drifts_in_isolation(self) -> None:
        state = make_state()
        snapshot = state.produce_snapshot()
        # Simulate only student_id drifting, isolating this specific check
        # from every other field comparison in the specification.
        state._student_id = "a-different-student"
        spec = SnapshotReflectsStateSpecification()
        assert not spec.is_satisfied_by(state, snapshot)
