"""Build a default OnboardingService for the Flask adapter layer."""

from __future__ import annotations

from application.onboarding.memory import (
    FixedClock,
    InMemoryOnboardingRepository,
    RecordingTwinInitializer,
    SequentialOnboardingIdGenerator,
    SystemClock,
)
from application.onboarding.onboarding_service import OnboardingService
from application.onboarding.ports import (
    Clock,
    OnboardingIdGenerator,
    OnboardingRepository,
    StudentTwinInitializer,
)


def build_onboarding_service(
    *,
    repository: OnboardingRepository | None = None,
    twin_initializer: StudentTwinInitializer | None = None,
    clock: Clock | None = None,
    id_generator: OnboardingIdGenerator | None = None,
) -> OnboardingService:
    """Assemble an ``OnboardingService`` with in-memory defaults."""
    return OnboardingService(
        repository=repository or InMemoryOnboardingRepository(),
        twin_initializer=twin_initializer or RecordingTwinInitializer(),
        clock=clock or SystemClock(),
        id_generator=id_generator or SequentialOnboardingIdGenerator(),
    )


__all__ = [
    "FixedClock",
    "InMemoryOnboardingRepository",
    "RecordingTwinInitializer",
    "SequentialOnboardingIdGenerator",
    "SystemClock",
    "build_onboarding_service",
]
