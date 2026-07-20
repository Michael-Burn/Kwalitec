"""Persistence DTOs for EducationalDigitalTwin."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MasteryStateDTO:
    band: str
    ratio: float | None = None


@dataclass(frozen=True, slots=True)
class RetentionStateDTO:
    band: str
    ratio: float | None = None


@dataclass(frozen=True, slots=True)
class ConfidenceProfileDTO:
    overall: str
    ratio: float | None = None


@dataclass(frozen=True, slots=True)
class TrajectoryPointDTO:
    sequence: int
    kind: str
    label: str


@dataclass(frozen=True, slots=True)
class LearningTrajectoryDTO:
    points: tuple[TrajectoryPointDTO, ...]


@dataclass(frozen=True, slots=True)
class LearnerStateDTO:
    learner_state_id: str
    student_id: str
    activity_status: str


@dataclass(frozen=True, slots=True)
class ConceptStateDTO:
    concept_state_id: str
    concept_id: str
    mastery: MasteryStateDTO
    retention: RetentionStateDTO
    evidence_count: int


@dataclass(frozen=True, slots=True)
class MisconceptionStateDTO:
    misconception_state_id: str
    misconception_id: str
    presence: str
    related_concept_id: str | None = None


@dataclass(frozen=True, slots=True)
class EvidenceHistoryEntryDTO:
    entry_id: str
    evidence_id: str
    evidence_type: str
    sequence: int
    concept_id: str | None = None
    note: str | None = None


@dataclass(frozen=True, slots=True)
class InterventionHistoryEntryDTO:
    entry_id: str
    intervention_ref: str
    sequence: int
    strategy_type: str | None = None
    intention_type: str | None = None
    concept_id: str | None = None
    note: str | None = None


@dataclass(frozen=True, slots=True)
class DigitalTwinDTO:
    twin_id: str
    student_id: str
    learner_state: LearnerStateDTO
    concept_states: tuple[ConceptStateDTO, ...]
    misconception_states: tuple[MisconceptionStateDTO, ...]
    evidence_history: tuple[EvidenceHistoryEntryDTO, ...]
    intervention_history: tuple[InterventionHistoryEntryDTO, ...]
    retention: RetentionStateDTO
    confidence: ConfidenceProfileDTO
    trajectory: LearningTrajectoryDTO
    status: str
