"""Aggregate behaviour tests for EducationalDecision."""

from __future__ import annotations

import pytest

from domain.education.decision import (
    DecisionIsExecutableSpecification,
    DecisionOutcome,
    DecisionStatus,
    InterventionIsReadySpecification,
    ReadinessBand,
    ReadinessIndicatorKind,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DecisionId
from tests.domain.education.decision.conftest import (
    make_approved_decision,
    make_confidence,
    make_constraint,
    make_decision,
    make_indicator,
    make_readiness,
    make_reason,
)


def test_create_pending_decision() -> None:
    decision = make_decision()
    assert decision.is_pending()
    assert decision.outcome is None
    assert decision.readiness.band is ReadinessBand.READY
    assert decision.indicator_count() == 5
    assert decision.priority_count() == 1
    assert decision.intention_count() == 1
    assert decision.strategy_count() == 1


def test_create_assesses_readiness_from_indicators() -> None:
    decision = make_decision(assess_readiness=True)
    assert decision.readiness.band is ReadinessBand.READY


def test_approve_teaches_now() -> None:
    decision = make_decision()
    decision.approve(reasons=[make_reason()])
    assert decision.is_approved()
    assert decision.teaches_now()
    assert decision.outcome is DecisionOutcome.TEACH_NOW
    assert DecisionIsExecutableSpecification().is_satisfied_by(decision)
    events = decision.pull_events()
    assert len(events) == 1
    assert events[0].outcome is DecisionOutcome.TEACH_NOW


def test_delay_and_reject_non_teach_outcomes() -> None:
    delayed = make_decision(decision_id="dec-delay")
    delayed.delay(DecisionOutcome.REQUIRE_PREREQUISITE_WORK)
    assert delayed.is_delayed()
    assert delayed.outcome is DecisionOutcome.REQUIRE_PREREQUISITE_WORK

    rejected = make_decision(decision_id="dec-reject")
    rejected.reject(DecisionOutcome.REQUIRE_REMEDIATION)
    assert rejected.is_rejected()
    assert rejected.outcome is DecisionOutcome.REQUIRE_REMEDIATION


def test_cannot_approve_when_not_ready() -> None:
    decision = make_decision(
        indicators=[
            make_indicator(
                kind=ReadinessIndicatorKind.PREREQUISITE_MISSING,
                supports_readiness=False,
            )
        ],
        readiness=make_readiness(ReadinessBand.BLOCKED),
    )
    with pytest.raises(EducationalInvariantViolation):
        decision.approve()


def test_cannot_approve_twice_without_reconsider() -> None:
    decision = make_approved_decision()
    with pytest.raises(EducationalInvariantViolation):
        decision.approve()


def test_reconsider_reopens_committed_decision() -> None:
    decision = make_approved_decision()
    decision.pull_events()
    decision.reconsider("new capacity evidence arrived")
    assert decision.is_reconsidered()
    assert decision.outcome is None
    events = decision.pull_events()
    assert len(events) == 1
    assert events[0].previous_status is DecisionStatus.APPROVED
    decision.approve(reasons=[make_reason(reason_id="r2")])
    assert decision.is_approved()


def test_cannot_reconsider_pending() -> None:
    decision = make_decision()
    with pytest.raises(EducationalInvariantViolation):
        decision.reconsider("too early")


def test_refresh_readiness_while_pending() -> None:
    decision = make_decision()
    decision.refresh_readiness(
        indicators=[
            make_indicator(
                indicator_id="ind-evidence",
                kind=ReadinessIndicatorKind.EVIDENCE_INSUFFICIENT,
                supports_readiness=False,
            ),
            make_indicator(
                indicator_id="ind-capacity",
                kind=ReadinessIndicatorKind.CAPACITY_ADEQUATE,
            ),
        ]
    )
    assert decision.readiness.band in {
        ReadinessBand.NOT_READY,
        ReadinessBand.PARTIALLY_READY,
    }


def test_equality_by_identity() -> None:
    left = make_decision(decision_id="same")
    right = make_decision(decision_id="same")
    other = make_decision(decision_id="other")
    assert left == right
    assert left != other
    assert hash(left) == hash(right)
    assert DecisionId("same") == left.decision_id


def test_intervention_ready_spec() -> None:
    decision = make_decision()
    assert InterventionIsReadySpecification().is_satisfied_by(decision)
    blocked = make_decision(
        decision_id="blocked",
        indicators=[
            make_indicator(
                kind=ReadinessIndicatorKind.AFFECTIVE_BLOCK,
                supports_readiness=False,
            )
        ],
        readiness=make_readiness(ReadinessBand.BLOCKED),
        confidence=make_confidence(ConfidenceLevel.MEDIUM),
    )
    assert not InterventionIsReadySpecification().is_satisfied_by(blocked)


def test_suggested_deferral_outcome() -> None:
    decision = make_decision(
        indicators=[
            make_indicator(
                kind=ReadinessIndicatorKind.REMEDIATION_REQUIRED,
                supports_readiness=False,
            )
        ],
        readiness=make_readiness(ReadinessBand.BLOCKED),
    )
    assert decision.suggested_deferral_outcome() is (
        DecisionOutcome.REQUIRE_REMEDIATION
    )


def test_constraint_blocks_approval() -> None:
    from domain.education.decision import ExecutionConstraintKind

    decision = make_decision(
        constraints=[
            make_constraint(
                kind=ExecutionConstraintKind.FORBID_OUTCOME,
                forbidden_outcome=DecisionOutcome.TEACH_NOW,
            )
        ]
    )
    with pytest.raises(EducationalInvariantViolation):
        decision.approve()


def test_has_helpers() -> None:
    decision = make_decision()
    assert decision.has_indicator_kind(ReadinessIndicatorKind.CAPACITY_ADEQUATE)
    assert decision.has_priority(decision.priority_references[0].priority_id)
    assert decision.has_intention(decision.intention_references[0].intention_id)
    assert decision.has_strategy(decision.strategy_references[0].strategy_id)
