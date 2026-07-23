"""Lifecycle transition tests for MissionExecutionEngine."""

from __future__ import annotations

from datetime import datetime

from application.education.mission_execution import (
    ExecutionId,
    ExecutionStatus,
    MissionExecutionEngine,
    MissionStarted,
)
from application.education.mission_generation import MissionId
from tests.application.education.mission_execution.conftest import (
    at,
    make_plan,
)


def test_start_from_plan(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    plan = make_plan()
    result = MissionExecutionEngine.start_execution(
        plan, mission_id, execution_id=execution_id, at=t0
    )
    assert result.ok
    assert result.execution is not None
    assert result.execution.status is ExecutionStatus.STARTED
    assert result.execution.started_at == t0
    assert len(result.events) == 1
    assert isinstance(result.events[0], MissionStarted)
    assert result.evidence  # study session started


def test_pause_resume_complete(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    plan = make_plan()
    started = MissionExecutionEngine.start_execution(
        plan, mission_id, execution_id=execution_id, at=t0
    ).execution
    assert started is not None

    paused = MissionExecutionEngine.pause_execution(started, at=at(t0, minutes=10))
    assert paused.ok
    assert paused.execution is not None
    assert paused.execution.status is ExecutionStatus.PAUSED
    assert paused.execution.elapsed_study_time_seconds == 600.0

    resumed = MissionExecutionEngine.resume_execution(
        paused.execution, at=at(t0, minutes=15)
    )
    assert resumed.ok
    assert resumed.execution is not None
    assert resumed.execution.status is ExecutionStatus.RESUMED
    assert resumed.execution.paused_duration_seconds == 300.0

    completed = MissionExecutionEngine.complete_execution(
        resumed.execution, at=at(t0, minutes=25)
    )
    assert completed.ok
    assert completed.execution is not None
    assert completed.execution.status is ExecutionStatus.COMPLETED
    assert completed.execution.finished_at == at(t0, minutes=25)
    assert completed.execution.elapsed_study_time_seconds == 1200.0  # 10 + 10


def test_abandon_from_started(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    plan = make_plan()
    started = MissionExecutionEngine.start_execution(
        plan, mission_id, execution_id=execution_id, at=t0
    ).execution
    assert started is not None
    abandoned = MissionExecutionEngine.abandon_execution(
        started, at=at(t0, minutes=5)
    )
    assert abandoned.ok
    assert abandoned.execution is not None
    assert abandoned.execution.status is ExecutionStatus.ABANDONED


def test_expire_from_planned(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    from application.education.mission_execution import MissionExecution

    plan = make_plan()
    planned = MissionExecution.plan_execution(
        execution_id=execution_id, mission_plan=plan, mission_id=mission_id
    )
    expired = MissionExecutionEngine.expire_execution(planned, at=t0)
    assert expired.ok
    assert expired.execution is not None
    assert expired.execution.status is ExecutionStatus.EXPIRED


def test_complete_from_paused(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    plan = make_plan()
    started = MissionExecutionEngine.start_execution(
        plan, mission_id, execution_id=execution_id, at=t0
    ).execution
    assert started is not None
    paused = MissionExecutionEngine.pause_execution(
        started, at=at(t0, minutes=5)
    ).execution
    assert paused is not None
    completed = MissionExecutionEngine.complete_execution(
        paused, at=at(t0, minutes=6)
    )
    assert completed.ok
    assert completed.execution is not None
    assert completed.execution.status is ExecutionStatus.COMPLETED
    assert completed.execution.paused_duration_seconds == 60.0
