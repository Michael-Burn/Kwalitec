"""Entity tests for Teaching Strategy."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import (
    DiagnosisType,
    TeachingIntentionType,
    TeachingStrategyType,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import (
    DiagnosisId,
    HypothesisId,
    TeachingIntentionId,
)
from domain.education.teaching_strategy import (
    ComplexityLevel,
    DiagnosisReference,
    HypothesisReference,
    IntentionReference,
    SecondaryStrategyReference,
    StrategyConstraint,
    StrategyConstraintId,
    StrategyConstraintKind,
    StrategyGoal,
    StrategyGoalId,
    StrategyRationale,
    StrategyRationaleId,
)
from tests.domain.education.teaching_strategy.conftest import (
    make_constraint,
    make_goal,
    make_rationale,
)


def test_strategy_goal_identity_equality() -> None:
    a = make_goal(goal_id="g1")
    b = StrategyGoal(
        goal_id=StrategyGoalId("g1"),
        statement="Different statement still same identity",
        strategy_type=TeachingStrategyType.ANALOGY,
    )
    assert a == b
    assert a.entity_id == b.entity_id


def test_strategy_goal_rejects_mastery() -> None:
    with pytest.raises(EducationalInvariantViolation, match="mastery"):
        make_goal(statement="Achieve mastery via worked examples")


def test_strategy_rationale_requires_substance() -> None:
    with pytest.raises(EducationalInvariantViolation, match="substantive"):
        StrategyRationale(
            rationale_id=StrategyRationaleId("r1"),
            statement="too short",
        )


def test_strategy_rationale_with_statement() -> None:
    original = make_rationale()
    amended = original.with_statement(
        "Revised educational justification for this instructional approach"
    )
    assert amended.rationale_id == original.rationale_id
    assert "Revised" in amended.statement


def test_intention_reference() -> None:
    ref = IntentionReference(
        intention_id=TeachingIntentionId("ti-1"),
        intention_type=TeachingIntentionType.BUILD_INTUITION,
    )
    assert "build_intuition" in str(ref)


def test_diagnosis_and_hypothesis_references() -> None:
    d = DiagnosisReference(
        diagnosis_id=DiagnosisId("d1"),
        diagnosis_type=DiagnosisType.MISCONCEPTION,
    )
    h = HypothesisReference(hypothesis_id=HypothesisId("h1"))
    assert "misconception" in str(d)
    assert str(h) == "h1"


def test_secondary_strategy_order_positive() -> None:
    with pytest.raises(EducationalInvariantViolation, match="positive"):
        SecondaryStrategyReference(
            strategy_type=TeachingStrategyType.WORKED_EXAMPLE,
            sequence_order=0,
        )


def test_constraint_cap_requires_payload() -> None:
    with pytest.raises(EducationalInvariantViolation, match="max_complexity"):
        StrategyConstraint(
            constraint_id=StrategyConstraintId("c1"),
            kind=StrategyConstraintKind.CAP_COMPLEXITY,
            statement="cap without payload",
        )


def test_constraint_forbid_requires_payload() -> None:
    with pytest.raises(EducationalInvariantViolation, match="forbidden_strategy"):
        make_constraint(kind=StrategyConstraintKind.FORBID_STRATEGY_TYPE)


def test_constraint_signature_distinct() -> None:
    a = make_constraint(
        constraint_id="a",
        kind=StrategyConstraintKind.FORBID_STRATEGY_TYPE,
        forbidden_strategy_type=TeachingStrategyType.EXAM_SIMULATION,
    )
    b = make_constraint(
        constraint_id="b",
        kind=StrategyConstraintKind.FORBID_STRATEGY_TYPE,
        forbidden_strategy_type=TeachingStrategyType.INTERLEAVING,
    )
    assert a.constraint_signature() != b.constraint_signature()


def test_constraint_with_complexity_cap() -> None:
    c = make_constraint(
        kind=StrategyConstraintKind.CAP_COMPLEXITY,
        max_complexity=ComplexityLevel.MODERATE,
    )
    assert c.max_complexity is ComplexityLevel.MODERATE
