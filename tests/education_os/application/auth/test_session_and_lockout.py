"""Session timeout and account lockout tests (BR-001)."""

from __future__ import annotations

import pytest

from application.auth.errors import AuthenticationError
from application.auth.requests import (
    LoginRequest,
    RegisterRequest,
    SessionValidationRequest,
    VerifyEmailRequest,
)
from domain.auth.enums import AuthFailureReason
from tests.education_os.application.auth.conftest import STRONG_PASSWORD


def _verified_user(auth_service):
    registered = auth_service.register(
        RegisterRequest(email="ada@example.com", password=STRONG_PASSWORD, client_key="a")
    )
    auth_service.verify_email(
        VerifyEmailRequest(token=registered.issued_token or "", client_key="a")
    )
    return auth_service.login(
        LoginRequest(email="ada@example.com", password=STRONG_PASSWORD, client_key="a")
    )


def test_session_timeout_idle(auth_service, clock) -> None:
    login = _verified_user(auth_service)
    assert login.session is not None
    clock.advance(seconds=301)
    with pytest.raises(AuthenticationError) as exc:
        auth_service.validate_session(
            SessionValidationRequest(
                user_id=login.session.user_id,
                created_at_iso=login.session.created_at.isoformat(),
                last_activity_at_iso=login.session.last_activity_at.isoformat(),
                remember_me=False,
            )
        )
    assert exc.value.reason is AuthFailureReason.SESSION_EXPIRED


def test_session_valid_within_idle_window(auth_service, clock) -> None:
    login = _verified_user(auth_service)
    assert login.session is not None
    clock.advance(seconds=120)
    result = auth_service.validate_session(
        SessionValidationRequest(
            user_id=login.session.user_id,
            created_at_iso=login.session.created_at.isoformat(),
            last_activity_at_iso=login.session.last_activity_at.isoformat(),
            remember_me=False,
        )
    )
    assert result.success
    assert result.session is not None


def test_account_lockout_after_failed_attempts(auth_service) -> None:
    _verified_user(auth_service)
    for _ in range(3):
        with pytest.raises(AuthenticationError):
            auth_service.login(
                LoginRequest(
                    email="ada@example.com",
                    password="WrongPassword!1",
                    client_key="lock",
                )
            )
    with pytest.raises(AuthenticationError) as exc:
        auth_service.login(
            LoginRequest(
                email="ada@example.com",
                password=STRONG_PASSWORD,
                client_key="lock",
            )
        )
    assert exc.value.reason is AuthFailureReason.ACCOUNT_LOCKED


def test_rate_limiting(auth_service, rate_limiter) -> None:
    # Tighten limiter for this test.
    rate_limiter._max_attempts = 2
    auth_service.register(
        RegisterRequest(email="one@example.com", password=STRONG_PASSWORD, client_key="ip")
    )
    auth_service.register(
        RegisterRequest(email="two@example.com", password=STRONG_PASSWORD, client_key="ip")
    )
    with pytest.raises(AuthenticationError) as exc:
        auth_service.register(
            RegisterRequest(
                email="three@example.com",
                password=STRONG_PASSWORD,
                client_key="ip",
            )
        )
    assert exc.value.reason is AuthFailureReason.RATE_LIMITED
