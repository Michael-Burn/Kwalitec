"""In-memory collaborators for onboarding tests and local wiring."""

from __future__ import annotations

from datetime import UTC, datetime
from itertools import count

from application.onboarding.ports import (
    Clock,
    OnboardingIdGenerator,
    OnboardingRepository,
    StudentTwinInitializer,
)
from application.onboarding.results import StudentTwinInitializationRequest
from domain.onboarding.enums import OnboardingStatus
from domain.onboarding.ids import OnboardingId, StudentId
from domain.onboarding.onboarding_session import OnboardingSession


class SystemClock(Clock):
    """Wall-clock UTC timestamps."""

    def now(self) -> datetime:
        return datetime.now(UTC)


class FixedClock(Clock):
    """Deterministic clock for tests."""

    def __init__(self, instant: datetime | None = None) -> None:
        self._instant = instant or datetime(2026, 7, 20, 12, 0, tzinfo=UTC)

    def now(self) -> datetime:
        return self._instant

    def set(self, instant: datetime) -> None:
        self._instant = instant


class SequentialOnboardingIdGenerator(OnboardingIdGenerator):
    """Allocate sequential onboarding ids."""

    def __init__(self, prefix: str = "ob") -> None:
        self._prefix = prefix
        self._counter = count(1)

    def next_identity(self) -> OnboardingId:
        return OnboardingId(f"{self._prefix}-{next(self._counter)}")


class InMemoryOnboardingRepository(OnboardingRepository):
    """Dict-backed onboarding session store."""

    def __init__(self) -> None:
        self._by_id: dict[str, OnboardingSession] = {}

    def get(self, onboarding_id: OnboardingId) -> OnboardingSession | None:
        return self._by_id.get(str(onboarding_id))

    def get_in_progress_for_student(
        self, student_id: StudentId
    ) -> OnboardingSession | None:
        matches = [
            session
            for session in self._by_id.values()
            if str(session.student_id) == str(student_id)
            and session.status is OnboardingStatus.IN_PROGRESS
        ]
        if not matches:
            return None
        return max(matches, key=lambda s: s.updated_at)

    def save(self, session: OnboardingSession) -> None:
        self._by_id[str(session.onboarding_id)] = session


class RecordingTwinInitializer(StudentTwinInitializer):
    """Records initialization requests and returns synthetic twin ids."""

    def __init__(self) -> None:
        self.requests: list[StudentTwinInitializationRequest] = []
        self._counter = count(1)

    def initialize(self, request: object) -> str:
        if not isinstance(request, StudentTwinInitializationRequest):
            raise TypeError("expected StudentTwinInitializationRequest")
        self.requests.append(request)
        return f"twin-{next(self._counter)}"
