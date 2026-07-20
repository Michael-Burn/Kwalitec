"""Priority factor — educational contribution to instructional ordering.

Architecture Source
    EDUCATIONAL_PRIORITY_MODEL.md
Concept
    Priority Factor
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.priority.enums import PriorityFactorKind


@dataclass(frozen=True, slots=True)
class PriorityFactorId(EducationalValueObject):
    """Identity of a priority factor within an EducationalPriority."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "PriorityFactorId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class PriorityFactor(EducationalEntity):
    """Educational factor contributing to instructional ordering.

    Factors describe *why* a diagnosed problem should be ordered ahead of
    others. They never diagnose, explain why the deficiency exists, or choose
    teaching strategies. Contribution is a qualitative weight in [0, 1].
    """

    factor_id: PriorityFactorId
    kind: PriorityFactorKind
    contribution: float
    rationale: str

    @property
    def entity_id(self) -> PriorityFactorId:
        return self.factor_id

    def _validate(self) -> None:
        if not isinstance(self.factor_id, PriorityFactorId):
            raise EducationalInvariantViolation(
                "factor_id must be a PriorityFactorId",
                invariant="PriorityFactor.factor_id.type",
            )
        if not isinstance(self.kind, PriorityFactorKind):
            raise EducationalInvariantViolation(
                "kind must be a PriorityFactorKind",
                invariant="PriorityFactor.kind.type",
            )
        if isinstance(self.contribution, bool) or not isinstance(
            self.contribution, int | float
        ):
            raise EducationalInvariantViolation(
                "contribution must be a real number",
                invariant="PriorityFactor.contribution.type",
            )
        if self.contribution < 0.0 or self.contribution > 1.0:
            raise EducationalInvariantViolation(
                "contribution must be between 0.0 and 1.0 inclusive",
                invariant="PriorityFactor.contribution.range",
            )
        object.__setattr__(self, "contribution", float(self.contribution))
        object.__setattr__(
            self,
            "rationale",
            require_non_empty_text(self.rationale, "rationale"),
        )

    def factor_signature(self) -> tuple[str, float]:
        """Structural fingerprint used to reject duplicate factors."""
        return (self.kind.value, round(self.contribution, 6))

    def with_contribution(self, contribution: float) -> PriorityFactor:
        """Return a copy with an amended contribution weight."""
        return PriorityFactor(
            factor_id=self.factor_id,
            kind=self.kind,
            contribution=contribution,
            rationale=self.rationale,
        )

    def with_rationale(self, rationale: str) -> PriorityFactor:
        """Return a copy with an amended educational rationale."""
        return PriorityFactor(
            factor_id=self.factor_id,
            kind=self.kind,
            contribution=self.contribution,
            rationale=rationale,
        )
