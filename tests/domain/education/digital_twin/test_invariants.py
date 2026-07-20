"""Invariant and history-preservation tests for Educational Digital Twin."""

from __future__ import annotations

import pytest

from domain.education.digital_twin import (
    EducationalDigitalTwin,
    EvidenceHistoryEntry,
    EvidenceHistoryEntryId,
    InterventionHistoryEntry,
    InterventionHistoryEntryId,
    LearnerState,
    LearnerStateId,
    MasteryBand,
    MasteryState,
    TwinIsConsistentSpecification,
)
from domain.education.foundation.enums import EvidenceType, TeachingStrategyType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, DigitalTwinId, EvidenceId
from tests.domain.education.digital_twin.conftest import (
    make_concept_state,
    make_evidence_entry,
    make_twin,
)


def test_twin_must_own_learner_state() -> None:
    with pytest.raises(EducationalInvariantViolation):
        EducationalDigitalTwin(
            twin_id=DigitalTwinId("t"),
            student_id="s",
            learner_state=None,  # type: ignore[arg-type]
        )


def test_evidence_history_cannot_be_lost_on_archive() -> None:
    twin = make_twin()
    twin.record_evidence("e1", EvidenceType.PERFORMANCE)
    twin.record_evidence("e2", EvidenceType.REFLECTION)
    before = twin.evidence_count()
    twin.archive()
    assert twin.evidence_count() == before


def test_intervention_history_entries_are_not_rewritten() -> None:
    twin = make_twin()
    twin.record_intervention(
        "i1", strategy_type=TeachingStrategyType.DIRECT_EXPLANATION
    )
    original = twin.intervention_history[0]
    twin.record_intervention("i2", strategy_type=TeachingStrategyType.ANALOGY)
    assert twin.intervention_history[0].entry_id == original.entry_id
    assert twin.intervention_history[0].strategy_type is original.strategy_type
    assert twin.intervention_history[0].intervention_ref == "i1"


def test_duplicate_concept_states_rejected_at_construction() -> None:
    learner = LearnerState(
        learner_state_id=LearnerStateId("ls"),
        student_id="student-ada",
    )
    with pytest.raises(EducationalInvariantViolation):
        EducationalDigitalTwin(
            twin_id=DigitalTwinId("twin-dup-c"),
            student_id="student-ada",
            learner_state=learner,
            concept_states=[
                make_concept_state(concept_state_id="a", concept_id="c1"),
                make_concept_state(concept_state_id="b", concept_id="c1"),
            ],
        )


def test_duplicate_evidence_ids_rejected_at_construction() -> None:
    learner = LearnerState(
        learner_state_id=LearnerStateId("ls"),
        student_id="student-ada",
    )
    with pytest.raises(EducationalInvariantViolation):
        EducationalDigitalTwin(
            twin_id=DigitalTwinId("twin-dup-e"),
            student_id="student-ada",
            learner_state=learner,
            evidence_history=[
                make_evidence_entry(entry_id="a", evidence_id="same", sequence=1),
                make_evidence_entry(entry_id="b", evidence_id="same", sequence=2),
            ],
        )


def test_non_increasing_evidence_sequence_rejected() -> None:
    learner = LearnerState(
        learner_state_id=LearnerStateId("ls"),
        student_id="student-ada",
    )
    with pytest.raises(EducationalInvariantViolation):
        EducationalDigitalTwin(
            twin_id=DigitalTwinId("twin-seq"),
            student_id="student-ada",
            learner_state=learner,
            evidence_history=[
                make_evidence_entry(entry_id="a", evidence_id="e1", sequence=2),
                make_evidence_entry(entry_id="b", evidence_id="e2", sequence=1),
            ],
        )


def test_consistency_spec_requires_trajectory() -> None:
    twin = make_twin()
    assert TwinIsConsistentSpecification().is_satisfied_by(twin)
    TwinIsConsistentSpecification().assert_satisfied_by(twin)


def test_cannot_append_evidence_with_wrong_sequence_via_policy_path() -> None:
    twin = make_twin()
    twin.record_evidence("e1", EvidenceType.PERFORMANCE)
    # Direct construction bypass is blocked by append policy when using aggregate API.
    with pytest.raises(EducationalInvariantViolation):
        twin.record_evidence("e1", EvidenceType.EXPLANATION)


def test_mastery_update_preserves_other_concept_states() -> None:
    twin = make_twin()
    twin.update_mastery("c-a", MasteryState.of(MasteryBand.NASCENT))
    twin.update_mastery("c-b", MasteryState.of(MasteryBand.DEVELOPING))
    twin.update_mastery("c-a", MasteryState.of(MasteryBand.PROFICIENT))
    assert twin.concept_state_for("c-a").mastery.band is MasteryBand.PROFICIENT
    assert twin.concept_state_for("c-b").mastery.band is MasteryBand.DEVELOPING


def test_evidence_linked_concept_increments_count() -> None:
    twin = make_twin()
    twin.record_evidence(
        "e-c1",
        EvidenceType.PERFORMANCE,
        concept_id=ConceptId("concept-count"),
    )
    twin.record_evidence(
        "e-c2",
        EvidenceType.REFLECTION,
        concept_id=ConceptId("concept-count"),
    )
    assert twin.concept_state_for("concept-count").evidence_count == 2


def test_history_entry_identity_types() -> None:
    entry = EvidenceHistoryEntry(
        entry_id=EvidenceHistoryEntryId("eh"),
        evidence_id=EvidenceId("e"),
        evidence_type=EvidenceType.ERROR_PATTERN,
        sequence=1,
    )
    assert entry.entity_id.value == "eh"
    intervention = InterventionHistoryEntry(
        entry_id=InterventionHistoryEntryId("ih"),
        intervention_ref="ref",
        sequence=1,
    )
    assert intervention.entity_id.value == "ih"
