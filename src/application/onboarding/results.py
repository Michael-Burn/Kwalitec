"""Frozen result DTOs for onboarding use-cases.

``CompletedOnboarding`` and ``StudentTwinInitializationRequest`` are the
canonical BR-002 outputs. They carry declarations only — never recommendations
or mission plans.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from domain.onboarding.enums import OnboardingStatus, OnboardingStep
from domain.onboarding.onboarding_session import OnboardingSession


@dataclass(frozen=True, slots=True)
class StudentTwinInitializationRequest:
    """Closed cargo for Student Twin birth after onboarding completes.

    Application validates structure and hands this to ``StudentTwinInitializer``.
    Contains self-declared educational evidence only — no mastery, readiness,
    or recommendation fields.
    """

    student_id: str
    onboarding_id: str
    pathway: str
    exam_paper: str
    intended_sitting_label: str
    prior_study: str
    core_reading: str
    previous_attempts: int
    sitting_intent: str
    weekday_minutes: int
    weekend_minutes: int
    preferred_session_minutes: int
    confidence_band: str
    confidence_notes: str
    study_habit_preference: str
    typical_start_time: str
    diagnostic_choice: str
    contract_version: str = "1.0"
    declaration_confirmation: bool = True


@dataclass(frozen=True, slots=True)
class CompletedOnboarding:
    """Sealed onboarding outcome ready for Twin initialization and redirect."""

    onboarding_id: str
    student_id: str
    completed_at: datetime
    twin_initialization: StudentTwinInitializationRequest
    twin_id: str | None = None
    redirect_path: str = "/eos/dashboard/"


@dataclass(frozen=True, slots=True)
class OnboardingSnapshot:
    """Framework-free snapshot of an in-progress or completed session."""

    onboarding_id: str
    student_id: str
    status: OnboardingStatus
    current_step: OnboardingStep
    progress_percent: float
    payloads: dict[str, dict[str, Any]]
    saved_steps: tuple[str, ...]
    updated_at: datetime
    completed_at: datetime | None = None

    @classmethod
    def from_session(cls, session: OnboardingSession) -> OnboardingSnapshot:
        payloads: dict[str, dict[str, Any]] = {}
        for step, payload in session.payloads.items():
            payloads[step.value] = _payload_to_dict(payload)
        return cls(
            onboarding_id=str(session.onboarding_id),
            student_id=str(session.student_id),
            status=session.status,
            current_step=session.current_step,
            progress_percent=session.progress_percent(),
            payloads=payloads,
            saved_steps=tuple(sorted(step.value for step in session.saved_steps)),
            updated_at=session.updated_at,
            completed_at=session.completed_at,
        )


@dataclass(frozen=True, slots=True)
class OnboardingResult:
    """Outcome of an onboarding use-case."""

    success: bool
    message: str = ""
    snapshot: OnboardingSnapshot | None = None
    completed: CompletedOnboarding | None = None


def _payload_to_dict(payload: object) -> dict[str, Any]:
    from dataclasses import asdict, is_dataclass

    if is_dataclass(payload) and not isinstance(payload, type):
        raw = asdict(payload)
        return {
            key: (value.value if hasattr(value, "value") else value)
            for key, value in raw.items()
        }
    return {}
