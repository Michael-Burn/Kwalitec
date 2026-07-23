"""Progress composition tests for Adaptive Study Workspace (XP-004)."""

from __future__ import annotations

from application.student_experience.workspace import (
    QualityIndicatorKind,
    StudyWorkspaceService,
)
from tests.application.student_experience.workspace.conftest import (
    make_active_execution,
    make_full_inputs,
    make_multi_step_mission,
    make_plan,
)


def test_progress_includes_completion_time_and_remaining(
    service: StudyWorkspaceService,
) -> None:
    view = service.build_workspace(make_full_inputs())
    assert view.progress.available is True
    assert view.progress.completion_percent is not None
    assert view.progress.completion_percent > 0
    assert view.progress.time_invested_minutes == 10
    assert view.progress.remaining_work_minutes is not None
    assert view.progress.remaining_work_minutes >= 0
    assert "%" in view.progress.completion_label


def test_progress_quality_indicators_from_execution(
    service: StudyWorkspaceService,
) -> None:
    view = service.build_workspace(make_full_inputs())
    kinds = {item.kind for item in view.progress.quality_indicators}
    assert QualityIndicatorKind.COMPLETION_RATE in kinds
    assert QualityIndicatorKind.TIME_ON_TASK in kinds
    assert QualityIndicatorKind.CONFIDENCE_TREND in kinds


def test_progress_scales_with_completed_steps(
    service: StudyWorkspaceService,
) -> None:
    mission = make_multi_step_mission("mission-prog", steps=4, duration_minutes=40)
    plan = make_plan((mission,), plan_id="plan-prog")
    early = make_active_execution(
        plan,
        mission_id="mission-prog",
        completed_step_indexes=(1,),
        elapsed_seconds=300.0,
    )
    later = make_active_execution(
        plan,
        mission_id="mission-prog",
        execution_id="exec-later",
        completed_step_indexes=(1, 2, 3),
        elapsed_seconds=1200.0,
    )
    early_view = service.build_workspace(
        make_full_inputs(mission_plan=plan, mission_execution=early)
    )
    later_view = service.build_workspace(
        make_full_inputs(mission_plan=plan, mission_execution=later)
    )
    assert early_view.progress.completion_percent is not None
    assert later_view.progress.completion_percent is not None
    assert (
        later_view.progress.completion_percent
        > early_view.progress.completion_percent
    )
    assert (
        later_view.progress.time_invested_minutes
        > early_view.progress.time_invested_minutes
    )
