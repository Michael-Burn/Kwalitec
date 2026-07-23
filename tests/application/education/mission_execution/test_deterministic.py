"""Deterministic execution tests."""

from __future__ import annotations

from datetime import datetime

from application.education.mission_execution import (
    ExecutionId,
    MissionExecutionEngine,
)
from application.education.mission_generation import MissionId, MissionStepId
from domain.education.foundation.enums import ConfidenceLevel
from tests.application.education.mission_execution.conftest import (
    at,
    make_plan,
)


def _run_script(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
):
    plan = make_plan()
    started = MissionExecutionEngine.start_execution(
        plan, mission_id, execution_id=execution_id, at=t0
    )
    assert started.ok and started.execution is not None
    step1 = MissionExecutionEngine.complete_step(
        started.execution, MissionStepId("step-1"), at=at(t0, minutes=5)
    )
    assert step1.ok and step1.execution is not None
    conf = MissionExecutionEngine.record_confidence(
        step1.execution, ConfidenceLevel.MEDIUM, at=at(t0, minutes=6)
    )
    assert conf.ok and conf.execution is not None
    paused = MissionExecutionEngine.pause_execution(
        conf.execution, at=at(t0, minutes=8)
    )
    assert paused.ok and paused.execution is not None
    resumed = MissionExecutionEngine.resume_execution(
        paused.execution, at=at(t0, minutes=10)
    )
    assert resumed.ok and resumed.execution is not None
    refl = MissionExecutionEngine.record_reflection(
        resumed.execution, "Ready to finish", at=at(t0, minutes=11)
    )
    assert refl.ok and refl.execution is not None
    done = MissionExecutionEngine.complete_execution(
        refl.execution, at=at(t0, minutes=15)
    )
    assert done.ok and done.execution is not None
    return done


def test_same_inputs_same_execution_state(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    a = _run_script(t0, execution_id, mission_id)
    b = _run_script(t0, execution_id, mission_id)
    assert a.execution is not None and b.execution is not None
    assert a.execution.status is b.execution.status
    assert (
        a.execution.elapsed_study_time_seconds
        == b.execution.elapsed_study_time_seconds
    )
    assert a.execution.paused_duration_seconds == b.execution.paused_duration_seconds
    assert a.execution.completed_step_ids == b.execution.completed_step_ids
    assert a.execution.metrics == b.execution.metrics
    assert a.execution.progress.completion_percentage == (
        b.execution.progress.completion_percentage
    )
    assert [e.kind for e in a.events] == [e.kind for e in b.events]
    assert [ev.evidence_id for ev in a.evidence] == [
        ev.evidence_id for ev in b.evidence
    ]


def test_event_sequences_monotonic(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    plan = make_plan()
    sequences: list[int] = []
    current = MissionExecutionEngine.start_execution(
        plan, mission_id, execution_id=execution_id, at=t0
    )
    assert current.ok and current.execution is not None
    sequences.append(current.events[0].sequence)

    for minutes, action in (
        (2, "step"),
        (3, "pause"),
        (5, "resume"),
        (8, "complete"),
    ):
        if action == "step":
            current = MissionExecutionEngine.complete_step(
                current.execution,
                MissionStepId("step-1"),
                at=at(t0, minutes=minutes),
            )
        elif action == "pause":
            current = MissionExecutionEngine.pause_execution(
                current.execution, at=at(t0, minutes=minutes)
            )
        elif action == "resume":
            current = MissionExecutionEngine.resume_execution(
                current.execution, at=at(t0, minutes=minutes)
            )
        else:
            current = MissionExecutionEngine.complete_execution(
                current.execution, at=at(t0, minutes=minutes)
            )
        assert current.ok and current.execution is not None
        sequences.append(current.events[0].sequence)

    assert sequences == sorted(sequences)
    assert sequences == list(range(1, len(sequences) + 1))
