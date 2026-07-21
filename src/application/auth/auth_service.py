"""AuthenticationService — production identity use-cases.

Framework-independent. Coordinates domain policies with ports for hashing,
persistence, email, and rate limiting.

Allowed: registration, login, logout claims invalidation helpers, remember-me
claims, email verification, password reset, change password, session timeout
checks, account lockout.

Forbidden: educational logic, Student Twin creation, onboarding, Flask,
SQLAlchemy, direct Argon2 library imports.
"""

from __future__ import annotations

from datetime import UTC, datetime

from application.auth.errors import AuthenticationError
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
from application.auth.security import generate_opaque_token
from domain.auth.auth_token import AuthToken
from domain.auth.email_address import EmailAddress
from domain.auth.enums import AuthFailureReason, AuthTokenPurpose
from domain.auth.errors import AuthDomainError, AuthInvariantViolation
from domain.auth.ids import UserId
from domain.auth.lockout_policy import LockoutPolicy
from domain.auth.password_policy import PasswordPolicy
from domain.auth.session_policy import SessionPolicy
from domain.auth.user_account import UserAccount


class AuthenticationService:
    """Coordinate authentication use-cases against injectable ports."""

    def __init__(
        self,
        *,
        users: UserAccountRepository,
        tokens: AuthTokenRepository,
        hasher: PasswordHasher,
        token_hasher: TokenHasher,
        email_sender: EmailSender,
        rate_limiter: RateLimiter,
        clock: Clock,
        password_policy: PasswordPolicy | None = None,
        lockout_policy: LockoutPolicy | None = None,
        session_policy: SessionPolicy | None = None,
        require_verified_email: bool = True,
        expose_tokens: bool = False,
    ) -> None:
        self._users = users
        self._tokens = tokens
        self._hasher = hasher
        self._token_hasher = token_hasher
        self._email = email_sender
        self._rate_limiter = rate_limiter
        self._clock = clock
        self._password_policy = password_policy or PasswordPolicy()
        self._lockout_policy = lockout_policy or LockoutPolicy()
        self._session_policy = session_policy or SessionPolicy()
        self._require_verified_email = require_verified_email
        self._expose_tokens = expose_tokens
        self._cached_dummy_hash: str | None = None

    def _dummy_password_hash(self) -> str:
        if self._cached_dummy_hash is None:
            self._cached_dummy_hash = self._hasher.hash("invalid-placeholder")
        return self._cached_dummy_hash

    def register(self, request: RegisterRequest) -> AuthResult:
        """Register a new account and issue an email verification token."""
        now = self._clock.now()
        self._assert_rate_limit(f"register:{request.client_key}", now)
        try:
            email = EmailAddress(request.email)
            password = self._password_policy.validate(request.password)
        except AuthInvariantViolation as exc:
            raise AuthenticationError(
                str(exc),
                reason=AuthFailureReason.WEAK_PASSWORD
                if "password" in str(exc).lower()
                else AuthFailureReason.VALIDATION_ERROR,
            ) from exc

        if self._users.get_by_email(email) is not None:
            raise AuthenticationError(
                "email is already registered",
                reason=AuthFailureReason.EMAIL_TAKEN,
            )

        user_id = self._users.next_identity()
        account = UserAccount.register(
            user_id=user_id,
            email=email,
            password_hash=self._hasher.hash(password),
            now=now,
        )
        self._users.save(account)
        raw_token = self._issue_token(
            account,
            purpose=AuthTokenPurpose.EMAIL_VERIFICATION,
            now=now,
        )
        self._email.send(
            to=email,
            subject="Verify your Kwalitec email",
            body=f"Verify your email with token: {raw_token}",
        )
        return AuthResult(
            success=True,
            message="registration successful; verify your email",
            user_id=account.user_id.value,
            email=account.email.value,
            status=account.status,
            issued_token=raw_token if self._expose_tokens else None,
        )

    def login(self, request: LoginRequest) -> AuthResult:
        """Authenticate credentials and return session claims on success."""
        now = self._clock.now()
        self._assert_rate_limit(f"login:{request.client_key}", now)

        try:
            email = EmailAddress(request.email)
        except AuthInvariantViolation as exc:
            raise AuthenticationError(
                "invalid email or password",
                reason=AuthFailureReason.INVALID_CREDENTIALS,
            ) from exc

        account = self._users.get_by_email(email)
        if account is None:
            # Exercise verify against a stable dummy hash to reduce timing skew.
            self._hasher.verify(request.password, self._dummy_password_hash())
            raise AuthenticationError(
                "invalid email or password",
                reason=AuthFailureReason.INVALID_CREDENTIALS,
            )

        try:
            account.assert_can_authenticate(
                now=now,
                lockout_policy=self._lockout_policy,
                require_verified_email=self._require_verified_email,
            )
        except AuthDomainError as exc:
            reason = AuthFailureReason.ACCOUNT_LOCKED
            lowered = str(exc).lower()
            if "disabled" in lowered:
                reason = AuthFailureReason.ACCOUNT_DISABLED
            elif "verified" in lowered:
                reason = AuthFailureReason.EMAIL_NOT_VERIFIED
            raise AuthenticationError(str(exc), reason=reason) from exc

        if not self._hasher.verify(request.password, account.password_hash):
            updated = account.record_failed_login(
                now=now,
                lockout_policy=self._lockout_policy,
            )
            self._users.save(updated)
            if updated.status.value == "locked" or self._lockout_policy.is_locked(
                locked_until=updated.locked_until,
                now=now,
            ):
                raise AuthenticationError(
                    "account is locked",
                    reason=AuthFailureReason.ACCOUNT_LOCKED,
                )
            raise AuthenticationError(
                "invalid email or password",
                reason=AuthFailureReason.INVALID_CREDENTIALS,
            )

        updated = account.record_successful_login(now=now)
        self._users.save(updated)
        session = AuthSessionClaims(
            user_id=updated.user_id.value,
            email=updated.email.value,
            remember_me=bool(request.remember_me),
            created_at=now,
            last_activity_at=now,
            email_verified=updated.email_verified,
        )
        return AuthResult(
            success=True,
            message="login successful",
            user_id=updated.user_id.value,
            email=updated.email.value,
            status=updated.status,
            session=session,
        )

    def logout(self, user_id: str | None) -> AuthResult:
        """Acknowledge logout. Session clearing is an adapter concern."""
        return AuthResult(
            success=True,
            message="logout successful",
            user_id=(user_id or "").strip() or None,
        )

    def verify_email(self, request: VerifyEmailRequest) -> AuthResult:
        """Consume an email verification token and activate the account."""
        now = self._clock.now()
        self._assert_rate_limit(f"verify:{request.client_key}", now)
        account = self._consume_token(
            raw_token=request.token,
            purpose=AuthTokenPurpose.EMAIL_VERIFICATION,
            now=now,
        )
        updated = account.mark_email_verified(now=now)
        self._users.save(updated)
        return AuthResult(
            success=True,
            message="email verified",
            user_id=updated.user_id.value,
            email=updated.email.value,
            status=updated.status,
        )

    def request_password_reset(
        self,
        request: RequestPasswordResetRequest,
    ) -> AuthResult:
        """Issue a password-reset token when the email exists.

        Always returns success to avoid account enumeration.
        """
        now = self._clock.now()
        self._assert_rate_limit(f"reset-request:{request.client_key}", now)
        issued: str | None = None
        try:
            email = EmailAddress(request.email)
        except AuthInvariantViolation:
            return AuthResult(
                success=True,
                message="if the account exists, a reset email was sent",
            )

        account = self._users.get_by_email(email)
        if account is not None:
            issued = self._issue_token(
                account,
                purpose=AuthTokenPurpose.PASSWORD_RESET,
                now=now,
            )
            self._email.send(
                to=email,
                subject="Reset your Kwalitec password",
                body=f"Reset your password with token: {issued}",
            )
        return AuthResult(
            success=True,
            message="if the account exists, a reset email was sent",
            issued_token=issued if self._expose_tokens else None,
        )

    def reset_password(self, request: ResetPasswordRequest) -> AuthResult:
        """Set a new password using a valid reset token."""
        now = self._clock.now()
        self._assert_rate_limit(f"reset:{request.client_key}", now)
        try:
            password = self._password_policy.validate(request.new_password)
        except AuthInvariantViolation as exc:
            raise AuthenticationError(
                str(exc),
                reason=AuthFailureReason.WEAK_PASSWORD,
            ) from exc

        account = self._consume_token(
            raw_token=request.token,
            purpose=AuthTokenPurpose.PASSWORD_RESET,
            now=now,
        )
        updated = account.change_password_hash(
            self._hasher.hash(password),
            now=now,
        )
        self._users.save(updated)
        self._tokens.invalidate_for_user(
            updated.user_id,
            AuthTokenPurpose.PASSWORD_RESET,
        )
        return AuthResult(
            success=True,
            message="password reset successful",
            user_id=updated.user_id.value,
            email=updated.email.value,
            status=updated.status,
        )

    def change_password(self, request: ChangePasswordRequest) -> AuthResult:
        """Change password for an authenticated user."""
        now = self._clock.now()
        self._assert_rate_limit(f"change:{request.client_key}", now)
        user_id = UserId(request.user_id)
        account = self._users.get_by_id(user_id)
        if account is None:
            raise AuthenticationError(
                "account not found",
                reason=AuthFailureReason.VALIDATION_ERROR,
            )
        if not self._hasher.verify(request.current_password, account.password_hash):
            raise AuthenticationError(
                "current password is incorrect",
                reason=AuthFailureReason.INVALID_CREDENTIALS,
            )
        try:
            password = self._password_policy.validate(request.new_password)
        except AuthInvariantViolation as exc:
            raise AuthenticationError(
                str(exc),
                reason=AuthFailureReason.WEAK_PASSWORD,
            ) from exc

        updated = account.change_password_hash(
            self._hasher.hash(password),
            now=now,
        )
        self._users.save(updated)
        return AuthResult(
            success=True,
            message="password changed",
            user_id=updated.user_id.value,
            email=updated.email.value,
            status=updated.status,
        )

    def validate_session(self, request: SessionValidationRequest) -> AuthResult:
        """Return success when session timestamps remain within policy."""
        now = self._clock.now()
        try:
            created_at = datetime.fromisoformat(request.created_at_iso)
            last_activity = datetime.fromisoformat(request.last_activity_at_iso)
        except ValueError as exc:
            raise AuthenticationError(
                "invalid session timestamps",
                reason=AuthFailureReason.SESSION_EXPIRED,
            ) from exc

        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=UTC)
        if last_activity.tzinfo is None:
            last_activity = last_activity.replace(tzinfo=UTC)

        if self._session_policy.is_expired(
            created_at=created_at,
            last_activity_at=last_activity,
            now=now,
            remember_me=request.remember_me,
        ):
            raise AuthenticationError(
                "session expired",
                reason=AuthFailureReason.SESSION_EXPIRED,
            )

        account = self._users.get_by_id(UserId(request.user_id))
        if account is None:
            raise AuthenticationError(
                "session expired",
                reason=AuthFailureReason.SESSION_EXPIRED,
            )

        session = AuthSessionClaims(
            user_id=account.user_id.value,
            email=account.email.value,
            remember_me=request.remember_me,
            created_at=created_at,
            last_activity_at=now,
            email_verified=account.email_verified,
        )
        return AuthResult(
            success=True,
            message="session valid",
            user_id=account.user_id.value,
            email=account.email.value,
            status=account.status,
            session=session,
        )

    def touch_session(self, claims: AuthSessionClaims) -> AuthSessionClaims:
        """Return claims with last_activity_at refreshed to now."""
        return AuthSessionClaims(
            user_id=claims.user_id,
            email=claims.email,
            remember_me=claims.remember_me,
            created_at=claims.created_at,
            last_activity_at=self._clock.now(),
            email_verified=claims.email_verified,
        )

    def _assert_rate_limit(self, key: str, now: datetime) -> None:
        cleaned = (key or "").strip() or "anonymous"
        if self._rate_limiter.is_limited(cleaned, now=now):
            raise AuthenticationError(
                "too many requests",
                reason=AuthFailureReason.RATE_LIMITED,
            )
        self._rate_limiter.record(cleaned, now=now)

    def _issue_token(
        self,
        account: UserAccount,
        *,
        purpose: AuthTokenPurpose,
        now: datetime,
    ) -> str:
        self._tokens.invalidate_for_user(account.user_id, purpose)
        raw = generate_opaque_token()
        token = AuthToken(
            user_id=account.user_id,
            purpose=purpose,
            token_hash=self._token_hasher.hash_token(raw),
            expires_at=now + AuthToken.default_ttl(purpose),
            created_at=now,
        )
        self._tokens.save(token)
        return raw

    def _consume_token(
        self,
        *,
        raw_token: str,
        purpose: AuthTokenPurpose,
        now: datetime,
    ) -> UserAccount:
        cleaned = (raw_token or "").strip()
        if not cleaned:
            raise AuthenticationError(
                "invalid or expired token",
                reason=AuthFailureReason.INVALID_TOKEN,
            )
        token_hash = self._token_hasher.hash_token(cleaned)
        token = self._tokens.find_usable(
            purpose=purpose,
            token_hash=token_hash,
            now=now,
        )
        if token is None:
            # Distinguish expired vs missing only when a matching consumed/expired
            # token is not required — keep response generic for security.
            raise AuthenticationError(
                "invalid or expired token",
                reason=AuthFailureReason.INVALID_TOKEN,
            )
        if not self._token_hasher.tokens_match(cleaned, token.token_hash):
            raise AuthenticationError(
                "invalid or expired token",
                reason=AuthFailureReason.INVALID_TOKEN,
            )
        self._tokens.mark_consumed(token, consumed_at=now)
        account = self._users.get_by_id(token.user_id)
        if account is None:
            raise AuthenticationError(
                "invalid or expired token",
                reason=AuthFailureReason.INVALID_TOKEN,
            )
        return account
