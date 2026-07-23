"""Illegal lifecycle transition tests — errors returned, never raised."""

from __future__ import annotations

from datetime import datetime

from application.education.mission_execution import (
    ExecutionId,
    ExecutionStatus,
    MissionExecution,
    MissionExecutionEngine,
)
from application.education.mission_generation import MissionId
from tests.application.education.mission_execution.conftest import (
    at,
    make_plan,
)


def _started(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
):
    plan = make_plan()
    result = MissionExecutionEngine.start_execution(
        plan, mission_id, execution_id=execution_id, at=t0
    )
    assert result.ok and result.execution is not None
    return result.execution


def test_cannot_start_twice(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    started = _started(t0, execution_id, mission_id)
    plan = make_plan()
    again = MissionExecutionEngine.start_execution(
        plan,
        mission_id,
        execution_id=execution_id,
        at=at(t0, minutes=1),
        execution=started,
    )
    assert not again.ok
    assert again.error is not None
    assert again.error.code == "invalid_lifecycle_transition"
    assert again.execution is None


def test_cannot_pause_from_planned(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    plan = make_plan()
    planned = MissionExecution.plan_execution(
        execution_id=execution_id, mission_plan=plan, mission_id=mission_id
    )
    result = MissionExecutionEngine.pause_execution(planned, at=t0)
    assert not result.ok
    assert result.error is not None
    assert result.error.code == "invalid_lifecycle_transition"
    assert result.error.from_status == ExecutionStatus.PLANNED.value


def test_cannot_resume_from_started(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    started = _started(t0, execution_id, mission_id)
    result = MissionExecutionEngine.resume_execution(started, at=at(t0, minutes=1))
    assert not result.ok
    assert result.error is not None
    assert result.error.code == "invalid_lifecycle_transition"


def test_cannot_transition_from_completed(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    started = _started(t0, execution_id, mission_id)
    completed = MissionExecutionEngine.complete_execution(
        started, at=at(t0, minutes=5)
    ).execution
    assert completed is not None
    assert completed.status is ExecutionStatus.COMPLETED

    for attempt in (
        MissionExecutionEngine.pause_execution(completed, at=at(t0, minutes=6)),
        MissionExecutionEngine.resume_execution(completed, at=at(t0, minutes=6)),
        MissionExecutionEngine.abandon_execution(completed, at=at(t0, minutes=6)),
        MissionExecutionEngine.expire_execution(completed, at=at(t0, minutes=6)),
        MissionExecutionEngine.complete_execution(completed, at=at(t0, minutes=6)),
    ):
        assert not attempt.ok
        assert attempt.error is not None
        assert attempt.error.code == "execution_terminal"


def test_cannot_complete_step_when_planned(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    from application.education.mission_generation import MissionStepId

    plan = make_plan()
    planned = MissionExecution.plan_execution(
        execution_id=execution_id, mission_plan=plan, mission_id=mission_id
    )
    result = MissionExecutionEngine.complete_step(
        planned, MissionStepId("step-1"), at=t0
    )
    assert not result.ok
    assert result.error is not None
    assert result.error.code == "execution_not_active"


def test_cannot_complete_unknown_step(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    from application.education.mission_generation import MissionStepId

    started = _started(t0, execution_id, mission_id)
    result = MissionExecutionEngine.complete_step(
        started, MissionStepId("missing"), at=at(t0, minutes=1)
    )
    assert not result.ok
    assert result.error is not None
    assert result.error.code == "step_not_found"


def test_cannot_complete_step_twice(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    from application.education.mission_generation import MissionStepId

    started = _started(t0, execution_id, mission_id)
    step = MissionStepId("step-1")
    first = MissionExecutionEngine.complete_step(started, step, at=at(t0, minutes=1))
    assert first.ok and first.execution is not None
    second = MissionExecutionEngine.complete_step(
        first.execution, step, at=at(t0, minutes=2)
    )
    assert not second.ok
    assert second.error is not None
    assert second.error.code == "step_already_completed"
