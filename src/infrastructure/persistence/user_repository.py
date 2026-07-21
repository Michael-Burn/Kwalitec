"""SQLAlchemy UserAccount and AuthToken repositories (BR-004)."""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from application.auth.ports import AuthTokenRepository, UserAccountRepository
from application.auth.security import constant_time_equals
from domain.auth.auth_token import AuthToken
from domain.auth.email_address import EmailAddress
from domain.auth.enums import AuthTokenPurpose
from domain.auth.ids import UserId
from domain.auth.user_account import UserAccount
from infrastructure.persistence.dto.user import AuthTokenDTO, UserAccountDTO
from infrastructure.persistence.mappers.user_mapper import AuthTokenMapper, UserAccountMapper
from infrastructure.persistence.sqlalchemy.models.auth_token import AuthTokenModel
from infrastructure.persistence.sqlalchemy.models.user_account import UserAccountModel
from infrastructure.persistence.sqlalchemy.repositories.row_codec import (
    dto_from_model,
    model_from_dto,
)


class ConcurrentUpdateError(RuntimeError):
    """Raised when an optimistic lock version does not match on write."""


class SqlAlchemyUserRepository(UserAccountRepository):
    """Persist UserAccount aggregates via SQLAlchemy.

    Row versions are remembered at load time. SQLAlchemy's identity map uses
    weak references, so re-reading ``row_version`` from ``session.get`` after
    the mapped instance is collected would observe the latest committed value
    and silently defeat optimistic concurrency.
    """

    def __init__(self, session: Session) -> None:
        self._session = session
        self._row_versions: dict[str, int] = {}

    def get_by_id(self, user_id: UserId) -> UserAccount | None:
        row = self._session.get(UserAccountModel, user_id.value)
        if row is None:
            return None
        dto = dto_from_model(UserAccountDTO, row)
        self._row_versions[dto.user_id] = int(dto.row_version)
        return UserAccountMapper.to_domain(dto)

    def get_by_email(self, email: EmailAddress) -> UserAccount | None:
        statement = select(UserAccountModel).where(UserAccountModel.email == email.value)
        row = self._session.scalars(statement).first()
        if row is None:
            return None
        dto = dto_from_model(UserAccountDTO, row)
        self._row_versions[dto.user_id] = int(dto.row_version)
        return UserAccountMapper.to_domain(dto)

    def save(self, account: UserAccount) -> None:
        existing = self._session.get(UserAccountModel, account.user_id.value)
        if existing is None:
            dto = UserAccountMapper.to_persistence(account, row_version=1)
            self._session.add(model_from_dto(UserAccountModel, dto))
            self._row_versions[account.user_id.value] = 1
            return

        expected = self._row_versions.get(account.user_id.value)
        if expected is None:
            # Aggregate was not loaded through this repository instance; use the
            # identity-map value only as a last resort for first contact.
            expected = int(existing.row_version)
        dto = UserAccountMapper.to_persistence(account, row_version=expected + 1)
        result = self._session.execute(
            update(UserAccountModel)
            .where(
                UserAccountModel.user_id == account.user_id.value,
                UserAccountModel.row_version == expected,
            )
            .values(
                email=dto.email,
                password_hash=dto.password_hash,
                status=dto.status,
                email_verified=dto.email_verified,
                failed_login_attempts=dto.failed_login_attempts,
                locked_until=dto.locked_until,
                created_at=dto.created_at,
                updated_at=dto.updated_at,
                password_changed_at=dto.password_changed_at,
                row_version=dto.row_version,
            )
        )
        if result.rowcount != 1:
            raise ConcurrentUpdateError(
                f"user {account.user_id.value} was updated concurrently"
            )
        # Keep the identity map consistent with the versioned write.
        existing.row_version = dto.row_version
        existing.email = dto.email
        existing.password_hash = dto.password_hash
        existing.status = dto.status
        existing.email_verified = dto.email_verified
        existing.failed_login_attempts = dto.failed_login_attempts
        existing.locked_until = dto.locked_until
        existing.created_at = dto.created_at
        existing.updated_at = dto.updated_at
        existing.password_changed_at = dto.password_changed_at
        self._row_versions[account.user_id.value] = dto.row_version

    def next_identity(self) -> UserId:
        return UserId(f"user-{uuid4().hex}")


class SqlAlchemyAuthTokenRepository(AuthTokenRepository):
    """Persist AuthToken records via SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, token: AuthToken) -> None:
        dto = AuthTokenMapper.to_persistence(token)
        self._session.add(model_from_dto(AuthTokenModel, dto))

    def find_usable(
        self,
        *,
        purpose: AuthTokenPurpose,
        token_hash: str,
        now: datetime,
    ) -> AuthToken | None:
        statement = (
            select(AuthTokenModel)
            .where(
                AuthTokenModel.purpose == purpose.value,
                AuthTokenModel.consumed_at.is_(None),
                AuthTokenModel.expires_at > now,
            )
            .order_by(AuthTokenModel.created_at.desc())
        )
        for row in self._session.scalars(statement):
            if constant_time_equals(row.token_hash, token_hash):
                return AuthTokenMapper.to_domain(dto_from_model(AuthTokenDTO, row))
        return None

    def mark_consumed(self, token: AuthToken, *, consumed_at: datetime) -> None:
        statement = (
            select(AuthTokenModel)
            .where(
                AuthTokenModel.user_id == token.user_id.value,
                AuthTokenModel.purpose == token.purpose.value,
                AuthTokenModel.created_at == token.created_at,
            )
            .order_by(AuthTokenModel.token_id.desc())
        )
        for row in self._session.scalars(statement):
            if constant_time_equals(row.token_hash, token.token_hash):
                row.consumed_at = consumed_at
                return

    def invalidate_for_user(
        self,
        user_id: UserId,
        purpose: AuthTokenPurpose,
    ) -> None:
        statement = (
            update(AuthTokenModel)
            .where(
                AuthTokenModel.user_id == user_id.value,
                AuthTokenModel.purpose == purpose.value,
                AuthTokenModel.consumed_at.is_(None),
            )
            .values(consumed_at=AuthTokenModel.created_at)
        )
        self._session.execute(statement)
