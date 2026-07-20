"""Shared factories for Educational Decision domain tests."""

from __future__ import annotations

import pytest

from domain.education.decision import (
    DecisionConfidence,
    DecisionOutcome,
    DecisionReason,
    DecisionReasonId,
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

PRIORITY_001 = PriorityId("prio-001")
PRIORITY_002 = PriorityId("prio-002")
INTENTION_001 = TeachingIntentionId("intention-001")
INTENTION_002 = TeachingIntentionId("intention-002")
STRATEGY_001 = TeachingStrategyId("strategy-001")
STRATEGY_002 = TeachingStrategyId("strategy-002")

DEFAULT_INTENTION = TeachingIntentionType.STRENGTHEN_PREREQUISITE
DEFAULT_STRATEGY = TeachingStrategyType.DIRECT_EXPLANATION

READY_INDICATOR_KINDS = (
    ReadinessIndicatorKind.PREREQUISITE_SATISFIED,
    ReadinessIndicatorKind.EVIDENCE_SUFFICIENT,
    ReadinessIndicatorKind.CAPACITY_ADEQUATE,
    ReadinessIndicatorKind.INTENTION_ALIGNED,
    ReadinessIndicatorKind.STRATEGY_APPLICABLE,
)


@pytest.fixture
def decision_id() -> DecisionId:
    return DecisionId("dec-001")


@pytest.fixture
def student_id() -> str:
    return "student-ada"


def make_confidence(
    level: ConfidenceLevel = ConfidenceLevel.HIGH,
    *,
    ratio: float | None = 0.8,
) -> DecisionConfidence:
    return DecisionConfidence.of(level, ratio=ratio)


def make_readiness(
    band: ReadinessBand = ReadinessBand.READY,
    *,
    ratio: float | None = 0.9,
    rationale: str | None = "ready for execution",
) -> ReadinessLevel:
    return ReadinessLevel.of(band, ratio=ratio, rationale=rationale)


def make_priority_ref(
    *,
    priority_id: PriorityId | str = PRIORITY_001,
) -> PriorityReference:
    if isinstance(priority_id, str):
        priority_id = PriorityId(priority_id)
    return PriorityReference(priority_id=priority_id)


def make_intention_ref(
    *,
    intention_id: TeachingIntentionId | str = INTENTION_001,
    intention_type: TeachingIntentionType = DEFAULT_INTENTION,
) -> IntentionReference:
    if isinstance(intention_id, str):
        intention_id = TeachingIntentionId(intention_id)
    return IntentionReference(
        intention_id=intention_id,
        intention_type=intention_type,
    )


def make_strategy_ref(
    *,
    strategy_id: TeachingStrategyId | str = STRATEGY_001,
    strategy_type: TeachingStrategyType = DEFAULT_STRATEGY,
) -> StrategyReference:
    if isinstance(strategy_id, str):
        strategy_id = TeachingStrategyId(strategy_id)
    return StrategyReference(
        strategy_id=strategy_id,
        strategy_type=strategy_type,
    )


def make_indicator(
    *,
    indicator_id: str = "ind-001",
    kind: ReadinessIndicatorKind = ReadinessIndicatorKind.PREREQUISITE_SATISFIED,
    description: str | None = None,
    supports_readiness: bool | None = None,
    weight: float = 0.85,
) -> ReadinessIndicator:
    if supports_readiness is None:
        supports_readiness = kind in {
            ReadinessIndicatorKind.PREREQUISITE_SATISFIED,
            ReadinessIndicatorKind.EVIDENCE_SUFFICIENT,
            ReadinessIndicatorKind.CAPACITY_ADEQUATE,
            ReadinessIndicatorKind.INTENTION_ALIGNED,
            ReadinessIndicatorKind.STRATEGY_APPLICABLE,
        }
    return ReadinessIndicator(
        indicator_id=ReadinessIndicatorId(indicator_id),
        kind=kind,
        description=description or f"Readiness indicator {kind.value}",
        supports_readiness=supports_readiness,
        weight=weight,
    )


def make_ready_indicators() -> list[ReadinessIndicator]:
    return [
        make_indicator(
            indicator_id=f"ind-{kind.value}",
            kind=kind,
            weight=0.9,
        )
        for kind in READY_INDICATOR_KINDS
    ]


def make_constraint(
    *,
    constraint_id: str = "constraint-001",
    kind: ExecutionConstraintKind = (
        ExecutionConstraintKind.FORBID_APPROVAL_WHEN_BLOCKED
    ),
    statement: str | None = None,
    related_indicator_kind: ReadinessIndicatorKind | None = None,
    min_readiness: ReadinessBand | None = None,
    min_confidence: ConfidenceLevel | None = None,
    forbidden_outcome: DecisionOutcome | None = None,
) -> ExecutionConstraint:
    return ExecutionConstraint(
        constraint_id=ExecutionConstraintId(constraint_id),
        kind=kind,
        statement=statement or f"Constraint {kind.value}",
        related_indicator_kind=related_indicator_kind,
        min_readiness=min_readiness,
        min_confidence=min_confidence,
        forbidden_outcome=forbidden_outcome,
    )


def make_reason(
    *,
    reason_id: str = "reason-001",
    statement: str = "Evidence thickness and capacity support teaching now",
    code: str | None = None,
) -> DecisionReason:
    return DecisionReason(
        reason_id=DecisionReasonId(reason_id),
        statement=statement,
        code=code,
    )


def make_decision(
    *,
    decision_id: str | DecisionId = "dec-001",
    student_id: str = "student-ada",
    priority_references: list[PriorityReference] | None = None,
    intention_references: list[IntentionReference] | None = None,
    strategy_references: list[StrategyReference] | None = None,
    indicators: list[ReadinessIndicator] | None = None,
    constraints: list[ExecutionConstraint] | None = None,
    reasons: list[DecisionReason] | None = None,
    confidence: DecisionConfidence | None = None,
    readiness: ReadinessLevel | None = None,
    assess_readiness: bool = False,
    intention_type: TeachingIntentionType = DEFAULT_INTENTION,
    strategy_type: TeachingStrategyType = DEFAULT_STRATEGY,
) -> EducationalDecision:
    if isinstance(decision_id, str):
        decision_id = DecisionId(decision_id)
    resolved_indicators = (
        indicators if indicators is not None else make_ready_indicators()
    )
    kwargs: dict = {
        "decision_id": decision_id,
        "student_id": student_id,
        "priority_references": priority_references
        if priority_references is not None
        else [make_priority_ref()],
        "intention_references": intention_references
        if intention_references is not None
        else [make_intention_ref(intention_type=intention_type)],
        "strategy_references": strategy_references
        if strategy_references is not None
        else [make_strategy_ref(strategy_type=strategy_type)],
        "indicators": resolved_indicators,
        "confidence": confidence or make_confidence(),
        "constraints": constraints,
        "reasons": reasons,
    }
    if assess_readiness and readiness is None:
        return EducationalDecision.create(**kwargs)
    return EducationalDecision.create(
        **kwargs,
        readiness=readiness or make_readiness(),
    )


def make_approved_decision(**kwargs) -> EducationalDecision:
    decision = make_decision(**kwargs)
    decision.approve(reasons=[make_reason()])
    return decision
