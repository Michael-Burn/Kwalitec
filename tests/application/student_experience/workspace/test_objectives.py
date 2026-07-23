"""Objectives composition tests for Adaptive Study Workspace (XP-004)."""

from __future__ import annotations

from application.education.mission_execution import (
    ExecutionId,
    ExecutionStatus,
    MissionExecution,
)
from application.education.mission_generation import MissionId, MissionObjectiveCode
from application.education.revision_planner.enums import SessionStatus
from application.student_experience.workspace import (
    ObjectiveStatus,
    StudyWorkspaceService,
)
from tests.application.student_experience.home.conftest import make_session
from tests.application.student_experience.workspace.conftest import (
    AS_OF,
    TODAY,
    make_active_execution,
    make_empty_inputs,
    make_full_inputs,
    make_multi_step_mission,
    make_plan,
)


def test_objectives_ordered_with_current_completed_remaining(
    service: StudyWorkspaceService,
) -> None:
    view = service.build_workspace(make_full_inputs())
    assert view.objectives.has_objectives is True
    assert len(view.objectives.items) == 3
    assert view.objectives.current is not None
    assert view.objectives.current.status is ObjectiveStatus.CURRENT
    assert len(view.objectives.completed) == 1
    assert view.objectives.completed[0].status is ObjectiveStatus.COMPLETED
    assert len(view.objectives.remaining) >= 1
    orders = [item.order for item in view.objectives.items]
    assert orders == sorted(orders)


def test_objectives_from_session_codes_without_execution(
    service: StudyWorkspaceService,
) -> None:
    session = make_session(
        session_id="session-obj",
        session_date=TODAY,
        mission_ids=("mission-ghost",),
        status=SessionStatus.PLANNED,
    )
    # StudySession requires objectives to be MissionObjectiveCode values —
    # rebuild via dataclass replace pattern from make_session fields.
    from application.education.mission_generation import MissionId as Mid
    from application.education.revision_planner.ids import SessionId
    from application.education.revision_planner.models.study_session import StudySession

    session = StudySession(
        session_id=SessionId("session-obj"),
        session_date=TODAY,
        start_time=session.start_time,
        end_time=session.end_time,
        estimated_duration_minutes=30,
        scheduled_mission_ids=(Mid("mission-ghost"),),
        objectives=(
            MissionObjectiveCode.COMPLETE_PRACTICE,
            MissionObjectiveCode.REVIEW_TARGET,
        ),
        status=SessionStatus.PLANNED,
    )
    view = service.build_workspace(
        make_empty_inputs(current_session=session, mission_plan=None)
    )
    assert view.objectives.has_objectives is True
    assert len(view.objectives.items) == 2
    assert view.objectives.current is not None
    assert view.objectives.current.label == "Complete practice"
    assert view.objectives.remaining[1].label == "Review"


def test_all_steps_completed_marks_objectives_complete(
    service: StudyWorkspaceService,
) -> None:
    mission = make_multi_step_mission("mission-done", steps=2)
    plan = make_plan((mission,), plan_id="plan-done")
    execution = MissionExecution.plan_execution(
        execution_id=ExecutionId("exec-done"),
        mission_plan=plan,
        mission_id=MissionId("mission-done"),
    )
    completed = tuple(step.step_id for step in execution.mission.steps)
    execution = execution.with_updates(
        status=ExecutionStatus.COMPLETED,
        started_at=AS_OF,
        finished_at=AS_OF,
        last_active_at=AS_OF,
        elapsed_study_time_seconds=1800.0,
        completed_step_ids=completed,
        current_step_id=None,
    )
    view = service.build_workspace(
        make_full_inputs(mission_plan=plan, mission_execution=execution)
    )
    assert len(view.objectives.completed) == 2
    assert view.objectives.current is None
    assert "complete" in view.objectives.summary.lower()


def test_active_execution_progresses_current_step(
    service: StudyWorkspaceService,
) -> None:
    mission = make_multi_step_mission("mission-mid", steps=3)
    plan = make_plan((mission,), plan_id="plan-mid")
    execution = make_active_execution(
        plan,
        mission_id="mission-mid",
        completed_step_indexes=(1, 2),
    )
    view = service.build_workspace(
        make_full_inputs(mission_plan=plan, mission_execution=execution)
    )
    assert view.objectives.current is not None
    assert view.objectives.current.order == 3
    assert len(view.objectives.completed) == 2
