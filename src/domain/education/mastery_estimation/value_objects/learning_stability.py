"""Learning stability — volatility of a student's demonstrated mastery signal.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    Learning Stability
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.mastery_estimation.enums import LearningStabilityBand

_MIN_EVIDENCE_FOR_STABILITY = 2

_BAND_THRESHOLDS: tuple[tuple[float, LearningStabilityBand], ...] = (
    (0.40, LearningStabilityBand.VOLATILE),
    (0.75, LearningStabilityBand.MODERATE),
)


@dataclass(frozen=True, slots=True)
class LearningStability(EducationalValueObject):
    """Immutable, deterministically computed learning-stability posture.

    ``magnitude`` is one minus the population variance of signed evidence
    contributions over time: ``1.0`` denotes perfectly consistent
    performance, ``0.0`` denotes maximal volatility. Fewer than two
    evidence points cannot support a variance measurement, so ``band`` is
    always ``INSUFFICIENT_DATA`` in that case regardless of ``magnitude``.
    """

    magnitude: float
    evidence_count: int = 0
    variance: float = 0.0

    def _validate(self) -> None:
        for field_name in ("magnitude", "variance"):
            value = getattr(self, field_name)
            if isinstance(value, bool) or not isinstance(value, int | float):
                raise EducationalInvariantViolation(
                    f"{field_name} must be a real number",
                    invariant=f"LearningStability.{field_name}.type",
                )
            if value < 0.0 or value > 1.0:
                raise EducationalInvariantViolation(
                    f"{field_name} must be between 0.0 and 1.0 inclusive",
                    invariant=f"LearningStability.{field_name}.range",
                )
            object.__setattr__(self, field_name, round(float(value), 4))
        if isinstance(self.evidence_count, bool) or not isinstance(
            self.evidence_count, int
        ):
            raise EducationalInvariantViolation(
                "evidence_count must be an integer",
                invariant="LearningStability.evidence_count.type",
            )
        if self.evidence_count < 0:
            raise EducationalInvariantViolation(
                "evidence_count must be non-negative",
                invariant="LearningStability.evidence_count.non_negative",
            )

    @property
    def band(self) -> LearningStabilityBand:
        if self.evidence_count < _MIN_EVIDENCE_FOR_STABILITY:
            return LearningStabilityBand.INSUFFICIENT_DATA
        for threshold, band in _BAND_THRESHOLDS:
            if self.magnitude < threshold:
                return band
        return LearningStabilityBand.STABLE

    @classmethod
    def insufficient_data(cls) -> LearningStability:
        return cls(magnitude=0.0, evidence_count=0, variance=0.0)

    def __str__(self) -> str:
        return f"{self.magnitude:.4f}:{self.band.value}"
