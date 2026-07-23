"""Shared factories for Adaptive Revision Planner tests."""

from __future__ import annotations

from datetime import UTC, date, datetime, time

import pytest

from application.education.mission_generation import (
    Mission,
    MissionEstimate,
    MissionId,
    MissionObjective,
    MissionObjectiveCode,
    MissionOrdering,
    MissionPlan,
    MissionPlanId,
    MissionStep,
    MissionStepAction,
    MissionStepId,
    MissionType,
)
from application.education.revision_planner import (
    ExamTarget,
    ExecutionHistory,
    PlanningConstraints,
    ScheduleId,
    SpacingPolicy,
    StudentAvailability,
    Weekday,
)
from application.education.revision_planner.student_availability import (
    AvailabilityWindow,
)

STUDENT_ID = "student-001"
SUBJECT_ALGEBRA = "algebra"
COMPETENCY_LINEAR = "linear-equations"
COMPETENCY_QUADRATIC = "quadratic-equations"


@pytest.fixture
def generated_at() -> datetime:
    return datetime(2026, 7, 23, 12, 0, 0, tzinfo=UTC)


@pytest.fixture
def start_date() -> date:
    return date(2026, 7, 27)  # Monday


@pytest.fixture
def schedule_id() -> ScheduleId:
    return ScheduleId("sched-001")


@pytest.fixture
def plan_id() -> MissionPlanId:
    return MissionPlanId("plan-001")


def make_mission(
    mission_id: str = "mission-001",
    *,
    mission_type: MissionType = MissionType.PRACTICE_QUESTIONS,
    duration_minutes: int = 30,
    priority: float = 0.70,
    rank: int = 1,
    subject: str | None = SUBJECT_ALGEBRA,
    competency: str | None = COMPETENCY_LINEAR,
    objective_code: MissionObjectiveCode = MissionObjectiveCode.COMPLETE_PRACTICE,
) -> Mission:
    return Mission(
        mission_id=MissionId(mission_id),
        mission_type=mission_type,
        objective=MissionObjective(
            code=objective_code,
            subject_id=subject,
            competency_id=competency,
        ),
        estimate=MissionEstimate(duration_minutes=duration_minutes),
        ordering=MissionOrdering(rank=rank, priority_magnitude=priority),
        steps=(
            MissionStep(
                step_id=MissionStepId(f"{mission_id}:s1"),
                action=MissionStepAction.PRACTICE,
                order=1,
                estimated_minutes=duration_minutes,
                subject_id=subject,
                competency_id=competency,
            ),
        ),
        subject_id=subject,
        competency_id=competency,
    )


def make_plan(
    missions: tuple[Mission, ...] | list[Mission] = (),
    *,
    plan_id: str = "plan-001",
    student_id: str = STUDENT_ID,
    generated_at: datetime | None = None,
) -> MissionPlan:
    at = generated_at or datetime(2026, 7, 23, 12, 0, 0, tzinfo=UTC)
    return MissionPlan(
        plan_id=MissionPlanId(plan_id),
        student_id=student_id,
        source_recommendation_set_id="recset-001",
        generated_at=at,
        missions=tuple(missions),
    )


def make_availability(
    *,
    student_id: str = STUDENT_ID,
    days: tuple[date, ...] = (),
    minutes_per_day: int = 90,
    start: time = time(9, 0),
    end: time = time(12, 0),
) -> StudentAvailability:
    windows = tuple(
        AvailabilityWindow(
            day=day,
            start_time=start,
            end_time=end,
            available_minutes=minutes_per_day,
        )
        for day in days
    )
    return StudentAvailability(student_id=student_id, windows=windows)


def default_constraints(**overrides) -> PlanningConstraints:
    base = dict(
        maximum_daily_study_minutes=120,
        preferred_session_minutes=30,
        maximum_session_minutes=45,
        preferred_window_start=time(9, 0),
        preferred_window_end=time(17, 0),
        rest_weekdays=(Weekday.SUNDAY,),
        weekly_workload_minutes=600,
        spacing_policy=SpacingPolicy.BALANCED,
    )
    base.update(overrides)
    return PlanningConstraints(**base)


def sample_missions() -> tuple[Mission, ...]:
    return (
        make_mission(
            "m-prereq",
            mission_type=MissionType.REVISE_PREREQUISITE,
            duration_minutes=25,
            priority=0.95,
            rank=1,
            competency=COMPETENCY_LINEAR,
            objective_code=MissionObjectiveCode.ADDRESS_PREREQUISITE,
        ),
        make_mission(
            "m-practice",
            mission_type=MissionType.PRACTICE_QUESTIONS,
            duration_minutes=40,
            priority=0.80,
            rank=2,
            competency=COMPETENCY_QUADRATIC,
        ),
        make_mission(
            "m-long",
            mission_type=MissionType.CONSOLIDATE_KNOWLEDGE,
            duration_minutes=90,
            priority=0.65,
            rank=3,
            competency="functions",
            objective_code=MissionObjectiveCode.CONSOLIDATE_TARGET,
        ),
        make_mission(
            "m-maintain",
            mission_type=MissionType.MAINTENANCE_REVIEW,
            duration_minutes=20,
            priority=0.30,
            rank=4,
            competency="polynomials",
            objective_code=MissionObjectiveCode.MAINTAIN_TARGET,
        ),
        make_mission(
            "m-maintain-2",
            mission_type=MissionType.MAINTENANCE_REVIEW,
            duration_minutes=15,
            priority=0.25,
            rank=5,
            competency="calculus",
            objective_code=MissionObjectiveCode.MAINTAIN_TARGET,
        ),
    )


@pytest.fixture
def mission_plan(generated_at: datetime) -> MissionPlan:
    return make_plan(sample_missions(), generated_at=generated_at)


@pytest.fixture
def exam_target() -> ExamTarget:
    return ExamTarget(examination_id="exam-cs1", exam_date=date(2026, 8, 20))


@pytest.fixture
def empty_history() -> ExecutionHistory:
    return ExecutionHistory()
