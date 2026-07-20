"""Map TeachingStrategy ↔ TeachingStrategyDTO."""

from __future__ import annotations

from domain.education.foundation.enums import (
    DiagnosisType,
    TeachingIntentionType,
    TeachingStrategyType,
)
from domain.education.foundation.ids import (
    DiagnosisId,
    HypothesisId,
    TeachingIntentionId,
    TeachingStrategyId,
)
from domain.education.teaching_strategy import (
    ComplexityLevel,
    CompositionPattern,
    DiagnosisReference,
    EffectivenessLevel,
    HypothesisReference,
    InstructionalComplexity,
    IntentionReference,
    SecondaryStrategyReference,
    StrategyConstraint,
    StrategyConstraintId,
    StrategyConstraintKind,
    StrategyEffectiveness,
    StrategyGoal,
    StrategyGoalId,
    StrategyRationale,
    StrategyRationaleId,
    StrategyStatus,
    TeachingStrategy,
)
from infrastructure.persistence.dto.teaching_strategy import (
    InstructionalComplexityDTO,
    SecondaryStrategyReferenceDTO,
    StrategyConstraintDTO,
    StrategyDiagnosisReferenceDTO,
    StrategyEffectivenessDTO,
    StrategyGoalDTO,
    StrategyHypothesisReferenceDTO,
    StrategyIntentionReferenceDTO,
    StrategyRationaleDTO,
    TeachingStrategyDTO,
)
from infrastructure.persistence.mappers.codec import (
    enum_value,
    id_value,
    optional_enum_value,
)


class TeachingStrategyMapper:
    """Pure structural mapper for TeachingStrategy."""

    @staticmethod
    def to_persistence(strategy: TeachingStrategy) -> TeachingStrategyDTO:
        return TeachingStrategyDTO(
            strategy_id=id_value(strategy.strategy_id),
            student_id=strategy.student_id,
            primary_strategy=enum_value(strategy.primary_strategy),
            goal=StrategyGoalDTO(
                goal_id=id_value(strategy.goal.goal_id),
                statement=strategy.goal.statement,
                strategy_type=enum_value(strategy.goal.strategy_type),
                expected_evidence_hint=strategy.goal.expected_evidence_hint,
            ),
            rationale=StrategyRationaleDTO(
                rationale_id=id_value(strategy.rationale.rationale_id),
                statement=strategy.rationale.statement,
                diagnosis_link=strategy.rationale.diagnosis_link,
                hypothesis_link=strategy.rationale.hypothesis_link,
                intention_link=strategy.rationale.intention_link,
            ),
            effectiveness=StrategyEffectivenessDTO(
                level=enum_value(strategy.effectiveness.level),
                rationale=strategy.effectiveness.rationale,
            ),
            complexity=InstructionalComplexityDTO(
                level=enum_value(strategy.complexity.level),
                rationale=strategy.complexity.rationale,
            ),
            intention_references=tuple(
                StrategyIntentionReferenceDTO(
                    intention_id=id_value(ref.intention_id),
                    intention_type=enum_value(ref.intention_type),
                )
                for ref in strategy.intention_references
            ),
            diagnosis_references=tuple(
                StrategyDiagnosisReferenceDTO(
                    diagnosis_id=id_value(ref.diagnosis_id),
                    diagnosis_type=enum_value(ref.diagnosis_type),
                )
                for ref in strategy.diagnosis_references
            ),
            hypothesis_references=tuple(
                StrategyHypothesisReferenceDTO(
                    hypothesis_id=id_value(ref.hypothesis_id)
                )
                for ref in strategy.hypothesis_references
            ),
            secondary_strategies=tuple(
                SecondaryStrategyReferenceDTO(
                    strategy_type=enum_value(ref.strategy_type),
                    sequence_order=ref.sequence_order,
                )
                for ref in strategy.secondary_strategies
            ),
            constraints=tuple(
                StrategyConstraintDTO(
                    constraint_id=id_value(constraint.constraint_id),
                    kind=enum_value(constraint.kind),
                    statement=constraint.statement,
                    forbidden_strategy_type=optional_enum_value(
                        constraint.forbidden_strategy_type
                    ),
                    max_complexity=optional_enum_value(constraint.max_complexity),
                )
                for constraint in strategy.constraints
            ),
            composition_pattern=optional_enum_value(strategy.composition_pattern),
            status=enum_value(strategy.status),
            retire_reason=strategy.retire_reason,
        )

    @staticmethod
    def to_domain(dto: TeachingStrategyDTO) -> TeachingStrategy:
        return TeachingStrategy(
            strategy_id=TeachingStrategyId(dto.strategy_id),
            student_id=dto.student_id,
            primary_strategy=TeachingStrategyType(dto.primary_strategy),
            goal=StrategyGoal(
                goal_id=StrategyGoalId(dto.goal.goal_id),
                statement=dto.goal.statement,
                strategy_type=TeachingStrategyType(dto.goal.strategy_type),
                expected_evidence_hint=dto.goal.expected_evidence_hint,
            ),
            rationale=StrategyRationale(
                rationale_id=StrategyRationaleId(dto.rationale.rationale_id),
                statement=dto.rationale.statement,
                diagnosis_link=dto.rationale.diagnosis_link,
                hypothesis_link=dto.rationale.hypothesis_link,
                intention_link=dto.rationale.intention_link,
            ),
            effectiveness=StrategyEffectiveness(
                level=EffectivenessLevel(dto.effectiveness.level),
                rationale=dto.effectiveness.rationale,
            ),
            complexity=InstructionalComplexity(
                level=ComplexityLevel(dto.complexity.level),
                rationale=dto.complexity.rationale,
            ),
            intention_references=tuple(
                IntentionReference(
                    intention_id=TeachingIntentionId(ref.intention_id),
                    intention_type=TeachingIntentionType(ref.intention_type),
                )
                for ref in dto.intention_references
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
            secondary_strategies=tuple(
                SecondaryStrategyReference(
                    strategy_type=TeachingStrategyType(ref.strategy_type),
                    sequence_order=ref.sequence_order,
                )
                for ref in dto.secondary_strategies
            ),
            constraints=tuple(
                StrategyConstraint(
                    constraint_id=StrategyConstraintId(constraint.constraint_id),
                    kind=StrategyConstraintKind(constraint.kind),
                    statement=constraint.statement,
                    forbidden_strategy_type=(
                        TeachingStrategyType(constraint.forbidden_strategy_type)
                        if constraint.forbidden_strategy_type is not None
                        else None
                    ),
                    max_complexity=(
                        ComplexityLevel(constraint.max_complexity)
                        if constraint.max_complexity is not None
                        else None
                    ),
                )
                for constraint in dto.constraints
            ),
            composition_pattern=(
                CompositionPattern(dto.composition_pattern)
                if dto.composition_pattern is not None
                else None
            ),
            status=StrategyStatus(dto.status),
            retire_reason=dto.retire_reason,
        )
