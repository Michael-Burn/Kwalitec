"""Recommendation confidence — warrant honesty of a recommendation.

Architecture Source
    PROJECT_CONTEXT.md
Concept
    Recommendation Confidence
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation

_BAND_THRESHOLDS: tuple[tuple[float, ConfidenceLevel], ...] = (
    (0.20, ConfidenceLevel.VERY_LOW),
    (0.40, ConfidenceLevel.LOW),
    (0.60, ConfidenceLevel.MEDIUM),
    (0.80, ConfidenceLevel.HIGH),
)


@dataclass(frozen=True, slots=True)
class RecommendationConfidence(EducationalValueObject):
    """Immutable confidence magnitude for a recommendation's warrant.

    Distinct from student self-report confidence and from mastery
    confidence: this measures how well-supported the *recommendation
    decision* is by the educational inputs that produced it.
    """

    magnitude: float

    def _validate(self) -> None:
        if isinstance(self.magnitude, bool) or not isinstance(
            self.magnitude, int | float
        ):
            raise EducationalInvariantViolation(
                "magnitude must be a real number",
                invariant="RecommendationConfidence.magnitude.type",
            )
        if self.magnitude < 0.0 or self.magnitude > 1.0:
            raise EducationalInvariantViolation(
                "magnitude must be between 0.0 and 1.0 inclusive",
                invariant="RecommendationConfidence.magnitude.range",
            )
        object.__setattr__(self, "magnitude", round(float(self.magnitude), 4))

    @property
    def band(self) -> ConfidenceLevel:
        for threshold, band in _BAND_THRESHOLDS:
            if self.magnitude < threshold:
                return band
        return ConfidenceLevel.VERY_HIGH

    @classmethod
    def zero(cls) -> RecommendationConfidence:
        return cls(magnitude=0.0)

    def __str__(self) -> str:
        return f"{self.magnitude:.4f}:{self.band.value}"
