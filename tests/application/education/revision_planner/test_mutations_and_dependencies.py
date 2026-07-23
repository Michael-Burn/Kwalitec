"""Dependency ordering, insertion, completion, and rescheduling tests."""

from __future__ import annotations

from datetime import date, datetime, time

from application.education.mission_generation import MissionId, MissionPlan, MissionType
from application.education.revision_planner import (
    AbandonmentPolicy,
    AdaptiveRevisionPlanner,
    CompletionMetrics,
    ExecutionHistory,
    ScheduledMissionStatus,
    ScheduleId,
    SessionStatus,
)
from application.education.revision_planner.services import DependencyResolver
from tests.application.education.revision_planner.conftest import (
    COMPETENCY_LINEAR,
    default_constraints,
    make_mission,
    make_plan,
    sample_missions,
)


def test_dependency_resolver_places_prerequisites_first() -> None:
    missions = (
        make_mission(
            "dep",
            mission_type=MissionType.PRACTICE_QUESTIONS,
            priority=0.99,
            competency=COMPETENCY_LINEAR,
        ),
        make_mission(
            "pre",
            mission_type=MissionType.REVISE_PREREQUISITE,
            priority=0.50,
            competency=COMPETENCY_LINEAR,
        ),
    )
    ordered = DependencyResolver.resolve(missions)
    assert ordered[0].mission_id.value == "pre"
    assert ordered[1].mission_id.value == "dep"


def test_schedule_preserves_prerequisite_before_dependent(
    schedule_id: ScheduleId,
    start_date: date,
    generated_at: datetime,
) -> None:
    plan = make_plan(
        (
            make_mission(
                "dep",
                mission_type=MissionType.PRACTICE_QUESTIONS,
                priority=0.99,
                duration_minutes=30,
            ),
            make_mission(
                "pre",
                mission_type=MissionType.REVISE_PREREQUISITE,
                priority=0.40,
                duration_minutes=30,
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
    assert by_id["pre"].scheduled_date <= by_id["dep"].scheduled_date
    if by_id["pre"].scheduled_date == by_id["dep"].scheduled_date:
        pre_sessions = [
            s
            for s in schedule.sessions
            if MissionId("pre") in s.scheduled_mission_ids
        ]
        dep_sessions = [
            s
            for s in schedule.sessions
            if MissionId("dep") in s.scheduled_mission_ids
        ]
        assert pre_sessions[0].start_time <= dep_sessions[0].start_time


def test_insert_new_mission_without_full_rebuild(
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
    original_session_ids = {s.session_id.value for s in schedule.sessions}
    new_mission = make_mission(
        "m-new",
        mission_type=MissionType.REVIEW_CONCEPT,
        duration_minutes=25,
        priority=0.55,
        competency="series",
    )
    updated = AdaptiveRevisionPlanner.insert_new_mission(
        schedule, new_mission, at=generated_at
    )
    assert updated.contains_mission(MissionId("m-new"))
    # Prior session identities are retained.
    assert original_session_ids <= {s.session_id.value for s in updated.sessions}
    assert len(updated.sessions) >= len(schedule.sessions)


def test_complete_session_marks_mission_completed(
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
    session = schedule.active_sessions()[0]
    metrics = CompletionMetrics(
        actual_duration_minutes=session.estimated_duration_minutes,
        missions_completed=1,
        objectives_met=1,
    )
    updated = AdaptiveRevisionPlanner.complete_session(
        schedule, session.session_id, completion_metrics=metrics, at=generated_at
    )
    completed = updated.session_by_id(session.session_id)
    assert completed is not None
    assert completed.status is SessionStatus.COMPLETED
    assert completed.completion_metrics == metrics
    for mission_id in session.scheduled_mission_ids:
        scheduled = next(
            m for m in updated.scheduled_missions if m.mission_id == mission_id
        )
        assert scheduled.status is ScheduledMissionStatus.COMPLETED


def test_cancel_and_reschedule(
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
    first, second = schedule.active_sessions()[0], schedule.active_sessions()[1]
    cancelled = AdaptiveRevisionPlanner.cancel_session(
        schedule, first.session_id, at=generated_at
    )
    assert cancelled.session_by_id(first.session_id).status is SessionStatus.CANCELLED

    target_date = date(2026, 7, 29)
    moved = AdaptiveRevisionPlanner.reschedule(
        cancelled,
        second.session_id,
        new_date=target_date,
        new_start_time=time(10, 0),
        at=generated_at,
    )
    relocated = moved.session_by_id(second.session_id)
    assert relocated is not None
    assert relocated.session_date == target_date
    assert relocated.start_time == time(10, 0)


def test_completed_missions_excluded_from_future_schedule(
    schedule_id: ScheduleId,
    start_date: date,
    generated_at: datetime,
) -> None:
    missions = sample_missions()
    plan = make_plan(missions, generated_at=generated_at)
    history = ExecutionHistory(
        completed_mission_ids=(MissionId("m-practice"),),
    )
    schedule = AdaptiveRevisionPlanner.create_schedule(
        plan,
        schedule_id=schedule_id,
        start_date=start_date,
        generated_at=generated_at,
        planning_constraints=default_constraints(),
        execution_history=history,
        horizon_days=14,
    )
    scheduled_ids = {m.mission_id.value for m in schedule.scheduled_missions}
    assert "m-practice" not in scheduled_ids
    assert "m-prereq" in scheduled_ids


def test_abandoned_missions_rescheduled_by_policy(
    schedule_id: ScheduleId,
    start_date: date,
    generated_at: datetime,
) -> None:
    plan = make_plan(sample_missions(), generated_at=generated_at)
    history = ExecutionHistory(abandoned_mission_ids=(MissionId("m-long"),))
    early = AdaptiveRevisionPlanner.create_schedule(
        plan,
        schedule_id=schedule_id,
        start_date=start_date,
        generated_at=generated_at,
        planning_constraints=default_constraints(
            abandonment_policy=AbandonmentPolicy.RESCHEDULE_EARLY
        ),
        execution_history=history,
        horizon_days=14,
    )
    assert early.contains_mission(MissionId("m-long"))

    dropped = AdaptiveRevisionPlanner.create_schedule(
        plan,
        schedule_id=ScheduleId("sched-drop"),
        start_date=start_date,
        generated_at=generated_at,
        planning_constraints=default_constraints(
            abandonment_policy=AbandonmentPolicy.DROP
        ),
        execution_history=history,
        horizon_days=14,
    )
    assert not dropped.contains_mission(MissionId("m-long"))


def test_replan_schedule(
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
    history = ExecutionHistory(completed_mission_ids=(MissionId("m-prereq"),))
    replanned = AdaptiveRevisionPlanner.replan_schedule(
        schedule,
        mission_plan,
        generated_at=generated_at,
        planning_constraints=default_constraints(),
        execution_history=history,
    )
    assert not replanned.contains_mission(MissionId("m-prereq"))
    assert replanned.schedule_id == schedule_id
