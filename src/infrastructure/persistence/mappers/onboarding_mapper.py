"""Structural mapping for OnboardingSession drafts (BR-004).

Serialises step payloads as JSON-friendly dicts. No educational inference.
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any

from domain.onboarding.enums import (
    ConfidenceBand,
    CoreReadingDeclaration,
    DiagnosticChoice,
    ExamSittingIntent,
    IfoaPathway,
    OnboardingStatus,
    OnboardingStep,
    PriorStudyPosture,
    StudyHabitPreference,
)
from domain.onboarding.ids import OnboardingId, StudentId
from domain.onboarding.onboarding_session import OnboardingSession
from domain.onboarding.step_payloads import (
    ConfidencePayload,
    ExamHistoryPayload,
    IfoaProfilePayload,
    OptionalDiagnosticPayload,
    ReviewPayload,
    StepPayload,
    StudyHabitsPayload,
    WeeklyAvailabilityPayload,
    WelcomePayload,
)
from infrastructure.persistence.dto.onboarding import OnboardingSessionDTO

_PAYLOAD_TYPES: dict[OnboardingStep, type[StepPayload]] = {
    OnboardingStep.WELCOME: WelcomePayload,
    OnboardingStep.IFOA_PROFILE: IfoaProfilePayload,
    OnboardingStep.EXAM_HISTORY: ExamHistoryPayload,
    OnboardingStep.WEEKLY_AVAILABILITY: WeeklyAvailabilityPayload,
    OnboardingStep.CONFIDENCE: ConfidencePayload,
    OnboardingStep.STUDY_HABITS: StudyHabitsPayload,
    OnboardingStep.OPTIONAL_DIAGNOSTIC: OptionalDiagnosticPayload,
    OnboardingStep.REVIEW: ReviewPayload,
}

_ENUM_FIELDS: dict[str, type[Enum]] = {
    "pathway": IfoaPathway,
    "prior_study": PriorStudyPosture,
    "core_reading": CoreReadingDeclaration,
    "sitting_intent": ExamSittingIntent,
    "band": ConfidenceBand,
    "preference": StudyHabitPreference,
    "choice": DiagnosticChoice,
}


class OnboardingSessionMapper:
    """Map OnboardingSession ↔ OnboardingSessionDTO."""

    @staticmethod
    def to_persistence(
        session: OnboardingSession, *, row_version: int = 1
    ) -> OnboardingSessionDTO:
        return OnboardingSessionDTO(
            onboarding_id=str(session.onboarding_id),
            student_id=str(session.student_id),
            status=session.status.value,
            current_step=session.current_step.value,
            payloads={
                step.value: _payload_to_dict(payload)
                for step, payload in session.payloads.items()
            },
            saved_steps=sorted(step.value for step in session.saved_steps),
            created_at=session.created_at,
            updated_at=session.updated_at,
            completed_at=session.completed_at,
            row_version=row_version,
        )

    @staticmethod
    def to_domain(dto: OnboardingSessionDTO) -> OnboardingSession:
        payloads: dict[OnboardingStep, StepPayload] = {}
        for key, raw in (dto.payloads or {}).items():
            step = OnboardingStep(str(key))
            payloads[step] = _payload_from_dict(step, dict(raw or {}))
        return OnboardingSession(
            onboarding_id=OnboardingId(dto.onboarding_id),
            student_id=StudentId(dto.student_id),
            status=OnboardingStatus(dto.status),
            current_step=OnboardingStep(dto.current_step),
            payloads=payloads,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            completed_at=dto.completed_at,
            saved_steps=frozenset(
                OnboardingStep(str(value)) for value in (dto.saved_steps or [])
            ),
        )


def _payload_to_dict(payload: StepPayload) -> dict[str, Any]:
    if not is_dataclass(payload):
        raise TypeError(f"expected dataclass payload, got {type(payload)!r}")
    raw = asdict(payload)
    return {
        key: (value.value if isinstance(value, Enum) else value)
        for key, value in raw.items()
    }


def _payload_from_dict(step: OnboardingStep, raw: dict[str, Any]) -> StepPayload:
    payload_cls = _PAYLOAD_TYPES[step]
    kwargs: dict[str, Any] = {}
    for field_name, value in raw.items():
        enum_cls = _ENUM_FIELDS.get(field_name)
        if enum_cls is not None and value is not None and not isinstance(value, enum_cls):
            kwargs[field_name] = enum_cls(str(value))
        else:
            kwargs[field_name] = value
    return payload_cls(**kwargs)  # type: ignore[call-arg]
