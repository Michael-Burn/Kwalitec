"""Map EducationalHypothesis ↔ HypothesisDTO."""

from __future__ import annotations

from domain.education.foundation.enums import DiagnosisType, LearningDimension
from domain.education.foundation.ids import (
    DiagnosisId,
    EvidenceId,
    HypothesisId,
    LearningEpisodeId,
)
from domain.education.hypothesis import (
    CompetingHypothesis,
    CompetingHypothesisId,
    DiagnosisReference,
    EducationalHypothesis,
    ExplanatoryStrength,
    ExplanatoryStrengthLevel,
    HypothesisKind,
    HypothesisReason,
    HypothesisReasonId,
    HypothesisScope,
    HypothesisScopeId,
    HypothesisScopeKind,
    HypothesisStatus,
    InterpretationReference,
    Plausibility,
    PlausibilityLevel,
)
from infrastructure.persistence.dto.hypothesis import (
    CompetingHypothesisDTO,
    ExplanatoryStrengthDTO,
    HypothesisDiagnosisReferenceDTO,
    HypothesisDTO,
    HypothesisInterpretationReferenceDTO,
    HypothesisReasonDTO,
    HypothesisScopeDTO,
    PlausibilityDTO,
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


class HypothesisMapper:
    """Pure structural mapper for EducationalHypothesis."""

    @staticmethod
    def to_persistence(hypothesis: EducationalHypothesis) -> HypothesisDTO:
        return HypothesisDTO(
            hypothesis_id=id_value(hypothesis.hypothesis_id),
            student_id=hypothesis.student_id,
            hypothesis_kind=enum_value(hypothesis.hypothesis_kind),
            explanation=hypothesis.explanation,
            scope=_scope_to_dto(hypothesis.scope),
            plausibility=PlausibilityDTO(
                level=enum_value(hypothesis.plausibility.level),
                ratio=hypothesis.plausibility.ratio,
            ),
            explanatory_strength=ExplanatoryStrengthDTO(
                level=enum_value(hypothesis.explanatory_strength.level)
            ),
            diagnosis_references=tuple(
                HypothesisDiagnosisReferenceDTO(
                    diagnosis_id=id_value(ref.diagnosis_id),
                    diagnosis_type=enum_value(ref.diagnosis_type),
                )
                for ref in hypothesis.diagnosis_references
            ),
            reasons=tuple(_reason_to_dto(reason) for reason in hypothesis.reasons),
            interpretation_references=tuple(
                HypothesisInterpretationReferenceDTO(
                    interpretation_id=ref.interpretation_id
                )
                for ref in hypothesis.interpretation_references
            ),
            evidence_ids=tuple(id_value(eid) for eid in hypothesis.evidence_ids),
            competing_hypotheses=tuple(
                _competitor_to_dto(item) for item in hypothesis.competing_hypotheses
            ),
            known_evidence_ids=sorted_id_values(hypothesis.known_evidence_ids),
            known_interpretation_ids=sorted_strings(
                hypothesis.known_interpretation_ids
            ),
            status=enum_value(hypothesis.status),
            discard_reason=hypothesis.discard_reason,
        )

    @staticmethod
    def to_domain(dto: HypothesisDTO) -> EducationalHypothesis:
        return EducationalHypothesis(
            hypothesis_id=HypothesisId(dto.hypothesis_id),
            student_id=dto.student_id,
            hypothesis_kind=HypothesisKind(dto.hypothesis_kind),
            explanation=dto.explanation,
            scope=_scope_from_dto(dto.scope),
            plausibility=Plausibility(
                level=PlausibilityLevel(dto.plausibility.level),
                ratio=dto.plausibility.ratio,
            ),
            explanatory_strength=ExplanatoryStrength(
                level=ExplanatoryStrengthLevel(dto.explanatory_strength.level)
            ),
            diagnosis_references=tuple(
                DiagnosisReference(
                    diagnosis_id=DiagnosisId(ref.diagnosis_id),
                    diagnosis_type=DiagnosisType(ref.diagnosis_type),
                )
                for ref in dto.diagnosis_references
            ),
            reasons=tuple(_reason_from_dto(reason) for reason in dto.reasons),
            interpretation_references=tuple(
                InterpretationReference(interpretation_id=ref.interpretation_id)
                for ref in dto.interpretation_references
            ),
            evidence_ids=tuple(EvidenceId(eid) for eid in dto.evidence_ids),
            competing_hypotheses=tuple(
                _competitor_from_dto(item) for item in dto.competing_hypotheses
            ),
            known_evidence_ids=frozenset(
                EvidenceId(eid) for eid in dto.known_evidence_ids
            ),
            known_interpretation_ids=frozenset(dto.known_interpretation_ids),
            status=HypothesisStatus(dto.status),
            discard_reason=dto.discard_reason,
        )


def _scope_to_dto(scope: HypothesisScope) -> HypothesisScopeDTO:
    return HypothesisScopeDTO(
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


def _scope_from_dto(dto: HypothesisScopeDTO) -> HypothesisScope:
    return HypothesisScope(
        scope_id=HypothesisScopeId(dto.scope_id),
        statement=dto.statement,
        scope_kind=HypothesisScopeKind(dto.scope_kind),
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


def _reason_to_dto(reason: HypothesisReason) -> HypothesisReasonDTO:
    return HypothesisReasonDTO(
        reason_id=id_value(reason.reason_id),
        statement=reason.statement,
        code=reason.code,
        evidence_ids=tuple(id_value(eid) for eid in reason.evidence_ids),
    )


def _reason_from_dto(dto: HypothesisReasonDTO) -> HypothesisReason:
    return HypothesisReason(
        reason_id=HypothesisReasonId(dto.reason_id),
        statement=dto.statement,
        code=dto.code,
        evidence_ids=tuple(EvidenceId(eid) for eid in dto.evidence_ids),
    )


def _competitor_to_dto(item: CompetingHypothesis) -> CompetingHypothesisDTO:
    plausibility = None
    if item.plausibility is not None:
        plausibility = PlausibilityDTO(
            level=enum_value(item.plausibility.level),
            ratio=item.plausibility.ratio,
        )
    return CompetingHypothesisDTO(
        competing_id=id_value(item.competing_id),
        hypothesis_kind=enum_value(item.hypothesis_kind),
        explanation=item.explanation,
        plausibility=plausibility,
    )


def _competitor_from_dto(dto: CompetingHypothesisDTO) -> CompetingHypothesis:
    plausibility = None
    if dto.plausibility is not None:
        plausibility = Plausibility(
            level=PlausibilityLevel(dto.plausibility.level),
            ratio=dto.plausibility.ratio,
        )
    return CompetingHypothesis(
        competing_id=CompetingHypothesisId(dto.competing_id),
        hypothesis_kind=HypothesisKind(dto.hypothesis_kind),
        explanation=dto.explanation,
        plausibility=plausibility,
    )
