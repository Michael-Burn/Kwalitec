"""Entity tests for Educational Decision."""

from __future__ import annotations

import pytest

from domain.education.decision import (
    DecisionOutcome,
    DecisionReason,
    DecisionReasonId,
    ExecutionConstraint,
    ExecutionConstraintId,
    ExecutionConstraintKind,
    IntentionReference,
    PriorityReference,
    ReadinessBand,
    ReadinessIndicator,
    ReadinessIndicatorId,
    ReadinessIndicatorKind,
    StrategyReference,
)
from domain.education.foundation.enums import (
    ConfidenceLevel,
    TeachingIntentionType,
    TeachingStrategyType,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import (
    PriorityId,
    TeachingIntentionId,
    TeachingStrategyId,
)
from tests.domain.education.decision.conftest import (
    make_constraint,
    make_indicator,
    make_reason,
)


def test_decision_reason_rejects_smuggling() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DecisionReason(
            reason_id=DecisionReasonId("r1"),
            statement="therefore diagnose misconception first",
        )


def test_decision_reason_signature_and_with_statement() -> None:
    reason = make_reason(statement="Capacity adequate for teaching now")
    amended = reason.with_statement("Capacity still adequate after rest")
    assert amended.reason_id == reason.reason_id
    assert reason.reason_signature()[0] != amended.reason_signature()[0]


@pytest.mark.parametrize("kind", list(ReadinessIndicatorKind))
def test_indicator_kind_polarity(kind: ReadinessIndicatorKind) -> None:
    supporting = kind in {
        ReadinessIndicatorKind.PREREQUISITE_SATISFIED,
        ReadinessIndicatorKind.EVIDENCE_SUFFICIENT,
        ReadinessIndicatorKind.CAPACITY_ADEQUATE,
        ReadinessIndicatorKind.INTENTION_ALIGNED,
        ReadinessIndicatorKind.STRATEGY_APPLICABLE,
    }
    indicator = make_indicator(
        indicator_id=f"i-{kind.value}",
        kind=kind,
        supports_readiness=supporting,
    )
    assert indicator.kind is kind
    assert indicator.is_blocking() is (not supporting)


def test_indicator_rejects_inverted_polarity() -> None:
    with pytest.raises(EducationalInvariantViolation):
        ReadinessIndicator(
            indicator_id=ReadinessIndicatorId("bad"),
            kind=ReadinessIndicatorKind.PREREQUISITE_MISSING,
            description="missing prerequisite",
            supports_readiness=True,
        )


@pytest.mark.parametrize("kind", list(ExecutionConstraintKind))
def test_constraint_kinds_constructible(kind: ExecutionConstraintKind) -> None:
    kwargs: dict = {
        "constraint_id": f"c-{kind.value}",
        "kind": kind,
    }
    if kind is ExecutionConstraintKind.REQUIRE_MINIMUM_READINESS:
        kwargs["min_readiness"] = ReadinessBand.READY
    elif kind is ExecutionConstraintKind.REQUIRE_MINIMUM_CONFIDENCE:
        kwargs["min_confidence"] = ConfidenceLevel.MEDIUM
    elif kind in {
        ExecutionConstraintKind.REQUIRE_INDICATOR,
        ExecutionConstraintKind.FORBID_INDICATOR,
    }:
        kwargs["related_indicator_kind"] = (
            ReadinessIndicatorKind.PREREQUISITE_SATISFIED
        )
    elif kind is ExecutionConstraintKind.FORBID_OUTCOME:
        kwargs["forbidden_outcome"] = DecisionOutcome.TEACH_NOW
    constraint = make_constraint(**kwargs)
    assert constraint.kind is kind
    assert constraint.constraint_signature()[0] == kind.value


def test_constraint_requires_payload() -> None:
    with pytest.raises(EducationalInvariantViolation):
        ExecutionConstraint(
            constraint_id=ExecutionConstraintId("c1"),
            kind=ExecutionConstraintKind.REQUIRE_MINIMUM_READINESS,
            statement="need readiness",
        )


def test_references_validate_types() -> None:
    priority = PriorityReference(priority_id=PriorityId("p1"))
    intention = IntentionReference(
        intention_id=TeachingIntentionId("i1"),
        intention_type=TeachingIntentionType.BUILD_INTUITION,
    )
    strategy = StrategyReference(
        strategy_id=TeachingStrategyId("s1"),
        strategy_type=TeachingStrategyType.ANALOGY,
    )
    assert "p1" in str(priority)
    assert "build_intuition" in str(intention)
    assert "analogy" in str(strategy)
