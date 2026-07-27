"""Confidence, difficulty, and evidence-strength value objects.

Architecture Source
    knowledge/product/AP-002/SCORING_MODEL.md
    knowledge/product/AP-002/QUESTION_MODEL.md
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.assessment.enums import (
    ConfidenceBand,
    DifficultyBand,
    EvidenceStrengthBand,
)
from domain.assessment.exceptions import (
    AssessmentInvariantViolation,
    InvalidConfidenceRangeError,
)
from domain.education.foundation.base import EducationalValueObject

_CONFIDENCE_TO_BAND: dict[int, ConfidenceBand] = {
    1: ConfidenceBand.VERY_LOW,
    2: ConfidenceBand.LOW,
    3: ConfidenceBand.MEDIUM,
    4: ConfidenceBand.HIGH,
    5: ConfidenceBand.VERY_HIGH,
}


@dataclass(frozen=True, slots=True)
class ConfidenceLevel(EducationalValueObject):
    """Self-reported certainty at response time (1–5 inclusive).

    Soft signal only — never alone upgrades Twin mastery.
    """

    value: int

    def _validate(self) -> None:
        if not isinstance(self.value, int) or isinstance(self.value, bool):
            raise InvalidConfidenceRangeError("ConfidenceLevel must be an integer")
        if self.value < 1 or self.value > 5:
            raise InvalidConfidenceRangeError(
                "ConfidenceLevel must be between 1 and 5 inclusive"
            )

    @property
    def band(self) -> ConfidenceBand:
        return _CONFIDENCE_TO_BAND[self.value]

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True, slots=True)
class DifficultyLevel(EducationalValueObject):
    """Selection difficulty metadata — not a prestige or shame label."""

    band: DifficultyBand

    def _validate(self) -> None:
        if not isinstance(self.band, DifficultyBand):
            raise AssessmentInvariantViolation(
                "band must be a DifficultyBand",
                invariant="DifficultyLevel.band.type",
            )

    def __str__(self) -> str:
        return self.band.value


@dataclass(frozen=True, slots=True)
class EvidenceStrength(EducationalValueObject):
    """Quality/density band of an observation bundle (evidence packaging).

    Exact thresholds for deriving strength belong to later milestones;
    this value object only holds a declared band.
    """

    band: EvidenceStrengthBand

    def _validate(self) -> None:
        if not isinstance(self.band, EvidenceStrengthBand):
            raise AssessmentInvariantViolation(
                "band must be an EvidenceStrengthBand",
                invariant="EvidenceStrength.band.type",
            )

    @classmethod
    def thin(cls) -> EvidenceStrength:
        return cls(band=EvidenceStrengthBand.THIN)

    @classmethod
    def moderate(cls) -> EvidenceStrength:
        return cls(band=EvidenceStrengthBand.MODERATE)

    @classmethod
    def strong(cls) -> EvidenceStrength:
        return cls(band=EvidenceStrengthBand.STRONG)

    def __str__(self) -> str:
        return self.band.value
