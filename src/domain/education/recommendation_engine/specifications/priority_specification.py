"""Specification: recommendation priority is educationally actionable.

Architecture Source
    PROJECT_CONTEXT.md
Concept
    Priority Specification
"""

from __future__ import annotations

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.recommendation_engine.enums import RecommendationPriorityBand
from domain.education.recommendation_engine.value_objects.recommendation import (
    Recommendation,
)
from domain.education.recommendation_engine.value_objects.recommendation_priority import (  # noqa: E501
    RecommendationPriority,
)


class PrioritySpecification:
    """A priority must be well-formed and band-consistent."""

    @staticmethod
    def is_satisfied_by(
        candidate: Recommendation | RecommendationPriority,
    ) -> bool:
        priority = (
            candidate.priority
            if isinstance(candidate, Recommendation)
            else candidate
        )
        if not isinstance(priority, RecommendationPriority):
            return False
        if priority.magnitude < 0.0 or priority.magnitude > 1.0:
            return False
        # Band must agree with magnitude thresholds.
        expected = RecommendationPriority(magnitude=priority.magnitude).band
        return priority.band is expected

    @staticmethod
    def assert_satisfied_by(
        candidate: Recommendation | RecommendationPriority,
    ) -> None:
        if not PrioritySpecification.is_satisfied_by(candidate):
            raise EducationalInvariantViolation(
                "priority must be well-formed with a consistent band",
                invariant="PrioritySpecification.well_formed",
            )

    @staticmethod
    def is_actionable(priority: RecommendationPriority) -> bool:
        """Priorities at or above MEDIUM are considered actionable."""
        return priority.band in {
            RecommendationPriorityBand.MEDIUM,
            RecommendationPriorityBand.HIGH,
            RecommendationPriorityBand.CRITICAL,
        }
