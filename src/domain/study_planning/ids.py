"""Study planning identity value objects."""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
)


@dataclass(frozen=True, slots=True)
class StudyPlanId(EducationalValueObject):
    """Identity of a generated StudyPlan."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "StudyPlanId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class StudySessionId(EducationalValueObject):
    """Identity of a StudySession within a StudyPlan."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "StudySessionId"),
        )

    def __str__(self) -> str:
        return self.value
