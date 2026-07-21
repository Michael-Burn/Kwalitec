"""Password reset and email verification tests (BR-001)."""

from __future__ import annotations

import pytest

from application.auth.errors import AuthenticationError
from application.auth.requests import (
    ChangePasswordRequest,
    LoginRequest,
    RegisterRequest,
    RequestPasswordResetRequest,
    ResetPasswordRequest,
    VerifyEmailRequest,
)
from domain.auth.enums import AuthFailureReason
from tests.education_os.application.auth.conftest import STRONG_PASSWORD


def _register_and_verify(auth_service):
    registered = auth_service.register(
        RegisterRequest(email="ada@example.com", password=STRONG_PASSWORD, client_key="a")
    )
    auth_service.verify_email(
        VerifyEmailRequest(token=registered.issued_token or "", client_key="a")
    )
    return registered


def test_email_verification_activates_account(auth_service, users) -> None:
    registered = auth_service.register(
        RegisterRequest(email="ada@example.com", password=STRONG_PASSWORD, client_key="a")
    )
    result = auth_service.verify_email(
        VerifyEmailRequest(token=registered.issued_token or "", client_key="a")
    )
    assert result.success
    from domain.auth.email_address import EmailAddress

    account = users.get_by_email(EmailAddress("ada@example.com"))
    assert account is not None
    assert account.email_verified is True


def test_invalid_verification_token_rejected(auth_service) -> None:
    with pytest.raises(AuthenticationError) as exc:
        auth_service.verify_email(
            VerifyEmailRequest(token="not-a-real-token", client_key="a")
        )
    assert exc.value.reason is AuthFailureReason.INVALID_TOKEN


def test_password_reset_flow(auth_service) -> None:
    _register_and_verify(auth_service)
    reset_request = auth_service.request_password_reset(
        RequestPasswordResetRequest(email="ada@example.com", client_key="a")
    )
    assert reset_request.issued_token
    new_password = "NewCorrectHorse!2"
    auth_service.reset_password(
        ResetPasswordRequest(
            token=reset_request.issued_token,
            new_password=new_password,
            client_key="a",
        )
    )
    with pytest.raises(AuthenticationError):
        auth_service.login(
            LoginRequest(email="ada@example.com", password=STRONG_PASSWORD, client_key="a")
        )
    login = auth_service.login(
        LoginRequest(email="ada@example.com", password=new_password, client_key="a")
    )
    assert login.success


def test_password_reset_enumeration_safe(auth_service) -> None:
    result = auth_service.request_password_reset(
        RequestPasswordResetRequest(email="missing@example.com", client_key="a")
    )
    assert result.success
    assert result.issued_token is None


def test_change_password(auth_service) -> None:
    registered = _register_and_verify(auth_service)
    new_password = "ChangedHorse!3"
    result = auth_service.change_password(
        ChangePasswordRequest(
            user_id=registered.user_id or "",
            current_password=STRONG_PASSWORD,
            new_password=new_password,
            client_key="a",
        )
    )
    assert result.success
    login = auth_service.login(
        LoginRequest(email="ada@example.com", password=new_password, client_key="a")
    )
    assert login.success
