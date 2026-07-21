"""Authentication domain — trusted student identities.

Pure domain rules for credentials, lockout, sessions, and tokens.

Allowed: value objects, policies, aggregates, invariants.

Forbidden: Flask, SQLAlchemy, Argon2 library calls, HTTP, email delivery,
educational logic, Student Twin creation, onboarding.
"""

from __future__ import annotations

from domain.auth.auth_token import AuthToken
from domain.auth.email_address import EmailAddress
from domain.auth.enums import AccountStatus, AuthFailureReason, AuthTokenPurpose
from domain.auth.errors import AuthDomainError, AuthInvariantViolation
from domain.auth.ids import UserId
from domain.auth.lockout_policy import LockoutPolicy
from domain.auth.password_policy import PasswordPolicy
from domain.auth.session_policy import SessionPolicy
from domain.auth.user_account import UserAccount

__all__ = [
    "AccountStatus",
    "AuthDomainError",
    "AuthFailureReason",
    "AuthInvariantViolation",
    "AuthToken",
    "AuthTokenPurpose",
    "EmailAddress",
    "LockoutPolicy",
    "PasswordPolicy",
    "SessionPolicy",
    "UserAccount",
    "UserId",
]
