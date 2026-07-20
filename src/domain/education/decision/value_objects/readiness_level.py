"""Readiness level — fitness of a planned intervention for execution.

Architecture Source
    EDUCATIONAL_DECISION_POINTS.md
Concept
    Readiness Level
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.decision.enums import ReadinessBand
from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation

_READINESS_ORDER: tuple[ReadinessBand, ...] = (
    ReadinessBand.BLOCKED,
    ReadinessBand.NOT_READY,
    ReadinessBand.PARTIALLY_READY,
    ReadinessBand.READY,
)


@dataclass(frozen=True, slots=True)
class ReadinessLevel(EducationalValueObject):
    """Immutable readiness posture for executing a planned intervention.

    Readiness answers whether the intervention may proceed *now*. It is not
    mastery, diagnosis severity, priority score, or strategy effectiveness.
    """

    band: ReadinessBand
    ratio: float | None = None
    rationale: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.band, ReadinessBand):
            raise EducationalInvariantViolation(
                "band must be a ReadinessBand",
                invariant="ReadinessLevel.band.type",
            )
        if self.ratio is not None:
            if isinstance(self.ratio, bool) or not isinstance(self.ratio, int | float):
                raise EducationalInvariantViolation(
                    "ratio must be a real number when provided",
                    invariant="ReadinessLevel.ratio.type",
                )
            if self.ratio < 0.0 or self.ratio > 1.0:
                raise EducationalInvariantViolation(
                    "ratio must be between 0.0 and 1.0 inclusive",
                    invariant="ReadinessLevel.ratio.range",
                )
            object.__setattr__(self, "ratio", float(self.ratio))
        if self.rationale is not None:
            cleaned = self.rationale.strip()
            if not cleaned:
                raise EducationalInvariantViolation(
                    "readiness rationale must be non-empty when provided",
                    invariant="ReadinessLevel.rationale.non_empty",
                )
            object.__setattr__(self, "rationale", cleaned)

    @classmethod
    def of(
        cls,
        band: ReadinessBand,
        *,
        ratio: float | None = None,
        rationale: str | None = None,
    ) -> ReadinessLevel:
        return cls(band=band, ratio=ratio, rationale=rationale)

    def is_at_least(self, other: ReadinessBand) -> bool:
        if other not in _READINESS_ORDER:
            raise EducationalInvariantViolation(
                "comparison requires a known ReadinessBand",
                invariant="ReadinessLevel.is_at_least.band",
            )
        return _READINESS_ORDER.index(self.band) >= _READINESS_ORDER.index(other)

    def is_ready(self) -> bool:
        return self.band is ReadinessBand.READY

    def is_blocked(self) -> bool:
        return self.band is ReadinessBand.BLOCKED

    def permits_approval(self) -> bool:
        """Approval requires READY; blocked or incomplete postures forbid it."""
        return self.band is ReadinessBand.READY

    def __str__(self) -> str:
        if self.ratio is None:
            return self.band.value
        return f"{self.band.value}({self.ratio:.2f})"
