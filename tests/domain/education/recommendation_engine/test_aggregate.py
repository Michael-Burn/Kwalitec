"""Unit tests for the RecommendationSet aggregate."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
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

AS_OF = datetime(2026, 7, 23, 12, 0, 0, tzinfo=UTC)


def _recommendation(
    *,
    recommendation_id: str,
    category: RecommendationCategory,
    priority: float,
    impact: float,
    rank: int,
    competency: str = "linear-equations",
) -> Recommendation:
    p = RecommendationPriority(priority)
    return Recommendation(
        recommendation_id=RecommendationId(recommendation_id),
        category=category,
        target=RecommendationTarget(
            subject_id=SubjectId("algebra"),
            competency_id=CompetencyId(competency),
        ),
        priority=p,
        impact=RecommendationImpact(impact),
        confidence=RecommendationConfidence(0.6),
        explanation=RecommendationExplanation.from_reasons(
            (
                RecommendationReason(
                    reason_code=RecommendationReasonCode.DIRECT_KNOWLEDGE_GAP,
                    subject_id=SubjectId("algebra"),
                ),
            )
        ),
        ordering=RecommendationOrdering(rank=rank, priority=p),
    )


def test_aggregate_construction_and_queries() -> None:
    recommendations = (
        _recommendation(
            recommendation_id="r1",
            category=RecommendationCategory.STUDY_PREREQUISITE,
            priority=0.9,
            impact=0.95,
            rank=1,
        ),
        _recommendation(
            recommendation_id="r2",
            category=RecommendationCategory.MAINTAIN_MASTERY,
            priority=0.35,
            impact=0.4,
            rank=2,
            competency="quadratic-equations",
        ),
    )
    constraints = (
        RecommendationConstraint(
            kind=RecommendationConstraintKind.BLOCK_ADVANCEMENT,
            subject_id=SubjectId("algebra"),
            competency_id=CompetencyId("quadratic-equations"),
        ),
    )
    aggregate = RecommendationSet(
        RecommendationSetId("set-001"),
        "student-001",
        AS_OF,
        recommendations=recommendations,
        constraints=constraints,
    )
    assert aggregate.recommendation_count() == 2
    assert not aggregate.is_empty()
    assert aggregate.highest_priority() is recommendations[0]
    assert len(aggregate.recommendations_for_subject(SubjectId("algebra"))) == 2
    assert (
        len(
            aggregate.recommendations_for_competency(
                CompetencyId("linear-equations")
            )
        )
        == 1
    )
    assert (
        len(
            aggregate.recommendations_of_category(
                RecommendationCategory.STUDY_PREREQUISITE
            )
        )
        == 1
    )
    assert aggregate.has_blocking_constraints()
    high = aggregate.highest_impact_actions(limit=1)
    assert len(high) == 1
    snapshot = aggregate.produce_snapshot()
    assert snapshot.set_id == aggregate.set_id
    assert snapshot.recommendation_count() == 2


def test_duplicate_recommendation_id_rejected() -> None:
    rec = _recommendation(
        recommendation_id="r1",
        category=RecommendationCategory.FOCUS_COMPETENCY,
        priority=0.7,
        impact=0.8,
        rank=1,
    )
    with pytest.raises(EducationalInvariantViolation):
        RecommendationSet(
            RecommendationSetId("set-001"),
            "student-001",
            AS_OF,
            recommendations=(rec, rec),
        )


def test_non_dense_ranks_rejected() -> None:
    with pytest.raises(EducationalInvariantViolation):
        RecommendationSet(
            RecommendationSetId("set-001"),
            "student-001",
            AS_OF,
            recommendations=(
                _recommendation(
                    recommendation_id="r1",
                    category=RecommendationCategory.FOCUS_COMPETENCY,
                    priority=0.7,
                    impact=0.8,
                    rank=1,
                ),
                _recommendation(
                    recommendation_id="r2",
                    category=RecommendationCategory.MAINTAIN_MASTERY,
                    priority=0.3,
                    impact=0.4,
                    rank=3,
                    competency="quadratic-equations",
                ),
            ),
        )


def test_ascending_priority_order_rejected() -> None:
    with pytest.raises(EducationalInvariantViolation):
        RecommendationSet(
            RecommendationSetId("set-001"),
            "student-001",
            AS_OF,
            recommendations=(
                _recommendation(
                    recommendation_id="r1",
                    category=RecommendationCategory.MAINTAIN_MASTERY,
                    priority=0.3,
                    impact=0.4,
                    rank=1,
                ),
                _recommendation(
                    recommendation_id="r2",
                    category=RecommendationCategory.STUDY_PREREQUISITE,
                    priority=0.9,
                    impact=0.95,
                    rank=2,
                    competency="quadratic-equations",
                ),
            ),
        )


def test_empty_set_is_valid() -> None:
    aggregate = RecommendationSet(
        RecommendationSetId("set-empty"),
        "student-001",
        AS_OF,
    )
    assert aggregate.is_empty()
    assert aggregate.highest_priority() is None
    assert aggregate.highest_impact_actions() == ()


def test_equality_and_hash() -> None:
    a = RecommendationSet(RecommendationSetId("set-001"), "student-001", AS_OF)
    b = RecommendationSet(RecommendationSetId("set-001"), "student-001", AS_OF)
    c = RecommendationSet(RecommendationSetId("set-002"), "student-001", AS_OF)
    assert a == b
    assert hash(a) == hash(b)
    assert a != c
