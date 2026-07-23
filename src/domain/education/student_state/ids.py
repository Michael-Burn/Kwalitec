"""Student Educational State identity value objects.

Opaque, immutable identifiers scoped to the Student Educational State
aggregate. Identities are not database keys and carry no persistence
semantics.
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
)


@dataclass(frozen=True, slots=True)
class StudentEducationalStateId(EducationalValueObject):
    """Identity of a StudentEducationalState aggregate."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "StudentEducationalStateId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class SubjectId(EducationalValueObject):
    """Identity of a subject within a student's educational state."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "SubjectId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class CompetencyId(EducationalValueObject):
    """Identity of a competency within a student's educational state."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "CompetencyId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class MissionId(EducationalValueObject):
    """Identity of a mission referenced by a student's educational state.

    Opaque cross-boundary reference — the aggregate does not own or
    interpret mission content.
    """

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "MissionId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class CheckpointId(EducationalValueObject):
    """Identity of a checkpoint referenced by a student's educational state.

    Opaque cross-boundary reference — the aggregate does not own or
    interpret checkpoint content.
    """

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "CheckpointId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class EducationalTimelineId(EducationalValueObject):
    """Identity of an educational timeline referenced by a student's state.

    Opaque cross-boundary reference — the aggregate does not own or
    interpret timeline content.
    """

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "EducationalTimelineId"),
        )

    def __str__(self) -> str:
        return self.value
