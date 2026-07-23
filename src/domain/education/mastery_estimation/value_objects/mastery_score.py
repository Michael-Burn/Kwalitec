"""Mastery score — a computed magnitude of demonstrated competency mastery.

Architecture Source
    KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md
Concept
    Mastery Score
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.mastery_estimation.enums import MasteryBand

_BAND_THRESHOLDS: tuple[tuple[float, MasteryBand], ...] = (
    (0.25, MasteryBand.NOT_STARTED),
    (0.60, MasteryBand.DEVELOPING),
    (0.85, MasteryBand.SECURE),
)


@dataclass(frozen=True, slots=True)
class MasteryScore(EducationalValueObject):
    """Immutable, deterministically computed mastery magnitude.

    ``band`` is always derived from ``magnitude`` and ``evidence_count`` —
    never supplied independently — so the two can never disagree. A
    competency with no supporting evidence is always ``NOT_ASSESSED``,
    regardless of magnitude.
    """

    magnitude: float
    evidence_count: int = 0

    def _validate(self) -> None:
        if isinstance(self.magnitude, bool) or not isinstance(
            self.magnitude, int | float
        ):
            raise EducationalInvariantViolation(
                "magnitude must be a real number",
                invariant="MasteryScore.magnitude.type",
            )
        if self.magnitude < 0.0 or self.magnitude > 1.0:
            raise EducationalInvariantViolation(
                "magnitude must be between 0.0 and 1.0 inclusive",
                invariant="MasteryScore.magnitude.range",
            )
        object.__setattr__(self, "magnitude", round(float(self.magnitude), 4))
        if isinstance(self.evidence_count, bool) or not isinstance(
            self.evidence_count, int
        ):
            raise EducationalInvariantViolation(
                "evidence_count must be an integer",
                invariant="MasteryScore.evidence_count.type",
            )
        if self.evidence_count < 0:
            raise EducationalInvariantViolation(
                "evidence_count must be non-negative",
                invariant="MasteryScore.evidence_count.non_negative",
            )

    @property
    def band(self) -> MasteryBand:
        if self.evidence_count == 0:
            return MasteryBand.NOT_ASSESSED
        for threshold, band in _BAND_THRESHOLDS:
            if self.magnitude < threshold:
                return band
        return MasteryBand.MASTERED

    @classmethod
    def not_assessed(cls) -> MasteryScore:
        return cls(magnitude=0.0, evidence_count=0)

    def has_evidence(self) -> bool:
        return self.evidence_count > 0

    def is_at_least(self, other: MasteryScore) -> bool:
        if not isinstance(other, MasteryScore):
            raise EducationalInvariantViolation(
                "other must be a MasteryScore",
                invariant="MasteryScore.is_at_least.type",
            )
        return self.magnitude >= other.magnitude

    def __str__(self) -> str:
        return f"{self.magnitude:.4f}:{self.band.value}"
