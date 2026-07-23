"""Progress summary and progress card tests."""

from __future__ import annotations

from datetime import timedelta

from application.education.mission_execution import ExecutionStatus
from application.education.revision_planner.enums import SessionStatus
from application.student_experience.home import MasteryTrendLabel, StudentHomeService
from tests.application.student_experience.home.conftest import (
    TODAY,
    make_assessment,
    make_execution,
    make_full_inputs,
    make_history,
    make_plan,
    make_schedule,
    make_session,
)


def test_summarise_progress_from_assessment_and_history(
    service: StudentHomeService,
) -> None:
    summary = service.summarise_progress(
        make_full_inputs(
            assessment=make_assessment(overall_mastery=0.72),
            execution_history=make_history(
                completed=("mission-001", "mission-002"),
                abandoned=("mission-003",),
                in_progress=("mission-004",),
            ),
        )
    )
    assert summary.mastery_trend is MasteryTrendLabel.STEADY_PROGRESS
    assert summary.completed_missions == 2
    assert summary.abandoned_missions == 1
    assert summary.in_progress_missions == 1
    assert summary.knowledge_gap_count >= 1
    assert "steady progress" in summary.mastery_message.lower()


def test_hours_studied_from_completed_missions_and_active_execution(
    service: StudentHomeService,
) -> None:
    plan = make_plan()
    execution = make_execution(
        plan, status=ExecutionStatus.STARTED, elapsed_seconds=1800
    )
    summary = service.summarise_progress(
        make_full_inputs(
            mission_plan=plan,
            current_execution=execution,
            execution_history=make_history(completed=("mission-001",)),
        )
    )
    # 30 minutes completed estimate + 30 minutes elapsed = 1.0 hour
    assert summary.hours_studied == 1.0


def test_study_consistency_from_completed_sessions(
    service: StudentHomeService,
) -> None:
    schedule = make_schedule(
        sessions=(
            make_session(
                session_id="s1",
                session_date=TODAY - timedelta(days=1),
                status=SessionStatus.COMPLETED,
            ),
            make_session(
                session_id="s2",
                session_date=TODAY,
                status=SessionStatus.PLANNED,
            ),
        )
    )
    home = service.build_home(make_full_inputs(schedule=schedule))
    assert home.progress.study_consistency_percent == 50.0


def test_progress_without_assessment(service: StudentHomeService) -> None:
    summary = service.summarise_progress(
        make_full_inputs(assessment=None, evaluation=None)
    )
    assert summary.mastery_trend is MasteryTrendLabel.NOT_YET_ASSESSED
    assert "start studying" in summary.mastery_message.lower()
