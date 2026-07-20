"""Policy tests for Educational Decision."""

from __future__ import annotations

import pytest

from domain.education.decision import (
    DecisionOutcome,
    DecisionPolicy,
    ExecutionConstraintKind,
    ReadinessBand,
    ReadinessIndicatorKind,
    ReadinessPolicy,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation
from tests.domain.education.decision.conftest import (
    make_confidence,
    make_constraint,
    make_indicator,
    make_readiness,
    make_ready_indicators,
)


def test_readiness_policy_assess_ready() -> None:
    readiness = ReadinessPolicy.assess(make_ready_indicators())
    assert readiness.band is ReadinessBand.READY


def test_readiness_policy_assess_blocked() -> None:
    readiness = ReadinessPolicy.assess(
        [
            make_indicator(
                kind=ReadinessIndicatorKind.PREREQUISITE_MISSING,
                supports_readiness=False,
            )
        ]
    )
    assert readiness.band is ReadinessBand.BLOCKED


@pytest.mark.parametrize(
    ("kind", "expected"),
    [
        (ReadinessIndicatorKind.REMEDIATION_REQUIRED, "require_remediation"),
        (ReadinessIndicatorKind.PREREQUISITE_MISSING, "require_prerequisite_work"),
        (ReadinessIndicatorKind.EVIDENCE_INSUFFICIENT, "require_additional_evidence"),
        (ReadinessIndicatorKind.CAPACITY_INSUFFICIENT, "delay"),
    ],
)
def test_suggested_deferral(kind: ReadinessIndicatorKind, expected: str) -> None:
    suggestion = ReadinessPolicy.suggested_deferral_outcome(
        [make_indicator(kind=kind, supports_readiness=False)]
    )
    assert suggestion == expected


def test_decision_policy_approval_lawful() -> None:
    DecisionPolicy.assert_approval_lawful(
        readiness=make_readiness(ReadinessBand.READY),
        confidence=make_confidence(ConfidenceLevel.HIGH),
        indicators=make_ready_indicators(),
        constraints=[],
    )


def test_decision_policy_approval_rejects_partial() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DecisionPolicy.assert_approval_lawful(
            readiness=make_readiness(ReadinessBand.PARTIALLY_READY),
            confidence=make_confidence(),
            indicators=make_ready_indicators(),
            constraints=[],
        )


def test_constraint_require_indicator_enforced() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DecisionPolicy.assert_constraints_satisfied(
            [
                make_constraint(
                    kind=ExecutionConstraintKind.REQUIRE_INDICATOR,
                    related_indicator_kind=ReadinessIndicatorKind.STRATEGY_APPLICABLE,
                )
            ],
            indicators=[
                make_indicator(kind=ReadinessIndicatorKind.CAPACITY_ADEQUATE)
            ],
            readiness=make_readiness(ReadinessBand.READY),
            confidence=make_confidence(),
        )


def test_forbid_outcome_on_approve_path() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DecisionPolicy.assert_constraints_satisfied(
            [
                make_constraint(
                    kind=ExecutionConstraintKind.FORBID_OUTCOME,
                    forbidden_outcome=DecisionOutcome.TEACH_NOW,
                )
            ],
            indicators=make_ready_indicators(),
            readiness=make_readiness(),
            confidence=make_confidence(),
            outcome=DecisionOutcome.TEACH_NOW,
            approving=True,
        )


def test_status_helpers() -> None:
    assert DecisionPolicy.status_for_approval().value == "approved"
    assert DecisionPolicy.status_for_delay().value == "delayed"
    assert DecisionPolicy.status_for_rejection().value == "rejected"
