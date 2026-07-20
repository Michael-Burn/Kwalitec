"""Map EducationalDecision ↔ DecisionDTO."""

from __future__ import annotations

from domain.education.decision import (
    DecisionConfidence,
    DecisionOutcome,
    DecisionReason,
    DecisionReasonId,
    DecisionStatus,
    EducationalDecision,
    ExecutionConstraint,
    ExecutionConstraintId,
    ExecutionConstraintKind,
    IntentionReference,
    PriorityReference,
    ReadinessBand,
    ReadinessIndicator,
    ReadinessIndicatorId,
    ReadinessIndicatorKind,
    ReadinessLevel,
    StrategyReference,
)
from domain.education.foundation.enums import (
    ConfidenceLevel,
    TeachingIntentionType,
    TeachingStrategyType,
)
from domain.education.foundation.ids import (
    DecisionId,
    PriorityId,
    TeachingIntentionId,
    TeachingStrategyId,
)
from infrastructure.persistence.dto.decision import (
    DecisionConfidenceDTO,
    DecisionDTO,
    DecisionIntentionReferenceDTO,
    DecisionPriorityReferenceDTO,
    DecisionReasonDTO,
    DecisionStrategyReferenceDTO,
    ExecutionConstraintDTO,
    ReadinessIndicatorDTO,
    ReadinessLevelDTO,
)
from infrastructure.persistence.mappers.codec import (
    enum_value,
    id_value,
    optional_enum_value,
)


class DecisionMapper:
    """Pure structural mapper for EducationalDecision."""

    @staticmethod
    def to_persistence(decision: EducationalDecision) -> DecisionDTO:
        return DecisionDTO(
            decision_id=id_value(decision.decision_id),
            student_id=decision.student_id,
            priority_references=tuple(
                DecisionPriorityReferenceDTO(priority_id=id_value(ref.priority_id))
                for ref in decision.priority_references
            ),
            intention_references=tuple(
                DecisionIntentionReferenceDTO(
                    intention_id=id_value(ref.intention_id),
                    intention_type=enum_value(ref.intention_type),
                )
                for ref in decision.intention_references
            ),
            strategy_references=tuple(
                DecisionStrategyReferenceDTO(
                    strategy_id=id_value(ref.strategy_id),
                    strategy_type=enum_value(ref.strategy_type),
                )
                for ref in decision.strategy_references
            ),
            indicators=tuple(
                ReadinessIndicatorDTO(
                    indicator_id=id_value(indicator.indicator_id),
                    kind=enum_value(indicator.kind),
                    description=indicator.description,
                    supports_readiness=indicator.supports_readiness,
                    weight=indicator.weight,
                )
                for indicator in decision.indicators
            ),
            constraints=tuple(
                ExecutionConstraintDTO(
                    constraint_id=id_value(constraint.constraint_id),
                    kind=enum_value(constraint.kind),
                    statement=constraint.statement,
                    related_indicator_kind=optional_enum_value(
                        constraint.related_indicator_kind
                    ),
                    min_readiness=optional_enum_value(constraint.min_readiness),
                    min_confidence=optional_enum_value(constraint.min_confidence),
                    forbidden_outcome=optional_enum_value(
                        constraint.forbidden_outcome
                    ),
                )
                for constraint in decision.constraints
            ),
            reasons=tuple(
                DecisionReasonDTO(
                    reason_id=id_value(reason.reason_id),
                    statement=reason.statement,
                    code=reason.code,
                )
                for reason in decision.reasons
            ),
            confidence=DecisionConfidenceDTO(
                level=enum_value(decision.confidence.level),
                ratio=decision.confidence.ratio,
            ),
            readiness=ReadinessLevelDTO(
                band=enum_value(decision.readiness.band),
                ratio=decision.readiness.ratio,
                rationale=decision.readiness.rationale,
            ),
            status=enum_value(decision.status),
            outcome=optional_enum_value(decision.outcome),
            reconsideration_reason=decision.reconsideration_reason,
        )

    @staticmethod
    def to_domain(dto: DecisionDTO) -> EducationalDecision:
        return EducationalDecision(
            decision_id=DecisionId(dto.decision_id),
            student_id=dto.student_id,
            priority_references=tuple(
                PriorityReference(priority_id=PriorityId(ref.priority_id))
                for ref in dto.priority_references
            ),
            intention_references=tuple(
                IntentionReference(
                    intention_id=TeachingIntentionId(ref.intention_id),
                    intention_type=TeachingIntentionType(ref.intention_type),
                )
                for ref in dto.intention_references
            ),
            strategy_references=tuple(
                StrategyReference(
                    strategy_id=TeachingStrategyId(ref.strategy_id),
                    strategy_type=TeachingStrategyType(ref.strategy_type),
                )
                for ref in dto.strategy_references
            ),
            indicators=tuple(
                ReadinessIndicator(
                    indicator_id=ReadinessIndicatorId(indicator.indicator_id),
                    kind=ReadinessIndicatorKind(indicator.kind),
                    description=indicator.description,
                    supports_readiness=indicator.supports_readiness,
                    weight=indicator.weight,
                )
                for indicator in dto.indicators
            ),
            constraints=tuple(
                ExecutionConstraint(
                    constraint_id=ExecutionConstraintId(constraint.constraint_id),
                    kind=ExecutionConstraintKind(constraint.kind),
                    statement=constraint.statement,
                    related_indicator_kind=(
                        ReadinessIndicatorKind(constraint.related_indicator_kind)
                        if constraint.related_indicator_kind is not None
                        else None
                    ),
                    min_readiness=(
                        ReadinessBand(constraint.min_readiness)
                        if constraint.min_readiness is not None
                        else None
                    ),
                    min_confidence=(
                        ConfidenceLevel(constraint.min_confidence)
                        if constraint.min_confidence is not None
                        else None
                    ),
                    forbidden_outcome=(
                        DecisionOutcome(constraint.forbidden_outcome)
                        if constraint.forbidden_outcome is not None
                        else None
                    ),
                )
                for constraint in dto.constraints
            ),
            reasons=tuple(
                DecisionReason(
                    reason_id=DecisionReasonId(reason.reason_id),
                    statement=reason.statement,
                    code=reason.code,
                )
                for reason in dto.reasons
            ),
            confidence=DecisionConfidence(
                level=ConfidenceLevel(dto.confidence.level),
                ratio=dto.confidence.ratio,
            ),
            readiness=ReadinessLevel(
                band=ReadinessBand(dto.readiness.band),
                ratio=dto.readiness.ratio,
                rationale=dto.readiness.rationale,
            ),
            status=DecisionStatus(dto.status),
            outcome=(
                DecisionOutcome(dto.outcome) if dto.outcome is not None else None
            ),
            reconsideration_reason=dto.reconsideration_reason,
        )
