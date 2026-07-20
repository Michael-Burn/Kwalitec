"""Urgency — temporal pressure on instructional ordering.

Architecture Source
    EDUCATIONAL_PRIORITY_MODEL.md
Concept
    Urgency
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.priority.enums import UrgencyLevel

_URGENCY_ORDER: tuple[UrgencyLevel, ...] = (
    UrgencyLevel.DEFERRED,
    UrgencyLevel.ROUTINE,
    UrgencyLevel.ELEVATED,
    UrgencyLevel.IMMEDIATE,
    UrgencyLevel.CRITICAL,
)


@dataclass(frozen=True, slots=True)
class Urgency(EducationalValueObject):
    """Immutable urgency attached to an educational priority.

    Urgency expresses ordering pressure (including exam horizon) without
    inventing need or overriding Priority Model gates 1–4.
    """

    level: UrgencyLevel
    rationale: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.level, UrgencyLevel):
            raise EducationalInvariantViolation(
                "level must be an UrgencyLevel",
                invariant="Urgency.level.type",
            )
        if self.rationale is not None:
            cleaned = self.rationale.strip()
            if not cleaned:
                raise EducationalInvariantViolation(
                    "urgency rationale must be non-empty when provided",
                    invariant="Urgency.rationale.non_empty",
                )
            object.__setattr__(self, "rationale", cleaned)

    @classmethod
    def of(
        cls,
        level: UrgencyLevel,
        *,
        rationale: str | None = None,
    ) -> Urgency:
        return cls(level=level, rationale=rationale)

    def is_at_least(self, other: UrgencyLevel) -> bool:
        if other not in _URGENCY_ORDER:
            raise EducationalInvariantViolation(
                "comparison requires a known UrgencyLevel",
                invariant="Urgency.is_at_least.level",
            )
        return _URGENCY_ORDER.index(self.level) >= _URGENCY_ORDER.index(other)

    def elevated(self) -> Urgency:
        """Return the next higher urgency level."""
        index = _URGENCY_ORDER.index(self.level)
        if index >= len(_URGENCY_ORDER) - 1:
            raise EducationalInvariantViolation(
                "urgency is already at maximum level",
                invariant="Urgency.elevate.max",
            )
        return Urgency(level=_URGENCY_ORDER[index + 1], rationale=self.rationale)

    def deferred(self) -> Urgency:
        """Return the next lower urgency level."""
        index = _URGENCY_ORDER.index(self.level)
        if index <= 0:
            raise EducationalInvariantViolation(
                "urgency is already at minimum level",
                invariant="Urgency.defer.min",
            )
        return Urgency(level=_URGENCY_ORDER[index - 1], rationale=self.rationale)

    def __str__(self) -> str:
        if self.rationale is None:
            return self.level.value
        return f"{self.level.value}: {self.rationale}"
