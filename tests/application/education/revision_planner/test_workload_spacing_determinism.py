"""Workload balancing, spacing, splitting, and determinism tests."""

from __future__ import annotations

from datetime import date, datetime

from application.education.mission_generation import MissionPlan, MissionType
from application.education.revision_planner import (
    AdaptiveRevisionPlanner,
    ScheduleId,
    SpacingPolicy,
)
from application.education.revision_planner.services import (
    SessionAllocator,
    SpacingStrategy,
    WorkloadBalancer,
)
from tests.application.education.revision_planner.conftest import (
    default_constraints,
    make_mission,
    make_plan,
)


def test_long_missions_are_split_across_sessions(
    schedule_id: ScheduleId,
    start_date: date,
    generated_at: datetime,
) -> None:
    plan = make_plan(
        (
            make_mission(
                "long-1",
                mission_type=MissionType.CONSOLIDATE_KNOWLEDGE,
                duration_minutes=90,
                priority=0.80,
            ),
        ),
        generated_at=generated_at,
    )
    schedule = AdaptiveRevisionPlanner.create_schedule(
        plan,
        schedule_id=schedule_id,
        start_date=start_date,
        generated_at=generated_at,
        planning_constraints=default_constraints(
            maximum_session_minutes=45,
            preferred_session_minutes=30,
        ),
        horizon_days=14,
    )
    scheduled = schedule.scheduled_missions[0]
    assert len(scheduled.session_ids) >= 2
    assert scheduled.allocated_minutes == 90
    assert sum(
        s.estimated_duration_minutes
        for s in schedule.sessions
        if s.session_id in scheduled.session_ids
    ) == 90


def test_maintenance_missions_are_spaced(
    schedule_id: ScheduleId,
    start_date: date,
    generated_at: datetime,
) -> None:
    plan = make_plan(
        (
            make_mission(
                "m1",
                mission_type=MissionType.MAINTENANCE_REVIEW,
                duration_minutes=15,
                priority=0.30,
                competency="a",
            ),
            make_mission(
                "m2",
                mission_type=MissionType.MAINTENANCE_REVIEW,
                duration_minutes=15,
                priority=0.25,
                competency="b",
            ),
            make_mission(
                "m3",
                mission_type=MissionType.MAINTENANCE_REVIEW,
                duration_minutes=15,
                priority=0.20,
                competency="c",
            ),
            make_mission(
                "core",
                mission_type=MissionType.PRACTICE_QUESTIONS,
                duration_minutes=30,
                priority=0.90,
            ),
        ),
        generated_at=generated_at,
    )
    schedule = AdaptiveRevisionPlanner.create_schedule(
        plan,
        schedule_id=schedule_id,
        start_date=start_date,
        generated_at=generated_at,
        planning_constraints=default_constraints(
            spacing_policy=SpacingPolicy.DISTRIBUTED,
            rest_weekdays=(),
        ),
        horizon_days=14,
    )
    maintenance_dates = sorted(
        {
            m.scheduled_date
            for m in schedule.scheduled_missions
            if m.is_maintenance
        }
    )
    assert len(maintenance_dates) >= 2


def test_spacing_strategy_policies() -> None:
    from datetime import timedelta

    base = date(2026, 7, 27)
    study_dates = tuple(base + timedelta(days=offset) for offset in range(10))
    missions = (
        make_mission("a", mission_type=MissionType.MAINTENANCE_REVIEW),
        make_mission("b", mission_type=MissionType.MAINTENANCE_REVIEW),
        make_mission("c", mission_type=MissionType.MAINTENANCE_REVIEW),
    )
    compact = SpacingStrategy.target_dates(
        missions, study_dates=study_dates, policy=SpacingPolicy.COMPACT
    )
    balanced = SpacingStrategy.target_dates(
        missions, study_dates=study_dates, policy=SpacingPolicy.BALANCED
    )
    distributed = SpacingStrategy.target_dates(
        missions, study_dates=study_dates, policy=SpacingPolicy.DISTRIBUTED
    )
    assert compact[0] == study_dates[0]
    assert balanced[0] == study_dates[0]
    assert balanced[-1] == study_dates[-1]
    assert distributed[0] >= study_dates[0]


