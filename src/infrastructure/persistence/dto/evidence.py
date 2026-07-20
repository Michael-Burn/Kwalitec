"""Persistence DTOs for EvidenceRecord."""

from __future__ import annotations

from dataclasses import dataclass

from infrastructure.persistence.dto.common import (
    ConceptReferenceDTO,
    LearningObjectiveReferenceDTO,
)


@dataclass(frozen=True, slots=True)
class EvidenceItemDTO:
    item_id: str
    kind: str
    observation: str
    concept_id: str | None = None
    learning_episode_id: str | None = None


@dataclass(frozen=True, slots=True)
class EvidenceSourceDTO:
    source_id: str
    kind: str
    label: str
    channel: str | None = None


@dataclass(frozen=True, slots=True)
class EvidenceContextDTO:
    context_id: str
    situation: str
    learning_dimension: str | None
    concept_references: tuple[ConceptReferenceDTO, ...]
    learning_objective_references: tuple[LearningObjectiveReferenceDTO, ...]
    learning_episode_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ConfidenceMeasureDTO:
    level: str
    ratio: float | None = None


@dataclass(frozen=True, slots=True)
class EvidenceStrengthDTO:
    level: str


@dataclass(frozen=True, slots=True)
class EvidenceRecordDTO:
    evidence_id: str
    student_id: str
    items: tuple[EvidenceItemDTO, ...]
    source: EvidenceSourceDTO
    context: EvidenceContextDTO
    confidence: ConfidenceMeasureDTO
    strength: EvidenceStrengthDTO
    timestamp: str
    known_concept_ids: tuple[str, ...]
    known_episode_ids: tuple[str, ...]
    concept_references: tuple[ConceptReferenceDTO, ...]
    learning_episode_ids: tuple[str, ...]
    status: str
    invalidation_reason: str | None = None
