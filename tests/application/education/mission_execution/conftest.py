"""Shared factories for Mission Execution Engine tests."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from application.education.mission_execution import ExecutionId
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

STUDENT_ID = "student-001"
SUBJECT_ALGEBRA = "algebra"
COMPETENCY_LINEAR = "linear-equations"
COMPETENCY_QUADRATIC = "quadratic-equations"


@pytest.fixture
def t0() -> datetime:
    return datetime(2026, 7, 23, 12, 0, 0, tzinfo=UTC)


@pytest.fixture
def execution_id() -> ExecutionId:
    return ExecutionId("exec-001")


@pytest.fixture
def mission_id() -> MissionId:
    return MissionId("mission-001")


def at(base: datetime, *, minutes: int = 0, seconds: int = 0) -> datetime:
    return base + timedelta(minutes=minutes, seconds=seconds)


def make_step(
    step_id: str,
    *,
    order: int = 1,
    action: MissionStepAction = MissionStepAction.PRACTICE,
    minutes: int = 10,
    subject: str | None = SUBJECT_ALGEBRA,
    competency: str | None = COMPETENCY_LINEAR,
) -> MissionStep:
    return MissionStep(
        step_id=MissionStepId(step_id),
        action=action,
        order=order,
        estimated_minutes=minutes,
        subject_id=subject,
        competency_id=competency,
    )


def make_mission(
    mission_id: str = "mission-001",
    *,
    steps: tuple[MissionStep, ...] | None = None,
    subject: str | None = SUBJECT_ALGEBRA,
    competency: str | None = COMPETENCY_LINEAR,
) -> Mission:
    if steps is None:
        steps = (
            make_step("step-1", order=1, competency=competency),
            make_step("step-2", order=2, competency=COMPETENCY_QUADRATIC),
            make_step("step-3", order=3, competency=competency),
        )
    return Mission(
        mission_id=MissionId(mission_id),
        mission_type=MissionType.PRACTICE_QUESTIONS,
        objective=MissionObjective(
            code=MissionObjectiveCode.COMPLETE_PRACTICE,
            subject_id=subject,
            competency_id=competency,
        ),
        estimate=MissionEstimate(duration_minutes=30),
        ordering=MissionOrdering(rank=1, priority_magnitude=0.80),
        steps=steps,
        subject_id=subject,
        competency_id=competency,
        source_recommendation_ids=("r1",),
    )


def make_plan(
    *,
    plan_id: str = "plan-001",
    student_id: str = STUDENT_ID,
    missions: tuple[Mission, ...] | None = None,
    generated_at: datetime | None = None,
) -> MissionPlan:
    return MissionPlan(
        plan_id=MissionPlanId(plan_id),
        student_id=student_id,
        source_recommendation_set_id="recset-001",
        generated_at=generated_at
        or datetime(2026, 7, 23, 11, 0, 0, tzinfo=UTC),
        missions=missions or (make_mission(),),
    )
