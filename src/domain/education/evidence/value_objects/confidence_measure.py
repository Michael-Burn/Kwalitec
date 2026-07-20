"""Confidence measure — observational certainty of recorded evidence.

Architecture Source
    EDUCATIONAL_EVIDENCE_MODEL.md /
    CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md
Concept
    Confidence Measure
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class ConfidenceMeasure(EducationalValueObject):
    """Immutable confidence attached to an educational evidence observation.

    Confidence describes how certain the *observation recording* is (signal
    clarity / attribution clarity). It is not a mastery score, readiness band,
    or student self-confidence diagnosis.
    """

    level: ConfidenceLevel
    ratio: float | None = None

    def _validate(self) -> None:
        if not isinstance(self.level, ConfidenceLevel):
            raise EducationalInvariantViolation(
                "level must be a ConfidenceLevel",
                invariant="ConfidenceMeasure.level.type",
            )
        if self.level is ConfidenceLevel.UNKNOWN:
            raise EducationalInvariantViolation(
                "evidence confidence must not be UNKNOWN",
                invariant="ConfidenceMeasure.level.known",
            )
        if self.ratio is not None:
            if isinstance(self.ratio, bool) or not isinstance(self.ratio, int | float):
                raise EducationalInvariantViolation(
                    "ratio must be a real number when provided",
                    invariant="ConfidenceMeasure.ratio.type",
                )
            if self.ratio < 0.0 or self.ratio > 1.0:
                raise EducationalInvariantViolation(
                    "ratio must be between 0.0 and 1.0 inclusive",
                    invariant="ConfidenceMeasure.ratio.range",
                )
            object.__setattr__(self, "ratio", float(self.ratio))

    @classmethod
    def of(
        cls, level: ConfidenceLevel, *, ratio: float | None = None
    ) -> ConfidenceMeasure:
        return cls(level=level, ratio=ratio)

    def is_at_least(self, other: ConfidenceLevel) -> bool:
        """Compare qualitative bands (UNKNOWN excluded by construction)."""
        order = (
            ConfidenceLevel.VERY_LOW,
            ConfidenceLevel.LOW,
            ConfidenceLevel.MEDIUM,
            ConfidenceLevel.HIGH,
            ConfidenceLevel.VERY_HIGH,
        )
        if other not in order:
            raise EducationalInvariantViolation(
                "comparison requires a known ConfidenceLevel",
                invariant="ConfidenceMeasure.is_at_least.level",
            )
        return order.index(self.level) >= order.index(other)

    def __str__(self) -> str:
        if self.ratio is None:
            return self.level.value
        return f"{self.level.value}({self.ratio:.2f})"
