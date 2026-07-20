"""Map EducationalDiagnosis ↔ DiagnosisDTO."""

from __future__ import annotations

from domain.education.diagnosis import (
    DiagnosisConfidence,
    DiagnosisIndicator,
    DiagnosisIndicatorId,
    DiagnosisReason,
    DiagnosisReasonId,
    DiagnosisScope,
    DiagnosisScopeId,
    DiagnosisSeverity,
    DiagnosisSeverityLevel,
    DiagnosisStatus,
    EducationalDiagnosis,
    EducationalScopeKind,
    IndicatorKind,
    InterpretationReference,
)
from domain.education.foundation.enums import (
    ConfidenceLevel,
    DiagnosisType,
    LearningDimension,
)
from domain.education.foundation.ids import DiagnosisId, EvidenceId, LearningEpisodeId
from infrastructure.persistence.dto.diagnosis import (
    DiagnosisConfidenceDTO,
    DiagnosisDTO,
    DiagnosisIndicatorDTO,
    DiagnosisReasonDTO,
    DiagnosisScopeDTO,
    DiagnosisSeverityDTO,
    InterpretationReferenceDTO,
)
from infrastructure.persistence.mappers.codec import (
    concept_ref_from_dto,
    concept_ref_to_dto,
    enum_value,
    id_value,
    objective_ref_from_dto,
    objective_ref_to_dto,
    optional_enum_value,
    sorted_id_values,
    sorted_strings,
)


class DiagnosisMapper:
    """Pure structural mapper for EducationalDiagnosis."""

    @staticmethod
    def to_persistence(diagnosis: EducationalDiagnosis) -> DiagnosisDTO:
        return DiagnosisDTO(
            diagnosis_id=id_value(diagnosis.diagnosis_id),
            student_id=diagnosis.student_id,
            diagnosis_type=enum_value(diagnosis.diagnosis_type),
            scope=_scope_to_dto(diagnosis.scope),
            confidence=DiagnosisConfidenceDTO(
                level=enum_value(diagnosis.confidence.level),
                ratio=diagnosis.confidence.ratio,
            ),
            severity=DiagnosisSeverityDTO(
                level=enum_value(diagnosis.severity.level),
                rationale=diagnosis.severity.rationale,
            ),
            indicators=tuple(
                _indicator_to_dto(indicator) for indicator in diagnosis.indicators
            ),
            reasons=tuple(_reason_to_dto(reason) for reason in diagnosis.reasons),
            known_evidence_ids=sorted_id_values(diagnosis.known_evidence_ids),
            known_interpretation_ids=sorted_strings(
                diagnosis.known_interpretation_ids
            ),
            interpretation_references=tuple(
                InterpretationReferenceDTO(interpretation_id=ref.interpretation_id)
                for ref in diagnosis.interpretation_references
            ),
            status=enum_value(diagnosis.status),
            invalidation_reason=diagnosis.invalidation_reason,
        )

    @staticmethod
    def to_domain(dto: DiagnosisDTO) -> EducationalDiagnosis:
        return EducationalDiagnosis(
            diagnosis_id=DiagnosisId(dto.diagnosis_id),
            student_id=dto.student_id,
            diagnosis_type=DiagnosisType(dto.diagnosis_type),
            scope=_scope_from_dto(dto.scope),
            confidence=DiagnosisConfidence(
                level=ConfidenceLevel(dto.confidence.level),
                ratio=dto.confidence.ratio,
            ),
            severity=DiagnosisSeverity(
                level=DiagnosisSeverityLevel(dto.severity.level),
                rationale=dto.severity.rationale,
            ),
            indicators=tuple(
                _indicator_from_dto(indicator) for indicator in dto.indicators
            ),
            reasons=tuple(_reason_from_dto(reason) for reason in dto.reasons),
            known_evidence_ids=frozenset(
                EvidenceId(eid) for eid in dto.known_evidence_ids
            ),
            known_interpretation_ids=frozenset(dto.known_interpretation_ids),
            interpretation_references=tuple(
                InterpretationReference(interpretation_id=ref.interpretation_id)
                for ref in dto.interpretation_references
            ),
            status=DiagnosisStatus(dto.status),
            invalidation_reason=dto.invalidation_reason,
        )


def _scope_to_dto(scope: DiagnosisScope) -> DiagnosisScopeDTO:
    return DiagnosisScopeDTO(
        scope_id=id_value(scope.scope_id),
        statement=scope.statement,
        scope_kind=enum_value(scope.scope_kind),
        learning_dimension=optional_enum_value(scope.learning_dimension),
        concept_references=tuple(
            concept_ref_to_dto(ref) for ref in scope.concept_references
        ),
        learning_objective_references=tuple(
            objective_ref_to_dto(ref) for ref in scope.learning_objective_references
        ),
        learning_episode_ids=tuple(
            id_value(eid) for eid in scope.learning_episode_ids
        ),
    )


def _scope_from_dto(dto: DiagnosisScopeDTO) -> DiagnosisScope:
    return DiagnosisScope(
        scope_id=DiagnosisScopeId(dto.scope_id),
        statement=dto.statement,
        scope_kind=EducationalScopeKind(dto.scope_kind),
        learning_dimension=(
            LearningDimension(dto.learning_dimension)
            if dto.learning_dimension is not None
            else None
        ),
        concept_references=tuple(
            concept_ref_from_dto(ref) for ref in dto.concept_references
        ),
        learning_objective_references=tuple(
            objective_ref_from_dto(ref) for ref in dto.learning_objective_references
        ),
        learning_episode_ids=tuple(
            LearningEpisodeId(eid) for eid in dto.learning_episode_ids
        ),
    )


def _indicator_to_dto(indicator: DiagnosisIndicator) -> DiagnosisIndicatorDTO:
    return DiagnosisIndicatorDTO(
        indicator_id=id_value(indicator.indicator_id),
        kind=enum_value(indicator.kind),
        description=indicator.description,
        interpretation_references=tuple(
            InterpretationReferenceDTO(interpretation_id=ref.interpretation_id)
            for ref in indicator.interpretation_references
        ),
        evidence_ids=tuple(id_value(eid) for eid in indicator.evidence_ids),
    )


def _indicator_from_dto(dto: DiagnosisIndicatorDTO) -> DiagnosisIndicator:
    return DiagnosisIndicator(
        indicator_id=DiagnosisIndicatorId(dto.indicator_id),
        kind=IndicatorKind(dto.kind),
        description=dto.description,
        interpretation_references=tuple(
            InterpretationReference(interpretation_id=ref.interpretation_id)
            for ref in dto.interpretation_references
        ),
        evidence_ids=tuple(EvidenceId(eid) for eid in dto.evidence_ids),
    )


def _reason_to_dto(reason: DiagnosisReason) -> DiagnosisReasonDTO:
    return DiagnosisReasonDTO(
        reason_id=id_value(reason.reason_id),
        statement=reason.statement,
        code=reason.code,
    )


def _reason_from_dto(dto: DiagnosisReasonDTO) -> DiagnosisReason:
    return DiagnosisReason(
        reason_id=DiagnosisReasonId(dto.reason_id),
        statement=dto.statement,
        code=dto.code,
    )
