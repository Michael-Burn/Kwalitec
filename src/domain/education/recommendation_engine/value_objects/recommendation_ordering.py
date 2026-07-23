"""Recommendation ordering — deterministic rank within a set.

Architecture Source
    PROJECT_CONTEXT.md
Concept
    Recommendation Ordering
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.recommendation_engine.value_objects.recommendation_priority import (  # noqa: E501
    RecommendationPriority,
)


@dataclass(frozen=True, slots=True)
class RecommendationOrdering(EducationalValueObject):
    """Immutable rank position of a recommendation inside a set.

    ``rank`` is 1-based and denser ranks are higher priority. The attached
    ``priority`` mirrors the priority used to compute the rank so
    consumers can audit ordering without re-ranking.
    """

    rank: int
    priority: RecommendationPriority

    def _validate(self) -> None:
        if isinstance(self.rank, bool) or not isinstance(self.rank, int):
            raise EducationalInvariantViolation(
                "rank must be an integer",
                invariant="RecommendationOrdering.rank.type",
            )
        if self.rank < 1:
            raise EducationalInvariantViolation(
                "rank must be a positive 1-based integer",
                invariant="RecommendationOrdering.rank.positive",
            )
        if not isinstance(self.priority, RecommendationPriority):
            raise EducationalInvariantViolation(
                "priority must be a RecommendationPriority",
                invariant="RecommendationOrdering.priority.type",
            )
