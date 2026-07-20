"""Evidence strength — epistemic warrant of an observation.

Architecture Source
    EDUCATIONAL_EVIDENCE_MODEL.md (§4 Evidence Quality Levels)
Concept
    Evidence Strength
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.evidence.enums import EvidenceStrengthLevel
from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation

# Quality Level (0–4) → Strength mapping from Educational Evidence Model §4.
_QUALITY_LEVEL_TO_STRENGTH: dict[int, EvidenceStrengthLevel] = {
    0: EvidenceStrengthLevel.WEAK,
    1: EvidenceStrengthLevel.WEAK,
    2: EvidenceStrengthLevel.MODERATE,
    3: EvidenceStrengthLevel.STRONG,
    4: EvidenceStrengthLevel.VERY_STRONG,
}

_STRENGTH_ORDER: tuple[EvidenceStrengthLevel, ...] = (
    EvidenceStrengthLevel.WEAK,
    EvidenceStrengthLevel.MODERATE,
    EvidenceStrengthLevel.STRONG,
    EvidenceStrengthLevel.VERY_STRONG,
)


@dataclass(frozen=True, slots=True)
class EvidenceStrength(EducationalValueObject):
    """Immutable epistemic strength of educational evidence.

    Strength answers how much observational warrant an observation carries.
    It does not diagnose, recommend, or prioritise learning actions.
    """

    level: EvidenceStrengthLevel

    def _validate(self) -> None:
        if not isinstance(self.level, EvidenceStrengthLevel):
            raise EducationalInvariantViolation(
                "level must be an EvidenceStrengthLevel",
                invariant="EvidenceStrength.level.type",
            )

    @classmethod
    def weak(cls) -> EvidenceStrength:
        return cls(level=EvidenceStrengthLevel.WEAK)

    @classmethod
    def moderate(cls) -> EvidenceStrength:
        return cls(level=EvidenceStrengthLevel.MODERATE)

    @classmethod
    def strong(cls) -> EvidenceStrength:
        return cls(level=EvidenceStrengthLevel.STRONG)

    @classmethod
    def very_strong(cls) -> EvidenceStrength:
        return cls(level=EvidenceStrengthLevel.VERY_STRONG)

    @classmethod
    def from_quality_level(cls, quality_level: int) -> EvidenceStrength:
        """Map Educational Evidence Model quality level (0–4) to strength."""
        if not isinstance(quality_level, int):
            raise EducationalInvariantViolation(
                "quality_level must be an integer",
                invariant="EvidenceStrength.quality_level.type",
            )
        if quality_level not in _QUALITY_LEVEL_TO_STRENGTH:
            raise EducationalInvariantViolation(
                "quality_level must be between 0 and 4 inclusive",
                invariant="EvidenceStrength.quality_level.range",
            )
        return cls(level=_QUALITY_LEVEL_TO_STRENGTH[quality_level])

    def is_weak(self) -> bool:
        return self.level is EvidenceStrengthLevel.WEAK

    def is_moderate(self) -> bool:
        return self.level is EvidenceStrengthLevel.MODERATE

    def is_strong(self) -> bool:
        return self.level is EvidenceStrengthLevel.STRONG

    def is_very_strong(self) -> bool:
        return self.level is EvidenceStrengthLevel.VERY_STRONG

    def at_least(self, other: EvidenceStrength) -> bool:
        """True when this strength is greater than or equal to ``other``."""
        if not isinstance(other, EvidenceStrength):
            raise EducationalInvariantViolation(
                "other must be an EvidenceStrength",
                invariant="EvidenceStrength.at_least.type",
            )
        return _STRENGTH_ORDER.index(self.level) >= _STRENGTH_ORDER.index(other.level)

    def __str__(self) -> str:
        return self.level.value
