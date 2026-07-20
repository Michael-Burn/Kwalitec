"""Instructional complexity — cognitive demand of a teaching strategy.

Architecture Source
    STRATEGY_SELECTION_MODEL.md (R-S11)
Concept
    Instructional Complexity / Cognitive Load Cap
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.teaching_strategy.enums import ComplexityLevel

_COMPLEXITY_ORDER: tuple[ComplexityLevel, ...] = (
    ComplexityLevel.LOW,
    ComplexityLevel.MODERATE,
    ComplexityLevel.HIGH,
    ComplexityLevel.VERY_HIGH,
)


@dataclass(frozen=True, slots=True)
class InstructionalComplexity(EducationalValueObject):
    """Immutable instructional complexity of a teaching strategy.

    Complexity caps strategy ambition under cognitive load. It is not
    curriculum difficulty, priority urgency, or a mastery claim.
    """

    level: ComplexityLevel
    rationale: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.level, ComplexityLevel):
            raise EducationalInvariantViolation(
                "level must be a ComplexityLevel",
                invariant="InstructionalComplexity.level.type",
            )
        if self.rationale is not None:
            cleaned = self.rationale.strip()
            if not cleaned:
                raise EducationalInvariantViolation(
                    "complexity rationale must be non-empty when provided",
                    invariant="InstructionalComplexity.rationale.non_empty",
                )
            object.__setattr__(self, "rationale", cleaned)

    @classmethod
    def of(
        cls,
        level: ComplexityLevel,
        *,
        rationale: str | None = None,
    ) -> InstructionalComplexity:
        return cls(level=level, rationale=rationale)

    @classmethod
    def low(cls, *, rationale: str | None = None) -> InstructionalComplexity:
        return cls(level=ComplexityLevel.LOW, rationale=rationale)

    @classmethod
    def moderate(cls, *, rationale: str | None = None) -> InstructionalComplexity:
        return cls(level=ComplexityLevel.MODERATE, rationale=rationale)

    @classmethod
    def high(cls, *, rationale: str | None = None) -> InstructionalComplexity:
        return cls(level=ComplexityLevel.HIGH, rationale=rationale)

    @classmethod
    def very_high(cls, *, rationale: str | None = None) -> InstructionalComplexity:
        return cls(level=ComplexityLevel.VERY_HIGH, rationale=rationale)

    def is_at_most(self, other: ComplexityLevel) -> bool:
        if other not in _COMPLEXITY_ORDER:
            raise EducationalInvariantViolation(
                "comparison requires a known ComplexityLevel",
                invariant="InstructionalComplexity.is_at_most.level",
            )
        return _COMPLEXITY_ORDER.index(self.level) <= _COMPLEXITY_ORDER.index(other)

    def exceeds(self, other: ComplexityLevel) -> bool:
        return not self.is_at_most(other)

    def __str__(self) -> str:
        if self.rationale is None:
            return self.level.value
        return f"{self.level.value}: {self.rationale}"
