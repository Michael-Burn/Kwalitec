"""Product UnitOfWork transaction and repository wiring tests (BR-004)."""

from __future__ import annotations

from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from infrastructure.persistence.checkpoint_repository import SqlAlchemyCheckpointRepository
from infrastructure.persistence.onboarding_repository import SqlAlchemyOnboardingRepository
from infrastructure.persistence.sqlalchemy_uow import SqlAlchemyProductUnitOfWork
from infrastructure.persistence.user_repository import (
    SqlAlchemyAuthTokenRepository,
    SqlAlchemyUserRepository,
)


def make_session() -> Mock:
    return Mock(spec=Session)


def test_context_manager_begins_rolls_back_and_closes_session() -> None:
    session = make_session()
    uow = SqlAlchemyProductUnitOfWork(Mock(return_value=session))

    with uow as entered:
        assert entered is uow
        assert uow.is_active is True

    session.begin.assert_called_once_with()
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()
    assert uow.is_active is False


def test_commit_persists_without_exit_rollback() -> None:
    session = make_session()
    uow = SqlAlchemyProductUnitOfWork(Mock(return_value=session))

    with uow:
        uow.commit()

    session.commit.assert_called_once_with()
    session.rollback.assert_not_called()
    session.close.assert_called_once_with()


def test_explicit_rollback_is_not_repeated_on_exit() -> None:
    session = make_session()
    uow = SqlAlchemyProductUnitOfWork(Mock(return_value=session))

    with uow:
        uow.rollback()

    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


def test_failed_commit_rolls_back_and_closes_session() -> None:
    session = make_session()
    session.commit.side_effect = RuntimeError("database unavailable")
    uow = SqlAlchemyProductUnitOfWork(Mock(return_value=session))

    with pytest.raises(RuntimeError, match="database unavailable"):
        with uow:
            uow.commit()

    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()
    assert uow.is_active is False


def test_repositories_share_the_unit_of_work_session() -> None:
    from infrastructure.persistence.evidence_repository import (
        SqlAlchemyEvidenceRepository,
    )
    from infrastructure.persistence.twin_repository import SqlAlchemyTwinRepository

    session = make_session()
    uow = SqlAlchemyProductUnitOfWork(Mock(return_value=session))
    expected = (
        ("users", SqlAlchemyUserRepository),
        ("tokens", SqlAlchemyAuthTokenRepository),
        ("twins", SqlAlchemyTwinRepository),
        ("evidence", SqlAlchemyEvidenceRepository),
        ("onboarding", SqlAlchemyOnboardingRepository),
        ("checkpoints", SqlAlchemyCheckpointRepository),
    )

    with uow:
        for property_name, repository_type in expected:
            repository = getattr(uow, property_name)
            assert isinstance(repository, repository_type)
            assert repository._session is session


def test_repository_access_requires_an_open_unit() -> None:
    uow = SqlAlchemyProductUnitOfWork(Mock(return_value=make_session()))

    with pytest.raises(RuntimeError, match="not active"):
        _ = uow.users
