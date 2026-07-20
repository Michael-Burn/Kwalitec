"""Persistence DTOs for TeachingIntention."""

from __future__ import annotations

from dataclasses import dataclass

from infrastructure.persistence.dto.common import (
    ConceptReferenceDTO,
    LearningObjectiveReferenceDTO,
    MisconceptionReferenceDTO,
)


@dataclass(frozen=True, slots=True)
class IntentionPriorityReferenceDTO:
    priority_id: str


@dataclass(frozen=True, slots=True)
class IntentionDiagnosisReferenceDTO:
    diagnosis_id: str
    diagnosis_type: str


@dataclass(frozen=True, slots=True)
class IntentionHypothesisReferenceDTO:
    hypothesis_id: str


@dataclass(frozen=True, slots=True)
class IntentionGoalDTO:
    goal_id: str
    statement: str
    intention_type: str
    success_evidence_hint: str | None = None


@dataclass(frozen=True, slots=True)
class IntentionScopeDTO:
    scope_id: str
    statement: str
    scope_kind: str
    learning_dimension: str | None
    concept_references: tuple[ConceptReferenceDTO, ...]
    learning_objective_references: tuple[LearningObjectiveReferenceDTO, ...]
    misconception_references: tuple[MisconceptionReferenceDTO, ...]


@dataclass(frozen=True, slots=True)
class ExpectedOutcomeDTO:
    statement: str
    success_evidence: str
    evaluable: bool = True


@dataclass(frozen=True, slots=True)
class IntentionStrengthDTO:
    level: str
    rationale: str | None = None


@dataclass(frozen=True, slots=True)
class IntentionConstraintDTO:
    constraint_id: str
    kind: str
    statement: str
    forbidden_intention_type: str | None = None
    max_strength: str | None = None


@dataclass(frozen=True, slots=True)
class TeachingIntentionDTO:
    intention_id: str
    student_id: str
    intention_type: str
    goal: IntentionGoalDTO
    scope: IntentionScopeDTO
    expected_outcome: ExpectedOutcomeDTO
    strength: IntentionStrengthDTO
    priority_references: tuple[IntentionPriorityReferenceDTO, ...]
    diagnosis_references: tuple[IntentionDiagnosisReferenceDTO, ...]
    hypothesis_references: tuple[IntentionHypothesisReferenceDTO, ...]
    constraints: tuple[IntentionConstraintDTO, ...]
    status: str
    retire_reason: str | None = None
