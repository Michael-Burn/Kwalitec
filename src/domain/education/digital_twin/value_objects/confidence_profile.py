"""Confidence profile — remembered confidence posture for Twin memory.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    Confidence Profile
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class ConfidenceProfile(EducationalValueObject):
    """Immutable confidence memory snapshot for a learner Twin.

    ConfidenceProfile stores a supplied confidence posture. It does not
    calibrate psychologically, diagnose false confidence, or choose teaching
    intentions.
    """

    overall: ConfidenceLevel
    ratio: float | None = None

    def _validate(self) -> None:
        if not isinstance(self.overall, ConfidenceLevel):
            raise EducationalInvariantViolation(
                "overall must be a ConfidenceLevel",
                invariant="ConfidenceProfile.overall.type",
            )
        if self.ratio is not None:
            if isinstance(self.ratio, bool) or not isinstance(self.ratio, int | float):
                raise EducationalInvariantViolation(
                    "ratio must be a real number when provided",
                    invariant="ConfidenceProfile.ratio.type",
                )
            if self.ratio < 0.0 or self.ratio > 1.0:
                raise EducationalInvariantViolation(
                    "ratio must be between 0.0 and 1.0 inclusive",
                    invariant="ConfidenceProfile.ratio.range",
                )
            object.__setattr__(self, "ratio", float(self.ratio))

    @classmethod
    def unknown(cls) -> ConfidenceProfile:
        return cls(overall=ConfidenceLevel.UNKNOWN)

    @classmethod
    def of(
        cls, overall: ConfidenceLevel, *, ratio: float | None = None
    ) -> ConfidenceProfile:
        return cls(overall=overall, ratio=ratio)

    def __str__(self) -> str:
        if self.ratio is None:
            return self.overall.value
        return f"{self.overall.value}({self.ratio:.2f})"
