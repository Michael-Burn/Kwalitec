"""Transactional rollback tests for BR-004 product repositories."""

from __future__ import annotations

from infrastructure.persistence.sqlalchemy_uow import SqlAlchemyProductUnitOfWork
from tests.education_os.infrastructure.persistence.br004.conftest import (
    build_onboarding_session,
    build_user_account,
    sample_checkpoint_events,
)


def test_rollback_discards_uncommitted_user(session_factory) -> None:
    account = build_user_account()
    with SqlAlchemyProductUnitOfWork(session_factory) as uow:
        uow.users.save(account)
        uow.rollback()

    with SqlAlchemyProductUnitOfWork(session_factory) as uow:
        assert uow.users.get_by_email(account.email) is None


def test_commit_then_new_unit_reads_persisted_data(session_factory) -> None:
    account = build_user_account()
    with SqlAlchemyProductUnitOfWork(session_factory) as uow:
        uow.users.save(account)
        uow.commit()

    with SqlAlchemyProductUnitOfWork(session_factory) as uow:
        loaded = uow.users.get_by_id(account.user_id)
        assert loaded is not None
        uow.commit()


def test_cross_repository_commit_is_atomic(session_factory) -> None:
    account = build_user_account()
    onboarding = build_onboarding_session()
    with SqlAlchemyProductUnitOfWork(session_factory) as uow:
        uow.users.save(account)
        uow.onboarding.save(onboarding)
        uow.commit()

    with SqlAlchemyProductUnitOfWork(session_factory) as uow:
        assert uow.users.get_by_id(account.user_id) is not None
        assert uow.onboarding.get(onboarding.onboarding_id) is not None


def test_checkpoint_rollback_discards_events(session_factory) -> None:
    events = sample_checkpoint_events()
    with SqlAlchemyProductUnitOfWork(session_factory) as uow:
        uow.checkpoints.save("session-rollback", events)
        uow.rollback()

    with SqlAlchemyProductUnitOfWork(session_factory) as uow:
        assert uow.checkpoints.load("session-rollback") is None
