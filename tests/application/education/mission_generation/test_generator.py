"""Core Adaptive Mission Generator behaviour tests."""

from __future__ import annotations

from datetime import datetime

from application.education.mission_generation import (
    AdaptiveMissionGenerator,
    LearningPace,
    MissionConstraintKind,
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


def test_generate_empty_set(
    plan_id: MissionPlanId, generated_at: datetime
) -> None:
    plan = AdaptiveMissionGenerator.generate(
        make_recommendation_set(),
        plan_id=plan_id,
        generated_at=generated_at,
    )
    assert plan.is_empty()
    assert plan.mission_count() == 0
    assert plan.produce_summary().is_empty()


def test_generate_maps_categories_to_mission_types(
    plan_id: MissionPlanId, generated_at: datetime
) -> None:
    recommendations = (
        make_recommendation(
            recommendation_id="r1",
            category=RecommendationCategory.STUDY_PREREQUISITE,
            priority=0.90,
            rank=1,
            competency="linear-equations",
        ),
        make_recommendation(
            recommendation_id="r2",
            category=RecommendationCategory.MAINTAIN_MASTERY,
            priority=0.35,
            rank=2,
            competency="quadratic-equations",
        ),
        make_recommendation(
            recommendation_id="r3",
            category=RecommendationCategory.FOCUS_COMPETENCY,
            priority=0.75,
            rank=3,
            competency="functions",
        ),
        make_recommendation(
            recommendation_id="r4",
            category=RecommendationCategory.CONSOLIDATE_KNOWLEDGE,
            priority=0.55,
            rank=4,
            competency="polynomials",
        ),
        make_recommendation(
            recommendation_id="r5",
            category=RecommendationCategory.PREPARE_ASSESSMENT,
            priority=0.58,
            rank=5,
            competency=None,
            checkpoint_id="checkpoint-001",
        ),
    )
    plan = AdaptiveMissionGenerator.generate(
        make_recommendation_set(recommendations),
        plan_id=plan_id,
        generated_at=generated_at,
    )
    types = {m.mission_type for m in plan.missions}
    assert MissionType.REVISE_PREREQUISITE in types
    assert MissionType.MAINTENANCE_REVIEW in types
    assert MissionType.PRACTICE_QUESTIONS in types
    assert MissionType.CONSOLIDATE_KNOWLEDGE in types
    assert MissionType.CHECKPOINT_PREPARATION in types


def test_delay_advanced_topic_produces_no_mission(
    plan_id: MissionPlanId, generated_at: datetime
) -> None:
    recommendations = (
        make_recommendation(
            recommendation_id="r1",
            category=RecommendationCategory.DELAY_ADVANCED_TOPIC,
            priority=0.72,
        ),
    )
    plan = AdaptiveMissionGenerator.generate(
        make_recommendation_set(recommendations),
        plan_id=plan_id,
        generated_at=generated_at,
    )
    assert plan.is_empty()


def test_study_prerequisite_before_dependent(
    plan_id: MissionPlanId, generated_at: datetime
) -> None:
    recommendations = (
        make_recommendation(
            recommendation_id="r1",
            category=RecommendationCategory.FOCUS_COMPETENCY,
            priority=0.80,
            rank=1,
            competency="quadratic-equations",
        ),
        make_recommendation(
            recommendation_id="r2",
            category=RecommendationCategory.STUDY_PREREQUISITE,
            priority=0.90,
            rank=2,
            competency="linear-equations",
        ),
    )
    plan = AdaptiveMissionGenerator.generate(
        make_recommendation_set(recommendations),
        plan_id=plan_id,
        generated_at=generated_at,
    )
    assert plan.missions[0].mission_type is MissionType.REVISE_PREREQUISITE
    assert plan.missions[0].ordering.rank == 1


def test_maintain_mastery_is_lightweight(
    plan_id: MissionPlanId, generated_at: datetime
) -> None:
    recommendations = (
        make_recommendation(
            recommendation_id="r1",
            category=RecommendationCategory.MAINTAIN_MASTERY,
            priority=0.35,
        ),
    )
    plan = AdaptiveMissionGenerator.generate(
        make_recommendation_set(recommendations),
        plan_id=plan_id,
        generated_at=generated_at,
    )
    assert len(plan.missions) == 1
    mission = plan.missions[0]
    assert mission.mission_type is MissionType.MAINTENANCE_REVIEW
    assert mission.is_lightweight()
    assert mission.estimate.duration_minutes <= 15
    assert mission.recurrence is MissionRecurrenceBand.REDUCED


def test_increase_revision_frequency_raises_recurrence_not_size(
    plan_id: MissionPlanId, generated_at: datetime
) -> None:
    increased = make_recommendation(
        recommendation_id="r1",
        category=RecommendationCategory.INCREASE_REVISION_FREQUENCY,
        priority=0.60,
    )
    normal = make_recommendation(
        recommendation_id="r2",
        category=RecommendationCategory.CONSOLIDATE_KNOWLEDGE,
        priority=0.55,
        competency="other",
    )
    increased_est = AdaptiveMissionGenerator.estimate_duration(
        MissionType.REVISION_SESSION,
        recurrence=MissionRecurrenceBand.INCREASED,
    )
    normal_est = AdaptiveMissionGenerator.estimate_duration(
        MissionType.REVISION_SESSION,
        recurrence=MissionRecurrenceBand.NORMAL,
    )
    assert increased_est.duration_minutes <= normal_est.duration_minutes

    plan = AdaptiveMissionGenerator.generate(
        make_recommendation_set((increased, normal)),
        plan_id=plan_id,
        generated_at=generated_at,
    )
    revision = next(
        m for m in plan.missions if m.mission_type is MissionType.REVISION_SESSION
    )
    assert revision.recurrence is MissionRecurrenceBand.INCREASED
    assert any(
        c.kind is MissionConstraintKind.INCREASE_RECURRENCE for c in plan.constraints
    )


def test_reduce_revision_frequency_preserves_coverage(
    plan_id: MissionPlanId, generated_at: datetime
) -> None:
    reduced_est = AdaptiveMissionGenerator.estimate_duration(
        MissionType.MAINTENANCE_REVIEW,
        recurrence=MissionRecurrenceBand.REDUCED,
    )
    normal_est = AdaptiveMissionGenerator.estimate_duration(
        MissionType.MAINTENANCE_REVIEW,
        recurrence=MissionRecurrenceBand.NORMAL,
    )
    assert reduced_est.duration_minutes == normal_est.duration_minutes

    recommendations = (
        make_recommendation(
            recommendation_id="r1",
            category=RecommendationCategory.REDUCE_REVISION_FREQUENCY,
            priority=0.30,
        ),
    )
    plan = AdaptiveMissionGenerator.generate(
        make_recommendation_set(recommendations),
        plan_id=plan_id,
        generated_at=generated_at,
    )
    assert plan.missions[0].recurrence is MissionRecurrenceBand.REDUCED
    kinds = {c.kind for c in plan.constraints}
    assert MissionConstraintKind.DECREASE_RECURRENCE in kinds
    assert MissionConstraintKind.PRESERVE_COVERAGE in kinds


def test_generate_daily_plan_caps_workload(
    plan_id: MissionPlanId, generated_at: datetime
) -> None:
    recommendations = tuple(
        make_recommendation(
            recommendation_id=f"r{i}",
            category=RecommendationCategory.STRENGTHEN_WEAK_AREA,
            priority=0.90 - i * 0.05,
            rank=i,
            competency=f"comp-{i}",
            confidence=0.70,
        )
        for i in range(1, 8)
    )
    plan = AdaptiveMissionGenerator.generate_daily_plan(
        make_recommendation_set(recommendations),
        plan_id=plan_id,
        generated_at=generated_at,
        planning_constraints=PlanningConstraints(maximum_daily_workload_minutes=40),
    )
    assert plan.total_duration_minutes() <= 40 or plan.mission_count() == 1


def test_generate_single_mission() -> None:
    recommendation = make_recommendation(
        category=RecommendationCategory.REVIEW_CONCEPT,
        confidence=0.70,
    )
    from application.education.mission_generation import MissionId

    mission = AdaptiveMissionGenerator.generate_single_mission(
        recommendation,
        mission_id=MissionId("mission-solo"),
        learning_pace=LearningPace.NORMAL,
    )
    assert mission is not None
    assert mission.mission_type is MissionType.REVIEW_CONCEPT
    assert mission.source_recommendation_ids == ("r1",)


def test_generate_single_mission_skips_delay() -> None:
    from application.education.mission_generation import MissionId

    recommendation = make_recommendation(
        category=RecommendationCategory.DELAY_ADVANCED_TOPIC,
    )
    mission = AdaptiveMissionGenerator.generate_single_mission(
        recommendation,
        mission_id=MissionId("mission-skip"),
    )
    assert mission is None


def test_low_confidence_maps_to_confidence_recovery() -> None:
    from application.education.mission_generation import MissionId

    recommendation = make_recommendation(
        category=RecommendationCategory.REVIEW_CONCEPT,
        confidence=0.20,
    )
    mission = AdaptiveMissionGenerator.generate_single_mission(
        recommendation,
        mission_id=MissionId("mission-recovery"),
    )
    assert mission is not None
    assert mission.mission_type is MissionType.CONFIDENCE_RECOVERY


def test_produce_snapshot(
    plan_id: MissionPlanId, generated_at: datetime
) -> None:
    recommendations = (
        make_recommendation(
            category=RecommendationCategory.FOCUS_COMPETENCY,
            priority=0.75,
        ),
    )
    plan = AdaptiveMissionGenerator.generate(
        make_recommendation_set(
            recommendations,
            constraints=(blocking_constraint(), prerequisite_constraint()),
        ),
        plan_id=plan_id,
        generated_at=generated_at,
    )
    snapshot = AdaptiveMissionGenerator.produce_snapshot(plan)
    assert snapshot.plan_id == plan.plan_id
    assert snapshot.mission_count() == plan.mission_count()
    assert snapshot.summary.mission_count == plan.mission_count()
    assert snapshot.highest_priority() == plan.highest_priority()


def test_source_recommendation_set_id_preserved(
    plan_id: MissionPlanId, generated_at: datetime
) -> None:
    plan = AdaptiveMissionGenerator.generate(
        make_recommendation_set(
            (make_recommendation(),),
            set_id="recset-xyz",
        ),
        plan_id=plan_id,
        generated_at=generated_at,
    )
    assert plan.source_recommendation_set_id == "recset-xyz"
    assert plan.student_id == "student-001"
