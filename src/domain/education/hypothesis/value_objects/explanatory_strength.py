"""Explanatory strength — how well a hypothesis accounts for observations.

Architecture Source
    EDUCATIONAL_HYPOTHESIS_MODEL.md
Concept
    Explanatory Strength
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.hypothesis.enums import ExplanatoryStrengthLevel

_STRENGTH_ORDER: tuple[ExplanatoryStrengthLevel, ...] = (
    ExplanatoryStrengthLevel.WEAK,
    ExplanatoryStrengthLevel.MODERATE,
    ExplanatoryStrengthLevel.STRONG,
    ExplanatoryStrengthLevel.COMPELLING,
)


@dataclass(frozen=True, slots=True)
class ExplanatoryStrength(EducationalValueObject):
    """Immutable explanatory strength of an educational hypothesis.

    Strength answers how thoroughly the explanation accounts for supporting
    and contradicting observations. It does not diagnose, prioritise, or
    select teaching strategy.
    """

    level: ExplanatoryStrengthLevel

    def _validate(self) -> None:
        if not isinstance(self.level, ExplanatoryStrengthLevel):
            raise EducationalInvariantViolation(
                "level must be an ExplanatoryStrengthLevel",
                invariant="ExplanatoryStrength.level.type",
            )

    @classmethod
    def of(cls, level: ExplanatoryStrengthLevel) -> ExplanatoryStrength:
        return cls(level=level)

    @classmethod
    def weak(cls) -> ExplanatoryStrength:
        return cls(level=ExplanatoryStrengthLevel.WEAK)

    @classmethod
    def moderate(cls) -> ExplanatoryStrength:
        return cls(level=ExplanatoryStrengthLevel.MODERATE)

    @classmethod
    def strong(cls) -> ExplanatoryStrength:
        return cls(level=ExplanatoryStrengthLevel.STRONG)

    @classmethod
    def compelling(cls) -> ExplanatoryStrength:
        return cls(level=ExplanatoryStrengthLevel.COMPELLING)

    def is_weak(self) -> bool:
        return self.level is ExplanatoryStrengthLevel.WEAK

    def is_moderate(self) -> bool:
        return self.level is ExplanatoryStrengthLevel.MODERATE

    def is_strong(self) -> bool:
        return self.level is ExplanatoryStrengthLevel.STRONG

    def is_compelling(self) -> bool:
        return self.level is ExplanatoryStrengthLevel.COMPELLING

    def at_least(self, other: ExplanatoryStrength) -> bool:
        """True when this strength is greater than or equal to ``other``."""
        if not isinstance(other, ExplanatoryStrength):
            raise EducationalInvariantViolation(
                "other must be an ExplanatoryStrength",
                invariant="ExplanatoryStrength.at_least.type",
            )
        return _STRENGTH_ORDER.index(self.level) >= _STRENGTH_ORDER.index(other.level)

    def strengthened(self) -> ExplanatoryStrength:
        """Return the next higher explanatory strength level."""
        index = _STRENGTH_ORDER.index(self.level)
        if index >= len(_STRENGTH_ORDER) - 1:
            raise EducationalInvariantViolation(
                "explanatory strength is already at maximum",
                invariant="ExplanatoryStrength.strengthen.max",
            )
        return ExplanatoryStrength(level=_STRENGTH_ORDER[index + 1])

    def weakened(self) -> ExplanatoryStrength:
        """Return the next lower explanatory strength level."""
        index = _STRENGTH_ORDER.index(self.level)
        if index <= 0:
            raise EducationalInvariantViolation(
                "explanatory strength is already at minimum",
                invariant="ExplanatoryStrength.weaken.min",
            )
        return ExplanatoryStrength(level=_STRENGTH_ORDER[index - 1])

    def __str__(self) -> str:
        return self.level.value
