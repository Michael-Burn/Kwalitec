"""Shared fixtures for onboarding application tests (BR-002)."""

from __future__ import annotations

import pytest

from application.onboarding.memory import (
    FixedClock,
    InMemoryOnboardingRepository,
    RecordingTwinInitializer,
    SequentialOnboardingIdGenerator,
)
from application.onboarding.onboarding_service import OnboardingService


@pytest.fixture
def repository() -> InMemoryOnboardingRepository:
    return InMemoryOnboardingRepository()


@pytest.fixture
def twin_initializer() -> RecordingTwinInitializer:
    return RecordingTwinInitializer()


@pytest.fixture
def clock() -> FixedClock:
    return FixedClock()


@pytest.fixture
def onboarding_service(
    repository: InMemoryOnboardingRepository,
    twin_initializer: RecordingTwinInitializer,
    clock: FixedClock,
) -> OnboardingService:
    return OnboardingService(
        repository=repository,
        twin_initializer=twin_initializer,
        clock=clock,
        id_generator=SequentialOnboardingIdGenerator(),
    )


def full_payloads() -> dict[str, dict]:
    """Valid payloads for every collection step."""
    return {
        "welcome": {"acknowledged": True},
        "ifoa_profile": {
            "pathway": "core_principles",
            "exam_paper": "CS1",
            "intended_sitting_label": "April 2027",
        },
        "exam_history": {
            "prior_study": "first_time",
            "core_reading": "none",
            "previous_attempts": 0,
            "sitting_intent": "first_sit",
        },
        "weekly_availability": {
            "weekday_minutes": 90,
            "weekend_minutes": 120,
            "preferred_session_minutes": 60,
        },
        "confidence": {"band": "moderate", "notes": ""},
        "study_habits": {
            "preference": "mixed",
            "typical_start_time": "19:00",
        },
        "optional_diagnostic": {"choice": "skipped"},
        "review": {"confirmed": True},
    }
