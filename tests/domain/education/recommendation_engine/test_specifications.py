"""Unit tests for Recommendation Engine specifications."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.recommendation_engine import (
    CompetencyId,
    ConstraintSpecification,
    PrioritySpecification,
    Recommendation,
    RecommendationCategory,
    RecommendationConfidence,
    RecommendationConsistencySpecification,
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
from domain.education.recommendation_engine.policies.ordering_policy import (
    OrderingPolicy,
)

AS_OF = datetime(2026, 7, 23, 12, 0, 0, tzinfo=UTC)


def _recommendation(
    *,
    recommendation_id: str,
    category: RecommendationCategory,
    priority: float,
    impact: float,
) -> Recommendation:
    p = RecommendationPriority(priority)
    return Recommendation(
        recommendation_id=RecommendationId(recommendation_id),
        category=category,
        target=RecommendationTarget(
            subject_id=SubjectId("algebra"),
            competency_id=CompetencyId("linear-equations"),
        ),
        priority=p,
        impact=RecommendationImpact(impact),
        confidence=RecommendationConfidence(0.5),
        explanation=RecommendationExplanation.from_reasons(
            (
                RecommendationReason(
                    reason_code=RecommendationReasonCode.DIRECT_KNOWLEDGE_GAP,
                    subject_id=SubjectId("algebra"),
                ),
            )
        ),
        ordering=RecommendationOrdering(rank=1, priority=p),
    )


def test_consistency_specification_satisfied() -> None:
    drafts = (
        _recommendation(
            recommendation_id="a",
            category=RecommendationCategory.STUDY_PREREQUISITE,
            priority=0.9,
            impact=0.95,
        ),
        _recommendation(
            recommendation_id="b",
            category=RecommendationCategory.MAINTAIN_MASTERY,
            priority=0.35,
            impact=0.4,
        ),
    )
    ranked = OrderingPolicy.rank(drafts)
    recommendation_set = RecommendationSet(
        RecommendationSetId("set-001"),
        "student-001",
        AS_OF,
        recommendations=ranked,
    )
    assert RecommendationConsistencySpecification.is_satisfied_by(recommendation_set)
    RecommendationConsistencySpecification.assert_satisfied_by(recommendation_set)


def test_priority_specification() -> None:
    priority = RecommendationPriority(0.8)
    assert PrioritySpecification.is_satisfied_by(priority)
    assert PrioritySpecification.is_actionable(priority)
    PrioritySpecification.assert_satisfied_by(priority)
    assert not PrioritySpecification.is_actionable(RecommendationPriority(0.1))


def test_constraint_specification_require_prerequisite() -> None:
    good = RecommendationConstraint(
        kind=RecommendationConstraintKind.REQUIRE_PREREQUISITE,
        competency_id=CompetencyId("linear-equations"),
    )
    assert ConstraintSpecification.is_satisfied_by(good)
    ConstraintSpecification.assert_satisfied_by(good)

    bad = RecommendationConstraint(
        kind=RecommendationConstraintKind.REQUIRE_PREREQUISITE,
    )
    assert not ConstraintSpecification.is_satisfied_by(bad)
    with pytest.raises(EducationalInvariantViolation):
        ConstraintSpecification.assert_satisfied_by(bad)


def test_constraint_specification_block_and_defer() -> None:
    block = RecommendationConstraint(
        kind=RecommendationConstraintKind.BLOCK_ADVANCEMENT,
        subject_id=SubjectId("algebra"),
    )
    assert ConstraintSpecification.is_satisfied_by(block)
    defer = RecommendationConstraint(
        kind=RecommendationConstraintKind.DEFER_CHECKPOINT,
        competency_id=CompetencyId("linear-equations"),
    )
    assert ConstraintSpecification.is_satisfied_by(defer)
    bad_defer = RecommendationConstraint(
        kind=RecommendationConstraintKind.DEFER_CHECKPOINT,
    )
    assert not ConstraintSpecification.is_satisfied_by(bad_defer)
