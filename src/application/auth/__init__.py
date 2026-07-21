"""Authentication application services — trusted student identities.

Framework-independent use-cases for registration, login, logout, remember-me
claims, email verification, password reset, change password, session timeout,
and account lockout.

Forbidden: educational logic, Student Twin creation, onboarding, Flask,
SQLAlchemy, direct Argon2 imports.
"""

from __future__ import annotations

from application.auth.auth_service import AuthenticationService
from application.auth.errors import AuthenticationError
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
from application.auth.requests import (
    ChangePasswordRequest,
    LoginRequest,
    RegisterRequest,
    RequestPasswordResetRequest,
    ResetPasswordRequest,
    SessionValidationRequest,
    VerifyEmailRequest,
)
from application.auth.results import AuthResult, AuthSessionClaims
from application.auth.security import (
    constant_time_equals,
    generate_opaque_token,
    hash_opaque_token,
)

__all__ = [
    "AuthResult",
    "AuthSessionClaims",
    "AuthTokenRepository",
    "AuthenticationError",
    "AuthenticationService",
    "ChangePasswordRequest",
    "Clock",
    "EmailSender",
    "InMemoryAuthTokenRepository",
    "InMemoryRateLimiter",
    "InMemoryUserAccountRepository",
    "LoginRequest",
    "PasswordHasher",
    "RateLimiter",
    "RecordingEmailSender",
    "RegisterRequest",
    "RequestPasswordResetRequest",
    "ResetPasswordRequest",
    "SessionValidationRequest",
    "Sha256TokenHasher",
    "StubPasswordHasher",
    "TokenHasher",
    "UserAccountRepository",
    "VerifyEmailRequest",
    "constant_time_equals",
    "generate_opaque_token",
    "hash_opaque_token",
]
