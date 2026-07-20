"""Instructional impact — consequence of addressing a priority first.

Architecture Source
    EDUCATIONAL_PRIORITY_MODEL.md
Concept
    Instructional Impact
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.priority.enums import InstructionalImpactLevel

_IMPACT_ORDER: tuple[InstructionalImpactLevel, ...] = (
    InstructionalImpactLevel.MARGINAL,
    InstructionalImpactLevel.MATERIAL,
    InstructionalImpactLevel.SUBSTANTIAL,
    InstructionalImpactLevel.TRANSFORMATIONAL,
)


@dataclass(frozen=True, slots=True)
class InstructionalImpact(EducationalValueObject):
    """Immutable statement of instructional consequence for priority ordering.

    Identifies what educational good is expected if this priority governs the
    next episode. It does not select a teaching strategy.
    """

    level: InstructionalImpactLevel
    statement: str

    def _validate(self) -> None:
        if not isinstance(self.level, InstructionalImpactLevel):
            raise EducationalInvariantViolation(
                "level must be an InstructionalImpactLevel",
                invariant="InstructionalImpact.level.type",
            )
        object.__setattr__(
            self,
            "statement",
            require_non_empty_text(self.statement, "statement"),
        )

    @classmethod
    def of(
        cls,
        level: InstructionalImpactLevel,
        statement: str,
    ) -> InstructionalImpact:
        return cls(level=level, statement=statement)

    def is_at_least(self, other: InstructionalImpactLevel) -> bool:
        if other not in _IMPACT_ORDER:
            raise EducationalInvariantViolation(
                "comparison requires a known InstructionalImpactLevel",
                invariant="InstructionalImpact.is_at_least.level",
            )
        return _IMPACT_ORDER.index(self.level) >= _IMPACT_ORDER.index(other)

    def __str__(self) -> str:
        return f"{self.level.value}: {self.statement}"
