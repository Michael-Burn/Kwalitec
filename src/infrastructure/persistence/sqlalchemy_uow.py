"""Product SQLAlchemy Unit of Work for BR-004 production persistence.

Coordinates Users, Auth Tokens, Student Twins, Evidence, Onboarding Drafts,
and Session Checkpoints in one transactional session. No educational logic.
"""

from __future__ import annotations

from collections.abc import Callable
from types import TracebackType
from typing import Self, TypeVar

from sqlalchemy.orm import Session

from application.auth.ports import AuthTokenRepository, UserAccountRepository
from application.onboarding.ports import OnboardingRepository
from application.ports.repositories import DigitalTwinRepository, EvidenceRepository
from infrastructure.persistence.checkpoint_repository import (
    SqlAlchemyCheckpointRepository,
)
from infrastructure.persistence.onboarding_repository import (
    SqlAlchemyOnboardingRepository,
)
from infrastructure.persistence.user_repository import (
    SqlAlchemyAuthTokenRepository,
    SqlAlchemyUserRepository,
)

SessionFactory = Callable[[], Session]
RepositoryT = TypeVar("RepositoryT")


class SqlAlchemyProductUnitOfWork:
    """Transactional boundary for BR-004 durable product repositories."""

    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory
        self._session: Session | None = None
        self._is_active = False
        self._users: UserAccountRepository | None = None
        self._tokens: AuthTokenRepository | None = None
        self._twins: DigitalTwinRepository | None = None
        self._evidence: EvidenceRepository | None = None
        self._onboarding: OnboardingRepository | None = None
        self._checkpoints: SqlAlchemyCheckpointRepository | None = None

    @property
    def users(self) -> UserAccountRepository:
        return self._require_repository(self._users)

    @property
    def tokens(self) -> AuthTokenRepository:
        return self._require_repository(self._tokens)

    @property
    def twins(self) -> DigitalTwinRepository:
        return self._require_repository(self._twins)

    @property
    def digital_twins(self) -> DigitalTwinRepository:
        """Alias for educational UnitOfWork consumers (init / evidence update)."""
        return self.twins

    @property
    def evidence(self) -> EvidenceRepository:
        return self._require_repository(self._evidence)

    @property
    def onboarding(self) -> OnboardingRepository:
        return self._require_repository(self._onboarding)

    @property
    def checkpoints(self) -> SqlAlchemyCheckpointRepository:
        return self._require_repository(self._checkpoints)

    @property
    def is_active(self) -> bool:
        return self._is_active

    def begin(self) -> None:
        if self._is_active:
            raise RuntimeError("unit of work is already active")
        session = self._session_factory()
        try:
            session.begin()
            self._wire_repositories(session)
        except Exception:
            session.close()
            raise
        self._session = session
        self._is_active = True

    def __enter__(self) -> Self:
        self.begin()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> bool:
        try:
            if self._is_active:
                self.rollback()
        finally:
            self._close_session()
        return False

    def commit(self) -> None:
        session = self._require_active_session()
        try:
            session.commit()
        except Exception:
            try:
                session.rollback()
            finally:
                self._is_active = False
            raise
        self._is_active = False

    def rollback(self) -> None:
        if not self._is_active:
            return
        session = self._require_active_session()
        try:
            session.rollback()
        finally:
            self._is_active = False

    def _wire_repositories(self, session: Session) -> None:
        # Twin/evidence adapters are imported lazily so BR-004 product surfaces
        # do not eagerly load the educational aggregate graph.
        from infrastructure.persistence.evidence_repository import (
            SqlAlchemyEvidenceRepository,
        )
        from infrastructure.persistence.twin_repository import SqlAlchemyTwinRepository

        self._users = SqlAlchemyUserRepository(session)
        self._tokens = SqlAlchemyAuthTokenRepository(session)
        self._twins = SqlAlchemyTwinRepository(session)
        self._evidence = SqlAlchemyEvidenceRepository(session)
        self._onboarding = SqlAlchemyOnboardingRepository(session)
        self._checkpoints = SqlAlchemyCheckpointRepository(session)

    def _require_active_session(self) -> Session:
        if not self._is_active or self._session is None:
            raise RuntimeError("unit of work is not active")
        return self._session

    @staticmethod
    def _require_repository(repository: RepositoryT | None) -> RepositoryT:
        if repository is None:
            raise RuntimeError("unit of work is not active")
        return repository

    def _close_session(self) -> None:
        if self._session is not None:
            self._session.close()
        self._session = None
        self._users = None
        self._tokens = None
        self._twins = None
        self._evidence = None
        self._onboarding = None
        self._checkpoints = None


# Canonical BR-004 export name for the product unit of work module.
SqlAlchemyUnitOfWork = SqlAlchemyProductUnitOfWork

__all__ = [
    "SqlAlchemyProductUnitOfWork",
    "SqlAlchemyUnitOfWork",
]
