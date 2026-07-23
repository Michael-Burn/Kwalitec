"""Quick actions composition tests."""

from __future__ import annotations

from datetime import timedelta

from application.education.mission_execution import ExecutionStatus
from application.education.mission_generation import MissionType
from application.education.revision_planner.enums import SessionStatus
from application.student_experience.home import QuickActionKind, StudentHomeService
from tests.application.student_experience.home.conftest import (
    TODAY,
    make_execution,
    make_full_inputs,
    make_history,
    make_mission,
    make_plan,
    make_schedule,
    make_session,
)


def _kinds(service: StudentHomeService, **overrides) -> set[QuickActionKind]:
    home = service.build_home(make_full_inputs(**overrides))
    return {action.kind for action in home.quick_actions.actions}


def test_start_todays_mission_action(service: StudentHomeService) -> None:
    kinds = _kinds(service)
    assert QuickActionKind.START_TODAYS_MISSION in kinds
    assert QuickActionKind.VIEW_SCHEDULE in kinds


def test_resume_paused_mission_action(service: StudentHomeService) -> None:
    plan = make_plan()
    execution = make_execution(plan, status=ExecutionStatus.PAUSED)
    kinds = _kinds(service, mission_plan=plan, current_execution=execution)
    assert QuickActionKind.RESUME_SESSION in kinds
    assert QuickActionKind.START_TODAYS_MISSION not in kinds


def test_continue_mission_action(service: StudentHomeService) -> None:
    plan = make_plan()
    execution = make_execution(plan, status=ExecutionStatus.RESUMED)
    kinds = _kinds(service, mission_plan=plan, current_execution=execution)
    assert QuickActionKind.CONTINUE_MISSION in kinds


def test_review_reflection_action(service: StudentHomeService) -> None:
    plan = make_plan()
    execution = make_execution(plan, status=ExecutionStatus.COMPLETED)
    kinds = _kinds(service, mission_plan=plan, current_execution=execution)
    assert QuickActionKind.REVIEW_REFLECTION in kinds


def test_review_yesterday_action(service: StudentHomeService) -> None:
    schedule = make_schedule(
        sessions=(
            make_session(
                session_id="session-y",
                session_date=TODAY - timedelta(days=1),
                mission_ids=("mission-001",),
                status=SessionStatus.COMPLETED,
            ),
            make_session(mission_ids=("mission-001",)),
        )
    )
    kinds = _kinds(service, schedule=schedule)
    assert QuickActionKind.REVIEW_YESTERDAY in kinds


def test_continue_revision_action(service: StudentHomeService) -> None:
    plan = make_plan(
        (
            make_mission("mission-001"),
            make_mission(
                "mission-rev",
                mission_type=MissionType.REVISION_SESSION,
                rank=2,
            ),
        )
    )
    kinds = _kinds(
        service,
        mission_plan=plan,
        execution_history=make_history(),
    )
    assert QuickActionKind.CONTINUE_REVISION in kinds
