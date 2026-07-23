"""Merge and split behaviour tests."""

from __future__ import annotations

from datetime import datetime

from application.education.mission_generation import (
    AdaptiveMissionGenerator,
    LearningPace,
    Mission,
    MissionEstimate,
    MissionId,
    MissionObjective,
    MissionObjectiveCode,
    MissionOrdering,
    MissionPlanId,
    MissionType,
    PlanningConstraints,
)
from domain.education.recommendation_engine import RecommendationCategory
from tests.application.education.mission_generation.conftest import (
    make_recommendation,
    make_recommendation_set,
)


def test_merge_similar_recommendations_same_target(
    plan_id: MissionPlanId, generated_at: datetime
) -> None:
    recommendations = (
        make_recommendation(
            recommendation_id="r1",
            category=RecommendationCategory.FOCUS_COMPETENCY,
            priority=0.75,
            competency="linear-equations",
        ),
        make_recommendation(
            recommendation_id="r2",
            category=RecommendationCategory.FOCUS_COMPETENCY,
            priority=0.70,
            competency="linear-equations",
        ),
    )
    groups = AdaptiveMissionGenerator.merge_similar_recommendations(recommendations)
    assert len(groups) == 1
    assert len(groups[0].recommendations) == 2
    assert groups[0].intent.priority_magnitude == 0.75

    plan = AdaptiveMissionGenerator.generate(
        make_recommendation_set(recommendations),
        plan_id=plan_id,
        generated_at=generated_at,
    )
    assert plan.mission_count() == 1
    assert set(plan.missions[0].source_recommendation_ids) == {"r1", "r2"}


def test_merge_does_not_merge_different_competencies(
    plan_id: MissionPlanId, generated_at: datetime
) -> None:
    recommendations = (
        make_recommendation(
            recommendation_id="r1",
            category=RecommendationCategory.FOCUS_COMPETENCY,
            competency="linear-equations",
        ),
        make_recommendation(
            recommendation_id="r2",
            category=RecommendationCategory.FOCUS_COMPETENCY,
            competency="quadratic-equations",
        ),
    )
    plan = AdaptiveMissionGenerator.generate(
        make_recommendation_set(recommendations),
        plan_id=plan_id,
        generated_at=generated_at,
    )
    assert plan.mission_count() == 2


def test_prerequisites_never_merge(
    plan_id: MissionPlanId, generated_at: datetime
) -> None:
    recommendations = (
        make_recommendation(
            recommendation_id="r1",
            category=RecommendationCategory.STUDY_PREREQUISITE,
            priority=0.90,
            competency="linear-equations",
        ),
        make_recommendation(
            recommendation_id="r2",
            category=RecommendationCategory.STUDY_PREREQUISITE,
            priority=0.88,
            competency="linear-equations",
        ),
    )
    plan = AdaptiveMissionGenerator.generate(
        make_recommendation_set(recommendations),
        plan_id=plan_id,
        generated_at=generated_at,
    )
    assert plan.mission_count() == 2


def test_split_large_missions() -> None:
    large = Mission(
        mission_id=MissionId("mission-large"),
        mission_type=MissionType.CHECKPOINT_PREPARATION,
        objective=MissionObjective(code=MissionObjectiveCode.PREPARE_CHECKPOINT),
        estimate=MissionEstimate(duration_minutes=90, workload_units=3.0),
        ordering=MissionOrdering(rank=1, priority_magnitude=0.80),
        subject_id="algebra",
        source_recommendation_ids=("r1",),
    )
    chunks = AdaptiveMissionGenerator.split_large_missions(
        (large,), maximum_mission_minutes=30
    )
    assert len(chunks) == 3
    assert sum(c.estimate.duration_minutes for c in chunks) == 90
    assert all(c.chunk_count == 3 for c in chunks)
    assert [c.chunk_index for c in chunks] == [1, 2, 3]
    assert all(c.source_recommendation_ids == ("r1",) for c in chunks)


def test_generate_splits_when_max_mission_minutes_low(
    plan_id: MissionPlanId, generated_at: datetime
) -> None:
    recommendations = (
        make_recommendation(
            recommendation_id="r1",
            category=RecommendationCategory.STRENGTHEN_WEAK_AREA,
            priority=0.85,
            confidence=0.70,
        ),
    )
    plan = AdaptiveMissionGenerator.generate(
        make_recommendation_set(recommendations),
        plan_id=plan_id,
        generated_at=generated_at,
        planning_constraints=PlanningConstraints(
            maximum_mission_minutes=10,
            learning_pace=LearningPace.SLOW,
        ),
    )
    assert plan.mission_count() >= 2
    assert all(m.estimate.duration_minutes <= 10 for m in plan.missions)


def test_split_noop_when_under_cap() -> None:
    small = Mission(
        mission_id=MissionId("mission-small"),
        mission_type=MissionType.MAINTENANCE_REVIEW,
        objective=MissionObjective(code=MissionObjectiveCode.MAINTAIN_TARGET),
        estimate=MissionEstimate(duration_minutes=10),
        ordering=MissionOrdering(rank=1, priority_magnitude=0.35),
    )
    result = AdaptiveMissionGenerator.split_large_missions(
        (small,), maximum_mission_minutes=30
    )
    assert len(result) == 1
    assert result[0].mission_id == small.mission_id
