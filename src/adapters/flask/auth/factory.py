"""Build a default AuthenticationService for the Flask adapter layer."""

from __future__ import annotations

from datetime import UTC, datetime

from application.auth.auth_service import AuthenticationService
from application.auth.memory import (
    InMemoryAuthTokenRepository,
    InMemoryRateLimiter,
    InMemoryUserAccountRepository,
    RecordingEmailSender,
    Sha256TokenHasher,
    StubPasswordHasher,
)
from application.auth.ports import (
    AuthTokenRepository,
    Clock,
    EmailSender,
    PasswordHasher,
    RateLimiter,
    TokenHasher,
    UserAccountRepository,
)


class UtcClock(Clock):
    """Wall-clock UTC source for authentication timestamps."""

    def now(self) -> datetime:
        return datetime.now(UTC)


def build_authentication_service(
    *,
    users: UserAccountRepository | None = None,
    tokens: AuthTokenRepository | None = None,
    hasher: PasswordHasher | None = None,
    token_hasher: TokenHasher | None = None,
    email_sender: EmailSender | None = None,
    rate_limiter: RateLimiter | None = None,
    clock: Clock | None = None,
    require_verified_email: bool = True,
    expose_tokens: bool = False,
    use_argon2: bool = True,
) -> AuthenticationService:
    """Assemble an ``AuthenticationService`` with sensible defaults.

    When ``use_argon2`` is True, prefers the infrastructure Argon2 hasher and
    falls back to the stub hasher only if Argon2 is unavailable.
    """
    resolved_hasher = hasher
    if resolved_hasher is None:
        if use_argon2:
            try:
                from infrastructure.security import Argon2PasswordHasher

                resolved_hasher = Argon2PasswordHasher()
            except ImportError:
                resolved_hasher = StubPasswordHasher()
        else:
            resolved_hasher = StubPasswordHasher()

    return AuthenticationService(
        users=users or InMemoryUserAccountRepository(),
        tokens=tokens or InMemoryAuthTokenRepository(),
        hasher=resolved_hasher,
        token_hasher=token_hasher or Sha256TokenHasher(),
        email_sender=email_sender or RecordingEmailSender(),
        rate_limiter=rate_limiter or InMemoryRateLimiter(),
        clock=clock or UtcClock(),
        require_verified_email=require_verified_email,
        expose_tokens=expose_tokens,
    )
