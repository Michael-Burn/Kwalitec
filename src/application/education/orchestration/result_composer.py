"""Result composition helpers — project domain products to application DTOs.

Projection only. No mastery estimation, no recommendation generation.
"""

from __future__ import annotations

from datetime import datetime

from application.education.orchestration.dto.educational_decision import (
    EducationalDecision,
)
from application.education.orchestration.dto.evaluation_snapshot import (
    EvaluationSnapshot,
)
from application.education.orchestration.dto.evaluation_summary import (
    EvaluationSummary,
)
from domain.education.mastery_estimation.aggregates.mastery_assessment import (
    MasteryAssessment,
)
from domain.education.recommendation_engine.aggregates.recommendation_set import (
    RecommendationSet,
)
from domain.education.recommendation_engine.value_objects.recommendation import (
    Recommendation,
)


def project_decisions(
    recommendation_set: RecommendationSet,
) -> tuple[EducationalDecision, ...]:
    """Project ranked recommendations into application decisions."""
    return tuple(
        _project_decision(recommendation)
        for recommendation in recommendation_set.recommendations
    )


def compose_summary(
    *,
    assessment: MasteryAssessment,
    recommendation_set: RecommendationSet,
    evidence_count: int,
    evaluated_at: datetime,
    decisions: tuple[EducationalDecision, ...],
) -> EvaluationSummary:
    """Compose an EvaluationSummary from domain products."""
    top_category = decisions[0].category if decisions else None
    return EvaluationSummary(
        student_id=assessment.student_id,
        assessment_id=str(assessment.assessment_id),
        recommendation_set_id=str(recommendation_set.set_id),
        mastery_magnitude=assessment.overall_mastery.magnitude,
        mastery_band=assessment.overall_mastery.band.value,
        confidence_magnitude=assessment.overall_confidence.score.magnitude,
        stability_band=assessment.overall_stability.band.value,
        knowledge_gap_count=len(assessment.knowledge_gaps),
        recommendation_count=recommendation_set.recommendation_count(),
        evidence_count=evidence_count,
        evaluated_at=evaluated_at,
        top_decision_category=top_category,
    )


def compose_snapshot(
    *,
    student_id: str,
    evaluated_at: datetime,
    stages_completed: tuple[str, ...],
    summary: EvaluationSummary,
    decisions: tuple[EducationalDecision, ...],
    evidence_id: str | None,
) -> EvaluationSnapshot:
    """Compose an EvaluationSnapshot from projected application artefacts."""
    return EvaluationSnapshot(
        student_id=student_id,
        evaluated_at=evaluated_at,
        stages_completed=stages_completed,
        summary=summary,
        decisions=decisions,
        evidence_id=evidence_id,
    )


def _project_decision(recommendation: Recommendation) -> EducationalDecision:
    target = recommendation.target
    subject_id = (
        target.subject_id.value if target.subject_id is not None else None
    )
    competency_id = (
        target.competency_id.value if target.competency_id is not None else None
    )
    return EducationalDecision(
        decision_id=str(recommendation.recommendation_id),
        category=recommendation.category.value,
        subject_id=subject_id,
        competency_id=competency_id,
        priority_band=recommendation.priority.band.value,
        impact_band=recommendation.impact.band.value,
        confidence_magnitude=recommendation.confidence.magnitude,
        reason_summary=recommendation.explanation.primary_reason_code.value,
        rank=recommendation.ordering.rank,
    )
