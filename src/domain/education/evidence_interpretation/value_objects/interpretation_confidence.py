"""Interpretation confidence — certainty of an interpreted pattern set.

Architecture Source
    EDUCATIONAL_EVIDENCE_MODEL.md /
    CAPABILITY_4_8_2_EDUCATIONAL_EVIDENCE_ANALYSIS.md
Concept
    Interpretation Confidence
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class InterpretationConfidence(EducationalValueObject):
    """Immutable confidence attached to an educational interpretation.

    Confidence describes how certain the *pattern interpretation* is given the
    referenced evidence. It is not a mastery score, readiness band, diagnosis
    strength, or recommendation priority.
    """

    level: ConfidenceLevel
    ratio: float | None = None

    def _validate(self) -> None:
        if not isinstance(self.level, ConfidenceLevel):
            raise EducationalInvariantViolation(
                "level must be a ConfidenceLevel",
                invariant="InterpretationConfidence.level.type",
            )
        if self.level is ConfidenceLevel.UNKNOWN:
            raise EducationalInvariantViolation(
                "interpretation confidence must not be UNKNOWN",
                invariant="InterpretationConfidence.level.known",
            )
        if self.ratio is not None:
            if isinstance(self.ratio, bool) or not isinstance(self.ratio, int | float):
                raise EducationalInvariantViolation(
                    "ratio must be a real number when provided",
                    invariant="InterpretationConfidence.ratio.type",
                )
            if self.ratio < 0.0 or self.ratio > 1.0:
                raise EducationalInvariantViolation(
                    "ratio must be between 0.0 and 1.0 inclusive",
                    invariant="InterpretationConfidence.ratio.range",
                )
            object.__setattr__(self, "ratio", float(self.ratio))

    @classmethod
    def of(
        cls, level: ConfidenceLevel, *, ratio: float | None = None
    ) -> InterpretationConfidence:
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
                invariant="InterpretationConfidence.is_at_least.level",
            )
        return order.index(self.level) >= order.index(other)

    def __str__(self) -> str:
        if self.ratio is None:
            return self.level.value
        return f"{self.level.value}({self.ratio:.2f})"
