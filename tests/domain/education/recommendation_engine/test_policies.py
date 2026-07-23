"""Unit tests for Recommendation Engine policies."""

from __future__ import annotations

from domain.education.mastery_estimation.enums import (
    KnowledgeGapKind,
    KnowledgeGapSeverity,
    LearningStabilityBand,
)
from domain.education.recommendation_engine import (
    CompetencyId,
    ConstraintPolicy,
    ImpactPolicy,
    OrderingPolicy,
    PriorityPolicy,
    Recommendation,
    RecommendationCategory,
    RecommendationConfidence,
    RecommendationConstraintKind,
    RecommendationExplanation,
    RecommendationId,
    RecommendationImpact,
    RecommendationOrdering,
    RecommendationPolicy,
    RecommendationPriority,
    RecommendationReason,
    RecommendationReasonCode,
    RecommendationTarget,
    SubjectId,
)
from tests.domain.education.recommendation_engine.conftest import (
    COMPETENCY_LINEAR_EQUATIONS,
    COMPETENCY_QUADRATIC_EQUATIONS,
    SUBJECT_ALGEBRA,
    contradictory_reason,
    make_competency_assessment,
    make_direct_gap,
    make_prerequisite_gap,
)


def _draft(
    category: RecommendationCategory,
    *,
    priority: float,
    impact: float,
    competency: str = COMPETENCY_LINEAR_EQUATIONS,
) -> Recommendation:
    p = RecommendationPriority(priority)
    return Recommendation(
        recommendation_id=RecommendationId(f"tmp-{category.value}-{competency}"),
        category=category,
        target=RecommendationTarget(
            subject_id=SubjectId(SUBJECT_ALGEBRA),
            competency_id=CompetencyId(competency),
        ),
        priority=p,
        impact=RecommendationImpact(impact),
        confidence=RecommendationConfidence(0.5),
        explanation=RecommendationExplanation.from_reasons(
            (
                RecommendationReason(
                    reason_code=RecommendationReasonCode.DIRECT_KNOWLEDGE_GAP,
                    subject_id=SubjectId(SUBJECT_ALGEBRA),
                ),
            )
        ),
        ordering=RecommendationOrdering(rank=1, priority=p),
    )


def test_policy_weak_prerequisite_category() -> None:
    gap = make_prerequisite_gap()
    assert (
        RecommendationPolicy.category_for_prerequisite_gap(gap)
        is RecommendationCategory.STUDY_PREREQUISITE
    )


def test_policy_low_mastery_high_confidence_strengthens() -> None:
    assessment = make_competency_assessment(
        mastery_magnitude=0.4,
        confidence_magnitude=0.75,
    )
    assert (
        RecommendationPolicy.category_for_competency(assessment)
        is RecommendationCategory.STRENGTHEN_WEAK_AREA
    )


def test_policy_low_mastery_low_confidence_foundation() -> None:
    assessment = make_competency_assessment(
        mastery_magnitude=0.1,
        evidence_count=1,
        confidence_magnitude=0.2,
    )
    assert (
        RecommendationPolicy.category_for_competency(assessment)
        is RecommendationCategory.REVISIT_FOUNDATION
    )


def test_policy_stable_high_mastery_maintains() -> None:
    assessment = make_competency_assessment(
        mastery_magnitude=0.92,
        evidence_count=5,
        confidence_magnitude=0.8,
        stability_band=LearningStabilityBand.STABLE,
    )
    assert (
        RecommendationPolicy.category_for_competency(assessment)
        is RecommendationCategory.MAINTAIN_MASTERY
    )
    assert RecommendationPolicy.should_reduce_revision(assessment)


def test_policy_contradictory_evidence_reviews() -> None:
    assessment = make_competency_assessment(
        mastery_magnitude=0.5,
        contradiction_ratio=0.4,
        reasons=(contradictory_reason(),),
    )
    assert (
        RecommendationPolicy.category_for_competency(assessment)
        is RecommendationCategory.REVIEW_CONCEPT
    )


