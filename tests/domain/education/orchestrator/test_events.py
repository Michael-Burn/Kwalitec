"""Domain event tests for Educational Orchestrator."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DecisionId, OrchestratorId
from domain.education.orchestrator import (
    OrchestrationCompleted,
    OrchestrationPaused,
    OrchestrationStageId,
    OrchestrationStarted,
)


def test_started_event_valid() -> None:
    event = OrchestrationStarted(
        orchestrator_id=OrchestratorId("orch-1"),
        student_id="student-ada",
        decision_id=DecisionId("dec-1"),
        first_stage_id=OrchestrationStageId("stage-1"),
        stage_count=3,
    )
    assert event.stage_count == 3


def test_started_rejects_zero_stages() -> None:
    with pytest.raises(EducationalInvariantViolation):
        OrchestrationStarted(
            orchestrator_id=OrchestratorId("orch-1"),
            student_id="student-ada",
            decision_id=DecisionId("dec-1"),
            first_stage_id=OrchestrationStageId("stage-1"),
            stage_count=0,
        )


def test_completed_event_valid() -> None:
    event = OrchestrationCompleted(
        orchestrator_id=OrchestratorId("orch-1"),
        student_id="student-ada",
        decision_id=DecisionId("dec-1"),
        completed_stages=4,
        evidence_collection_points_reached=1,
        episode_count=1,
    )
    assert event.episode_count == 1


def test_paused_event_valid() -> None:
    event = OrchestrationPaused(
        orchestrator_id=OrchestratorId("orch-1"),
        student_id="student-ada",
        reason="break",
        current_stage_id=OrchestrationStageId("stage-2"),
        completed_stages=1,
    )
    assert event.reason == "break"


def test_paused_rejects_blank_reason() -> None:
    with pytest.raises(EducationalInvariantViolation):
        OrchestrationPaused(
            orchestrator_id=OrchestratorId("orch-1"),
            student_id="student-ada",
            reason="  ",
            current_stage_id=None,
            completed_stages=0,
        )
