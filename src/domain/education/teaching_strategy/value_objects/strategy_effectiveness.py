"""Strategy effectiveness — expected instructional efficacy estimate.

Architecture Source
    TEACHING_STRATEGY_ARCHITECTURE.md
Concept
    Expected Effectiveness
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.teaching_strategy.enums import EffectivenessLevel


@dataclass(frozen=True, slots=True)
class StrategyEffectiveness(EducationalValueObject):
    """Immutable expected-effectiveness estimate for a teaching strategy.

    Effectiveness expresses how well the tutor expects the chosen approach
    to advance the Teaching Intention. It is not mastery, twin score, or
    engagement.
    """

    level: EffectivenessLevel
    rationale: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.level, EffectivenessLevel):
            raise EducationalInvariantViolation(
                "level must be an EffectivenessLevel",
                invariant="StrategyEffectiveness.level.type",
            )
        if self.rationale is not None:
            cleaned = self.rationale.strip()
            if not cleaned:
                raise EducationalInvariantViolation(
                    "effectiveness rationale must be non-empty when provided",
                    invariant="StrategyEffectiveness.rationale.non_empty",
                )
            object.__setattr__(self, "rationale", cleaned)
            self._assert_no_mastery_claim(cleaned)

    @staticmethod
    def _assert_no_mastery_claim(text: str) -> None:
        lowered = text.casefold()
        forbidden = ("mastered", "achieve mastery", "declare mastery", "full mastery")
        for token in forbidden:
            if token in lowered:
                raise EducationalInvariantViolation(
                    "strategy effectiveness must never claim mastery",
                    invariant="StrategyEffectiveness.no_mastery_claim",
                )

    @classmethod
    def of(
        cls,
        level: EffectivenessLevel,
        *,
        rationale: str | None = None,
    ) -> StrategyEffectiveness:
        return cls(level=level, rationale=rationale)

    @classmethod
    def low(cls, *, rationale: str | None = None) -> StrategyEffectiveness:
        return cls(level=EffectivenessLevel.LOW, rationale=rationale)

    @classmethod
    def moderate(cls, *, rationale: str | None = None) -> StrategyEffectiveness:
        return cls(level=EffectivenessLevel.MODERATE, rationale=rationale)

    @classmethod
    def high(cls, *, rationale: str | None = None) -> StrategyEffectiveness:
        return cls(level=EffectivenessLevel.HIGH, rationale=rationale)

    @classmethod
    def uncertain(cls, *, rationale: str | None = None) -> StrategyEffectiveness:
        return cls(level=EffectivenessLevel.UNCERTAIN, rationale=rationale)

    def is_at_least(self, other: EffectivenessLevel) -> bool:
        order = (
            EffectivenessLevel.UNCERTAIN,
            EffectivenessLevel.LOW,
            EffectivenessLevel.MODERATE,
            EffectivenessLevel.HIGH,
        )
        if other not in order or self.level not in order:
            raise EducationalInvariantViolation(
                "comparison requires a known EffectivenessLevel",
                invariant="StrategyEffectiveness.is_at_least.level",
            )
        return order.index(self.level) >= order.index(other)

    def __str__(self) -> str:
        if self.rationale is None:
            return self.level.value
        return f"{self.level.value}: {self.rationale}"
