"""Specification tests for Educational Digital Twin."""

from __future__ import annotations

import pytest

from domain.education.digital_twin import (
    LearnerActivityStatus,
    MisconceptionPresence,
    StateTransitionIsValidSpecification,
    TwinIsConsistentSpecification,
    TwinStatus,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from tests.domain.education.digital_twin.conftest import make_twin


def test_twin_is_consistent_for_created_twin() -> None:
    twin = make_twin()
    spec = TwinIsConsistentSpecification()
    assert spec.is_satisfied_by(twin)
    spec.assert_satisfied_by(twin)


def test_twin_is_consistent_after_memory_updates() -> None:
    from domain.education.digital_twin import MasteryBand, MasteryState
    from domain.education.foundation.enums import EvidenceType

    twin = make_twin(twin_id="twin-cons")
    twin.record_evidence("e1", EvidenceType.PERFORMANCE)
    twin.record_intervention("i1")
    twin.update_mastery("c1", MasteryState.of(MasteryBand.DEVELOPING))
    assert TwinIsConsistentSpecification().is_satisfied_by(twin)


def test_status_transition_active_to_archived() -> None:
    spec = StateTransitionIsValidSpecification()
    assert spec.is_satisfied_by_status(TwinStatus.ACTIVE, TwinStatus.ARCHIVED)
    assert spec.is_satisfied_by_status(TwinStatus.ACTIVE, TwinStatus.ACTIVE)
    assert not spec.is_satisfied_by_status(TwinStatus.ARCHIVED, TwinStatus.ACTIVE)
    with pytest.raises(EducationalInvariantViolation):
        spec.assert_status(TwinStatus.ARCHIVED, TwinStatus.ACTIVE)


def test_learner_activity_transition_rules() -> None:
    spec = StateTransitionIsValidSpecification()
    assert spec.is_satisfied_by_learner_activity(
        LearnerActivityStatus.ENGAGED, LearnerActivityStatus.PAUSED
    )
    assert not spec.is_satisfied_by_learner_activity(
        LearnerActivityStatus.JOURNEY_COMPLETE,
        LearnerActivityStatus.ENGAGED,
    )


@pytest.mark.parametrize("current", list(MisconceptionPresence))
@pytest.mark.parametrize("nxt", list(MisconceptionPresence))
def test_misconception_presence_matrix(
    current: MisconceptionPresence, nxt: MisconceptionPresence
) -> None:
    spec = StateTransitionIsValidSpecification()
    assert spec.is_satisfied_by_misconception_presence(current, nxt)
