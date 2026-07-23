"""Mastery summary — supplied aggregate mastery posture.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
    KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md
Concept
    Mastery Summary
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.student_state.enums import MasteryBand


@dataclass(frozen=True, slots=True)
class MasterySummary(EducationalValueObject):
    """Immutable, supplied summary of mastery across a student's state.

    MasterySummary stores a supplied overall band and competency-band
    tallies. It does not compute, estimate, or infer mastery — those
    figures must be supplied by an authorised writer.
    """

    overall_band: MasteryBand
    overall_ratio: float | None = None
    mastered_count: int = 0
    secure_count: int = 0
    developing_count: int = 0
    not_started_count: int = 0

    def _validate(self) -> None:
        if not isinstance(self.overall_band, MasteryBand):
            raise EducationalInvariantViolation(
                "overall_band must be a MasteryBand",
                invariant="MasterySummary.overall_band.type",
            )
        if self.overall_ratio is not None:
            if isinstance(self.overall_ratio, bool) or not isinstance(
                self.overall_ratio, int | float
            ):
                raise EducationalInvariantViolation(
                    "overall_ratio must be a real number when provided",
                    invariant="MasterySummary.overall_ratio.type",
                )
            if self.overall_ratio < 0.0 or self.overall_ratio > 1.0:
                raise EducationalInvariantViolation(
                    "overall_ratio must be between 0.0 and 1.0 inclusive",
                    invariant="MasterySummary.overall_ratio.range",
                )
            object.__setattr__(
                self, "overall_ratio", float(self.overall_ratio)
            )
        for field_name in (
            "mastered_count",
            "secure_count",
            "developing_count",
            "not_started_count",
        ):
            value = getattr(self, field_name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise EducationalInvariantViolation(
                    f"{field_name} must be an integer",
                    invariant=f"MasterySummary.{field_name}.type",
                )
            if value < 0:
                raise EducationalInvariantViolation(
                    f"{field_name} must be non-negative",
                    invariant=f"MasterySummary.{field_name}.non_negative",
                )

    @classmethod
    def unknown(cls) -> MasterySummary:
        return cls(overall_band=MasteryBand.UNKNOWN)

    def total_count(self) -> int:
        return (
            self.mastered_count
            + self.secure_count
            + self.developing_count
            + self.not_started_count
        )
