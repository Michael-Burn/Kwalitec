"""Map EducationalPriority ↔ PriorityDTO."""

from __future__ import annotations

from domain.education.foundation.enums import DiagnosisType, LearningDimension
from domain.education.foundation.ids import (
    DiagnosisId,
    HypothesisId,
    LearningEpisodeId,
    PriorityId,
)
from domain.education.priority import (
    DiagnosisReference,
    EducationalPriority,
    HypothesisReference,
    InstructionalImpact,
    InstructionalImpactLevel,
    PriorityConstraint,
    PriorityConstraintId,
    PriorityConstraintKind,
    PriorityFactor,
    PriorityFactorId,
    PriorityFactorKind,
    PriorityScope,
    PriorityScopeId,
    PriorityScopeKind,
    PriorityScore,
    PriorityScoreBand,
    PriorityStatus,
    Urgency,
    UrgencyLevel,
)
from infrastructure.persistence.dto.priority import (
    InstructionalImpactDTO,
    PriorityConstraintDTO,
    PriorityDiagnosisReferenceDTO,
    PriorityDTO,
    PriorityFactorDTO,
    PriorityHypothesisReferenceDTO,
    PriorityScopeDTO,
    PriorityScoreDTO,
    UrgencyDTO,
)
from infrastructure.persistence.mappers.codec import (
    concept_ref_from_dto,
    concept_ref_to_dto,
    enum_value,
    id_value,
    objective_ref_from_dto,
    objective_ref_to_dto,
    optional_enum_value,
)


class PriorityMapper:
    """Pure structural mapper for EducationalPriority."""

    @staticmethod
    def to_persistence(priority: EducationalPriority) -> PriorityDTO:
        return PriorityDTO(
            priority_id=id_value(priority.priority_id),
            student_id=priority.student_id,
            scope=_scope_to_dto(priority.scope),
            diagnosis_references=tuple(
                PriorityDiagnosisReferenceDTO(
                    diagnosis_id=id_value(ref.diagnosis_id),
                    diagnosis_type=enum_value(ref.diagnosis_type),
                )
                for ref in priority.diagnosis_references
            ),
            hypothesis_references=tuple(
                PriorityHypothesisReferenceDTO(
                    hypothesis_id=id_value(ref.hypothesis_id)
                )
                for ref in priority.hypothesis_references
            ),
            factors=tuple(_factor_to_dto(factor) for factor in priority.factors),
            score=PriorityScoreDTO(
                band=enum_value(priority.score.band),
                ratio=priority.score.ratio,
                rationale=priority.score.rationale,
            ),
            urgency=UrgencyDTO(
                level=enum_value(priority.urgency.level),
                rationale=priority.urgency.rationale,
            ),
            instructional_impact=InstructionalImpactDTO(
                level=enum_value(priority.instructional_impact.level),
                statement=priority.instructional_impact.statement,
            ),
            constraints=tuple(
                _constraint_to_dto(constraint) for constraint in priority.constraints
            ),
            status=enum_value(priority.status),
            stabilisation_reason=priority.stabilisation_reason,
        )

    @staticmethod
    def to_domain(dto: PriorityDTO) -> EducationalPriority:
        return EducationalPriority(
            priority_id=PriorityId(dto.priority_id),
            student_id=dto.student_id,
            scope=_scope_from_dto(dto.scope),
            diagnosis_references=tuple(
                DiagnosisReference(
                    diagnosis_id=DiagnosisId(ref.diagnosis_id),
                    diagnosis_type=DiagnosisType(ref.diagnosis_type),
                )
                for ref in dto.diagnosis_references
            ),
            hypothesis_references=tuple(
                HypothesisReference(hypothesis_id=HypothesisId(ref.hypothesis_id))
                for ref in dto.hypothesis_references
            ),
            factors=tuple(_factor_from_dto(factor) for factor in dto.factors),
            score=PriorityScore(
                band=PriorityScoreBand(dto.score.band),
                ratio=dto.score.ratio,
                rationale=dto.score.rationale,
            ),
            urgency=Urgency(
                level=UrgencyLevel(dto.urgency.level),
                rationale=dto.urgency.rationale,
            ),
            instructional_impact=InstructionalImpact(
                level=InstructionalImpactLevel(dto.instructional_impact.level),
                statement=dto.instructional_impact.statement,
            ),
            constraints=tuple(
                _constraint_from_dto(constraint) for constraint in dto.constraints
            ),
            status=PriorityStatus(dto.status),
            stabilisation_reason=dto.stabilisation_reason,
        )


def _scope_to_dto(scope: PriorityScope) -> PriorityScopeDTO:
    return PriorityScopeDTO(
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


def _scope_from_dto(dto: PriorityScopeDTO) -> PriorityScope:
    return PriorityScope(
        scope_id=PriorityScopeId(dto.scope_id),
        statement=dto.statement,
        scope_kind=PriorityScopeKind(dto.scope_kind),
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


def _factor_to_dto(factor: PriorityFactor) -> PriorityFactorDTO:
    return PriorityFactorDTO(
        factor_id=id_value(factor.factor_id),
        kind=enum_value(factor.kind),
        contribution=factor.contribution,
        rationale=factor.rationale,
    )


def _factor_from_dto(dto: PriorityFactorDTO) -> PriorityFactor:
    return PriorityFactor(
        factor_id=PriorityFactorId(dto.factor_id),
        kind=PriorityFactorKind(dto.kind),
        contribution=dto.contribution,
        rationale=dto.rationale,
    )


def _constraint_to_dto(constraint: PriorityConstraint) -> PriorityConstraintDTO:
    return PriorityConstraintDTO(
        constraint_id=id_value(constraint.constraint_id),
        kind=enum_value(constraint.kind),
        statement=constraint.statement,
        related_factor_kind=optional_enum_value(constraint.related_factor_kind),
        max_urgency=optional_enum_value(constraint.max_urgency),
        max_score_band=optional_enum_value(constraint.max_score_band),
    )


def _constraint_from_dto(dto: PriorityConstraintDTO) -> PriorityConstraint:
    return PriorityConstraint(
        constraint_id=PriorityConstraintId(dto.constraint_id),
        kind=PriorityConstraintKind(dto.kind),
        statement=dto.statement,
        related_factor_kind=(
            PriorityFactorKind(dto.related_factor_kind)
            if dto.related_factor_kind is not None
            else None
        ),
        max_urgency=(
            UrgencyLevel(dto.max_urgency) if dto.max_urgency is not None else None
        ),
        max_score_band=(
            PriorityScoreBand(dto.max_score_band)
            if dto.max_score_band is not None
            else None
        ),
    )
