"""Constraint handling and duration estimation tests."""

from __future__ import annotations

from datetime import datetime

import pytest

from application.education.mission_generation import (
    AdaptiveMissionGenerator,
    LearningPace,
    MissionConstraintKind,
    MissionDurationBand,
    MissionInvariantViolation,
    MissionPlanId,
    MissionRecurrenceBand,
    MissionType,
    PlanningConstraints,
)
from domain.education.recommendation_engine import RecommendationCategory
from tests.application.education.mission_generation.conftest import (
    blocking_constraint,
    make_recommendation,
    make_recommendation_set,
    prerequisite_constraint,
)


def test_planning_constraints_projected(
    plan_id: MissionPlanId, generated_at: datetime
) -> None:
    constraints = PlanningConstraints(
        available_study_minutes=45,
        maximum_daily_workload_minutes=60,
        target_examination="AP-Calculus",
        preferred_mission_types=(MissionType.PRACTICE_QUESTIONS,),
        learning_pace=LearningPace.FAST,
    )
    plan = AdaptiveMissionGenerator.generate(
        make_recommendation_set((make_recommendation(),)),
        plan_id=plan_id,
        generated_at=generated_at,
        planning_constraints=constraints,
    )
    kinds = {c.kind for c in plan.constraints}
    assert MissionConstraintKind.RESPECT_AVAILABLE_TIME in kinds
    assert MissionConstraintKind.LIMIT_DAILY_WORKLOAD in kinds
    assert MissionConstraintKind.TARGET_EXAMINATION in kinds
    assert MissionConstraintKind.PREFER_MISSION_TYPE in kinds


def test_recommendation_constraints_projected(
    plan_id: MissionPlanId, generated_at: datetime
) -> None:
    plan = AdaptiveMissionGenerator.generate(
        make_recommendation_set(
            (make_recommendation(),),
            constraints=(blocking_constraint(), prerequisite_constraint()),
        ),
        plan_id=plan_id,
        generated_at=generated_at,
    )
    kinds = {c.kind for c in plan.constraints}
    assert MissionConstraintKind.BLOCK_ADVANCEMENT in kinds
    assert MissionConstraintKind.REQUIRE_PREREQUISITE_FIRST in kinds


def test_available_time_caps_missions(
    plan_id: MissionPlanId, generated_at: datetime
) -> None:
    recommendations = tuple(
        make_recommendation(
            recommendation_id=f"r{i}",
            category=RecommendationCategory.STRENGTHEN_WEAK_AREA,
            priority=0.90 - i * 0.05,
            competency=f"comp-{i}",
            confidence=0.70,
        )
        for i in range(1, 6)
    )
    plan = AdaptiveMissionGenerator.generate(
        make_recommendation_set(recommendations),
        plan_id=plan_id,
        generated_at=generated_at,
        planning_constraints=PlanningConstraints(available_study_minutes=30),
    )
    assert plan.total_duration_minutes() <= 30 or plan.mission_count() == 1


def test_estimate_duration_bands_and_pace() -> None:
    short = AdaptiveMissionGenerator.estimate_duration(
        MissionType.MAINTENANCE_REVIEW,
        learning_pace=LearningPace.FAST,
    )
    long = AdaptiveMissionGenerator.estimate_duration(
        MissionType.CHECKPOINT_PREPARATION,
        learning_pace=LearningPace.SLOW,
    )
    assert short.duration_band is MissionDurationBand.SHORT
    assert long.duration_minutes > short.duration_minutes
    assert long.duration_band in {
        MissionDurationBand.MEDIUM,
        MissionDurationBand.LONG,
    }


def test_estimate_duration_merge_factor() -> None:
    single = AdaptiveMissionGenerator.estimate_duration(
        MissionType.PRACTICE_QUESTIONS, source_count=1
    )
    merged = AdaptiveMissionGenerator.estimate_duration(
        MissionType.PRACTICE_QUESTIONS, source_count=3
    )
    assert merged.duration_minutes > single.duration_minutes


def test_sessions_per_week_by_recurrence() -> None:
    from application.education.mission_generation import DurationRules

    assert DurationRules.sessions_per_week(MissionRecurrenceBand.INCREASED) == 4
    assert DurationRules.sessions_per_week(MissionRecurrenceBand.NORMAL) == 2
    assert DurationRules.sessions_per_week(MissionRecurrenceBand.REDUCED) == 1


def test_planning_constraints_validation() -> None:
    with pytest.raises(MissionInvariantViolation):
        PlanningConstraints(available_study_minutes=0)
    with pytest.raises(MissionInvariantViolation):
        PlanningConstraints(maximum_daily_workload_minutes=-1)
    with pytest.raises(MissionInvariantViolation):
        PlanningConstraints(maximum_mission_minutes=0)


def test_effective_daily_cap_uses_tightest() -> None:
    constraints = PlanningConstraints(
        available_study_minutes=40,
        maximum_daily_workload_minutes=60,
    )
    assert constraints.effective_daily_cap_minutes() == 40
