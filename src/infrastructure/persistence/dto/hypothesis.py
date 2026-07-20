"""Persistence DTOs for EducationalHypothesis."""

from __future__ import annotations

from dataclasses import dataclass

from infrastructure.persistence.dto.common import (
    ConceptReferenceDTO,
    LearningObjectiveReferenceDTO,
)


@dataclass(frozen=True, slots=True)
class HypothesisDiagnosisReferenceDTO:
    diagnosis_id: str
    diagnosis_type: str


@dataclass(frozen=True, slots=True)
class HypothesisInterpretationReferenceDTO:
    interpretation_id: str


@dataclass(frozen=True, slots=True)
class HypothesisScopeDTO:
    scope_id: str
    statement: str
    scope_kind: str
    learning_dimension: str | None
    concept_references: tuple[ConceptReferenceDTO, ...]
    learning_objective_references: tuple[LearningObjectiveReferenceDTO, ...]
    learning_episode_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PlausibilityDTO:
    level: str
    ratio: float | None = None


@dataclass(frozen=True, slots=True)
class ExplanatoryStrengthDTO:
    level: str


@dataclass(frozen=True, slots=True)
class HypothesisReasonDTO:
    reason_id: str
    statement: str
    code: str | None
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CompetingHypothesisDTO:
    competing_id: str
    hypothesis_kind: str
    explanation: str
    plausibility: PlausibilityDTO | None = None


@dataclass(frozen=True, slots=True)
class HypothesisDTO:
    hypothesis_id: str
    student_id: str
    hypothesis_kind: str
    explanation: str
    scope: HypothesisScopeDTO
    plausibility: PlausibilityDTO
    explanatory_strength: ExplanatoryStrengthDTO
    diagnosis_references: tuple[HypothesisDiagnosisReferenceDTO, ...]
    reasons: tuple[HypothesisReasonDTO, ...]
    interpretation_references: tuple[HypothesisInterpretationReferenceDTO, ...]
    evidence_ids: tuple[str, ...]
    competing_hypotheses: tuple[CompetingHypothesisDTO, ...]
    known_evidence_ids: tuple[str, ...]
    known_interpretation_ids: tuple[str, ...]
    status: str
    discard_reason: str | None = None
