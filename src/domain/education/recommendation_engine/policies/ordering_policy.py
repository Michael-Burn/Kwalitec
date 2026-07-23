"""Ordering policy — deterministic ranking of recommendations.

Architecture Source
    PROJECT_CONTEXT.md
Concept
    Ordering Policy
"""

from __future__ import annotations

from collections.abc import Sequence

from domain.education.recommendation_engine.value_objects.recommendation import (
    Recommendation,
)
from domain.education.recommendation_engine.value_objects.recommendation_ordering import (  # noqa: E501
    RecommendationOrdering,
)


class OrderingPolicy:
    """Deterministically ranks recommendations by educational priority.

    Sort key (descending priority, then descending impact, then stable
    category/target tie-breakers):

    1. priority.magnitude (desc)
    2. impact.magnitude (desc)
    3. category.value (asc)
    4. target.correlation_key() (asc)
    """

    @staticmethod
    def sort_key(recommendation: Recommendation) -> tuple:
        return (
            -recommendation.priority.magnitude,
            -recommendation.impact.magnitude,
            recommendation.category.value,
            recommendation.target.correlation_key(),
        )

    @staticmethod
    def rank(
        recommendations: Sequence[Recommendation],
    ) -> tuple[Recommendation, ...]:
        ordered = sorted(recommendations, key=OrderingPolicy.sort_key)
        ranked: list[Recommendation] = []
        for index, recommendation in enumerate(ordered, start=1):
            ordering = RecommendationOrdering(
                rank=index,
                priority=recommendation.priority,
            )
            ranked.append(recommendation.with_ordering(ordering))
        return tuple(ranked)

    @staticmethod
    def prioritise(
        recommendations: Sequence[Recommendation],
    ) -> tuple[Recommendation, ...]:
        """Alias for ``rank`` — expose the milestone vocabulary."""
        return OrderingPolicy.rank(recommendations)
