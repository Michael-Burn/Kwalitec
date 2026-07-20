"""Persistence DTOs for EducationalDiagnosis."""

from __future__ import annotations

from dataclasses import dataclass

from infrastructure.persistence.dto.common import (
    ConceptReferenceDTO,
    LearningObjectiveReferenceDTO,
)


@dataclass(frozen=True, slots=True)
class InterpretationReferenceDTO:
    interpretation_id: str


@dataclass(frozen=True, slots=True)
class DiagnosisScopeDTO:
    scope_id: str
    statement: str
    scope_kind: str
    learning_dimension: str | None
    concept_references: tuple[ConceptReferenceDTO, ...]
    learning_objective_references: tuple[LearningObjectiveReferenceDTO, ...]
    learning_episode_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DiagnosisIndicatorDTO:
    indicator_id: str
    kind: str
    description: str
    interpretation_references: tuple[InterpretationReferenceDTO, ...]
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DiagnosisReasonDTO:
    reason_id: str
    statement: str
    code: str | None = None


@dataclass(frozen=True, slots=True)
class DiagnosisConfidenceDTO:
    level: str
    ratio: float | None = None


@dataclass(frozen=True, slots=True)
class DiagnosisSeverityDTO:
    level: str
    rationale: str | None = None


@dataclass(frozen=True, slots=True)
class DiagnosisDTO:
    diagnosis_id: str
    student_id: str
    diagnosis_type: str
    scope: DiagnosisScopeDTO
    confidence: DiagnosisConfidenceDTO
    severity: DiagnosisSeverityDTO
    indicators: tuple[DiagnosisIndicatorDTO, ...]
    reasons: tuple[DiagnosisReasonDTO, ...]
    known_evidence_ids: tuple[str, ...]
    known_interpretation_ids: tuple[str, ...]
    interpretation_references: tuple[InterpretationReferenceDTO, ...]
    status: str
    invalidation_reason: str | None = None
