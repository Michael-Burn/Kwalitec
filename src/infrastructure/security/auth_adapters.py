"""Production authentication support adapters (non-persistence).

Email delivery, rate limiting, and token hashing for the composition root.
Not recording doubles and not repository stores.
"""

from __future__ import annotations

import hashlib
import hmac
import logging
from collections import defaultdict
from datetime import datetime, timedelta

from application.auth.ports import EmailSender, RateLimiter, TokenHasher
from application.auth.security import constant_time_equals, hash_opaque_token
from domain.auth.email_address import EmailAddress

logger = logging.getLogger(__name__)


class Sha256TokenHasher(TokenHasher):
    """SHA-256 token hasher with constant-time verify."""

    def hash_token(self, raw_token: str) -> str:
        return hash_opaque_token(raw_token)

    def tokens_match(self, raw_token: str, token_hash: str) -> bool:
        return constant_time_equals(self.hash_token(raw_token), token_hash)


class LoggingEmailSender(EmailSender):
    """Deliver auth emails by structured logging (SMTP wired in a later milestone)."""

    def send(self, *, to: EmailAddress, subject: str, body: str) -> None:
        logger.info(
            "auth_email_dispatch",
            extra={
                "email_to": to.value,
                "email_subject": subject,
                "email_body_length": len(body or ""),
            },
        )


class ProcessRateLimiter(RateLimiter):
    """Process-local sliding-window rate limiter for authentication endpoints."""

    def __init__(
        self,
        *,
        max_attempts: int = 20,
        window_seconds: int = 60,
    ) -> None:
        self._max_attempts = max_attempts
        self._window = timedelta(seconds=window_seconds)
        self._events: dict[str, list[datetime]] = defaultdict(list)

    def is_limited(self, key: str, *, now: datetime) -> bool:
        self._prune(key, now)
        return len(self._events[key]) >= self._max_attempts

    def record(self, key: str, *, now: datetime) -> None:
        self._prune(key, now)
        self._events[key].append(now)

    def _prune(self, key: str, now: datetime) -> None:
        cutoff = now - self._window
        self._events[key] = [ts for ts in self._events[key] if ts >= cutoff]


class HmacStubPasswordHasher:
    """Deterministic hasher only for environments without Argon2 installed.

    Production composition prefers Argon2PasswordHasher and falls back here
    solely when the argon2 package is unavailable.
    """

    def __init__(self, pepper: str = "eos-auth-fallback-pepper") -> None:
        self._pepper = pepper.encode("utf-8")

    def hash(self, password: str) -> str:
        digest = hmac.new(
            self._pepper,
            (password or "").encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return f"stub${digest}"

    def verify(self, password: str, password_hash: str) -> bool:
        expected = self.hash(password)
        return constant_time_equals(expected, password_hash or "")
