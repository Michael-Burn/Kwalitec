"""Value object tests for orchestration state and progress."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.orchestrator import (
    OrchestrationStageId,
    OrchestrationState,
    OrchestrationStatus,
)


def test_planned_factory() -> None:
    state = OrchestrationState.planned()
    assert state.is_planned()
    assert state.current_stage_id is None


def test_active_factory() -> None:
    state = OrchestrationState.active(OrchestrationStageId("s1"))
    assert state.is_active()
    assert state.current_stage_id == OrchestrationStageId("s1")


def test_paused_requires_reason() -> None:
    with pytest.raises(EducationalInvariantViolation):
        OrchestrationState(
            status=OrchestrationStatus.PAUSED,
            pause_reason=None,
        )


def test_paused_factory() -> None:
    state = OrchestrationState.paused(
        "capacity",
        current_stage_id=OrchestrationStageId("s1"),
    )
    assert state.is_paused()
    assert state.pause_reason == "capacity"


def test_completed_forbids_active_stage() -> None:
    with pytest.raises(EducationalInvariantViolation):
        OrchestrationState(
            status=OrchestrationStatus.COMPLETED,
            current_stage_id=OrchestrationStageId("s1"),
        )


def test_planned_forbids_pause_reason() -> None:
    with pytest.raises(EducationalInvariantViolation):
        OrchestrationState(
            status=OrchestrationStatus.PLANNED,
            pause_reason="nope",
        )


def test_pause_reason_only_when_paused() -> None:
    with pytest.raises(EducationalInvariantViolation):
        OrchestrationState(
            status=OrchestrationStatus.ACTIVE,
            current_stage_id=OrchestrationStageId("s1"),
            pause_reason="wrong",
        )


def test_completed_factory() -> None:
    state = OrchestrationState.completed()
    assert state.is_completed()
    assert state.is_terminal()
