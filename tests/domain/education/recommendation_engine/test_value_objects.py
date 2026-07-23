"""Unit tests for Recommendation Engine value objects."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
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
    RecommendationImpactBand,
    RecommendationOrdering,
    RecommendationPriority,
    RecommendationPriorityBand,
    RecommendationReason,
    RecommendationReasonCode,
    RecommendationSetId,
    RecommendationSnapshot,
    RecommendationTarget,
    SubjectId,
)


def test_priority_band_derived_from_magnitude() -> None:
    assert RecommendationPriority(0.1).band is RecommendationPriorityBand.LOW
    assert RecommendationPriority(0.4).band is RecommendationPriorityBand.MEDIUM
    assert RecommendationPriority(0.6).band is RecommendationPriorityBand.HIGH
    assert RecommendationPriority(0.9).band is RecommendationPriorityBand.CRITICAL


def test_impact_band_derived_from_magnitude() -> None:
    assert RecommendationImpact(0.2).band is RecommendationImpactBand.LOW
    assert RecommendationImpact(0.5).band is RecommendationImpactBand.MEDIUM
    assert RecommendationImpact(0.9).band is RecommendationImpactBand.HIGH


def test_priority_rejects_out_of_range() -> None:
    with pytest.raises(EducationalInvariantViolation):
        RecommendationPriority(1.5)


def test_confidence_zero_factory() -> None:
    assert RecommendationConfidence.zero().magnitude == 0.0


def test_target_requires_scope() -> None:
    with pytest.raises(EducationalInvariantViolation):
        RecommendationTarget()


def test_target_correlation_key_is_stable() -> None:
    target = RecommendationTarget(
        subject_id=SubjectId("algebra"),
        competency_id=CompetencyId("linear-equations"),
    )
    assert target.correlation_key() == "algebra:linear-equations:-:-"


def test_explanation_requires_primary_among_reasons() -> None:
    reason = RecommendationReason(
        reason_code=RecommendationReasonCode.WEAK_PREREQUISITE,
        subject_id=SubjectId("algebra"),
    )
    with pytest.raises(EducationalInvariantViolation):
        RecommendationExplanation(
            reasons=(reason,),
            primary_reason_code=RecommendationReasonCode.ACTIVE_MISSION,
        )


def test_explanation_from_reasons() -> None:
    reason = RecommendationReason(
        reason_code=RecommendationReasonCode.DEVELOPING_MASTERY,
        subject_id=SubjectId("algebra"),
        competency_id=CompetencyId("linear-equations"),
        detail=0.45,
    )
    explanation = RecommendationExplanation.from_reasons((reason,))
    assert (
        explanation.primary_reason_code
        is RecommendationReasonCode.DEVELOPING_MASTERY
    )


def test_recommendation_ordering_must_match_priority() -> None:
    priority = RecommendationPriority(0.7)
    other = RecommendationPriority(0.3)
    explanation = RecommendationExplanation.from_reasons(
        (
            RecommendationReason(
                reason_code=RecommendationReasonCode.DIRECT_KNOWLEDGE_GAP,
                subject_id=SubjectId("algebra"),
            ),
        )
    )
    with pytest.raises(EducationalInvariantViolation):
        Recommendation(
            recommendation_id=RecommendationId("r-001"),
            category=RecommendationCategory.FOCUS_COMPETENCY,
            target=RecommendationTarget(subject_id=SubjectId("algebra")),
            priority=priority,
            impact=RecommendationImpact(0.8),
            confidence=RecommendationConfidence(0.5),
            explanation=explanation,
            ordering=RecommendationOrdering(rank=1, priority=other),
        )


def test_value_objects_are_immutable() -> None:
    priority = RecommendationPriority(0.5)
    with pytest.raises(FrozenInstanceError):
        priority.magnitude = 0.9  # type: ignore[misc]


def test_constraint_blocks_advancement() -> None:
    constraint = RecommendationConstraint(
        kind=RecommendationConstraintKind.BLOCK_ADVANCEMENT,
        subject_id=SubjectId("algebra"),
        competency_id=CompetencyId("quadratic-equations"),
    )
    assert constraint.blocks_advancement()


def test_snapshot_counts() -> None:
    explanation = RecommendationExplanation.from_reasons(
        (
            RecommendationReason(
                reason_code=RecommendationReasonCode.STABLE_HIGH_MASTERY,
                subject_id=SubjectId("algebra"),
            ),
        )
    )
    priority = RecommendationPriority(0.9)
    recommendation = Recommendation(
        recommendation_id=RecommendationId("r-001"),
        category=RecommendationCategory.STUDY_PREREQUISITE,
        target=RecommendationTarget(subject_id=SubjectId("algebra")),
        priority=priority,
        impact=RecommendationImpact(0.95),
        confidence=RecommendationConfidence(0.8),
        explanation=explanation,
        ordering=RecommendationOrdering(rank=1, priority=priority),
    )
    snapshot = RecommendationSnapshot(
        set_id=RecommendationSetId("set-001"),
        student_id="student-001",
        recommendations=(recommendation,),
        constraints=(),
        recommended_at=datetime(2026, 7, 23, 12, 0, 0, tzinfo=UTC),
    )
    assert snapshot.recommendation_count() == 1
    assert snapshot.high_impact_count() == 1
    assert snapshot.highest_priority() is recommendation


def test_ids_reject_whitespace() -> None:
    with pytest.raises(EducationalInvariantViolation):
        RecommendationSetId("bad id")
