"""Determinism and snapshot fidelity tests."""

from __future__ import annotations

from datetime import datetime

from application.education.mission_generation import (
    AdaptiveMissionGenerator,
    LearningPace,
    MissionPlanId,
    PlanningConstraints,
)
from domain.education.recommendation_engine import RecommendationCategory
from tests.application.education.mission_generation.conftest import (
    blocking_constraint,
    make_recommendation,
    make_recommendation_set,
    prerequisite_constraint,
)


def _diverse_set():
    return make_recommendation_set(
        (
            make_recommendation(
                recommendation_id="r1",
                category=RecommendationCategory.STUDY_PREREQUISITE,
                priority=0.90,
                competency="linear-equations",
            ),
            make_recommendation(
                recommendation_id="r2",
                category=RecommendationCategory.FOCUS_COMPETENCY,
                priority=0.75,
                competency="quadratic-equations",
            ),
            make_recommendation(
                recommendation_id="r3",
                category=RecommendationCategory.MAINTAIN_MASTERY,
                priority=0.35,
                competency="functions",
            ),
            make_recommendation(
                recommendation_id="r4",
                category=RecommendationCategory.INCREASE_REVISION_FREQUENCY,
                priority=0.60,
                competency="polynomials",
            ),
            make_recommendation(
                recommendation_id="r5",
                category=RecommendationCategory.DELAY_ADVANCED_TOPIC,
                priority=0.72,
                competency="calculus",
            ),
        ),
        constraints=(blocking_constraint(), prerequisite_constraint()),
    )


def test_generate_is_deterministic(
    plan_id: MissionPlanId, generated_at: datetime
) -> None:
    constraints = PlanningConstraints(
        available_study_minutes=90,
        learning_pace=LearningPace.NORMAL,
        maximum_mission_minutes=30,
        target_examination="exam-1",
    )
    recommendation_set = _diverse_set()
    plan_a = AdaptiveMissionGenerator.generate(
        recommendation_set,
        plan_id=plan_id,
        generated_at=generated_at,
        planning_constraints=constraints,
    )
    plan_b = AdaptiveMissionGenerator.generate(
        recommendation_set,
        plan_id=plan_id,
        generated_at=generated_at,
        planning_constraints=constraints,
    )
    assert plan_a == plan_b
    assert [m.mission_id.value for m in plan_a.missions] == [
        m.mission_id.value for m in plan_b.missions
    ]
    assert [m.estimate.duration_minutes for m in plan_a.missions] == [
        m.estimate.duration_minutes for m in plan_b.missions
    ]


def test_snapshot_mirrors_plan(
    plan_id: MissionPlanId, generated_at: datetime
) -> None:
    plan = AdaptiveMissionGenerator.generate(
        _diverse_set(),
        plan_id=plan_id,
        generated_at=generated_at,
    )
    snapshot = AdaptiveMissionGenerator.produce_snapshot(plan)
    assert snapshot.plan_id == plan.plan_id
    assert snapshot.student_id == plan.student_id
    assert snapshot.source_recommendation_set_id == plan.source_recommendation_set_id
    assert snapshot.generated_at == plan.generated_at
    assert snapshot.missions == plan.missions
    assert snapshot.constraints == plan.constraints
    assert snapshot.summary == plan.produce_summary()


def test_daily_plan_default_cap_is_deterministic(
    plan_id: MissionPlanId, generated_at: datetime
) -> None:
    recommendation_set = _diverse_set()
    a = AdaptiveMissionGenerator.generate_daily_plan(
        recommendation_set, plan_id=plan_id, generated_at=generated_at
    )
    b = AdaptiveMissionGenerator.generate_daily_plan(
        recommendation_set, plan_id=plan_id, generated_at=generated_at
    )
    assert a == b
