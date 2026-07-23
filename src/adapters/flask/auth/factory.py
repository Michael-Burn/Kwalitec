"""Build an AuthenticationService for the Flask adapter layer.

Production composition injects SQLAlchemy repositories via
``SqlAlchemyProductUnitOfWork``. This factory never constructs in-memory
repositories or recording doubles — callers must supply persistence ports.
"""

from __future__ import annotations

from datetime import UTC, datetime

from application.auth.auth_service import AuthenticationService
from application.auth.ports import (
    AuthTokenRepository,
    Clock,
    EmailSender,
    PasswordHasher,
    RateLimiter,
    TokenHasher,
    UserAccountRepository,
)
from infrastructure.security.auth_adapters import (
    HmacStubPasswordHasher,
    LoggingEmailSender,
    ProcessRateLimiter,
    Sha256TokenHasher,
)


class UtcClock(Clock):
    """Wall-clock UTC source for authentication timestamps."""

    def now(self) -> datetime:
        return datetime.now(UTC)


def build_authentication_service(
    *,
    users: UserAccountRepository,
    tokens: AuthTokenRepository,
    hasher: PasswordHasher | None = None,
    token_hasher: TokenHasher | None = None,
    email_sender: EmailSender | None = None,
    rate_limiter: RateLimiter | None = None,
    clock: Clock | None = None,
    require_verified_email: bool = True,
    expose_tokens: bool = False,
    use_argon2: bool = True,
) -> AuthenticationService:
    """Assemble an ``AuthenticationService`` from injected adapters.

    Persistence ports (``users``, ``tokens``) are required. Defaults for
    non-persistence collaborators are production infrastructure adapters,
    never recording or in-memory doubles.
    """
    resolved_hasher = hasher
    if resolved_hasher is None:
        if use_argon2:
            try:
                from infrastructure.security.argon2_password_hasher import (
                    Argon2PasswordHasher,
                )

                resolved_hasher = Argon2PasswordHasher()
            except Exception:  # pragma: no cover - optional dependency guard
                resolved_hasher = HmacStubPasswordHasher()  # type: ignore[assignment]
        else:
            resolved_hasher = HmacStubPasswordHasher()  # type: ignore[assignment]

    return AuthenticationService(
        users=users,
        tokens=tokens,
        hasher=resolved_hasher,
        token_hasher=token_hasher or Sha256TokenHasher(),
        email_sender=email_sender or LoggingEmailSender(),
        rate_limiter=rate_limiter or ProcessRateLimiter(),
        clock=clock or UtcClock(),
        require_verified_email=require_verified_email,
        expose_tokens=expose_tokens,
    )
