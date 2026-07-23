"""Primary focus selection tests."""

from __future__ import annotations

from datetime import timedelta

from application.education.mission_execution import ExecutionStatus
from application.education.mission_generation import MissionType
from application.student_experience.home import FocusActionKind, StudentHomeService
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


def test_focus_prefers_paused_execution(service: StudentHomeService) -> None:
    plan = make_plan()
    execution = make_execution(plan, status=ExecutionStatus.PAUSED)
    focus = service.determine_primary_focus(
        make_full_inputs(mission_plan=plan, current_execution=execution)
    )
    assert focus.action_kind is FocusActionKind.RESUME_SESSION
    assert focus.has_focus is True
    assert focus.mission_id == "mission-001"
    assert focus.action_label == "Resume Session"


def test_focus_continues_active_execution(service: StudentHomeService) -> None:
    plan = make_plan()
    execution = make_execution(plan, status=ExecutionStatus.STARTED)
    focus = service.determine_primary_focus(
        make_full_inputs(mission_plan=plan, current_execution=execution)
    )
    assert focus.action_kind is FocusActionKind.CONTINUE_MISSION
    assert focus.action_label == "Continue Mission"


def test_focus_reviews_reflection_after_completion(service: StudentHomeService) -> None:
    plan = make_plan()
    execution = make_execution(plan, status=ExecutionStatus.COMPLETED)
    focus = service.determine_primary_focus(
        make_full_inputs(mission_plan=plan, current_execution=execution)
    )
    assert focus.action_kind is FocusActionKind.REVIEW_REFLECTION
    assert focus.action_label == "Review Reflection"


def test_focus_prepares_checkpoint(service: StudentHomeService) -> None:
    plan = make_plan(
        (
            make_mission(
                "mission-checkpoint",
                rank=1,
                mission_type=MissionType.CHECKPOINT_PREPARATION,
                competency="bayes-theorem",
            ),
        )
    )
    schedule = make_schedule(
        sessions=(make_session(mission_ids=("mission-checkpoint",)),)
    )
    focus = service.determine_primary_focus(
        make_full_inputs(mission_plan=plan, schedule=schedule)
    )
    assert focus.action_kind is FocusActionKind.PREPARE_CHECKPOINT
    assert focus.action_label == "Prepare Checkpoint"


def test_focus_uses_todays_scheduled_mission(service: StudentHomeService) -> None:
    plan = make_plan(
        (
            make_mission("mission-today", rank=1, competency="bayes-theorem"),
            make_mission("mission-later", rank=2, competency="linear-equations"),
        )
    )
    schedule = make_schedule(
        sessions=(
            make_session(mission_ids=("mission-today",)),
            make_session(
                session_id="session-002",
                session_date=TODAY + timedelta(days=1),
                mission_ids=("mission-later",),
            ),
        )
    )
    focus = service.determine_primary_focus(
        make_full_inputs(mission_plan=plan, schedule=schedule)
    )
    assert focus.action_kind is FocusActionKind.START_MISSION
    assert focus.mission_id == "mission-today"
    assert focus.estimated_duration_minutes == 30
    assert focus.study_objective is not None


def test_focus_falls_back_to_next_pending_mission(service: StudentHomeService) -> None:
    plan = make_plan(
        (
            make_mission("mission-done", rank=1),
            make_mission(
                "mission-next",
                rank=2,
                mission_type=MissionType.REVIEW_CONCEPT,
                competency="variance",
            ),
        )
    )
    focus = service.determine_primary_focus(
        make_full_inputs(
            mission_plan=plan,
            schedule=None,
            execution_history=make_history(completed=("mission-done",)),
        )
    )
    assert focus.mission_id == "mission-next"
    assert focus.action_kind is FocusActionKind.START_MISSION


def test_focus_view_schedule_when_no_missions(service: StudentHomeService) -> None:
    focus = service.determine_primary_focus(
        make_full_inputs(mission_plan=make_plan(()), schedule=make_schedule())
    )
    assert focus.has_focus is False
    assert focus.action_kind is FocusActionKind.VIEW_SCHEDULE


def test_focus_none_when_empty(service: StudentHomeService) -> None:
    from application.student_experience.home import HomeInputs
    from tests.application.student_experience.home.conftest import AS_OF, STUDENT_ID

    focus = service.determine_primary_focus(
        HomeInputs(student_id=STUDENT_ID, as_of=AS_OF)
    )
    assert focus.action_kind is FocusActionKind.NONE
    assert focus.has_focus is False
