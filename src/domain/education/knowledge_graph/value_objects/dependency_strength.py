"""Dependency strength — educational force of a relationship edge.

Architecture Source
    KNOWLEDGE_DEPENDENCY_MODEL.md
Concept
    Dependency Strength and Adequacy
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.knowledge_graph.enums import DependencyStrengthBand

_BAND_RANK: dict[DependencyStrengthBand, int] = {
    DependencyStrengthBand.OPTIONAL: 0,
    DependencyStrengthBand.HELPFUL: 1,
    DependencyStrengthBand.IMPORTANT: 2,
    DependencyStrengthBand.CRITICAL: 3,
}


@dataclass(frozen=True, slots=True)
class DependencyStrength(EducationalValueObject):
    """Immutable, supplied educational force of a dependency relationship.

    DependencyStrength records a qualitative band and an optional numeric
    weight. It does not compute or infer strength from evidence — the band
    is a claim supplied by an authorised writer of the graph.
    """

    band: DependencyStrengthBand
    weight: float | None = None

    def _validate(self) -> None:
        if not isinstance(self.band, DependencyStrengthBand):
            raise EducationalInvariantViolation(
                "band must be a DependencyStrengthBand",
                invariant="DependencyStrength.band.type",
            )
        if self.weight is not None:
            if isinstance(self.weight, bool) or not isinstance(
                self.weight, int | float
            ):
                raise EducationalInvariantViolation(
                    "weight must be a real number when provided",
                    invariant="DependencyStrength.weight.type",
                )
            if self.weight < 0.0 or self.weight > 1.0:
                raise EducationalInvariantViolation(
                    "weight must be between 0.0 and 1.0 inclusive",
                    invariant="DependencyStrength.weight.range",
                )
            object.__setattr__(self, "weight", float(self.weight))

    @classmethod
    def critical(cls, *, weight: float | None = None) -> DependencyStrength:
        return cls(band=DependencyStrengthBand.CRITICAL, weight=weight)

    @classmethod
    def important(cls, *, weight: float | None = None) -> DependencyStrength:
        return cls(band=DependencyStrengthBand.IMPORTANT, weight=weight)

    @classmethod
    def helpful(cls, *, weight: float | None = None) -> DependencyStrength:
        return cls(band=DependencyStrengthBand.HELPFUL, weight=weight)

    @classmethod
    def optional(cls, *, weight: float | None = None) -> DependencyStrength:
        return cls(band=DependencyStrengthBand.OPTIONAL, weight=weight)

    def rank(self) -> int:
        """Ordinal rank of the band, low (optional) to high (critical)."""
        return _BAND_RANK[self.band]

    def is_stronger_than(self, other: DependencyStrength) -> bool:
        """True when this strength's band outranks ``other``'s band."""
        return self.rank() > other.rank()

    def __str__(self) -> str:
        return self.band.value
