"""Map TeachingIntention ↔ TeachingIntentionDTO."""

from __future__ import annotations

from domain.education.foundation.enums import (
    DiagnosisType,
    LearningDimension,
    TeachingIntentionType,
)
from domain.education.foundation.ids import (
    DiagnosisId,
    HypothesisId,
    PriorityId,
    TeachingIntentionId,
)
from domain.education.teaching_intention import (
    DiagnosisReference,
    ExpectedOutcome,
    HypothesisReference,
    IntentionConstraint,
    IntentionConstraintId,
    IntentionConstraintKind,
    IntentionGoal,
    IntentionGoalId,
    IntentionScope,
    IntentionScopeId,
    IntentionScopeKind,
    IntentionStatus,
    IntentionStrength,
    IntentionStrengthLevel,
    PriorityReference,
    TeachingIntention,
)
from infrastructure.persistence.dto.teaching_intention import (
    ExpectedOutcomeDTO,
    IntentionConstraintDTO,
    IntentionDiagnosisReferenceDTO,
    IntentionGoalDTO,
    IntentionHypothesisReferenceDTO,
    IntentionPriorityReferenceDTO,
    IntentionScopeDTO,
    IntentionStrengthDTO,
    TeachingIntentionDTO,
)
from infrastructure.persistence.mappers.codec import (
    concept_ref_from_dto,
    concept_ref_to_dto,
    enum_value,
    id_value,
    misconception_ref_from_dto,
    misconception_ref_to_dto,
    objective_ref_from_dto,
    objective_ref_to_dto,
    optional_enum_value,
)


class TeachingIntentionMapper:
    """Pure structural mapper for TeachingIntention."""

    @staticmethod
    def to_persistence(intention: TeachingIntention) -> TeachingIntentionDTO:
        return TeachingIntentionDTO(
            intention_id=id_value(intention.intention_id),
            student_id=intention.student_id,
            intention_type=enum_value(intention.intention_type),
            goal=IntentionGoalDTO(
                goal_id=id_value(intention.goal.goal_id),
                statement=intention.goal.statement,
                intention_type=enum_value(intention.goal.intention_type),
                success_evidence_hint=intention.goal.success_evidence_hint,
            ),
            scope=IntentionScopeDTO(
                scope_id=id_value(intention.scope.scope_id),
                statement=intention.scope.statement,
                scope_kind=enum_value(intention.scope.scope_kind),
                learning_dimension=optional_enum_value(
                    intention.scope.learning_dimension
                ),
                concept_references=tuple(
                    concept_ref_to_dto(ref)
                    for ref in intention.scope.concept_references
                ),
                learning_objective_references=tuple(
                    objective_ref_to_dto(ref)
                    for ref in intention.scope.learning_objective_references
                ),
                misconception_references=tuple(
                    misconception_ref_to_dto(ref)
                    for ref in intention.scope.misconception_references
                ),
            ),
            expected_outcome=ExpectedOutcomeDTO(
                statement=intention.expected_outcome.statement,
                success_evidence=intention.expected_outcome.success_evidence,
                evaluable=intention.expected_outcome.evaluable,
            ),
            strength=IntentionStrengthDTO(
                level=enum_value(intention.strength.level),
                rationale=intention.strength.rationale,
            ),
            priority_references=tuple(
                IntentionPriorityReferenceDTO(priority_id=id_value(ref.priority_id))
                for ref in intention.priority_references
            ),
            diagnosis_references=tuple(
                IntentionDiagnosisReferenceDTO(
                    diagnosis_id=id_value(ref.diagnosis_id),
                    diagnosis_type=enum_value(ref.diagnosis_type),
                )
                for ref in intention.diagnosis_references
            ),
            hypothesis_references=tuple(
                IntentionHypothesisReferenceDTO(
                    hypothesis_id=id_value(ref.hypothesis_id)
                )
                for ref in intention.hypothesis_references
            ),
            constraints=tuple(
                IntentionConstraintDTO(
                    constraint_id=id_value(constraint.constraint_id),
                    kind=enum_value(constraint.kind),
                    statement=constraint.statement,
                    forbidden_intention_type=optional_enum_value(
                        constraint.forbidden_intention_type
                    ),
                    max_strength=optional_enum_value(constraint.max_strength),
                )
                for constraint in intention.constraints
            ),
            status=enum_value(intention.status),
            retire_reason=intention.retire_reason,
        )

    @staticmethod
    def to_domain(dto: TeachingIntentionDTO) -> TeachingIntention:
        return TeachingIntention(
            intention_id=TeachingIntentionId(dto.intention_id),
            student_id=dto.student_id,
            intention_type=TeachingIntentionType(dto.intention_type),
            goal=IntentionGoal(
                goal_id=IntentionGoalId(dto.goal.goal_id),
                statement=dto.goal.statement,
                intention_type=TeachingIntentionType(dto.goal.intention_type),
                success_evidence_hint=dto.goal.success_evidence_hint,
            ),
            scope=IntentionScope(
                scope_id=IntentionScopeId(dto.scope.scope_id),
                statement=dto.scope.statement,
                scope_kind=IntentionScopeKind(dto.scope.scope_kind),
                learning_dimension=(
                    LearningDimension(dto.scope.learning_dimension)
                    if dto.scope.learning_dimension is not None
                    else None
                ),
                concept_references=tuple(
                    concept_ref_from_dto(ref) for ref in dto.scope.concept_references
                ),
                learning_objective_references=tuple(
                    objective_ref_from_dto(ref)
                    for ref in dto.scope.learning_objective_references
                ),
                misconception_references=tuple(
                    misconception_ref_from_dto(ref)
                    for ref in dto.scope.misconception_references
                ),
            ),
            expected_outcome=ExpectedOutcome(
                statement=dto.expected_outcome.statement,
                success_evidence=dto.expected_outcome.success_evidence,
                evaluable=dto.expected_outcome.evaluable,
            ),
            strength=IntentionStrength(
                level=IntentionStrengthLevel(dto.strength.level),
                rationale=dto.strength.rationale,
            ),
            priority_references=tuple(
                PriorityReference(priority_id=PriorityId(ref.priority_id))
                for ref in dto.priority_references
            ),
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
            constraints=tuple(
                IntentionConstraint(
                    constraint_id=IntentionConstraintId(constraint.constraint_id),
                    kind=IntentionConstraintKind(constraint.kind),
                    statement=constraint.statement,
                    forbidden_intention_type=(
                        TeachingIntentionType(constraint.forbidden_intention_type)
                        if constraint.forbidden_intention_type is not None
                        else None
                    ),
                    max_strength=(
                        IntentionStrengthLevel(constraint.max_strength)
                        if constraint.max_strength is not None
                        else None
                    ),
                )
                for constraint in dto.constraints
            ),
            status=IntentionStatus(dto.status),
            retire_reason=dto.retire_reason,
        )
