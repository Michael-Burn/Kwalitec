"""Specification tests for Educational Decision."""

from __future__ import annotations

import pytest

from domain.education.decision import (
    DecisionIsExecutableSpecification,
    DecisionOutcome,
    InterventionIsReadySpecification,
    ReadinessBand,
    ReadinessIndicatorKind,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from tests.domain.education.decision.conftest import (
    make_approved_decision,
    make_decision,
    make_indicator,
    make_readiness,
    make_reason,
)


def test_intervention_is_ready_for_pending_ready() -> None:
    decision = make_decision()
    InterventionIsReadySpecification().assert_satisfied_by(decision)


def test_intervention_not_ready_when_blocked() -> None:
    decision = make_decision(
        indicators=[
            make_indicator(
                kind=ReadinessIndicatorKind.SESSION_CONSTRAINT,
                supports_readiness=False,
            )
        ],
        readiness=make_readiness(ReadinessBand.BLOCKED),
    )
    assert not InterventionIsReadySpecification().is_satisfied_by(decision)
    with pytest.raises(EducationalInvariantViolation):
        InterventionIsReadySpecification().assert_satisfied_by(decision)


def test_decision_is_executable_only_when_approved_teach_now() -> None:
    pending = make_decision()
    assert not DecisionIsExecutableSpecification().is_satisfied_by(pending)

    approved = make_approved_decision(decision_id="dec-exec")
    DecisionIsExecutableSpecification().assert_satisfied_by(approved)

    delayed = make_decision(decision_id="dec-delay-spec")
    delayed.delay(DecisionOutcome.DELAY, reasons=[make_reason()])
    assert not DecisionIsExecutableSpecification().is_satisfied_by(delayed)
