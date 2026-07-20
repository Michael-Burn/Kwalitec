"""Student Experience identity value objects."""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
)


@dataclass(frozen=True, slots=True)
class StudentExperienceId(EducationalValueObject):
    """Identity of a generated StudentExperience projection."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "StudentExperienceId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class AchievementId(EducationalValueObject):
    """Identity of a presentation Achievement within a StudentExperience."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "AchievementId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class CelebrationId(EducationalValueObject):
    """Identity of a presentation Celebration within a StudentExperience."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "CelebrationId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class ReminderId(EducationalValueObject):
    """Identity of a presentation Reminder within a StudentExperience."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "ReminderId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class MotivationId(EducationalValueObject):
    """Identity of a presentation Motivation message."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "MotivationId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class SessionSummaryId(EducationalValueObject):
    """Identity of a presentation SessionSummary."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "SessionSummaryId"),
        )

    def __str__(self) -> str:
        return self.value
