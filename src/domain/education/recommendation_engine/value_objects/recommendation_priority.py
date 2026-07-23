"""Recommendation priority — educational urgency of acting on a recommendation.

Architecture Source
    PROJECT_CONTEXT.md
Concept
    Recommendation Priority
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.recommendation_engine.enums import RecommendationPriorityBand

_BAND_THRESHOLDS: tuple[tuple[float, RecommendationPriorityBand], ...] = (
    (0.25, RecommendationPriorityBand.LOW),
    (0.50, RecommendationPriorityBand.MEDIUM),
    (0.75, RecommendationPriorityBand.HIGH),
)


@dataclass(frozen=True, slots=True)
class RecommendationPriority(EducationalValueObject):
    """Immutable priority magnitude with a derived qualitative band.

    ``band`` is always derived from ``magnitude`` — never supplied
    independently — so the two can never disagree.
    """

    magnitude: float

    def _validate(self) -> None:
        if isinstance(self.magnitude, bool) or not isinstance(
            self.magnitude, int | float
        ):
            raise EducationalInvariantViolation(
                "magnitude must be a real number",
                invariant="RecommendationPriority.magnitude.type",
            )
        if self.magnitude < 0.0 or self.magnitude > 1.0:
            raise EducationalInvariantViolation(
                "magnitude must be between 0.0 and 1.0 inclusive",
                invariant="RecommendationPriority.magnitude.range",
            )
        object.__setattr__(self, "magnitude", round(float(self.magnitude), 4))

    @property
    def band(self) -> RecommendationPriorityBand:
        for threshold, band in _BAND_THRESHOLDS:
            if self.magnitude < threshold:
                return band
        return RecommendationPriorityBand.CRITICAL

    def is_at_least(self, other: RecommendationPriority) -> bool:
        if not isinstance(other, RecommendationPriority):
            raise EducationalInvariantViolation(
                "other must be a RecommendationPriority",
                invariant="RecommendationPriority.is_at_least.type",
            )
        return self.magnitude >= other.magnitude

    def __str__(self) -> str:
        return f"{self.magnitude:.4f}:{self.band.value}"
