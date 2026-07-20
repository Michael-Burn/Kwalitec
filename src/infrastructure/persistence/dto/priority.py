"""Persistence DTOs for EducationalPriority."""

from __future__ import annotations

from dataclasses import dataclass

from infrastructure.persistence.dto.common import (
    ConceptReferenceDTO,
    LearningObjectiveReferenceDTO,
)


@dataclass(frozen=True, slots=True)
class PriorityDiagnosisReferenceDTO:
    diagnosis_id: str
    diagnosis_type: str


@dataclass(frozen=True, slots=True)
class PriorityHypothesisReferenceDTO:
    hypothesis_id: str


@dataclass(frozen=True, slots=True)
class PriorityScopeDTO:
    scope_id: str
    statement: str
    scope_kind: str
    learning_dimension: str | None
    concept_references: tuple[ConceptReferenceDTO, ...]
    learning_objective_references: tuple[LearningObjectiveReferenceDTO, ...]
    learning_episode_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PriorityFactorDTO:
    factor_id: str
    kind: str
    contribution: float
    rationale: str


@dataclass(frozen=True, slots=True)
class PriorityConstraintDTO:
    constraint_id: str
    kind: str
    statement: str
    related_factor_kind: str | None = None
    max_urgency: str | None = None
    max_score_band: str | None = None


@dataclass(frozen=True, slots=True)
class PriorityScoreDTO:
    band: str
    ratio: float | None = None
    rationale: str | None = None


@dataclass(frozen=True, slots=True)
class UrgencyDTO:
    level: str
    rationale: str | None = None


@dataclass(frozen=True, slots=True)
class InstructionalImpactDTO:
    level: str
    statement: str


@dataclass(frozen=True, slots=True)
class PriorityDTO:
    priority_id: str
    student_id: str
    scope: PriorityScopeDTO
    diagnosis_references: tuple[PriorityDiagnosisReferenceDTO, ...]
    hypothesis_references: tuple[PriorityHypothesisReferenceDTO, ...]
    factors: tuple[PriorityFactorDTO, ...]
    score: PriorityScoreDTO
    urgency: UrgencyDTO
    instructional_impact: InstructionalImpactDTO
    constraints: tuple[PriorityConstraintDTO, ...]
    status: str
    stabilisation_reason: str | None = None