def test_workload_stays_within_daily_cap(
    mission_plan: MissionPlan,
    schedule_id: ScheduleId,
    start_date: date,
    generated_at: datetime,
) -> None:
    constraints = default_constraints(maximum_daily_study_minutes=60)
    schedule = AdaptiveRevisionPlanner.create_schedule(
        mission_plan,
        schedule_id=schedule_id,
        start_date=start_date,
        generated_at=generated_at,
        planning_constraints=constraints,
        horizon_days=21,
    )
    for day in schedule.study_days():
        assert day.active_allocated_minutes() <= 60


def test_rebalance_preserves_session_count(
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
    rebalanced = AdaptiveRevisionPlanner.rebalance(schedule, at=generated_at)
    assert len(rebalanced.sessions) == len(schedule.sessions)
    assert [s.sequence_index for s in rebalanced.active_sessions()] == list(
        range(1, len(rebalanced.active_sessions()) + 1)
    )


def test_create_schedule_is_deterministic(
    mission_plan: MissionPlan,
    schedule_id: ScheduleId,
    start_date: date,
    generated_at: datetime,
) -> None:
    constraints = default_constraints()
    a = AdaptiveRevisionPlanner.create_schedule(
        mission_plan,
        schedule_id=schedule_id,
        start_date=start_date,
        generated_at=generated_at,
        planning_constraints=constraints,
        horizon_days=14,
    )
    b = AdaptiveRevisionPlanner.create_schedule(
        mission_plan,
        schedule_id=schedule_id,
        start_date=start_date,
        generated_at=generated_at,
        planning_constraints=constraints,
        horizon_days=14,
    )
    assert [s.session_id.value for s in a.sessions] == [
        s.session_id.value for s in b.sessions
    ]
    assert [s.session_date for s in a.sessions] == [s.session_date for s in b.sessions]
    assert [s.start_time for s in a.sessions] == [s.start_time for s in b.sessions]
    assert [m.mission_id.value for m in a.scheduled_missions] == [
        m.mission_id.value for m in b.scheduled_missions
    ]
    assert a.produce_snapshot(captured_at=generated_at).summary == b.produce_snapshot(
        captured_at=generated_at
    ).summary


def test_high_priority_scheduled_early(
    schedule_id: ScheduleId,
    start_date: date,
    generated_at: datetime,
) -> None:
    plan = make_plan(
        (
            make_mission(
                "low",
                mission_type=MissionType.PRACTICE_QUESTIONS,
                priority=0.20,
                duration_minutes=30,
                competency="z",
            ),
            make_mission(
                "high",
                mission_type=MissionType.PRACTICE_QUESTIONS,
                priority=0.95,
                duration_minutes=30,
                competency="a",
            ),
        ),
        generated_at=generated_at,
    )
    schedule = AdaptiveRevisionPlanner.create_schedule(
        plan,
        schedule_id=schedule_id,
        start_date=start_date,
        generated_at=generated_at,
        planning_constraints=default_constraints(),
        horizon_days=7,
    )
    by_id = {m.mission_id.value: m for m in schedule.scheduled_missions}
    assert by_id["high"].scheduled_date <= by_id["low"].scheduled_date


def test_session_allocator_split_duration() -> None:
    chunks = SessionAllocator._split_duration(
        100,
        maximum_session_minutes=45,
        preferred_session_minutes=30,
    )
    assert sum(chunks) == 100
    assert all(c <= 45 for c in chunks)
    assert len(chunks) >= 3


def test_workload_balancer_selects_underfilled_day() -> None:
    from application.education.revision_planner.services.workload_balancer import (
        DayCapacity,
    )

    capacities = (
        DayCapacity(
            day_date=date(2026, 7, 27),
            available_minutes=120,
            allocated_minutes=100,
        ),
        DayCapacity(
            day_date=date(2026, 7, 28),
            available_minutes=120,
            allocated_minutes=10,
        ),
    )
    chosen = WorkloadBalancer.select_day(capacities, minutes=30)
    assert chosen is not None
    assert chosen.day_date == date(2026, 7, 28)
