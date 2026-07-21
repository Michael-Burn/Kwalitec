"""Onboarding domain — first-run educational evidence collection.

Pure domain rules for step navigation, validation, autosave, and resume.

Allowed: value objects, policies, aggregates, invariants.

Forbidden: Flask, SQLAlchemy, AI, HTTP, recommendations, mission planning,
educational diagnosis, Student Twin mutation logic.
"""

from __future__ import annotations

from domain.onboarding.enums import (
    COLLECTION_STEPS,
    STEP_LABELS,
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
from domain.onboarding.errors import (
    OnboardingDomainError,
    OnboardingInvariantViolation,
    OnboardingValidationError,
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
from domain.onboarding.step_policy import StepNavigationPolicy

__all__ = [
    "COLLECTION_STEPS",
    "STEP_LABELS",
    "ConfidenceBand",
    "ConfidencePayload",
    "CoreReadingDeclaration",
    "DiagnosticChoice",
    "ExamHistoryPayload",
    "ExamSittingIntent",
    "IfoaPathway",
    "IfoaProfilePayload",
    "OnboardingDomainError",
    "OnboardingId",
    "OnboardingInvariantViolation",
    "OnboardingSession",
    "OnboardingStatus",
    "OnboardingStep",
    "OnboardingValidationError",
    "OptionalDiagnosticPayload",
    "PriorStudyPosture",
    "ReviewPayload",
    "StepNavigationPolicy",
    "StepPayload",
    "StudentId",
    "StudyHabitPreference",
    "StudyHabitsPayload",
    "WeeklyAvailabilityPayload",
    "WelcomePayload",
]
