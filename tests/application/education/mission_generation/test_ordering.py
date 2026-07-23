"""Priority ordering and prerequisite sequencing tests."""

from __future__ import annotations

from datetime import datetime

from application.education.mission_generation import (
    AdaptiveMissionGenerator,
    Mission,
    MissionEstimate,
    MissionId,
    MissionObjective,
    MissionObjectiveCode,
    MissionOrdering,
    MissionPlanId,
    MissionType,
)
from application.education.mission_generation.rules import OrderingRules
from domain.education.recommendation_engine import RecommendationCategory
from tests.application.education.mission_generation.conftest import (
    make_recommendation,
    make_recommendation_set,
)


def test_prioritise_orders_by_priority_then_type(
    plan_id: MissionPlanId, generated_at: datetime
) -> None:
    recommendations = (
        make_recommendation(
            recommendation_id="r1",
            category=RecommendationCategory.MAINTAIN_MASTERY,
            priority=0.35,
            rank=1,
            competency="a",
        ),
        make_recommendation(
            recommendation_id="r2",
            category=RecommendationCategory.STRENGTHEN_WEAK_AREA,
            priority=0.70,
            rank=2,
            competency="b",
            confidence=0.70,
        ),
        make_recommendation(
            recommendation_id="r3",
            category=RecommendationCategory.STUDY_PREREQUISITE,
            priority=0.90,
            rank=3,
            competency="c",
        ),
    )
    plan = AdaptiveMissionGenerator.generate(
        make_recommendation_set(recommendations),
        plan_id=plan_id,
        generated_at=generated_at,
    )
    ranks = [m.ordering.rank for m in plan.missions]
    assert ranks == list(range(1, len(plan.missions) + 1))
    assert plan.missions[0].mission_type is MissionType.REVISE_PREREQUISITE
    assert plan.missions[-1].mission_type is MissionType.MAINTENANCE_REVIEW


def test_prioritise_is_stable_for_equal_priority(
    plan_id: MissionPlanId, generated_at: datetime
) -> None:
    recommendations = (
        make_recommendation(
            recommendation_id="r1",
            category=RecommendationCategory.FOCUS_COMPETENCY,
            priority=0.75,
            competency="alpha",
        ),
        make_recommendation(
            recommendation_id="r2",
            category=RecommendationCategory.FOCUS_COMPETENCY,
            priority=0.75,
            competency="beta",
        ),
    )
    plan_a = AdaptiveMissionGenerator.generate(
        make_recommendation_set(recommendations),
        plan_id=plan_id,
        generated_at=generated_at,
    )
    plan_b = AdaptiveMissionGenerator.generate(
        make_recommendation_set(recommendations),
        plan_id=plan_id,
        generated_at=generated_at,
    )
    assert [m.mission_id for m in plan_a.missions] == [
        m.mission_id for m in plan_b.missions
    ]


def test_ensure_prerequisites_before_dependents_helper() -> None:
    practice = Mission(
        mission_id=MissionId("m-practice"),
        mission_type=MissionType.PRACTICE_QUESTIONS,
        objective=MissionObjective(code=MissionObjectiveCode.COMPLETE_PRACTICE),
        estimate=MissionEstimate(duration_minutes=20),
        ordering=MissionOrdering(rank=1, priority_magnitude=0.80),
        subject_id="algebra",
    )
    prereq = Mission(
        mission_id=MissionId("m-prereq"),
        mission_type=MissionType.REVISE_PREREQUISITE,
        objective=MissionObjective(code=MissionObjectiveCode.ADDRESS_PREREQUISITE),
        estimate=MissionEstimate(duration_minutes=20),
        ordering=MissionOrdering(rank=2, priority_magnitude=0.80),
        subject_id="algebra",
    )
    ordered = OrderingRules.ensure_prerequisites_before_dependents((practice, prereq))
    assert ordered[0].mission_type is MissionType.REVISE_PREREQUISITE
