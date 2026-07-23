"""Build an OnboardingService for the Flask adapter layer.

Production composition injects SQLAlchemy repositories and the Student Twin
initializer via ``SqlAlchemyProductUnitOfWork``. This factory never constructs
in-memory repositories or recording doubles — callers must supply those ports.
"""

from __future__ import annotations

from uuid import uuid4

from application.onboarding.memory import SystemClock
from application.onboarding.onboarding_service import OnboardingService
from application.onboarding.ports import (
    Clock,
    OnboardingIdGenerator,
    OnboardingRepository,
    StudentTwinInitializer,
)
from domain.onboarding.ids import OnboardingId


class UuidOnboardingIdGenerator(OnboardingIdGenerator):
    """Allocate opaque onboarding identities for adapter-assembled services."""

    def next_identity(self) -> OnboardingId:
        return OnboardingId(f"ob-{uuid4().hex}")


def build_onboarding_service(
    *,
    repository: OnboardingRepository,
    twin_initializer: StudentTwinInitializer,
    clock: Clock | None = None,
    id_generator: OnboardingIdGenerator | None = None,
) -> OnboardingService:
    """Assemble an ``OnboardingService`` from injected adapters.

    Persistence and twin-initialization ports are required. No in-memory or
    recording defaults are installed here.
    """
    return OnboardingService(
        repository=repository,
        twin_initializer=twin_initializer,
        clock=clock or SystemClock(),
        id_generator=id_generator or UuidOnboardingIdGenerator(),
    )


__all__ = [
    "UuidOnboardingIdGenerator",
    "build_onboarding_service",
]
