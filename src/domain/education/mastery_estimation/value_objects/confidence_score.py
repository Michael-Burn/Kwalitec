"""Confidence score — deterministically computed reliability of an estimate.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    Mastery Confidence
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation

# Fixed threshold table — magnitude -> band. Deterministic, never estimated
# by anything other than this table. Reuses the shared foundation
# ConfidenceLevel vocabulary since this is genuinely the same educational
# concept, unlike per-context mastery vocabulary.
_BAND_THRESHOLDS: tuple[tuple[float, ConfidenceLevel], ...] = (
    (0.20, ConfidenceLevel.VERY_LOW),
    (0.40, ConfidenceLevel.LOW),
    (0.60, ConfidenceLevel.MEDIUM),
    (0.80, ConfidenceLevel.HIGH),
)


@dataclass(frozen=True, slots=True)
class ConfidenceScore(EducationalValueObject):
    """Immutable, deterministically computed confidence magnitude.

    ``band`` is always derived from ``magnitude`` by a fixed threshold
    table — never supplied independently.
    """

    magnitude: float

    def _validate(self) -> None:
        if isinstance(self.magnitude, bool) or not isinstance(
            self.magnitude, int | float
        ):
            raise EducationalInvariantViolation(
                "magnitude must be a real number",
                invariant="ConfidenceScore.magnitude.type",
            )
        if self.magnitude < 0.0 or self.magnitude > 1.0:
            raise EducationalInvariantViolation(
                "magnitude must be between 0.0 and 1.0 inclusive",
                invariant="ConfidenceScore.magnitude.range",
            )
        object.__setattr__(self, "magnitude", round(float(self.magnitude), 4))

    @property
    def band(self) -> ConfidenceLevel:
        for threshold, band in _BAND_THRESHOLDS:
            if self.magnitude < threshold:
                return band
        return ConfidenceLevel.VERY_HIGH

    @classmethod
    def zero(cls) -> ConfidenceScore:
        return cls(magnitude=0.0)

    def is_at_least(self, other: ConfidenceScore) -> bool:
        if not isinstance(other, ConfidenceScore):
            raise EducationalInvariantViolation(
                "other must be a ConfidenceScore",
                invariant="ConfidenceScore.is_at_least.type",
            )
        return self.magnitude >= other.magnitude

    def __str__(self) -> str:
        return f"{self.magnitude:.4f}:{self.band.value}"
