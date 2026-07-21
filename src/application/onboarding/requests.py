"""Frozen request DTOs for onboarding use-cases."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class StartOnboardingRequest:
    """Begin first-run onboarding for an authenticated student."""

    student_id: str


@dataclass(frozen=True, slots=True)
class ResumeOnboardingRequest:
    """Resume an incomplete onboarding session for a student."""

    student_id: str


@dataclass(frozen=True, slots=True)
class SaveStepRequest:
    """Autosave a step payload without advancing."""

    onboarding_id: str
    student_id: str
    step: str
    payload: dict[str, Any]


@dataclass(frozen=True, slots=True)
class AdvanceStepRequest:
    """Validate the current step and advance to the next."""

    onboarding_id: str
    student_id: str


@dataclass(frozen=True, slots=True)
class GoBackRequest:
    """Move to the previous collection step."""

    onboarding_id: str
    student_id: str


@dataclass(frozen=True, slots=True)
class SkipOptionalRequest:
    """Skip the optional diagnostic with an explicit skip declaration."""

    onboarding_id: str
    student_id: str


@dataclass(frozen=True, slots=True)
class CompleteOnboardingRequest:
    """Confirm Review and emit Twin initialization request."""

    onboarding_id: str
    student_id: str
