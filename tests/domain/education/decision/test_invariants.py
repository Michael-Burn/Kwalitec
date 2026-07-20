"""Invariant enforcement tests for Educational Decision."""

from __future__ import annotations

import pytest

from domain.education.decision import (
    DecisionOutcome,
    ExecutionConstraintKind,
    ReadinessBand,
    ReadinessIndicatorKind,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation
from tests.domain.education.decision.conftest import (
    make_confidence,
    make_constraint,
    make_decision,
    make_indicator,
    make_intention_ref,
    make_priority_ref,
    make_readiness,
    make_ready_indicators,
    make_reason,
    make_strategy_ref,
)


def test_must_reference_priority() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        make_decision(priority_references=[])
    assert "priority" in (exc.value.invariant or "")


def test_must_reference_intention() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        make_decision(intention_references=[])
    assert "intention" in (exc.value.invariant or "")


def test_must_reference_strategy() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        make_decision(strategy_references=[])
    assert "strategy" in (exc.value.invariant or "")


def test_must_possess_indicators() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_decision(indicators=[])


def test_must_possess_confidence_and_readiness() -> None:
    decision = make_decision(
        confidence=make_confidence(ConfidenceLevel.MEDIUM),
        readiness=make_readiness(ReadinessBand.PARTIALLY_READY, ratio=0.4),
    )
    assert decision.confidence.level is ConfidenceLevel.MEDIUM
    assert decision.readiness.band is ReadinessBand.PARTIALLY_READY


def test_duplicate_priority_rejected() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_decision(
            priority_references=[
                make_priority_ref(),
                make_priority_ref(),
            ]
        )


def test_duplicate_indicator_kind_rejected() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_decision(
            indicators=[
                make_indicator(
                    indicator_id="a",
                    kind=ReadinessIndicatorKind.CAPACITY_ADEQUATE,
                ),
                make_indicator(
                    indicator_id="b",
                    kind=ReadinessIndicatorKind.CAPACITY_ADEQUATE,
                ),
            ]
        )


def test_contradictory_require_forbid_indicator() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_decision(
            constraints=[
                make_constraint(
                    constraint_id="req",
                    kind=ExecutionConstraintKind.REQUIRE_INDICATOR,
                    related_indicator_kind=ReadinessIndicatorKind.EVIDENCE_SUFFICIENT,
                ),
                make_constraint(
                    constraint_id="forbid",
                    kind=ExecutionConstraintKind.FORBID_INDICATOR,
                    related_indicator_kind=ReadinessIndicatorKind.EVIDENCE_SUFFICIENT,
                ),
            ]
        )


def test_ready_contradicts_hard_block_indicator() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_decision(
            indicators=[
                make_indicator(
                    kind=ReadinessIndicatorKind.PREREQUISITE_MISSING,
                    supports_readiness=False,
                )
            ],
            readiness=make_readiness(ReadinessBand.READY),
        )


def test_cannot_approve_with_very_low_confidence() -> None:
    decision = make_decision(confidence=make_confidence(ConfidenceLevel.VERY_LOW))
    with pytest.raises(EducationalInvariantViolation):
        decision.approve()


def test_cannot_delay_with_teach_now_outcome() -> None:
    decision = make_decision()
    with pytest.raises(EducationalInvariantViolation):
        decision.delay(DecisionOutcome.TEACH_NOW)


def test_duplicate_reason_rejected_on_approve() -> None:
    decision = make_decision()
    with pytest.raises(EducationalInvariantViolation):
        decision.approve(
            reasons=[
                make_reason(reason_id="r1", statement="same statement"),
                make_reason(reason_id="r2", statement="same statement"),
            ]
        )


def test_references_present_on_lawful_decision() -> None:
    decision = make_decision(
        priority_references=[make_priority_ref(priority_id="prio-a")],
        intention_references=[make_intention_ref(intention_id="int-a")],
        strategy_references=[make_strategy_ref(strategy_id="str-a")],
        indicators=make_ready_indicators(),
    )
    assert decision.has_priority(decision.priority_references[0].priority_id)
    assert decision.constraint_count() == 0
