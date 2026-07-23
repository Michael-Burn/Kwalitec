"""Typed identifiers for Experience Integration artefacts."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.integration.errors import (
    IntegrationInvariantViolation,
)


@dataclass(frozen=True, slots=True)
class ExperienceBundleId:
    """Opaque identifier for a composed experience snapshot bundle."""

    value: str

    def __post_init__(self) -> None:
        value = (self.value or "").strip()
        if not value:
            raise IntegrationInvariantViolation(
                "ExperienceBundleId value must be a non-empty string",
                invariant="ExperienceBundleId.value.required",
            )
        object.__setattr__(self, "value", value)

    def __str__(self) -> str:
        return self.value
