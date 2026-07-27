"""State transition validation tests."""

from __future__ import annotations

import pytest

from domain.assessment import (
    ALLOWED_TRANSITIONS,
    AssessmentStatus,
    InvalidAssessmentStateTransition,
    assert_can_transition,
    can_transition,
)


def test_happy_path_transitions() -> None:
    path = [
        AssessmentStatus.DRAFT,
        AssessmentStatus.READY,
        AssessmentStatus.IN_PROGRESS,
        AssessmentStatus.SUBMITTED,
        AssessmentStatus.OBSERVED,
        AssessmentStatus.REASONED,
        AssessmentStatus.CLOSED,
    ]
    for current, target in zip(path[:-1], path[1:], strict=True):
        assert can_transition(current, target)
        assert_can_transition(current, target)


def test_pause_and_resume() -> None:
    assert can_transition(AssessmentStatus.IN_PROGRESS, AssessmentStatus.PAUSED)
    assert can_transition(AssessmentStatus.PAUSED, AssessmentStatus.IN_PROGRESS)


def test_invalid_transition_rejected() -> None:
    assert not can_transition(AssessmentStatus.SUBMITTED, AssessmentStatus.IN_PROGRESS)
    with pytest.raises(InvalidAssessmentStateTransition) as exc:
        assert_can_transition(
            AssessmentStatus.SUBMITTED, AssessmentStatus.IN_PROGRESS
        )
    assert exc.value.from_status == "submitted"
    assert exc.value.to_status == "in_progress"


def test_terminal_states_have_no_outbound() -> None:
    for status in (
        AssessmentStatus.CLOSED,
        AssessmentStatus.ABANDONED,
        AssessmentStatus.INVALIDATED,
    ):
        assert ALLOWED_TRANSITIONS[status] == frozenset()
