"""Shared factories for Adaptive Mission Generator tests."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from application.education.mission_generation import MissionPlanId
from domain.education.recommendation_engine import (
    CompetencyId,
    Recommendation,
    RecommendationCategory,
    RecommendationConfidence,
    RecommendationConstraint,
    RecommendationConstraintKind,
    RecommendationExplanation,
    RecommendationId,
    RecommendationImpact,
    RecommendationOrdering,
    RecommendationPriority,
    RecommendationReason,
    RecommendationReasonCode,
    RecommendationSet,
    RecommendationSetId,
    RecommendationTarget,
    SubjectId,
)

STUDENT_ID = "student-001"
SUBJECT_ALGEBRA = "algebra"
COMPETENCY_LINEAR = "linear-equations"
COMPETENCY_QUADRATIC = "quadratic-equations"


@pytest.fixture
def generated_at() -> datetime:
    return datetime(2026, 7, 23, 12, 0, 0, tzinfo=UTC)


@pytest.fixture
def plan_id() -> MissionPlanId:
    return MissionPlanId("plan-001")


def make_recommendation(
    *,
    recommendation_id: str = "r1",
    category: RecommendationCategory = RecommendationCategory.FOCUS_COMPETENCY,
    priority: float = 0.75,
    impact: float = 0.70,
    confidence: float = 0.60,
    rank: int = 1,
    subject: str = SUBJECT_ALGEBRA,
    competency: str | None = COMPETENCY_LINEAR,
    mission_id: str | None = None,
    checkpoint_id: str | None = None,
) -> Recommendation:
    p = RecommendationPriority(priority)
    target_kwargs: dict = {"subject_id": SubjectId(subject)}
    if competency is not None:
        target_kwargs["competency_id"] = CompetencyId(competency)
    if mission_id is not None:
        target_kwargs["mission_id"] = mission_id
    if checkpoint_id is not None:
        target_kwargs["checkpoint_id"] = checkpoint_id
    return Recommendation(
        recommendation_id=RecommendationId(recommendation_id),
        category=category,
        target=RecommendationTarget(**target_kwargs),
        priority=p,
        impact=RecommendationImpact(impact),
        confidence=RecommendationConfidence(confidence),
        explanation=RecommendationExplanation.from_reasons(
            (
                RecommendationReason(
                    reason_code=RecommendationReasonCode.DIRECT_KNOWLEDGE_GAP,
                    subject_id=SubjectId(subject),
                    competency_id=(
                        CompetencyId(competency) if competency is not None else None
                    ),
                ),
            )
        ),
        ordering=RecommendationOrdering(rank=rank, priority=p),
    )


def make_recommendation_set(
    recommendations: tuple[Recommendation, ...] | list[Recommendation] = (),
    *,
    set_id: str = "recset-001",
    student_id: str = STUDENT_ID,
    recommended_at: datetime | None = None,
    constraints: tuple[RecommendationConstraint, ...] = (),
) -> RecommendationSet:
    """Build a RecommendationSet with lawful rank/priority ordering."""
    items = list(recommendations)
    items.sort(
        key=lambda rec: (
            -rec.priority.magnitude,
            -rec.impact.magnitude,
            rec.category.value,
            rec.target.correlation_key(),
        )
    )
    normalised: list[Recommendation] = []
    for index, recommendation in enumerate(items, start=1):
        ordering = RecommendationOrdering(
            rank=index,
            priority=recommendation.priority,
        )
        normalised.append(recommendation.with_ordering(ordering))
    return RecommendationSet(
        RecommendationSetId(set_id),
        student_id,
        recommended_at or datetime(2026, 7, 23, 12, 0, 0, tzinfo=UTC),
        recommendations=tuple(normalised),
        constraints=constraints,
    )


def blocking_constraint(
    *,
    competency: str = COMPETENCY_QUADRATIC,
) -> RecommendationConstraint:
    return RecommendationConstraint(
        kind=RecommendationConstraintKind.BLOCK_ADVANCEMENT,
        subject_id=SubjectId(SUBJECT_ALGEBRA),
        competency_id=CompetencyId(competency),
    )


def prerequisite_constraint(
    *,
    competency: str = COMPETENCY_LINEAR,
) -> RecommendationConstraint:
    return RecommendationConstraint(
        kind=RecommendationConstraintKind.REQUIRE_PREREQUISITE,
        subject_id=SubjectId(SUBJECT_ALGEBRA),
        competency_id=CompetencyId(competency),
    )
