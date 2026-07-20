"""Recommendation identity value objects."""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
)


@dataclass(frozen=True, slots=True)
class RecommendationSpecificationId(EducationalValueObject):
    """Identity of a generated RecommendationSpecification."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "RecommendationSpecificationId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class RecommendationId(EducationalValueObject):
    """Identity of a Recommendation within a RecommendationSpecification."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "RecommendationId"),
        )

    def __str__(self) -> str:
        return self.value
