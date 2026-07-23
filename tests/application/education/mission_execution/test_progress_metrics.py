"""Progress, metrics, confidence, reflection, and snapshot tests."""

from __future__ import annotations

from datetime import datetime

from application.education.mission_execution import (
    ConfidenceTrend,
    ExecutionId,
    ExecutionStatus,
    MissionExecutionEngine,
    StepOutcome,
)
from application.education.mission_generation import MissionId, MissionStepId
from domain.education.foundation.enums import ConfidenceLevel
from tests.application.education.mission_execution.conftest import (
    at,
    make_plan,
)


def _started(t0: datetime, execution_id: ExecutionId, mission_id: MissionId):
    result = MissionExecutionEngine.start_execution(
        make_plan(), mission_id, execution_id=execution_id, at=t0
    )
    assert result.ok and result.execution is not None
    return result.execution


def test_progress_from_completed_steps_only(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    execution = _started(t0, execution_id, mission_id)
    after_complete = MissionExecutionEngine.complete_step(
        execution, MissionStepId("step-1"), at=at(t0, minutes=2)
    ).execution
    assert after_complete is not None
    assert after_complete.progress.completed_count == 1
    assert after_complete.progress.completion_percentage == round(100.0 / 3, 4)

    after_skip = MissionExecutionEngine.skip_step(
        after_complete, MissionStepId("step-2"), at=at(t0, minutes=3)
    ).execution
    assert after_skip is not None
    # Skipped steps do not increase completion percentage.
    assert after_skip.progress.completed_count == 1
    assert after_skip.progress.skipped_count == 1
    assert after_skip.progress.completion_percentage == round(100.0 / 3, 4)
    assert after_skip.progress.current_step_id == MissionStepId("step-3")
    outcomes = dict(after_skip.progress.step_outcomes)
    assert outcomes[MissionStepId("step-1")] is StepOutcome.COMPLETED
    assert outcomes[MissionStepId("step-2")] is StepOutcome.SKIPPED
    assert outcomes[MissionStepId("step-3")] is StepOutcome.PENDING


def test_execution_metrics(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    execution = _started(t0, execution_id, mission_id)
    paused = MissionExecutionEngine.pause_execution(
        execution, at=at(t0, minutes=10)
    ).execution
    assert paused is not None
    resumed = MissionExecutionEngine.resume_execution(
        paused, at=at(t0, minutes=12)
    ).execution
    assert resumed is not None
    with_step = MissionExecutionEngine.complete_step(
        resumed, MissionStepId("step-1"), at=at(t0, minutes=17)
    ).execution
    assert with_step is not None
    with_conf = MissionExecutionEngine.record_confidence(
        with_step, ConfidenceLevel.MEDIUM, at=at(t0, minutes=17, seconds=30)
    ).execution
    assert with_conf is not None
    with_ref = MissionExecutionEngine.record_reflection(
        with_conf, "Solid progress", at=at(t0, minutes=18)
    ).execution
    assert with_ref is not None
    completed = MissionExecutionEngine.complete_execution(
        with_ref, at=at(t0, minutes=20)
    ).execution
    assert completed is not None

    metrics = completed.metrics
    assert metrics.elapsed_study_time_seconds == 1080.0  # 10 + 5 + 3
    assert metrics.paused_duration_seconds == 120.0
    assert metrics.mission_duration_seconds == 1200.0  # started→finished
    assert metrics.skipped_steps == 0
    assert metrics.reflection_count == 1
    assert metrics.confidence_count == 1
    assert metrics.completion_percentage == round(100.0 / 3, 4)
    assert metrics.step_completion_rate == round(1 / 3, 4)


def test_confidence_history_preserved(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    execution = _started(t0, execution_id, mission_id)
    first = MissionExecutionEngine.record_confidence(
        execution, ConfidenceLevel.LOW, at=at(t0, minutes=1)
    ).execution
    assert first is not None
    second = MissionExecutionEngine.record_confidence(
        first, ConfidenceLevel.HIGH, at=at(t0, minutes=2)
    ).execution
    assert second is not None
    assert len(second.confidence_history) == 2
    assert second.confidence is not None
    assert second.confidence.level is ConfidenceLevel.HIGH
    assert second.metrics.confidence_trend is ConfidenceTrend.RISING


def test_reflection_history_append_only(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    execution = _started(t0, execution_id, mission_id)
    first = MissionExecutionEngine.record_reflection(
        execution, "First thought", at=at(t0, minutes=1)
    ).execution
    assert first is not None
    second = MissionExecutionEngine.record_reflection(
        first, "Second thought", at=at(t0, minutes=2)
    ).execution
    assert second is not None
    assert [r.text for r in second.reflection_history] == [
        "First thought",
        "Second thought",
    ]
    assert second.reflection is not None
    assert second.reflection.text == "Second thought"


def test_empty_reflection_rejected(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    execution = _started(t0, execution_id, mission_id)
    result = MissionExecutionEngine.record_reflection(execution, "   ", at=t0)
    assert not result.ok
    assert result.error is not None
    assert result.error.code == "invalid_reflection"


def test_produce_snapshot(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    execution = _started(t0, execution_id, mission_id)
    with_step = MissionExecutionEngine.complete_step(
        execution, MissionStepId("step-1"), at=at(t0, minutes=5)
    ).execution
    assert with_step is not None
    snapshot = MissionExecutionEngine.produce_snapshot(
        with_step, at=at(t0, minutes=5)
    )
    assert snapshot.execution_id == execution_id
    assert snapshot.status is ExecutionStatus.STARTED
    assert snapshot.progress.completed_count == 1
    assert snapshot.captured_at == at(t0, minutes=5)
    assert snapshot.summary.completed_steps == 1
    # Snapshot holds the same mission reference content; plan is untouched.
    assert snapshot.mission.mission_id == mission_id


def test_mission_plan_not_mutated(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    plan = make_plan()
    original_missions = plan.missions
    started = MissionExecutionEngine.start_execution(
        plan, mission_id, execution_id=execution_id, at=t0
    ).execution
    assert started is not None
    MissionExecutionEngine.complete_step(
        started, MissionStepId("step-1"), at=at(t0, minutes=1)
    )
    assert plan.missions is original_missions
    assert plan.missions[0].steps[0].step_id == MissionStepId("step-1")
