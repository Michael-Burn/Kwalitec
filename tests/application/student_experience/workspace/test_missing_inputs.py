"""Missing optional inputs degrade gracefully for Study Workspace (XP-004)."""

from __future__ import annotations

from application.student_experience.workspace import (
    SessionPresence,
    StudyWorkspaceService,
    TimerDisplayState,
)
from tests.application.student_experience.home.conftest import (
    make_mission,
    make_plan,
    make_schedule,
    make_session,
)
from tests.application.student_experience.workspace.conftest import make_empty_inputs


def test_empty_inputs_produce_unavailable_session(
    service: StudyWorkspaceService,
) -> None:
    view = service.build_workspace(make_empty_inputs())
    assert view.current_session.available is False
    assert view.current_session.presence is SessionPresence.UNAVAILABLE
    assert view.mission.available is False
    assert view.objectives.has_objectives is False
    assert view.resources.has_resources is False
    assert view.progress.available is False
    assert view.focus.has_prompts is False
    assert view.session_timer.display_state is TimerDisplayState.UNAVAILABLE
    assert view.completion.available is True
    preview = view.completion.next_session_preview.lower()
    assert "will appear" in preview or "not" in preview or "schedule" in preview


def test_plan_without_session_still_projects_mission(
    service: StudyWorkspaceService,
) -> None:
    plan = make_plan((make_mission("mission-solo"),))
    view = service.build_workspace(make_empty_inputs(mission_plan=plan))
    assert view.mission.available is True
    assert view.current_session.available is True
    assert view.objectives.has_objectives is True
    assert view.session_timer.available is True


def test_schedule_without_execution_resolves_todays_session(
    service: StudyWorkspaceService,
) -> None:
    plan = make_plan((make_mission("mission-sched"),))
    schedule = make_schedule(
        sessions=(make_session(mission_ids=("mission-sched",)),),
        plan_id=plan.plan_id.value,
    )
    view = service.build_workspace(
        make_empty_inputs(schedule=schedule, mission_plan=plan, current_session=None)
    )
    assert view.current_session.available is True
    assert view.current_session.session_id == "session-001"
    assert view.mission.available is True
