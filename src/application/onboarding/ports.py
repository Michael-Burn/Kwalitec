"""Outbound ports for onboarding use-cases.

Persistence and Twin birth are injected. Application never imports Flask,
SQLAlchemy, or AI SDKs.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

from domain.onboarding.ids import OnboardingId, StudentId
from domain.onboarding.onboarding_session import OnboardingSession

if TYPE_CHECKING:
    from application.onboarding.results import StudentTwinInitializationRequest


class Clock(ABC):
    """Injectable time source for onboarding timestamps."""

    @abstractmethod
    def now(self) -> datetime:
        """Return a timezone-aware UTC timestamp."""


class OnboardingIdGenerator(ABC):
    """Allocate onboarding session identities."""

    @abstractmethod
    def next_identity(self) -> OnboardingId:
        """Return a new onboarding id."""


class OnboardingRepository(ABC):
    """Persistence port for onboarding sessions."""

    @abstractmethod
    def get(self, onboarding_id: OnboardingId) -> OnboardingSession | None:
        """Load a session by id."""

    @abstractmethod
    def get_in_progress_for_student(
        self, student_id: StudentId
    ) -> OnboardingSession | None:
        """Load the incomplete session for a student, if any."""

    @abstractmethod
    def save(self, session: OnboardingSession) -> None:
        """Insert or update a session."""


class StudentTwinInitializer(ABC):
    """Port that births a Student Twin from a sealed initialization request.

    Implementations must not diagnose or recommend. They only initialise Twin
    identity/priors from the closed request cargo.
    """

    @abstractmethod
    def initialize(self, request: StudentTwinInitializationRequest) -> str:
        """Accept a StudentTwinInitializationRequest; return twin id."""
