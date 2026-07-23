"""Impact policy — assigns deterministic educational impact magnitudes.

Architecture Source
    PROJECT_CONTEXT.md
Concept
    Impact Policy
"""

from __future__ import annotations

from domain.education.recommendation_engine.enums import RecommendationCategory
from domain.education.recommendation_engine.value_objects.recommendation_impact import (
    RecommendationImpact,
)

_CATEGORY_IMPACT: dict[RecommendationCategory, float] = {
    RecommendationCategory.STUDY_PREREQUISITE: 0.95,
    RecommendationCategory.REVISIT_FOUNDATION: 0.90,
    RecommendationCategory.DELAY_ADVANCED_TOPIC: 0.85,
    RecommendationCategory.FOCUS_COMPETENCY: 0.80,
    RecommendationCategory.STRENGTHEN_WEAK_AREA: 0.78,
    RecommendationCategory.REVIEW_CONCEPT: 0.75,
    RecommendationCategory.CONSOLIDATE_KNOWLEDGE: 0.65,
    RecommendationCategory.INCREASE_REVISION_FREQUENCY: 0.55,
    RecommendationCategory.ATTEMPT_CHECKPOINT: 0.70,
    RecommendationCategory.PREPARE_ASSESSMENT: 0.60,
    RecommendationCategory.CONTINUE_CURRENT_MISSION: 0.50,
    RecommendationCategory.MAINTAIN_MASTERY: 0.40,
    RecommendationCategory.REDUCE_REVISION_FREQUENCY: 0.30,
}


class ImpactPolicy:
    """Deterministically assigns RecommendationImpact magnitudes."""

    @staticmethod
    def impact_for(category: RecommendationCategory) -> RecommendationImpact:
        magnitude = _CATEGORY_IMPACT.get(category, 0.40)
        return RecommendationImpact(magnitude=magnitude)

    @staticmethod
    def is_highest_impact(impact: RecommendationImpact) -> bool:
        return impact.magnitude >= 0.67
