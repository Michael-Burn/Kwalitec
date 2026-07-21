"""Typed onboarding identities."""

from __future__ import annotations

from dataclasses import dataclass

from domain.onboarding.errors import OnboardingInvariantViolation


@dataclass(frozen=True, slots=True)
class OnboardingId:
    """Stable identity for one onboarding session."""

    value: str

    def __post_init__(self) -> None:
        cleaned = (self.value or "").strip()
        if not cleaned:
            raise OnboardingInvariantViolation(
                "onboarding id is required",
                invariant="onboarding_id_non_empty",
            )
        object.__setattr__(self, "value", cleaned)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class StudentId:
    """Authenticated student identity owning the onboarding session."""

    value: str

    def __post_init__(self) -> None:
        cleaned = (self.value or "").strip()
        if not cleaned:
            raise OnboardingInvariantViolation(
                "student id is required",
                invariant="student_id_non_empty",
            )
        object.__setattr__(self, "value", cleaned)

    def __str__(self) -> str:
        return self.value
