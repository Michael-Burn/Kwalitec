"""Optimistic locking concurrency tests for BR-004 mutable repositories."""

from __future__ import annotations

import pytest
from sqlalchemy.orm import Session, sessionmaker

from infrastructure.persistence.onboarding_repository import SqlAlchemyOnboardingRepository
from infrastructure.persistence.user_repository import (
    ConcurrentUpdateError,
    SqlAlchemyUserRepository,
)
from tests.education_os.infrastructure.persistence.br004.conftest import (
    FIXED_NOW,
    build_onboarding_session,
    build_user_account,
)


def _open_session(session_factory: sessionmaker[Session]) -> Session:
    return session_factory()


def test_concurrent_user_update_raises(session_factory) -> None:
    account = build_user_account()
    first = _open_session(session_factory)
    second = _open_session(session_factory)
    try:
        SqlAlchemyUserRepository(first).save(account)
        first.commit()

        repo_one = SqlAlchemyUserRepository(first)
        repo_two = SqlAlchemyUserRepository(second)
        loaded_one = repo_one.get_by_id(account.user_id)
        loaded_two = repo_two.get_by_id(account.user_id)
        assert loaded_one is not None
        assert loaded_two is not None

        repo_two.save(loaded_two.mark_email_verified(now=FIXED_NOW))
        second.commit()

        with pytest.raises(ConcurrentUpdateError, match="updated concurrently"):
            repo_one.save(loaded_one.mark_email_verified(now=FIXED_NOW))
            first.commit()
    finally:
        first.close()
        second.close()


def test_concurrent_onboarding_update_raises(session_factory) -> None:
    onboarding = build_onboarding_session()
    first = _open_session(session_factory)
    second = _open_session(session_factory)
    try:
        SqlAlchemyOnboardingRepository(first).save(onboarding)
        first.commit()

        repo_one = SqlAlchemyOnboardingRepository(first)
        repo_two = SqlAlchemyOnboardingRepository(second)
        loaded_one = repo_one.get(onboarding.onboarding_id)
        loaded_two = repo_two.get(onboarding.onboarding_id)
        assert loaded_one is not None
        assert loaded_two is not None

        from dataclasses import replace

        repo_two.save(replace(loaded_two, updated_at=FIXED_NOW))
        second.commit()

        with pytest.raises(ConcurrentUpdateError, match="updated concurrently"):
            repo_one.save(replace(loaded_one, updated_at=FIXED_NOW))
            first.commit()
    finally:
        first.close()
        second.close()
