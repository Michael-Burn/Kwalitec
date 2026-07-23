"""Focused invariant tests for StudentEducationalState.

Complements test_student_educational_state.py with invariant-specific
scenarios: identity mandatory, single active episode/mission/checkpoint,
no duplicate subjects/competencies, and snapshot accuracy under mutation.
"""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import LearningEpisodeId
from domain.education.student_state import (
    CompetencyState,
    StudentEducationalState,
    StudentEducationalStateId,
    SubjectState,
)
from tests.domain.education.student_state.conftest import (
    make_competency_state,
    make_state,
    make_subject_state,
)


def test_student_identity_is_mandatory() -> None:
    with pytest.raises(EducationalInvariantViolation):
        StudentEducationalState(
            state_id=StudentEducationalStateId("s1"), student_id="   "
        )


def test_only_one_active_learning_episode_at_a_time() -> None:
    state = make_state()
    state.attach_learning_episode("episode-a")
    state.attach_learning_episode("episode-b")
    state.attach_learning_episode("episode-c")
    assert state.active_learning_episode_id == LearningEpisodeId("episode-c")
    # No hidden accumulation — the field remains a single scalar reference.
    assert isinstance(state.active_learning_episode_id, LearningEpisodeId)


def test_only_one_current_mission_at_a_time() -> None:
    state = make_state()
    state.attach_current_mission("mission-a")
    state.attach_current_mission("mission-b")
    assert state.current_mission.mission_id.value == "mission-b"


def test_only_one_current_checkpoint_at_a_time() -> None:
    state = make_state()
    state.attach_checkpoint("checkpoint-a")
    state.attach_checkpoint("checkpoint-b")
    assert state.current_checkpoint.checkpoint_id.value == "checkpoint-b"


def test_no_duplicate_subject_states_via_constructor() -> None:
    with pytest.raises(EducationalInvariantViolation):
        StudentEducationalState(
            state_id=StudentEducationalStateId("s1"),
            student_id="student-1",
            subject_states=[
                make_subject_state(subject_id="math"),
                make_subject_state(subject_id="math"),
            ],
        )


def test_no_duplicate_subject_states_via_direct_list_mutation_guard() -> None:
    # The aggregate always re-validates through the policy on update, so even
    # constructing with a list containing repeats fails identically to tuples.
    with pytest.raises(EducationalInvariantViolation):
        StudentEducationalState(
            state_id=StudentEducationalStateId("s1"),
            student_id="student-1",
            subject_states=(
                make_subject_state(subject_id="math"),
                make_subject_state(subject_id="math"),
            ),
        )


def test_no_duplicate_competency_identifiers_via_constructor() -> None:
    with pytest.raises(EducationalInvariantViolation):
        StudentEducationalState(
            state_id=StudentEducationalStateId("s1"),
            student_id="student-1",
            competency_states=[
                make_competency_state(competency_id="algebra"),
                make_competency_state(competency_id="algebra"),
            ],
        )


def test_invalid_educational_state_not_constructible_from_bad_collections() -> None:
    with pytest.raises(EducationalInvariantViolation):
        StudentEducationalState(
            state_id=StudentEducationalStateId("s1"),
            student_id="student-1",
            subject_states=["not-a-subject-state"],  # type: ignore[list-item]
        )
    with pytest.raises(EducationalInvariantViolation):
        StudentEducationalState(
            state_id=StudentEducationalStateId("s1"),
            student_id="student-1",
            competency_states=[42],  # type: ignore[list-item]
        )


def test_subject_states_property_returns_defensive_copy() -> None:
    state = make_state()
    state.update_subject_state(make_subject_state(subject_id="math"))
    snapshot_tuple = state.subject_states
    assert isinstance(snapshot_tuple, tuple)
    # Mutating a local reference must not affect the aggregate internals.
    mutable_list = list(snapshot_tuple)
    mutable_list.append(make_subject_state(subject_id="physics"))
    assert state.subject_count() == 1


def test_snapshot_accurately_reflects_state_across_many_mutations() -> None:
    state = make_state()
    for i in range(5):
        state.update_subject_state(make_subject_state(subject_id=f"subject-{i}"))
        state.update_competency(
            make_competency_state(
                competency_id=f"competency-{i}", subject_id=f"subject-{i}"
            )
        )
    state.attach_learning_episode("episode-final")
    state.attach_current_mission("mission-final")
    state.attach_checkpoint("checkpoint-final")

    snapshot = state.produce_snapshot()

    assert snapshot.subject_states == state.subject_states
    assert snapshot.competency_states == state.competency_states
    assert snapshot.active_learning_episode_id == state.active_learning_episode_id
    assert snapshot.current_mission == state.current_mission
    assert snapshot.current_checkpoint == state.current_checkpoint


def test_value_objects_are_immutable_frozen_dataclasses() -> None:
    subject = make_subject_state()
    competency = make_competency_state()
    assert isinstance(subject, SubjectState)
    assert isinstance(competency, CompetencyState)
    with pytest.raises(Exception):
        subject.__dict__  # slots=True objects have no __dict__
