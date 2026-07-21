"""Onboarding application services — first-run Student Twin initialization path.

Framework-independent use-cases for step navigation, autosave, resume,
validation, and emitting ``CompletedOnboarding`` /
``StudentTwinInitializationRequest``.

Forbidden: educational recommendations, mission planning, AI, Flask,
SQLAlchemy, educational diagnosis.
"""

from __future__ import annotations

from application.onboarding.errors import OnboardingApplicationError
from application.onboarding.memory import (
    FixedClock,
    InMemoryOnboardingRepository,
    RecordingTwinInitializer,
    SequentialOnboardingIdGenerator,
    SystemClock,
)
from application.onboarding.onboarding_service import (
    DASHBOARD_REDIRECT_PATH,
    OnboardingService,
)
from application.onboarding.payload_mapper import build_payload, parse_step
from application.onboarding.ports import (
    Clock,
    OnboardingIdGenerator,
    OnboardingRepository,
    StudentTwinInitializer,
)
from application.onboarding.requests import (
    AdvanceStepRequest,
    CompleteOnboardingRequest,
    GoBackRequest,
    ResumeOnboardingRequest,
    SaveStepRequest,
    SkipOptionalRequest,
    StartOnboardingRequest,
)
from application.onboarding.results import (
    CompletedOnboarding,
    OnboardingResult,
    OnboardingSnapshot,
    StudentTwinInitializationRequest,
)

__all__ = [
    "AdvanceStepRequest",
    "Clock",
    "CompleteOnboardingRequest",
    "CompletedOnboarding",
    "DASHBOARD_REDIRECT_PATH",
    "FixedClock",
    "GoBackRequest",
    "InMemoryOnboardingRepository",
    "OnboardingApplicationError",
    "OnboardingIdGenerator",
    "OnboardingRepository",
    "OnboardingResult",
    "OnboardingService",
    "OnboardingSnapshot",
    "RecordingTwinInitializer",
    "ResumeOnboardingRequest",
    "SaveStepRequest",
    "SequentialOnboardingIdGenerator",
    "SkipOptionalRequest",
    "StartOnboardingRequest",
    "StudentTwinInitializationRequest",
    "StudentTwinInitializer",
    "SystemClock",
    "build_payload",
    "parse_step",
]
