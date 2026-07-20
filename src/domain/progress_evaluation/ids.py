"""Progress evaluation identity value objects."""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
)


@dataclass(frozen=True, slots=True)
class ProgressReportId(EducationalValueObject):
    """Identity of a generated ProgressReport."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "ProgressReportId"),
        )

    def __str__(self) -> str:
        return self.value
