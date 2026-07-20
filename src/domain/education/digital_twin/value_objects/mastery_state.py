"""Mastery state — remembered mastery band for Twin memory.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
    KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md
Concept
    Mastery State
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.digital_twin.enums import MasteryBand
from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class MasteryState(EducationalValueObject):
    """Immutable mastery memory snapshot.

    MasteryState records a supplied mastery band. It does not diagnose,
    interpret evidence, or invent educational meaning.
    """

    band: MasteryBand
    ratio: float | None = None

    def _validate(self) -> None:
        if not isinstance(self.band, MasteryBand):
            raise EducationalInvariantViolation(
                "band must be a MasteryBand",
                invariant="MasteryState.band.type",
            )
        if self.ratio is not None:
            if isinstance(self.ratio, bool) or not isinstance(self.ratio, int | float):
                raise EducationalInvariantViolation(
                    "ratio must be a real number when provided",
                    invariant="MasteryState.ratio.type",
                )
            if self.ratio < 0.0 or self.ratio > 1.0:
                raise EducationalInvariantViolation(
                    "ratio must be between 0.0 and 1.0 inclusive",
                    invariant="MasteryState.ratio.range",
                )
            object.__setattr__(self, "ratio", float(self.ratio))

    @classmethod
    def unknown(cls) -> MasteryState:
        return cls(band=MasteryBand.UNKNOWN)

    @classmethod
    def of(cls, band: MasteryBand, *, ratio: float | None = None) -> MasteryState:
        return cls(band=band, ratio=ratio)

    def __str__(self) -> str:
        if self.ratio is None:
            return self.band.value
        return f"{self.band.value}({self.ratio:.2f})"
