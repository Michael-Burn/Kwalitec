"""Unit tests for registration, login, logout (BR-001)."""

from __future__ import annotations

import pytest

from application.auth.errors import AuthenticationError
from application.auth.requests import LoginRequest, RegisterRequest
from domain.auth.enums import AuthFailureReason
from tests.education_os.application.auth.conftest import STRONG_PASSWORD


def test_register_creates_pending_account(auth_service, users, emails) -> None:
    result = auth_service.register(
        RegisterRequest(
            email="Ada@Example.com",
            password=STRONG_PASSWORD,
            client_key="test",
        )
    )
    assert result.success
    assert result.email == "ada@example.com"
    from domain.auth.email_address import EmailAddress

    account = users.get_by_email(EmailAddress("ada@example.com"))
    assert account is not None
    assert account.email_verified is False
    assert emails.messages
    assert result.issued_token


def test_login_requires_verified_email(auth_service) -> None:
    auth_service.register(
        RegisterRequest(email="ada@example.com", password=STRONG_PASSWORD, client_key="a")
    )
    with pytest.raises(AuthenticationError) as exc:
        auth_service.login(
            LoginRequest(email="ada@example.com", password=STRONG_PASSWORD, client_key="a")
        )
    assert exc.value.reason is AuthFailureReason.EMAIL_NOT_VERIFIED


def test_login_and_logout_after_verification(auth_service) -> None:
    registered = auth_service.register(
        RegisterRequest(email="ada@example.com", password=STRONG_PASSWORD, client_key="a")
    )
    from application.auth.requests import VerifyEmailRequest

    auth_service.verify_email(
        VerifyEmailRequest(token=registered.issued_token or "", client_key="a")
    )
    login = auth_service.login(
        LoginRequest(
            email="ada@example.com",
            password=STRONG_PASSWORD,
            remember_me=True,
            client_key="a",
        )
    )
    assert login.success
    assert login.session is not None
    assert login.session.remember_me is True
    logout = auth_service.logout(login.user_id)
    assert logout.success


def test_login_rejects_bad_password(auth_service) -> None:
    registered = auth_service.register(
        RegisterRequest(email="ada@example.com", password=STRONG_PASSWORD, client_key="a")
    )
    from application.auth.requests import VerifyEmailRequest

    auth_service.verify_email(
        VerifyEmailRequest(token=registered.issued_token or "", client_key="a")
    )
    with pytest.raises(AuthenticationError) as exc:
        auth_service.login(
            LoginRequest(
                email="ada@example.com",
                password="WrongPassword!1",
                client_key="a",
            )
        )
    assert exc.value.reason is AuthFailureReason.INVALID_CREDENTIALS


def test_duplicate_registration_rejected(auth_service) -> None:
    auth_service.register(
        RegisterRequest(email="ada@example.com", password=STRONG_PASSWORD, client_key="a")
    )
    with pytest.raises(AuthenticationError) as exc:
        auth_service.register(
            RegisterRequest(
                email="ada@example.com",
                password=STRONG_PASSWORD,
                client_key="a",
            )
        )
    assert exc.value.reason is AuthFailureReason.EMAIL_TAKEN
