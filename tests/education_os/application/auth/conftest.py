"""Shared fixtures for authentication application tests (BR-001)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from application.auth.auth_service import AuthenticationService
from application.auth.memory import (
    InMemoryAuthTokenRepository,
    InMemoryRateLimiter,
    InMemoryUserAccountRepository,
    RecordingEmailSender,
    Sha256TokenHasher,
    StubPasswordHasher,
)
from application.auth.ports import Clock
from domain.auth.lockout_policy import LockoutPolicy
from domain.auth.password_policy import PasswordPolicy
from domain.auth.session_policy import SessionPolicy


class FixedClock(Clock):
    """Deterministic clock for authentication tests."""

    def __init__(self, instant: datetime | None = None) -> None:
        self._now = instant or datetime(2026, 7, 20, 12, 0, tzinfo=UTC)

    def now(self) -> datetime:
        return self._now

    def advance(self, **kwargs: float) -> datetime:
        self._now = self._now + timedelta(**kwargs)
        return self._now


@pytest.fixture
def clock() -> FixedClock:
    return FixedClock()


@pytest.fixture
def users() -> InMemoryUserAccountRepository:
    return InMemoryUserAccountRepository()


@pytest.fixture
def tokens() -> InMemoryAuthTokenRepository:
    return InMemoryAuthTokenRepository()


@pytest.fixture
def emails() -> RecordingEmailSender:
    return RecordingEmailSender()


@pytest.fixture
def rate_limiter() -> InMemoryRateLimiter:
    return InMemoryRateLimiter(max_attempts=100, window_seconds=60)


@pytest.fixture
def auth_service(
    users,
    tokens,
    emails,
    rate_limiter,
    clock,
) -> AuthenticationService:
    return AuthenticationService(
        users=users,
        tokens=tokens,
        hasher=StubPasswordHasher(),
        token_hasher=Sha256TokenHasher(),
        email_sender=emails,
        rate_limiter=rate_limiter,
        clock=clock,
        password_policy=PasswordPolicy(min_length=12),
        lockout_policy=LockoutPolicy(
            max_failed_attempts=3,
            lockout_duration_seconds=600,
        ),
        session_policy=SessionPolicy(
            absolute_timeout_seconds=3_600,
            idle_timeout_seconds=300,
            remember_me_seconds=86_400,
        ),
        require_verified_email=True,
        expose_tokens=True,
    )


STRONG_PASSWORD = "CorrectHorse!1"
