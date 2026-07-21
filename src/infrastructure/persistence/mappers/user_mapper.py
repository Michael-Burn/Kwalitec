"""Structural mapping for UserAccount and AuthToken aggregates (BR-004).

Domain ↔ persistence DTO only. No authentication policy. No educational behaviour.
"""

from __future__ import annotations

from domain.auth.auth_token import AuthToken
from domain.auth.email_address import EmailAddress
from domain.auth.enums import AccountStatus, AuthTokenPurpose
from domain.auth.ids import UserId
from domain.auth.user_account import UserAccount
from infrastructure.persistence.dto.user import AuthTokenDTO, UserAccountDTO


class UserAccountMapper:
    """Map UserAccount ↔ UserAccountDTO."""

    @staticmethod
    def to_persistence(account: UserAccount, *, row_version: int = 1) -> UserAccountDTO:
        return UserAccountDTO(
            user_id=account.user_id.value,
            email=account.email.value,
            password_hash=account.password_hash,
            status=account.status.value,
            email_verified=account.email_verified,
            failed_login_attempts=account.failed_login_attempts,
            locked_until=account.locked_until,
            created_at=account.created_at,
            updated_at=account.updated_at,
            password_changed_at=account.password_changed_at,
            row_version=row_version,
        )

    @staticmethod
    def to_domain(dto: UserAccountDTO) -> UserAccount:
        return UserAccount(
            user_id=UserId(dto.user_id),
            email=EmailAddress(dto.email),
            password_hash=dto.password_hash,
            status=AccountStatus(dto.status),
            email_verified=dto.email_verified,
            failed_login_attempts=dto.failed_login_attempts,
            locked_until=dto.locked_until,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            password_changed_at=dto.password_changed_at,
        )


class AuthTokenMapper:
    """Map AuthToken ↔ AuthTokenDTO."""

    @staticmethod
    def to_persistence(token: AuthToken) -> AuthTokenDTO:
        return AuthTokenDTO(
            user_id=token.user_id.value,
            purpose=token.purpose.value,
            token_hash=token.token_hash,
            expires_at=token.expires_at,
            created_at=token.created_at,
            consumed_at=token.consumed_at,
        )

    @staticmethod
    def to_domain(dto: AuthTokenDTO) -> AuthToken:
        return AuthToken(
            user_id=UserId(dto.user_id),
            purpose=AuthTokenPurpose(dto.purpose),
            token_hash=dto.token_hash,
            expires_at=dto.expires_at,
            created_at=dto.created_at,
            consumed_at=dto.consumed_at,
        )
