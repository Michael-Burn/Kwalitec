"""Schedule generation, weekly, and daily planning tests."""

from __future__ import annotations

from datetime import date, datetime

from application.education.mission_generation import MissionPlan
from application.education.revision_planner import (
    AdaptiveRevisionPlanner,
    DayKind,
    ExamTarget,
    ScheduleId,
    SessionStatus,
    SpacingPolicy,
    Weekday,
)
from tests.application.education.revision_planner.conftest import (
    default_constraints,
    make_availability,
    make_plan,
    sample_missions,
)


def test_create_schedule_generates_sessions(
    mission_plan: MissionPlan,
    schedule_id: ScheduleId,
    start_date: date,
    generated_at: datetime,
) -> None:
    schedule = AdaptiveRevisionPlanner.create_schedule(
        mission_plan,
        schedule_id=schedule_id,
        start_date=start_date,
        generated_at=generated_at,
        planning_constraints=default_constraints(),
        horizon_days=14,
    )
    assert schedule.schedule_id == schedule_id
    assert schedule.student_id == mission_plan.student_id
    assert schedule.source_plan_id == mission_plan.plan_id
    assert len(schedule.sessions) >= 1
    assert len(schedule.scheduled_missions) >= 1
    assert all(s.status is SessionStatus.PLANNED for s in schedule.active_sessions())
    assert schedule.produce_summary().session_count == len(schedule.active_sessions())


def test_create_schedule_respects_rest_weekdays(
    mission_plan: MissionPlan,
    schedule_id: ScheduleId,
    start_date: date,
    generated_at: datetime,
) -> None:
    constraints = default_constraints(rest_weekdays=(Weekday.SATURDAY, Weekday.SUNDAY))
    schedule = AdaptiveRevisionPlanner.create_schedule(
        mission_plan,
        schedule_id=schedule_id,
        start_date=start_date,
        generated_at=generated_at,
        planning_constraints=constraints,
        horizon_days=14,
    )
    for day in schedule.days:
        if day.day_date.isoweekday() in (6, 7):
            assert day.kind is DayKind.REST
            assert day.active_allocated_minutes() == 0


def test_create_schedule_honours_exam_target(
    mission_plan: MissionPlan,
    schedule_id: ScheduleId,
    start_date: date,
    generated_at: datetime,
) -> None:
    exam = ExamTarget(examination_id="exam-1", exam_date=date(2026, 8, 5))
    schedule = AdaptiveRevisionPlanner.create_schedule(
        mission_plan,
        schedule_id=schedule_id,
        start_date=start_date,
        generated_at=generated_at,
        planning_constraints=default_constraints(),
        exam_target=exam,
    )
    assert schedule.end_date == date(2026, 8, 4)
    assert schedule.produce_summary().utilises_exam_deadline is True
    exam_day = schedule.day_for(exam.exam_date)
    # Exam date itself is outside the schedule horizon (ends day before).
    assert exam_day is None or exam_day.kind is DayKind.EXAM


def test_schedule_week(
    mission_plan: MissionPlan,
    schedule_id: ScheduleId,
    start_date: date,
    generated_at: datetime,
) -> None:
    schedule = AdaptiveRevisionPlanner.schedule_week(
        mission_plan,
        schedule_id=schedule_id,
        week_start=start_date,
        generated_at=generated_at,
        planning_constraints=default_constraints(),
    )
    assert schedule.start_date == start_date
    assert schedule.end_date == date(2026, 8, 2)
    assert schedule.day_count() == 7


def test_schedule_day(
    mission_plan: MissionPlan,
    schedule_id: ScheduleId,
    start_date: date,
    generated_at: datetime,
) -> None:
    schedule = AdaptiveRevisionPlanner.schedule_day(
        mission_plan,
        schedule_id=schedule_id,
        day=start_date,
        generated_at=generated_at,
        planning_constraints=default_constraints(),
    )
    assert schedule.start_date == start_date
    assert schedule.end_date == start_date
    assert schedule.day_count() == 1


def test_availability_windows_constrain_capacity(
    schedule_id: ScheduleId,
    start_date: date,
    generated_at: datetime,
) -> None:
    plan = make_plan(sample_missions(), generated_at=generated_at)
    availability = make_availability(
        days=(start_date, date(2026, 7, 28)),
        minutes_per_day=60,
    )
    schedule = AdaptiveRevisionPlanner.create_schedule(
        plan,
        schedule_id=schedule_id,
        start_date=start_date,
        generated_at=generated_at,
        availability=availability,
        planning_constraints=default_constraints(),
        horizon_days=7,
    )
    monday = schedule.day_for(start_date)
    assert monday is not None
    assert monday.available_minutes == 60
    assert monday.active_allocated_minutes() <= 60


def test_empty_plan_produces_empty_sessions(
    schedule_id: ScheduleId,
    start_date: date,
    generated_at: datetime,
) -> None:
    plan = make_plan((), generated_at=generated_at)
    schedule = AdaptiveRevisionPlanner.create_schedule(
        plan,
        schedule_id=schedule_id,
        start_date=start_date,
        generated_at=generated_at,
        planning_constraints=default_constraints(),
        horizon_days=7,
    )
    assert schedule.sessions == ()
    assert schedule.scheduled_missions == ()
    assert schedule.day_count() == 7


def test_snapshot_and_calendar_projection(
    mission_plan: MissionPlan,
    schedule_id: ScheduleId,
    start_date: date,
    generated_at: datetime,
) -> None:
    schedule = AdaptiveRevisionPlanner.create_schedule(
        mission_plan,
        schedule_id=schedule_id,
        start_date=start_date,
        generated_at=generated_at,
        planning_constraints=default_constraints(spacing_policy=SpacingPolicy.BALANCED),
        horizon_days=10,
    )
    snapshot = AdaptiveRevisionPlanner.produce_snapshot(
        schedule, captured_at=generated_at
    )
    assert snapshot.schedule_id == schedule_id
    assert snapshot.summary.mission_count >= 1
    assert snapshot.calendar.day_count() == schedule.day_count()
    assert snapshot.metrics.total_sessions == len(schedule.sessions)
