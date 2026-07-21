"""Outbound ports for authentication use-cases."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from domain.auth.auth_token import AuthToken
from domain.auth.email_address import EmailAddress
from domain.auth.enums import AuthTokenPurpose
from domain.auth.ids import UserId
from domain.auth.user_account import UserAccount


class Clock(ABC):
    """Injectable time source for authentication timestamps.

    Defined locally so authentication does not import educational ports.
    """

    @abstractmethod
    def now(self) -> datetime:
        """Return a timezone-aware UTC timestamp."""


class PasswordHasher(ABC):
    """Hash and verify passwords (Argon2 in infrastructure)."""

    @abstractmethod
    def hash(self, password: str) -> str:
        """Return a password hash for storage."""

    @abstractmethod
    def verify(self, password: str, password_hash: str) -> bool:
        """Return True when password matches hash (constant-time where possible)."""


class TokenHasher(ABC):
    """Hash opaque tokens for at-rest storage."""

    @abstractmethod
    def hash_token(self, raw_token: str) -> str:
        """Return a digestsuitable for persistence."""

    @abstractmethod
    def tokens_match(self, raw_token: str, token_hash: str) -> bool:
        """Constant-time compare of raw token against stored hash."""


class UserAccountRepository(ABC):
    """Persistence port for user accounts."""

    @abstractmethod
    def get_by_id(self, user_id: UserId) -> UserAccount | None:
        """Load an account by identity."""

    @abstractmethod
    def get_by_email(self, email: EmailAddress) -> UserAccount | None:
        """Load an account by normalised email."""

    @abstractmethod
    def save(self, account: UserAccount) -> None:
        """Insert or update an account."""

    @abstractmethod
    def next_identity(self) -> UserId:
        """Allocate a new user identity."""


class AuthTokenRepository(ABC):
    """Persistence port for single-use auth tokens."""

    @abstractmethod
    def save(self, token: AuthToken) -> None:
        """Persist a token record."""

    @abstractmethod
    def find_usable(
        self,
        *,
        purpose: AuthTokenPurpose,
        token_hash: str,
        now: datetime,
    ) -> AuthToken | None:
        """Find a non-consumed, non-expired token by hash and purpose."""

    @abstractmethod
    def mark_consumed(self, token: AuthToken, *, consumed_at: datetime) -> None:
        """Mark a token as consumed."""

    @abstractmethod
    def invalidate_for_user(
        self,
        user_id: UserId,
        purpose: AuthTokenPurpose,
    ) -> None:
        """Invalidate outstanding tokens for a user and purpose."""


class EmailSender(ABC):
    """Outbound email delivery for verification and reset messages."""

    @abstractmethod
    def send(self, *, to: EmailAddress, subject: str, body: str) -> None:
        """Deliver a plaintext email message."""


class RateLimiter(ABC):
    """Request rate limiting for authentication endpoints."""

    @abstractmethod
    def is_limited(self, key: str, *, now: datetime) -> bool:
        """Return True when the key exceeds the allowed rate."""

    @abstractmethod
    def record(self, key: str, *, now: datetime) -> None:
        """Record an attempt for the key."""
