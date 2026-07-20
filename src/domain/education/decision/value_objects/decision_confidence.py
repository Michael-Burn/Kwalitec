"""Decision confidence — certainty of an educational execution decision.

Architecture Source
    EDUCATIONAL_DECISION_POINTS.md
Concept
    Decision Confidence
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class DecisionConfidence(EducationalValueObject):
    """Immutable confidence attached to an educational execution decision.

    Confidence describes how certain the readiness posture is for proceeding
    (or deferring) now. It is not mastery, twin certainty, priority ranking,
    or a teaching-strategy recommendation.
    """

    level: ConfidenceLevel
    ratio: float | None = None

    def _validate(self) -> None:
        if not isinstance(self.level, ConfidenceLevel):
            raise EducationalInvariantViolation(
                "level must be a ConfidenceLevel",
                invariant="DecisionConfidence.level.type",
            )
        if self.level is ConfidenceLevel.UNKNOWN:
            raise EducationalInvariantViolation(
                "decision confidence must not be UNKNOWN",
                invariant="DecisionConfidence.level.known",
            )
        if self.ratio is not None:
            if isinstance(self.ratio, bool) or not isinstance(self.ratio, int | float):
                raise EducationalInvariantViolation(
                    "ratio must be a real number when provided",
                    invariant="DecisionConfidence.ratio.type",
                )
            if self.ratio < 0.0 or self.ratio > 1.0:
                raise EducationalInvariantViolation(
                    "ratio must be between 0.0 and 1.0 inclusive",
                    invariant="DecisionConfidence.ratio.range",
                )
            object.__setattr__(self, "ratio", float(self.ratio))

    @classmethod
    def of(
        cls, level: ConfidenceLevel, *, ratio: float | None = None
    ) -> DecisionConfidence:
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
                invariant="DecisionConfidence.is_at_least.level",
            )
        return order.index(self.level) >= order.index(other)

    def __str__(self) -> str:
        if self.ratio is None:
            return self.level.value
        return f"{self.level.value}({self.ratio:.2f})"
