"""Explainability identity value objects."""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
)


@dataclass(frozen=True, slots=True)
class EducationalExplanationId(EducationalValueObject):
    """Identity of a generated EducationalExplanation."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "EducationalExplanationId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class ExplanationSectionId(EducationalValueObject):
    """Identity of an ExplanationSection within an EducationalExplanation."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "ExplanationSectionId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class DecisionTraceId(EducationalValueObject):
    """Identity of a DecisionTrace within an EducationalExplanation."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "DecisionTraceId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class EvidenceReferenceId(EducationalValueObject):
    """Identity of an EvidenceReference within an EducationalExplanation."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "EvidenceReferenceId"),
        )

    def __str__(self) -> str:
        return self.value
