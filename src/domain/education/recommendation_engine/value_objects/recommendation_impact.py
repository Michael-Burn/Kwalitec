"""Recommendation impact — expected educational effect of acting.

Architecture Source
    PROJECT_CONTEXT.md
Concept
    Recommendation Impact
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.recommendation_engine.enums import RecommendationImpactBand

_BAND_THRESHOLDS: tuple[tuple[float, RecommendationImpactBand], ...] = (
    (0.34, RecommendationImpactBand.LOW),
    (0.67, RecommendationImpactBand.MEDIUM),
)


@dataclass(frozen=True, slots=True)
class RecommendationImpact(EducationalValueObject):
    """Immutable impact magnitude with a derived qualitative band.

    ``band`` is always derived from ``magnitude`` — never supplied
    independently.
    """

    magnitude: float

    def _validate(self) -> None:
        if isinstance(self.magnitude, bool) or not isinstance(
            self.magnitude, int | float
        ):
            raise EducationalInvariantViolation(
                "magnitude must be a real number",
                invariant="RecommendationImpact.magnitude.type",
            )
        if self.magnitude < 0.0 or self.magnitude > 1.0:
            raise EducationalInvariantViolation(
                "magnitude must be between 0.0 and 1.0 inclusive",
                invariant="RecommendationImpact.magnitude.range",
            )
        object.__setattr__(self, "magnitude", round(float(self.magnitude), 4))

    @property
    def band(self) -> RecommendationImpactBand:
        for threshold, band in _BAND_THRESHOLDS:
            if self.magnitude < threshold:
                return band
        return RecommendationImpactBand.HIGH

    def is_at_least(self, other: RecommendationImpact) -> bool:
        if not isinstance(other, RecommendationImpact):
            raise EducationalInvariantViolation(
                "other must be a RecommendationImpact",
                invariant="RecommendationImpact.is_at_least.type",
            )
        return self.magnitude >= other.magnitude

    def __str__(self) -> str:
        return f"{self.magnitude:.4f}:{self.band.value}"
