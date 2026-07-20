"""Entity tests for Educational Digital Twin."""

from __future__ import annotations

import pytest

from domain.education.digital_twin import (
    ConceptState,
    ConceptStateId,
    EvidenceHistoryEntry,
    EvidenceHistoryEntryId,
    InterventionHistoryEntry,
    InterventionHistoryEntryId,
    LearnerActivityStatus,
    LearnerState,
    LearnerStateId,
    MasteryBand,
    MasteryState,
    MisconceptionPresence,
    MisconceptionState,
    MisconceptionStateId,
    RetentionBand,
    RetentionState,
)
from domain.education.foundation.enums import EvidenceType, TeachingStrategyType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, EvidenceId, MisconceptionId
from tests.domain.education.digital_twin.conftest import (
    make_concept_state,
    make_evidence_entry,
    make_intervention_entry,
    make_learner_state,
    make_misconception_state,
)


def test_learner_state_identity_equality() -> None:
    left = make_learner_state(learner_state_id="ls-1")
    right = make_learner_state(
        learner_state_id="ls-1",
        activity_status=LearnerActivityStatus.IDLE,
    )
    assert left == right
    assert left.activity_status is not right.activity_status


def test_learner_state_with_activity_status() -> None:
    state = make_learner_state()
    nxt = state.with_activity_status(LearnerActivityStatus.PAUSED)
    assert nxt.activity_status is LearnerActivityStatus.PAUSED
    assert state.activity_status is LearnerActivityStatus.ENGAGED


@pytest.mark.parametrize("status", list(LearnerActivityStatus))
def test_learner_state_all_statuses(status: LearnerActivityStatus) -> None:
    state = LearnerState(
        learner_state_id=LearnerStateId("ls"),
        student_id="student-x",
        activity_status=status,
    )
    assert state.activity_status is status


def test_concept_state_with_mastery_and_retention() -> None:
    state = make_concept_state()
    nxt = state.with_mastery(MasteryState.of(MasteryBand.MASTERED, ratio=0.9))
    assert nxt.mastery.band is MasteryBand.MASTERED
    nxt2 = nxt.with_retention(RetentionState.of(RetentionBand.DURABLE))
    assert nxt2.retention.band is RetentionBand.DURABLE


def test_concept_state_rejects_negative_evidence_count() -> None:
    with pytest.raises(EducationalInvariantViolation):
        ConceptState(
            concept_state_id=ConceptStateId("cs"),
            concept_id=ConceptId("c1"),
            mastery=MasteryState.unknown(),
            retention=RetentionState.unknown(),
            evidence_count=-1,
        )


@pytest.mark.parametrize("presence", list(MisconceptionPresence))
def test_misconception_state_presence(presence: MisconceptionPresence) -> None:
    state = make_misconception_state(presence=presence)
    assert state.presence is presence
    assert state.with_presence(MisconceptionPresence.CLEARED).presence is (
        MisconceptionPresence.CLEARED
    )


def test_misconception_state_identity() -> None:
    a = MisconceptionState(
        misconception_state_id=MisconceptionStateId("ms"),
        misconception_id=MisconceptionId("m1"),
        presence=MisconceptionPresence.SUSPECTED,
    )
    b = MisconceptionState(
        misconception_state_id=MisconceptionStateId("ms"),
        misconception_id=MisconceptionId("m1"),
        presence=MisconceptionPresence.ACTIVE,
    )
    assert a == b


@pytest.mark.parametrize("evidence_type", list(EvidenceType))
def test_evidence_history_entry_types(evidence_type: EvidenceType) -> None:
    entry = make_evidence_entry(
        entry_id=f"eh-{evidence_type.value}",
        evidence_id=f"ev-{evidence_type.value}",
        evidence_type=evidence_type,
    )
    assert entry.evidence_type is evidence_type


def test_evidence_history_rejects_smuggling_note() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_evidence_entry(note="therefore diagnose the learner")


def test_evidence_history_rejects_non_positive_sequence() -> None:
    with pytest.raises(EducationalInvariantViolation):
        EvidenceHistoryEntry(
            entry_id=EvidenceHistoryEntryId("eh"),
            evidence_id=EvidenceId("e1"),
            evidence_type=EvidenceType.REFLECTION,
            sequence=0,
        )


def test_intervention_history_rejects_smuggling_note() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_intervention_entry(note="approve this intervention now")


@pytest.mark.parametrize("strategy", list(TeachingStrategyType)[:8])
def test_intervention_history_strategy_types(strategy: TeachingStrategyType) -> None:
    entry = make_intervention_entry(
        entry_id=f"ih-{strategy.value}",
        intervention_ref=f"int-{strategy.value}",
        strategy_type=strategy,
    )
    assert entry.strategy_type is strategy


def test_intervention_history_requires_intervention_ref() -> None:
    with pytest.raises(EducationalInvariantViolation):
        InterventionHistoryEntry(
            entry_id=InterventionHistoryEntryId("ih"),
            intervention_ref="  ",
            sequence=1,
        )


def test_entity_ids_reject_whitespace() -> None:
    with pytest.raises(EducationalInvariantViolation):
        LearnerStateId("learner 1")
    with pytest.raises(EducationalInvariantViolation):
        ConceptStateId("cs 1")
    with pytest.raises(EducationalInvariantViolation):
        MisconceptionStateId("ms 1")
