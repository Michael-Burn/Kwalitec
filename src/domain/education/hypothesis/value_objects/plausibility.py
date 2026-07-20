"""Plausibility — provisional confidence posture of a hypothesis.

Architecture Source
    EDUCATIONAL_HYPOTHESIS_MODEL.md
Concept
    Hypothesis Plausibility
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.hypothesis.enums import PlausibilityLevel

_PLAUSIBILITY_ORDER: tuple[PlausibilityLevel, ...] = (
    PlausibilityLevel.TENTATIVE,
    PlausibilityLevel.WORKING,
    PlausibilityLevel.STRONG,
)


@dataclass(frozen=True, slots=True)
class Plausibility(EducationalValueObject):
    """Immutable plausibility attached to an educational hypothesis.

    Plausibility describes how warranted the *current explanation* is. It is
    not a mastery score, diagnosis confidence, priority ranking, or teaching
    recommendation. SUSPENDED holds the hypothesis aside while a competitor
    is tested.
    """

    level: PlausibilityLevel
    ratio: float | None = None

    def _validate(self) -> None:
        if not isinstance(self.level, PlausibilityLevel):
            raise EducationalInvariantViolation(
                "level must be a PlausibilityLevel",
                invariant="Plausibility.level.type",
            )
        if self.ratio is not None:
            if isinstance(self.ratio, bool) or not isinstance(self.ratio, int | float):
                raise EducationalInvariantViolation(
                    "ratio must be a real number when provided",
                    invariant="Plausibility.ratio.type",
                )
            if self.ratio < 0.0 or self.ratio > 1.0:
                raise EducationalInvariantViolation(
                    "ratio must be between 0.0 and 1.0 inclusive",
                    invariant="Plausibility.ratio.range",
                )
            object.__setattr__(self, "ratio", float(self.ratio))

    @classmethod
    def of(
        cls, level: PlausibilityLevel, *, ratio: float | None = None
    ) -> Plausibility:
        return cls(level=level, ratio=ratio)

    @classmethod
    def tentative(cls, *, ratio: float | None = None) -> Plausibility:
        return cls(level=PlausibilityLevel.TENTATIVE, ratio=ratio)

    @classmethod
    def working(cls, *, ratio: float | None = None) -> Plausibility:
        return cls(level=PlausibilityLevel.WORKING, ratio=ratio)

    @classmethod
    def strong(cls, *, ratio: float | None = None) -> Plausibility:
        return cls(level=PlausibilityLevel.STRONG, ratio=ratio)

    @classmethod
    def suspended(cls, *, ratio: float | None = None) -> Plausibility:
        return cls(level=PlausibilityLevel.SUSPENDED, ratio=ratio)

    def is_suspended(self) -> bool:
        return self.level is PlausibilityLevel.SUSPENDED

    def is_at_least(self, other: PlausibilityLevel) -> bool:
        """Compare ordered postures (SUSPENDED is not ordered)."""
        if self.level is PlausibilityLevel.SUSPENDED:
            return False
        if other is PlausibilityLevel.SUSPENDED:
            raise EducationalInvariantViolation(
                "comparison requires a non-suspended PlausibilityLevel",
                invariant="Plausibility.is_at_least.level",
            )
        if other not in _PLAUSIBILITY_ORDER:
            raise EducationalInvariantViolation(
                "comparison requires a known PlausibilityLevel",
                invariant="Plausibility.is_at_least.level",
            )
        return _PLAUSIBILITY_ORDER.index(self.level) >= _PLAUSIBILITY_ORDER.index(
            other
        )

    def strengthened(self) -> Plausibility:
        """Return the next higher ordered plausibility posture."""
        if self.level is PlausibilityLevel.SUSPENDED:
            raise EducationalInvariantViolation(
                "cannot strengthen a suspended plausibility posture",
                invariant="Plausibility.strengthen.suspended",
            )
        index = _PLAUSIBILITY_ORDER.index(self.level)
        if index >= len(_PLAUSIBILITY_ORDER) - 1:
            raise EducationalInvariantViolation(
                "plausibility is already at maximum strength",
                invariant="Plausibility.strengthen.max",
            )
        return Plausibility(level=_PLAUSIBILITY_ORDER[index + 1], ratio=self.ratio)

    def weakened(self) -> Plausibility:
        """Return the next lower ordered plausibility posture."""
        if self.level is PlausibilityLevel.SUSPENDED:
            raise EducationalInvariantViolation(
                "cannot weaken a suspended plausibility posture",
                invariant="Plausibility.weaken.suspended",
            )
        index = _PLAUSIBILITY_ORDER.index(self.level)
        if index <= 0:
            raise EducationalInvariantViolation(
                "plausibility is already at minimum strength",
                invariant="Plausibility.weaken.min",
            )
        return Plausibility(level=_PLAUSIBILITY_ORDER[index - 1], ratio=self.ratio)

    def __str__(self) -> str:
        if self.ratio is None:
            return self.level.value
        return f"{self.level.value}({self.ratio:.2f})"
