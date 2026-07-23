"""Model invariant and edge-case tests."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from application.education.mission_generation import (
    AdaptiveMissionGenerator,
    Mission,
    MissionConstraint,
    MissionConstraintKind,
    MissionEstimate,
    MissionGenerationError,
    MissionId,
    MissionInvariantViolation,
    MissionObjective,
    MissionObjectiveCode,
    MissionOrdering,
    MissionPlan,
    MissionPlanId,
    MissionStep,
    MissionStepAction,
    MissionStepId,
    MissionSummary,
    MissionType,
)
from domain.education.recommendation_engine import RecommendationCategory
from tests.application.education.mission_generation.conftest import (
    make_recommendation,
    make_recommendation_set,
)


def test_mission_plan_invariants() -> None:
    with pytest.raises(MissionInvariantViolation):
        MissionPlan(
            plan_id=MissionPlanId("plan-1"),
            student_id="",
            source_recommendation_set_id="set-1",
            generated_at=datetime(2026, 7, 23, tzinfo=UTC),
        )


def test_mission_estimate_and_ordering_bands() -> None:
    estimate = MissionEstimate(duration_minutes=12)
    assert estimate.duration_band.value == "short"
    assert estimate.exceeds(10)
    ordering = MissionOrdering(rank=1, priority_magnitude=0.80)
    assert ordering.priority_band.value == "critical"


def test_mission_summary_type_counts() -> None:
    summary = MissionSummary(
        mission_count=2,
        total_duration_minutes=40,
        prerequisite_mission_count=1,
        maintenance_mission_count=0,
        type_counts=(
            (MissionType.REVISE_PREREQUISITE, 1),
            (MissionType.PRACTICE_QUESTIONS, 1),
        ),
        highest_priority_mission_id="m1",
    )
    assert not summary.is_empty()


def test_mission_step_and_objective_validation() -> None:
    with pytest.raises(MissionInvariantViolation):
        MissionStep(
            step_id=MissionStepId("s1"),
            action=MissionStepAction.PRACTICE,
            order=0,
            estimated_minutes=10,
        )
    with pytest.raises(MissionInvariantViolation):
        MissionObjective(
            code=MissionObjectiveCode.COMPLETE_PRACTICE,
            coverage_weight=0.0,
        )


def test_mission_chunk_invariant() -> None:
    with pytest.raises(MissionInvariantViolation):
        Mission(
            mission_id=MissionId("m1"),
            mission_type=MissionType.PRACTICE_QUESTIONS,
            objective=MissionObjective(code=MissionObjectiveCode.COMPLETE_PRACTICE),
            estimate=MissionEstimate(duration_minutes=10),
            ordering=MissionOrdering(rank=1, priority_magnitude=0.5),
            chunk_index=2,
            chunk_count=1,
        )


def test_generate_rejects_invalid_inputs() -> None:
    with pytest.raises(MissionGenerationError):
        AdaptiveMissionGenerator.generate(
            "not-a-set",  # type: ignore[arg-type]
            plan_id=MissionPlanId("plan-1"),
            generated_at=datetime(2026, 7, 23, tzinfo=UTC),
        )
    with pytest.raises(MissionGenerationError):
        AdaptiveMissionGenerator.generate(
            make_recommendation_set(),
            plan_id=MissionPlanId("plan-1"),
            generated_at="now",  # type: ignore[arg-type]
        )
    with pytest.raises(MissionGenerationError):
        AdaptiveMissionGenerator.generate(
            make_recommendation_set(),
            plan_id="plan-1",  # type: ignore[arg-type]
            generated_at=datetime(2026, 7, 23, tzinfo=UTC),
        )


def test_time_cap_keeps_first_mission_when_oversize(
    plan_id: MissionPlanId,
) -> None:
    from application.education.mission_generation import PlanningConstraints

    recommendations = (
        make_recommendation(
            category=RecommendationCategory.PREPARE_ASSESSMENT,
            priority=0.90,
            competency=None,
            checkpoint_id="cp-1",
        ),
    )
    plan = AdaptiveMissionGenerator.generate(
        make_recommendation_set(recommendations),
        plan_id=plan_id,
        generated_at=datetime(2026, 7, 23, tzinfo=UTC),
        planning_constraints=PlanningConstraints(available_study_minutes=5),
    )
    assert plan.mission_count() == 1


def test_identity_str_and_none() -> None:
    assert str(MissionId("m1")) == "m1"
    assert str(MissionPlanId("p1")) == "p1"
    assert str(MissionStepId("s1")) == "s1"
    with pytest.raises(MissionInvariantViolation):
        MissionId(None)  # type: ignore[arg-type]


def test_continue_current_mission_maps_to_mixed_practice() -> None:
    from application.education.mission_generation import MissionId

    recommendation = make_recommendation(
        category=RecommendationCategory.CONTINUE_CURRENT_MISSION,
        competency=None,
        mission_id="mission-active",
    )
    mission = AdaptiveMissionGenerator.generate_single_mission(
        recommendation,
        mission_id=MissionId("m-continue"),
    )
    assert mission is not None
    assert mission.mission_type is MissionType.MIXED_PRACTICE


def test_mission_constraint_helpers() -> None:
    constraint = MissionConstraint(
        kind=MissionConstraintKind.REQUIRE_PREREQUISITE_FIRST,
        subject_id="algebra",
        competency_id="linear-equations",
    )
    assert constraint.requires_prerequisite_first()
    workload = MissionConstraint(
        kind=MissionConstraintKind.LIMIT_DAILY_WORKLOAD,
        detail=45.0,
    )
    assert workload.limits_workload()


def test_ids_reject_whitespace() -> None:
    with pytest.raises(MissionInvariantViolation):
        MissionId("bad id")
    with pytest.raises(MissionInvariantViolation):
        MissionPlanId("")


def test_empty_recommendation_set_snapshot() -> None:
    plan = AdaptiveMissionGenerator.generate(
        make_recommendation_set(),
        plan_id=MissionPlanId("plan-empty"),
        generated_at=datetime(2026, 7, 23, tzinfo=UTC),
    )
    snapshot = plan.produce_snapshot()
    assert snapshot.mission_count() == 0
    assert snapshot.highest_priority() is None
    assert snapshot.summary.is_empty()
