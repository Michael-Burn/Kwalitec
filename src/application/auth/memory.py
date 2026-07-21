"""In-memory authentication adapters for tests and default EOS wiring.

Not production persistence. Implements application ports without Flask or SQL.
"""

from __future__ import annotations

import hashlib
import hmac
from collections import defaultdict
from datetime import datetime, timedelta
from uuid import uuid4

from application.auth.ports import (
    AuthTokenRepository,
    EmailSender,
    PasswordHasher,
    RateLimiter,
    TokenHasher,
    UserAccountRepository,
)
from application.auth.security import (
    constant_time_equals,
    generate_opaque_token,
    hash_opaque_token,
)
from domain.auth.auth_token import AuthToken
from domain.auth.email_address import EmailAddress
from domain.auth.enums import AuthTokenPurpose
from domain.auth.ids import UserId
from domain.auth.user_account import UserAccount


class Sha256TokenHasher(TokenHasher):
    """SHA-256 token hasher with constant-time verify."""

    def hash_token(self, raw_token: str) -> str:
        return hash_opaque_token(raw_token)

    def tokens_match(self, raw_token: str, token_hash: str) -> bool:
        return constant_time_equals(self.hash_token(raw_token), token_hash)


class StubPasswordHasher(PasswordHasher):
    """Deterministic hasher for tests when Argon2 is unavailable.

    Uses HMAC-SHA256 with a fixed test key. Production wiring must use Argon2.
    """

    def __init__(self, pepper: str = "eos-auth-test-pepper") -> None:
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


class InMemoryUserAccountRepository(UserAccountRepository):
    """Process-local user account store."""

    def __init__(self) -> None:
        self._by_id: dict[str, UserAccount] = {}
        self._by_email: dict[str, str] = {}

    def get_by_id(self, user_id: UserId) -> UserAccount | None:
        return self._by_id.get(user_id.value)

    def get_by_email(self, email: EmailAddress) -> UserAccount | None:
        user_id = self._by_email.get(email.value)
        if user_id is None:
            return None
        return self._by_id.get(user_id)

    def save(self, account: UserAccount) -> None:
        previous = self._by_id.get(account.user_id.value)
        if previous is not None and previous.email.value != account.email.value:
            self._by_email.pop(previous.email.value, None)
        self._by_id[account.user_id.value] = account
        self._by_email[account.email.value] = account.user_id.value

    def next_identity(self) -> UserId:
        return UserId(f"user-{uuid4().hex}")


class InMemoryAuthTokenRepository(AuthTokenRepository):
    """Process-local auth token store."""

    def __init__(self) -> None:
        self._tokens: list[AuthToken] = []

    def save(self, token: AuthToken) -> None:
        self._tokens.append(token)

    def find_usable(
        self,
        *,
        purpose: AuthTokenPurpose,
        token_hash: str,
        now: datetime,
    ) -> AuthToken | None:
        for token in reversed(self._tokens):
            if (
                token.purpose is purpose
                and constant_time_equals(token.token_hash, token_hash)
                and token.is_usable(now)
            ):
                return token
        return None

    def mark_consumed(self, token: AuthToken, *, consumed_at: datetime) -> None:
        for index, existing in enumerate(self._tokens):
            if (
                existing.user_id.value == token.user_id.value
                and constant_time_equals(existing.token_hash, token.token_hash)
                and existing.purpose is token.purpose
                and existing.created_at == token.created_at
            ):
                from dataclasses import replace

                self._tokens[index] = replace(existing, consumed_at=consumed_at)
                return

    def invalidate_for_user(
        self,
        user_id: UserId,
        purpose: AuthTokenPurpose,
    ) -> None:
        from dataclasses import replace

        now = datetime.fromtimestamp(0, tz=None)
        updated: list[AuthToken] = []
        for token in self._tokens:
            if (
                token.user_id.value == user_id.value
                and token.purpose is purpose
                and token.consumed_at is None
            ):
                updated.append(replace(token, consumed_at=token.created_at or now))
            else:
                updated.append(token)
        self._tokens = updated


class RecordingEmailSender(EmailSender):
    """Capture outbound emails for tests."""

    def __init__(self) -> None:
        self.messages: list[tuple[str, str, str]] = []

    def send(self, *, to: EmailAddress, subject: str, body: str) -> None:
        self.messages.append((to.value, subject, body))


class InMemoryRateLimiter(RateLimiter):
    """Sliding-window rate limiter for authentication endpoints."""

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


def new_opaque_token() -> str:
    """Generate a fresh opaque token for email / reset flows."""
    return generate_opaque_token()