def test_policy_volatile_increases_revision() -> None:
    assessment = make_competency_assessment(
        mastery_magnitude=0.88,
        evidence_count=5,
        confidence_magnitude=0.7,
        stability_band=LearningStabilityBand.VOLATILE,
    )
    assert (
        RecommendationPolicy.category_for_competency(assessment)
        is RecommendationCategory.INCREASE_REVISION_FREQUENCY
    )


def test_priority_policy_orders_categories() -> None:
    study = PriorityPolicy.priority_for(RecommendationCategory.STUDY_PREREQUISITE)
    maintain = PriorityPolicy.priority_for(RecommendationCategory.MAINTAIN_MASTERY)
    assert study.magnitude > maintain.magnitude


def test_priority_policy_severity_bonus() -> None:
    base = PriorityPolicy.priority_for(RecommendationCategory.FOCUS_COMPETENCY)
    boosted = PriorityPolicy.priority_for(
        RecommendationCategory.FOCUS_COMPETENCY,
        severity=KnowledgeGapSeverity.CRITICAL,
    )
    assert boosted.magnitude > base.magnitude


def test_impact_policy_highest_impact() -> None:
    impact = ImpactPolicy.impact_for(RecommendationCategory.STUDY_PREREQUISITE)
    assert ImpactPolicy.is_highest_impact(impact)


def test_constraint_policy_for_prerequisite_gap() -> None:
    gap = make_prerequisite_gap()
    constraints = ConstraintPolicy.constraints_for_gap(
        gap, subject_id=SubjectId(SUBJECT_ALGEBRA)
    )
    kinds = {c.kind for c in constraints}
    assert RecommendationConstraintKind.REQUIRE_PREREQUISITE in kinds
    assert RecommendationConstraintKind.BLOCK_ADVANCEMENT in kinds


def test_constraint_policy_defers_checkpoint_on_prereq() -> None:
    assessment = make_competency_assessment(
        competency_id=COMPETENCY_QUADRATIC_EQUATIONS,
        gaps=(make_prerequisite_gap(),),
    )
    assert ConstraintPolicy.should_defer_checkpoint(assessment)


def test_ordering_policy_ranks_by_priority_then_impact() -> None:
    low = _draft(RecommendationCategory.MAINTAIN_MASTERY, priority=0.3, impact=0.4)
    high = _draft(
        RecommendationCategory.STUDY_PREREQUISITE, priority=0.9, impact=0.95
    )
    ranked = OrderingPolicy.rank((low, high))
    assert ranked[0].category is RecommendationCategory.STUDY_PREREQUISITE
    assert ranked[0].ordering.rank == 1
    assert ranked[1].ordering.rank == 2


def test_ordering_is_deterministic() -> None:
    a = _draft(RecommendationCategory.FOCUS_COMPETENCY, priority=0.7, impact=0.8)
    b = _draft(
        RecommendationCategory.STRENGTHEN_WEAK_AREA,
        priority=0.7,
        impact=0.78,
        competency=COMPETENCY_QUADRATIC_EQUATIONS,
    )
    first = OrderingPolicy.rank((a, b))
    second = OrderingPolicy.rank((b, a))
    assert [r.recommendation_id for r in first] == [
        r.recommendation_id for r in second
    ]


def test_reason_for_category_mapping() -> None:
    reason = RecommendationPolicy.reason_for_category(
        RecommendationCategory.REVIEW_CONCEPT,
        subject_id=SubjectId(SUBJECT_ALGEBRA),
        competency_id=CompetencyId(COMPETENCY_LINEAR_EQUATIONS),
    )
    assert reason.reason_code is RecommendationReasonCode.CONTRADICTORY_EVIDENCE


def test_should_delay_advanced_when_prereq_gaps() -> None:
    assessment = make_competency_assessment(
        competency_id=COMPETENCY_QUADRATIC_EQUATIONS,
        gaps=(make_prerequisite_gap(),),
    )
    assert RecommendationPolicy.should_delay_advanced(assessment)


def test_direct_gap_limit_scope_constraint() -> None:
    gap = make_direct_gap()
    assert gap.kind is KnowledgeGapKind.WEAK_EVIDENCE
    constraints = ConstraintPolicy.constraints_for_gap(
        gap, subject_id=SubjectId(SUBJECT_ALGEBRA)
    )
    assert constraints[0].kind is RecommendationConstraintKind.LIMIT_SCOPE
