"""Mission generation identity value objects."""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
)


@dataclass(frozen=True, slots=True)
class MissionSpecificationId(EducationalValueObject):
    """Identity of a generated MissionSpecification."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "MissionSpecificationId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class MissionTaskId(EducationalValueObject):
    """Identity of a MissionTask within a MissionSequence."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "MissionTaskId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class MissionObjectiveId(EducationalValueObject):
    """Identity of a MissionObjective within a MissionSpecification."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "MissionObjectiveId"),
        )

    def __str__(self) -> str:
        return self.value
