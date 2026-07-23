"""Priority policy — assigns deterministic priority magnitudes.

Architecture Source
    PROJECT_CONTEXT.md
Concept
    Priority Policy
"""

from __future__ import annotations

from domain.education.mastery_estimation.enums import KnowledgeGapSeverity
from domain.education.recommendation_engine.enums import RecommendationCategory
from domain.education.recommendation_engine.value_objects.recommendation_priority import (  # noqa: E501
    RecommendationPriority,
)

_CATEGORY_BASE: dict[RecommendationCategory, float] = {
    RecommendationCategory.STUDY_PREREQUISITE: 0.90,
    RecommendationCategory.REVISIT_FOUNDATION: 0.85,
    RecommendationCategory.REVIEW_CONCEPT: 0.80,
    RecommendationCategory.FOCUS_COMPETENCY: 0.75,
    RecommendationCategory.STRENGTHEN_WEAK_AREA: 0.70,
    RecommendationCategory.DELAY_ADVANCED_TOPIC: 0.72,
    RecommendationCategory.CONSOLIDATE_KNOWLEDGE: 0.55,
    RecommendationCategory.INCREASE_REVISION_FREQUENCY: 0.60,
    RecommendationCategory.ATTEMPT_CHECKPOINT: 0.65,
    RecommendationCategory.PREPARE_ASSESSMENT: 0.58,
    RecommendationCategory.CONTINUE_CURRENT_MISSION: 0.50,
    RecommendationCategory.MAINTAIN_MASTERY: 0.35,
    RecommendationCategory.REDUCE_REVISION_FREQUENCY: 0.30,
}

_SEVERITY_BONUS: dict[KnowledgeGapSeverity, float] = {
    KnowledgeGapSeverity.MINOR: 0.00,
    KnowledgeGapSeverity.MODERATE: 0.03,
    KnowledgeGapSeverity.SEVERE: 0.06,
    KnowledgeGapSeverity.CRITICAL: 0.10,
}


class PriorityPolicy:
    """Deterministically assigns RecommendationPriority magnitudes."""

    @staticmethod
    def priority_for(
        category: RecommendationCategory,
        *,
        severity: KnowledgeGapSeverity | None = None,
    ) -> RecommendationPriority:
        base = _CATEGORY_BASE.get(category, 0.40)
        bonus = _SEVERITY_BONUS.get(severity, 0.0) if severity is not None else 0.0
        magnitude = min(1.0, base + bonus)
        return RecommendationPriority(magnitude=magnitude)
