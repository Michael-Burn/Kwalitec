"""Intention strength — commitment to seeking an educational change.

Architecture Source
    TEACHING_INTENTION_MODEL.md
Concept
    Intention Strength
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.teaching_intention.enums import IntentionStrengthLevel

_STRENGTH_ORDER: tuple[IntentionStrengthLevel, ...] = (
    IntentionStrengthLevel.TENTATIVE,
    IntentionStrengthLevel.MODERATE,
    IntentionStrengthLevel.FIRM,
    IntentionStrengthLevel.COMMITTED,
)


@dataclass(frozen=True, slots=True)
class IntentionStrength(EducationalValueObject):
    """Immutable commitment strength of a teaching intention.

    Strength describes how firmly the tutor commits to this educational
    change. It is not priority, diagnosis confidence, or mastery.
    """

    level: IntentionStrengthLevel
    rationale: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.level, IntentionStrengthLevel):
            raise EducationalInvariantViolation(
                "level must be an IntentionStrengthLevel",
                invariant="IntentionStrength.level.type",
            )
        if self.rationale is not None:
            cleaned = self.rationale.strip()
            if not cleaned:
                raise EducationalInvariantViolation(
                    "strength rationale must be non-empty when provided",
                    invariant="IntentionStrength.rationale.non_empty",
                )
            object.__setattr__(self, "rationale", cleaned)

    @classmethod
    def of(
        cls,
        level: IntentionStrengthLevel,
        *,
        rationale: str | None = None,
    ) -> IntentionStrength:
        return cls(level=level, rationale=rationale)

    @classmethod
    def tentative(cls, *, rationale: str | None = None) -> IntentionStrength:
        return cls(level=IntentionStrengthLevel.TENTATIVE, rationale=rationale)

    @classmethod
    def moderate(cls, *, rationale: str | None = None) -> IntentionStrength:
        return cls(level=IntentionStrengthLevel.MODERATE, rationale=rationale)

    @classmethod
    def firm(cls, *, rationale: str | None = None) -> IntentionStrength:
        return cls(level=IntentionStrengthLevel.FIRM, rationale=rationale)

    @classmethod
    def committed(cls, *, rationale: str | None = None) -> IntentionStrength:
        return cls(level=IntentionStrengthLevel.COMMITTED, rationale=rationale)

    def is_at_least(self, other: IntentionStrengthLevel) -> bool:
        if other not in _STRENGTH_ORDER:
            raise EducationalInvariantViolation(
                "comparison requires a known IntentionStrengthLevel",
                invariant="IntentionStrength.is_at_least.level",
            )
        return _STRENGTH_ORDER.index(self.level) >= _STRENGTH_ORDER.index(other)

    def strengthened(self) -> IntentionStrength:
        """Return the next higher commitment strength."""
        index = _STRENGTH_ORDER.index(self.level)
        if index >= len(_STRENGTH_ORDER) - 1:
            raise EducationalInvariantViolation(
                "intention strength is already at maximum",
                invariant="IntentionStrength.strengthen.max",
            )
        return IntentionStrength(
            level=_STRENGTH_ORDER[index + 1],
            rationale=self.rationale,
        )

    def weakened(self) -> IntentionStrength:
        """Return the next lower commitment strength."""
        index = _STRENGTH_ORDER.index(self.level)
        if index <= 0:
            raise EducationalInvariantViolation(
                "intention strength is already at minimum",
                invariant="IntentionStrength.weaken.min",
            )
        return IntentionStrength(
            level=_STRENGTH_ORDER[index - 1],
            rationale=self.rationale,
        )

    def __str__(self) -> str:
        if self.rationale is None:
            return self.level.value
        return f"{self.level.value}: {self.rationale}"
