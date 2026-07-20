"""Policy tests for Educational Digital Twin."""

from __future__ import annotations

import pytest

from domain.education.digital_twin import (
    LearnerActivityStatus,
    MisconceptionPresence,
    StateValidationPolicy,
    TwinStatus,
    TwinUpdatePolicy,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DigitalTwinId
from tests.domain.education.digital_twin.conftest import (
    make_evidence_entry,
    make_intervention_entry,
    make_learner_state,
)


def test_assert_identity_and_student() -> None:
    assert StateValidationPolicy.assert_identity(DigitalTwinId("t1")).value == "t1"
    assert StateValidationPolicy.assert_student_id("student-x") == "student-x"
    with pytest.raises(EducationalInvariantViolation):
        StateValidationPolicy.assert_student_id("  ")


def test_assert_mutable_blocks_archived() -> None:
    TwinUpdatePolicy.assert_mutable(TwinStatus.ACTIVE, action="record_evidence")
    with pytest.raises(EducationalInvariantViolation):
        TwinUpdatePolicy.assert_mutable(TwinStatus.ARCHIVED, action="record_evidence")


def test_assert_can_archive() -> None:
    TwinUpdatePolicy.assert_can_archive(TwinStatus.ACTIVE)
    with pytest.raises(EducationalInvariantViolation):
        TwinUpdatePolicy.assert_can_archive(TwinStatus.ARCHIVED)


def test_evidence_appendable_sequence_and_uniqueness() -> None:
    history = [make_evidence_entry(entry_id="a", evidence_id="e1", sequence=1)]
    ok = make_evidence_entry(entry_id="b", evidence_id="e2", sequence=2)
    TwinUpdatePolicy.assert_evidence_appendable(history, ok)
    with pytest.raises(EducationalInvariantViolation):
        TwinUpdatePolicy.assert_evidence_appendable(
            history,
            make_evidence_entry(entry_id="c", evidence_id="e3", sequence=3),
        )
    with pytest.raises(EducationalInvariantViolation):
        TwinUpdatePolicy.assert_evidence_appendable(
            history,
            make_evidence_entry(entry_id="d", evidence_id="e1", sequence=2),
        )


def test_intervention_appendable_rejects_duplicate_entry() -> None:
    history = [make_intervention_entry(entry_id="same", sequence=1)]
    with pytest.raises(EducationalInvariantViolation):
        TwinUpdatePolicy.assert_intervention_appendable(
            history,
            make_intervention_entry(
                entry_id="same",
                intervention_ref="other",
                sequence=2,
            ),
        )


def test_history_preserved_guard() -> None:
    TwinUpdatePolicy.assert_history_preserved(2, 3, kind="evidence")
    with pytest.raises(EducationalInvariantViolation):
        TwinUpdatePolicy.assert_history_preserved(3, 2, kind="evidence")


def test_learner_activity_terminal() -> None:
    TwinUpdatePolicy.assert_learner_activity_transition(
        LearnerActivityStatus.ENGAGED,
        LearnerActivityStatus.IDLE,
    )
    with pytest.raises(EducationalInvariantViolation):
        TwinUpdatePolicy.assert_learner_activity_transition(
            LearnerActivityStatus.JOURNEY_COMPLETE,
            LearnerActivityStatus.ENGAGED,
        )


@pytest.mark.parametrize("presence", list(MisconceptionPresence))
def test_misconception_presence_transition_allows_all(
    presence: MisconceptionPresence,
) -> None:
    assert (
        TwinUpdatePolicy.assert_misconception_presence_transition(
            MisconceptionPresence.ACTIVE, presence
        )
        is presence
    )


def test_learner_matches_student() -> None:
    state = make_learner_state(student_id="student-ada")
    StateValidationPolicy.assert_learner_matches_student(state, "student-ada")
    with pytest.raises(EducationalInvariantViolation):
        StateValidationPolicy.assert_learner_matches_student(state, "other")


def test_next_sequences() -> None:
    assert TwinUpdatePolicy.next_evidence_sequence([]) == 1
    assert (
        TwinUpdatePolicy.next_evidence_sequence(
            [make_evidence_entry(sequence=3, evidence_id="e3", entry_id="eh3")]
        )
        == 4
    )
    assert TwinUpdatePolicy.next_intervention_sequence([]) == 1
