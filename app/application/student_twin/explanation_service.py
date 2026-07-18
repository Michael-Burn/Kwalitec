"""Explanation service — educational explanations for Twin recommendations."""

from __future__ import annotations

from app.application.student_twin.dto.recommendation_snapshot import (
    RecommendationExplanation,
)
from app.application.student_twin.exceptions import ExplanationError
from app.domain.student_twin.digital_twin import DigitalTwin


class ExplanationService:
    """Produce educational explanations for Twin recommendations."""

    @staticmethod
    def explain_recommendation(
        twin: DigitalTwin,
        recommendation_id: str,
    ) -> RecommendationExplanation:
        """Explain a recommendation from Twin recommendation state."""
        for rec in twin.recommendations.recommendations:
            if rec.recommendation_id == recommendation_id:
                return RecommendationExplanation(
                    recommendation_id=rec.recommendation_id,
                    kind=rec.kind.value,
                    topic_id=rec.topic_id,
                    evidence_ids=rec.evidence_ids,
                    rationale=rec.rationale,
                    expected_benefit=rec.expected_benefit,
                    confidence=rec.confidence.value,
                    priority=rec.priority,
                )
        raise ExplanationError(
            f"recommendation not found: {recommendation_id!r}"
        )

    @staticmethod
    def explain_all(twin: DigitalTwin) -> tuple[RecommendationExplanation, ...]:
        """Explain all current Twin recommendations."""
        return tuple(
            ExplanationService.explain_recommendation(twin, rec.recommendation_id)
            for rec in twin.recommendations.recommendations
        )
