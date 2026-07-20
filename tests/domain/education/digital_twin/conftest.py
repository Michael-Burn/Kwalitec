"""Shared factories for Educational Digital Twin domain tests."""

from __future__ import annotations

import pytest

from domain.education.digital_twin import (
    ConceptState,
    ConceptStateId,
    ConfidenceProfile,
    EducationalDigitalTwin,
    EvidenceHistoryEntry,
    EvidenceHistoryEntryId,
    InterventionHistoryEntry,
    InterventionHistoryEntryId,
    LearnerActivityStatus,
    LearnerState,
    LearnerStateId,
    LearningTrajectory,
    MasteryBand,
    MasteryState,
    MisconceptionPresence,
    MisconceptionState,
    MisconceptionStateId,
    RetentionBand,
    RetentionState,
    TrajectoryPoint,
    TrajectoryPointKind,
    TwinStatus,
)
from domain.education.foundation.enums import (
    ConfidenceLevel,
    EvidenceType,
    TeachingIntentionType,
    TeachingStrategyType,
)
from domain.education.foundation.ids import (
    ConceptId,
    DigitalTwinId,
    EvidenceId,
    MisconceptionId,
)

CONCEPT_001 = ConceptId("concept-001")
CONCEPT_002 = ConceptId("concept-002")
MISCONCEPTION_001 = MisconceptionId("misc-001")
EVIDENCE_001 = EvidenceId("evidence-001")

DEFAULT_STRATEGY = TeachingStrategyType.DIRECT_EXPLANATION
DEFAULT_INTENTION = TeachingIntentionType.CONSOLIDATE_UNDERSTANDING


@pytest.fixture
def twin_id() -> DigitalTwinId:
    return DigitalTwinId("twin-001")


@pytest.fixture
def student_id() -> str:
    return "student-ada"


def make_mastery(
    band: MasteryBand = MasteryBand.DEVELOPING,
    *,
    ratio: float | None = 0.55,
) -> MasteryState:
    return MasteryState.of(band, ratio=ratio)


def make_retention(
    band: RetentionBand = RetentionBand.STABLE,
    *,
    ratio: float | None = 0.7,
) -> RetentionState:
    return RetentionState.of(band, ratio=ratio)


def make_confidence(
    overall: ConfidenceLevel = ConfidenceLevel.MEDIUM,
    *,
    ratio: float | None = 0.6,
) -> ConfidenceProfile:
    return ConfidenceProfile.of(overall, ratio=ratio)


def make_learner_state(
    *,
    learner_state_id: str = "learner-001",
    student_id: str = "student-ada",
    activity_status: LearnerActivityStatus = LearnerActivityStatus.ENGAGED,
) -> LearnerState:
    return LearnerState(
        learner_state_id=LearnerStateId(learner_state_id),
        student_id=student_id,
        activity_status=activity_status,
    )


def make_concept_state(
    *,
    concept_state_id: str = "cs-001",
    concept_id: ConceptId | str = CONCEPT_001,
    mastery: MasteryState | None = None,
    retention: RetentionState | None = None,
    evidence_count: int = 0,
) -> ConceptState:
    if isinstance(concept_id, str):
        concept_id = ConceptId(concept_id)
    return ConceptState(
        concept_state_id=ConceptStateId(concept_state_id),
        concept_id=concept_id,
        mastery=mastery or make_mastery(),
        retention=retention or make_retention(),
        evidence_count=evidence_count,
    )


def make_misconception_state(
    *,
    misconception_state_id: str = "ms-001",
    misconception_id: MisconceptionId | str = MISCONCEPTION_001,
    presence: MisconceptionPresence = MisconceptionPresence.ACTIVE,
    related_concept_id: ConceptId | str | None = CONCEPT_001,
) -> MisconceptionState:
    if isinstance(misconception_id, str):
        misconception_id = MisconceptionId(misconception_id)
    rid: ConceptId | None
    if related_concept_id is None:
        rid = None
    elif isinstance(related_concept_id, ConceptId):
        rid = related_concept_id
    else:
        rid = ConceptId(related_concept_id)
    return MisconceptionState(
        misconception_state_id=MisconceptionStateId(misconception_state_id),
        misconception_id=misconception_id,
        presence=presence,
        related_concept_id=rid,
    )


def make_evidence_entry(
    *,
    entry_id: str = "eh-001",
    evidence_id: EvidenceId | str = EVIDENCE_001,
    evidence_type: EvidenceType = EvidenceType.PERFORMANCE,
    sequence: int = 1,
    concept_id: ConceptId | str | None = CONCEPT_001,
    note: str | None = None,
) -> EvidenceHistoryEntry:
    if isinstance(evidence_id, str):
        evidence_id = EvidenceId(evidence_id)
    cid: ConceptId | None
    if concept_id is None:
        cid = None
    elif isinstance(concept_id, ConceptId):
        cid = concept_id
    else:
        cid = ConceptId(concept_id)
    return EvidenceHistoryEntry(
        entry_id=EvidenceHistoryEntryId(entry_id),
        evidence_id=evidence_id,
        evidence_type=evidence_type,
        sequence=sequence,
        concept_id=cid,
        note=note,
    )


def make_intervention_entry(
    *,
    entry_id: str = "ih-001",
    intervention_ref: str = "intervention-001",
    sequence: int = 1,
    strategy_type: TeachingStrategyType | None = DEFAULT_STRATEGY,
    intention_type: TeachingIntentionType | None = DEFAULT_INTENTION,
    concept_id: ConceptId | str | None = CONCEPT_001,
    note: str | None = None,
) -> InterventionHistoryEntry:
    cid: ConceptId | None
    if concept_id is None:
        cid = None
    elif isinstance(concept_id, ConceptId):
        cid = concept_id
    else:
        cid = ConceptId(concept_id)
    return InterventionHistoryEntry(
        entry_id=InterventionHistoryEntryId(entry_id),
        intervention_ref=intervention_ref,
        sequence=sequence,
        strategy_type=strategy_type,
        intention_type=intention_type,
        concept_id=cid,
        note=note,
    )


def make_trajectory(*labels: str) -> LearningTrajectory:
    points = [
        TrajectoryPoint(
            sequence=i + 1,
            kind=(
                TrajectoryPointKind.CREATED
                if i == 0
                else TrajectoryPointKind.EVIDENCE
            ),
            label=label,
        )
        for i, label in enumerate(labels or ("twin-created",))
    ]
    return LearningTrajectory.of(*points)


def make_twin(
    *,
    twin_id: DigitalTwinId | str = "twin-001",
    student_id: str = "student-ada",
    activity_status: LearnerActivityStatus = LearnerActivityStatus.ENGAGED,
    retention: RetentionState | None = None,
    confidence: ConfidenceProfile | None = None,
    pull_created: bool = True,
) -> EducationalDigitalTwin:
    if isinstance(twin_id, str):
        twin_id = DigitalTwinId(twin_id)
    twin = EducationalDigitalTwin.create(
        twin_id=twin_id,
        student_id=student_id,
        activity_status=activity_status,
        retention=retention,
        confidence=confidence,
    )
    if pull_created:
        twin.pull_events()
    return twin


def make_archived_twin(**kwargs) -> EducationalDigitalTwin:
    twin = make_twin(**kwargs)
    twin.archive()
    twin.pull_events()
    assert twin.status is TwinStatus.ARCHIVED
    return twin
