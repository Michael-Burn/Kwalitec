"""Retention state — remembered retention band for Twin memory.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    Retention State
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.digital_twin.enums import RetentionBand
from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class RetentionState(EducationalValueObject):
    """Immutable retention memory snapshot.

    RetentionState records a supplied retention band. It does not schedule
    revision, diagnose fading, or choose strategies.
    """

    band: RetentionBand
    ratio: float | None = None

    def _validate(self) -> None:
        if not isinstance(self.band, RetentionBand):
            raise EducationalInvariantViolation(
                "band must be a RetentionBand",
                invariant="RetentionState.band.type",
            )
        if self.ratio is not None:
            if isinstance(self.ratio, bool) or not isinstance(self.ratio, int | float):
                raise EducationalInvariantViolation(
                    "ratio must be a real number when provided",
                    invariant="RetentionState.ratio.type",
                )
            if self.ratio < 0.0 or self.ratio > 1.0:
                raise EducationalInvariantViolation(
                    "ratio must be between 0.0 and 1.0 inclusive",
                    invariant="RetentionState.ratio.range",
                )
            object.__setattr__(self, "ratio", float(self.ratio))

    @classmethod
    def unknown(cls) -> RetentionState:
        return cls(band=RetentionBand.UNKNOWN)

    @classmethod
    def of(
        cls, band: RetentionBand, *, ratio: float | None = None
    ) -> RetentionState:
        return cls(band=band, ratio=ratio)

    def __str__(self) -> str:
        if self.ratio is None:
            return self.band.value
        return f"{self.band.value}({self.ratio:.2f})"
