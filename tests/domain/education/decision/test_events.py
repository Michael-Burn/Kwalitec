"""Domain event tests for Educational Decision."""

from __future__ import annotations

import pytest

from domain.education.decision import (
    DecisionMade,
    DecisionOutcome,
    DecisionReconsidered,
    DecisionStatus,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DecisionId
from tests.domain.education.decision.conftest import (
    make_approved_decision,
    make_decision,
    make_reason,
)


def test_decision_made_event_on_approve() -> None:
    decision = make_decision()
    decision.approve(reasons=[make_reason()])
    events = decision.pull_events()
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, DecisionMade)
    assert event.outcome is DecisionOutcome.TEACH_NOW
    assert event.status is DecisionStatus.APPROVED
    assert event.indicator_count >= 1
    assert decision.pull_events() == []


def test_decision_reconsidered_event() -> None:
    decision = make_approved_decision()
    decision.pull_events()
    decision.reconsider("capacity recovered")
    events = decision.pull_events()
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, DecisionReconsidered)
    assert event.previous_outcome is DecisionOutcome.TEACH_NOW
    assert "capacity" in event.reason


def test_decision_made_rejects_unknown_confidence() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DecisionMade(
            decision_id=DecisionId("d1"),
            student_id="student-ada",
            outcome=DecisionOutcome.TEACH_NOW,
            status=DecisionStatus.APPROVED,
            readiness_band="ready",
            confidence_level=ConfidenceLevel.UNKNOWN,
            indicator_count=1,
            constraint_count=0,
            reason_count=0,
        )


def test_reconsidered_requires_reason() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DecisionReconsidered(
            decision_id=DecisionId("d1"),
            student_id="student-ada",
            previous_outcome=DecisionOutcome.DELAY,
            previous_status=DecisionStatus.DELAYED,
            reason="  ",
        )
