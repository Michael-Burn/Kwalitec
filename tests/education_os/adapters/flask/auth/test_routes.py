"""Flask auth adapter integration tests (BR-001)."""

from __future__ import annotations

import re
from datetime import UTC, datetime

import pytest
from flask import Flask

from adapters.flask.auth import (
    AuthAdapterDependencies,
    build_authentication_service,
    register_auth,
)
from application.auth.auth_service import AuthenticationService
from application.auth.memory import (
    InMemoryAuthTokenRepository,
    InMemoryRateLimiter,
    InMemoryUserAccountRepository,
    RecordingEmailSender,
    Sha256TokenHasher,
    StubPasswordHasher,
)
from application.auth.requests import RegisterRequest, VerifyEmailRequest
from application.auth.ports import Clock
from domain.auth.lockout_policy import LockoutPolicy
from domain.auth.password_policy import PasswordPolicy
from domain.auth.session_policy import SessionPolicy
from tests.education_os.application.auth.conftest import STRONG_PASSWORD


class FixedClock(Clock):
    def __init__(self) -> None:
        self._now = datetime(2026, 7, 20, 12, 0, tzinfo=UTC)

    def now(self) -> datetime:
        return self._now


@pytest.fixture
def auth_app():
    users = InMemoryUserAccountRepository()
    tokens = InMemoryAuthTokenRepository()
    emails = RecordingEmailSender()
    service = AuthenticationService(
        users=users,
        tokens=tokens,
        hasher=StubPasswordHasher(),
        token_hasher=Sha256TokenHasher(),
        email_sender=emails,
        rate_limiter=InMemoryRateLimiter(max_attempts=100),
        clock=FixedClock(),
        password_policy=PasswordPolicy(),
        lockout_policy=LockoutPolicy(max_failed_attempts=5),
        session_policy=SessionPolicy(),
        require_verified_email=True,
        expose_tokens=True,
    )
    app = Flask("eos_auth_test")
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "eos-auth-test-secret"
    register_auth(
        app,
        dependencies=AuthAdapterDependencies(auth_service=service),
        secure_cookies=True,
    )
    app.extensions["eos_auth_test_emails"] = emails
    app.extensions["eos_auth_test_service"] = service
    return app


@pytest.fixture
def client(auth_app):
    return auth_app.test_client()


def _csrf(html: str) -> str:
    match = re.search(r'name="csrf_token" value="([^"]+)"', html)
    assert match, html
    return match.group(1)


def test_register_login_logout_flow(client, auth_app) -> None:
    page = client.get("/eos/auth/register")
    assert page.status_code == 200
    csrf = _csrf(page.get_data(as_text=True))
    registered = client.post(
        "/eos/auth/register",
        data={
            "csrf_token": csrf,
            "email": "ada@example.com",
            "password": STRONG_PASSWORD,
        },
    )
    assert registered.status_code == 200
    assert b"registration successful" in registered.data

    emails = auth_app.extensions["eos_auth_test_emails"]
    token = emails.messages[-1][2].rsplit(" ", 1)[-1]

    verify_page = client.get("/eos/auth/verify-email")
    csrf = _csrf(verify_page.get_data(as_text=True))
    verified = client.post(
        "/eos/auth/verify-email",
        data={"csrf_token": csrf, "token": token},
    )
    assert verified.status_code == 200
    assert b"email verified" in verified.data

    login_page = client.get("/eos/auth/login")
    csrf = _csrf(login_page.get_data(as_text=True))
    logged_in = client.post(
        "/eos/auth/login",
        data={
            "csrf_token": csrf,
            "email": "ada@example.com",
            "password": STRONG_PASSWORD,
            "remember_me": "1",
        },
        follow_redirects=False,
    )
    assert logged_in.status_code == 302
    assert "/eos/dashboard/" in logged_in.headers["Location"]

    change = client.get("/eos/auth/change-password")
    csrf = _csrf(change.get_data(as_text=True))
    logged_out = client.post(
        "/eos/auth/logout",
        data={"csrf_token": csrf},
        follow_redirects=False,
    )
    assert logged_out.status_code == 302
    assert "/eos/auth/login" in logged_out.headers["Location"]


def test_csrf_rejection(client) -> None:
    response = client.post(
        "/eos/auth/login",
        data={
            "csrf_token": "forged",
            "email": "ada@example.com",
            "password": STRONG_PASSWORD,
        },
    )
    assert response.status_code == 400
    assert b"Invalid CSRF token" in response.data


def test_password_reset_http(client, auth_app) -> None:
    service = auth_app.extensions["eos_auth_test_service"]
    registered = service.register(
        RegisterRequest(email="ada@example.com", password=STRONG_PASSWORD, client_key="t")
    )
    service.verify_email(
        VerifyEmailRequest(token=registered.issued_token or "", client_key="t")
    )

    page = client.get("/eos/auth/forgot-password")
    csrf = _csrf(page.get_data(as_text=True))
    client.post(
        "/eos/auth/forgot-password",
        data={"csrf_token": csrf, "email": "ada@example.com"},
    )
    emails = auth_app.extensions["eos_auth_test_emails"]
    token = emails.messages[-1][2].rsplit(" ", 1)[-1]
    reset_page = client.get("/eos/auth/reset-password")
    csrf = _csrf(reset_page.get_data(as_text=True))
    new_password = "BrandNewHorse!9"
    reset = client.post(
        "/eos/auth/reset-password",
        data={
            "csrf_token": csrf,
            "token": token,
            "new_password": new_password,
        },
    )
    assert reset.status_code == 200
    assert b"password reset successful" in reset.data

    login_page = client.get("/eos/auth/login")
    csrf = _csrf(login_page.get_data(as_text=True))
    logged_in = client.post(
        "/eos/auth/login",
        data={
            "csrf_token": csrf,
            "email": "ada@example.com",
            "password": new_password,
        },
        follow_redirects=False,
    )
    assert logged_in.status_code == 302


def test_secure_cookies_applied_in_testing(auth_app) -> None:
    assert auth_app.config["SESSION_COOKIE_HTTPONLY"] is True
    assert auth_app.config["SESSION_COOKIE_SAMESITE"] == "Lax"
    assert auth_app.config["SESSION_COOKIE_SECURE"] is False


def test_factory_builds_service() -> None:
    service = build_authentication_service(
        users=InMemoryUserAccountRepository(),
        tokens=InMemoryAuthTokenRepository(),
        use_argon2=False,
        expose_tokens=True,
    )
    assert service is not None
