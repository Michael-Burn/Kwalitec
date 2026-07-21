"""Controller unit tests for authentication adapter (BR-001)."""

from __future__ import annotations

from datetime import UTC, datetime

from adapters.flask.auth.controller import AuthController
from adapters.flask.auth.dependency_provider import AuthAdapterDependencies
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
from tests.education_os.application.auth.conftest import STRONG_PASSWORD


class _Clock(Clock):
    def now(self) -> datetime:
        return datetime(2026, 7, 20, 12, 0, tzinfo=UTC)


def test_controller_register_and_login() -> None:
    service = AuthenticationService(
        users=InMemoryUserAccountRepository(),
        tokens=InMemoryAuthTokenRepository(),
        hasher=StubPasswordHasher(),
        token_hasher=Sha256TokenHasher(),
        email_sender=RecordingEmailSender(),
        rate_limiter=InMemoryRateLimiter(max_attempts=100),
        clock=_Clock(),
        password_policy=PasswordPolicy(),
        lockout_policy=LockoutPolicy(),
        session_policy=SessionPolicy(),
        require_verified_email=True,
        expose_tokens=True,
    )
    controller = AuthController(AuthAdapterDependencies(auth_service=service))
    registered = controller.register(
        email="ada@example.com",
        password=STRONG_PASSWORD,
        client_key="c",
    )
    assert registered.success
    controller.verify_email(token=registered.issued_token or "", client_key="c")
    login = controller.login(
        email="ada@example.com",
        password=STRONG_PASSWORD,
        remember_me=True,
        client_key="c",
    )
    assert login.session is not None
    logout = controller.logout(login.user_id)
    assert logout.success
