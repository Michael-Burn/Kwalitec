"""AuthController — Flask-free orchestration for authentication use-cases."""

from __future__ import annotations

from adapters.flask.auth.dependency_provider import AuthAdapterDependencies
from application.auth.auth_service import AuthenticationService
from application.auth.errors import AuthenticationError
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


class AuthController:
    """Invoke authentication application services without Flask imports."""

    def __init__(self, dependencies: AuthAdapterDependencies) -> None:
        self._dependencies = dependencies

    @property
    def service(self) -> AuthenticationService:
        service = self._dependencies.auth_service
        if service is None:
            raise RuntimeError("authentication service is not configured")
        return service

    def register(
        self,
        *,
        email: str,
        password: str,
        client_key: str = "",
    ) -> AuthResult:
        return self.service.register(
            RegisterRequest(email=email, password=password, client_key=client_key)
        )

    def login(
        self,
        *,
        email: str,
        password: str,
        remember_me: bool = False,
        client_key: str = "",
    ) -> AuthResult:
        return self.service.login(
            LoginRequest(
                email=email,
                password=password,
                remember_me=remember_me,
                client_key=client_key,
            )
        )

    def logout(self, user_id: str | None) -> AuthResult:
        return self.service.logout(user_id)

    def verify_email(self, *, token: str, client_key: str = "") -> AuthResult:
        return self.service.verify_email(
            VerifyEmailRequest(token=token, client_key=client_key)
        )

    def request_password_reset(
        self,
        *,
        email: str,
        client_key: str = "",
    ) -> AuthResult:
        return self.service.request_password_reset(
            RequestPasswordResetRequest(email=email, client_key=client_key)
        )

    def reset_password(
        self,
        *,
        token: str,
        new_password: str,
        client_key: str = "",
    ) -> AuthResult:
        return self.service.reset_password(
            ResetPasswordRequest(
                token=token,
                new_password=new_password,
                client_key=client_key,
            )
        )

    def change_password(
        self,
        *,
        user_id: str,
        current_password: str,
        new_password: str,
        client_key: str = "",
    ) -> AuthResult:
        return self.service.change_password(
            ChangePasswordRequest(
                user_id=user_id,
                current_password=current_password,
                new_password=new_password,
                client_key=client_key,
            )
        )

    def validate_session(self, claims: AuthSessionClaims) -> AuthResult:
        return self.service.validate_session(
            SessionValidationRequest(
                user_id=claims.user_id,
                created_at_iso=claims.created_at.isoformat(),
                last_activity_at_iso=claims.last_activity_at.isoformat(),
                remember_me=claims.remember_me,
            )
        )

    def touch_session(self, claims: AuthSessionClaims) -> AuthSessionClaims:
        return self.service.touch_session(claims)


def auth_error_message(exc: AuthenticationError) -> str:
    """Return a safe user-facing message for an authentication error."""
    return exc.message
