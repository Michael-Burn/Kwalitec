"""Aggregate behaviour tests for EducationalDigitalTwin."""

from __future__ import annotations

import pytest

from domain.education.digital_twin import (
    ConfidenceProfile,
    EducationalDigitalTwin,
    LearnerActivityStatus,
    MasteryBand,
    MasteryChanged,
    MasteryState,
    MisconceptionPresence,
    RetentionBand,
    RetentionState,
    TwinCreated,
    TwinIsConsistentSpecification,
    TwinStatus,
    TwinUpdated,
    TwinUpdateKind,
)
from domain.education.foundation.enums import (
    ConfidenceLevel,
    EvidenceType,
    TeachingIntentionType,
    TeachingStrategyType,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, DigitalTwinId, EvidenceId
from tests.domain.education.digital_twin.conftest import (
    CONCEPT_001,
    make_archived_twin,
    make_twin,
)


def test_create_emits_twin_created_and_owns_learner_state() -> None:
    twin = EducationalDigitalTwin.create(
        twin_id=DigitalTwinId("twin-create"),
        student_id="student-ada",
    )
    events = twin.pull_events()
    assert len(events) == 1
    assert isinstance(events[0], TwinCreated)
    assert twin.learner_state.student_id == "student-ada"
    assert twin.is_active()
    assert TwinIsConsistentSpecification().is_satisfied_by(twin)


def test_record_evidence_appends_history_and_trajectory() -> None:
    twin = make_twin()
    twin.record_evidence(
        EvidenceId("ev-1"),
        EvidenceType.PERFORMANCE,
        concept_id=CONCEPT_001,
    )
    assert twin.evidence_count() == 1
    assert twin.has_evidence("ev-1")
    assert twin.has_concept(CONCEPT_001)
    events = twin.pull_events()
    assert any(
        isinstance(e, TwinUpdated) and e.update_kind is TwinUpdateKind.EVIDENCE_RECORDED
        for e in events
    )


def test_record_evidence_rejects_duplicate_evidence_id() -> None:
    twin = make_twin()
    twin.record_evidence("ev-dup", EvidenceType.EXPLANATION)
    with pytest.raises(EducationalInvariantViolation):
        twin.record_evidence("ev-dup", EvidenceType.REFLECTION)


def test_record_intervention_preserves_prior_entries() -> None:
    twin = make_twin()
    twin.record_intervention(
        "int-1",
        strategy_type=TeachingStrategyType.WORKED_EXAMPLE,
        intention_type=TeachingIntentionType.BUILD_INTUITION,
    )
    first = twin.intervention_history[0]
    twin.record_intervention("int-2", strategy_type=TeachingStrategyType.ANALOGY)
    assert twin.intervention_count() == 2
    assert twin.intervention_history[0] is first
    assert twin.intervention_history[0].intervention_ref == "int-1"


def test_update_mastery_emits_mastery_changed() -> None:
    twin = make_twin()
    twin.update_mastery(CONCEPT_001, MasteryState.of(MasteryBand.PROFICIENT, ratio=0.8))
    events = twin.pull_events()
    mastery_events = [e for e in events if isinstance(e, MasteryChanged)]
    assert len(mastery_events) == 1
    assert mastery_events[0].previous_band is MasteryBand.UNKNOWN
    assert mastery_events[0].new_band is MasteryBand.PROFICIENT
    assert twin.concept_state_for(CONCEPT_001) is not None


def test_update_mastery_replaces_existing_concept_memory() -> None:
    twin = make_twin()
    twin.update_mastery(CONCEPT_001, MasteryState.of(MasteryBand.NASCENT))
    twin.pull_events()
    twin.update_mastery(CONCEPT_001, MasteryState.of(MasteryBand.MASTERED, ratio=0.95))
    events = twin.pull_events()
    changed = next(e for e in events if isinstance(e, MasteryChanged))
    assert changed.previous_band is MasteryBand.NASCENT
    assert twin.concept_state_for(CONCEPT_001).mastery.band is MasteryBand.MASTERED


def test_update_retention_twin_level_and_concept_level() -> None:
    twin = make_twin()
    twin.update_retention(RetentionState.of(RetentionBand.DURABLE, ratio=0.9))
    assert twin.retention.band is RetentionBand.DURABLE
    twin.update_retention(
        RetentionState.of(RetentionBand.FADING),
        concept_id=ConceptId("concept-ret"),
    )
    assert twin.concept_state_for("concept-ret").retention.band is RetentionBand.FADING


def test_update_confidence_and_learner_activity() -> None:
    twin = make_twin()
    twin.update_confidence(ConfidenceProfile.of(ConfidenceLevel.HIGH, ratio=0.85))
    assert twin.confidence.overall is ConfidenceLevel.HIGH
    twin.update_learner_activity(LearnerActivityStatus.IDLE)
    assert twin.learner_state.activity_status is LearnerActivityStatus.IDLE
    twin2 = make_twin(twin_id="twin-act")
    twin2.update_learner_activity(LearnerActivityStatus.PAUSED)
    assert twin2.learner_state.activity_status is LearnerActivityStatus.PAUSED


def test_record_misconception_state() -> None:
    twin = make_twin()
    twin.record_misconception_state(
        "misc-x",
        MisconceptionPresence.SUSPECTED,
        related_concept_id=CONCEPT_001,
    )
    assert twin.has_misconception("misc-x")
    twin.record_misconception_state("misc-x", MisconceptionPresence.CLEARED)
    assert (
        twin.misconception_state_for("misc-x").presence is MisconceptionPresence.CLEARED
    )


def test_archive_preserves_history_and_blocks_mutation() -> None:
    twin = make_twin()
    twin.record_evidence("ev-a", EvidenceType.PERFORMANCE)
    twin.record_intervention("int-a")
    twin.archive(note="end-of-sitting")
    assert twin.is_archived()
    assert twin.evidence_count() == 1
    assert twin.intervention_count() == 1
    with pytest.raises(EducationalInvariantViolation):
        twin.record_evidence("ev-b", EvidenceType.REFLECTION)
    with pytest.raises(EducationalInvariantViolation):
        twin.record_intervention("int-b")
    with pytest.raises(EducationalInvariantViolation):
        twin.update_mastery(CONCEPT_001, MasteryState.of(MasteryBand.DEVELOPING))
    with pytest.raises(EducationalInvariantViolation):
        twin.update_retention(RetentionState.of(RetentionBand.STABLE))
    with pytest.raises(EducationalInvariantViolation):
        twin.archive()


def test_archived_twin_cannot_update_confidence() -> None:
    twin = make_archived_twin()
    with pytest.raises(EducationalInvariantViolation):
        twin.update_confidence(ConfidenceProfile.of(ConfidenceLevel.LOW))


def test_create_rejects_mismatched_reconstruction() -> None:
    from domain.education.digital_twin import LearnerState, LearnerStateId

    with pytest.raises(EducationalInvariantViolation):
        EducationalDigitalTwin(
            twin_id=DigitalTwinId("twin-bad"),
            student_id="student-a",
            learner_state=LearnerState(
                learner_state_id=LearnerStateId("ls"),
                student_id="student-b",
            ),
        )


def test_trajectory_grows_with_memory_updates() -> None:
    twin = make_twin()
    start_len = twin.trajectory.length()
    twin.record_evidence("ev-t", EvidenceType.TRANSFER_PROBE)
    twin.record_intervention("int-t")
    twin.update_mastery("c-t", MasteryState.of(MasteryBand.DEVELOPING))
    twin.update_retention(RetentionState.of(RetentionBand.STABLE))
    assert twin.trajectory.length() == start_len + 4


def test_status_enum_and_consistency_after_busy_path() -> None:
    twin = make_twin(twin_id="twin-busy")
    for i in range(5):
        twin.record_evidence(f"ev-{i}", list(EvidenceType)[i % len(EvidenceType)])
        twin.record_intervention(f"int-{i}")
    twin.update_mastery(CONCEPT_001, MasteryState.of(MasteryBand.PROFICIENT))
    assert TwinIsConsistentSpecification().is_satisfied_by(twin)
    assert twin.status is TwinStatus.ACTIVE
