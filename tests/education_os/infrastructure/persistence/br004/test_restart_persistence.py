"""Restart persistence tests — data survives session close and reopen (BR-004)."""

from __future__ import annotations

from sqlalchemy.orm import Session, sessionmaker

from infrastructure.persistence.checkpoint_repository import SqlAlchemyCheckpointRepository
from infrastructure.persistence.onboarding_repository import SqlAlchemyOnboardingRepository
from infrastructure.persistence.user_repository import SqlAlchemyUserRepository
from tests.education_os.infrastructure.persistence.br004.conftest import (
    build_onboarding_session,
    build_user_account,
    sample_checkpoint_events,
)


def _persist_and_close(
    session_factory: sessionmaker[Session],
    *,
    user=None,
    onboarding=None,
    checkpoint_session_id: str | None = None,
    checkpoint_events=None,
) -> None:
    session = session_factory()
    try:
        if user is not None:
            SqlAlchemyUserRepository(session).save(user)
        if onboarding is not None:
            SqlAlchemyOnboardingRepository(session).save(onboarding)
        if checkpoint_session_id is not None and checkpoint_events is not None:
            SqlAlchemyCheckpointRepository(session).save(
                checkpoint_session_id, checkpoint_events
            )
        session.commit()
    finally:
        session.close()


def test_user_survives_session_restart(session_factory) -> None:
    account = build_user_account(verified=True)
    _persist_and_close(session_factory, user=account)

    session = session_factory()
    try:
        loaded = SqlAlchemyUserRepository(session).get_by_id(account.user_id)
        assert loaded is not None
        assert loaded.email_verified is True
    finally:
        session.close()


def test_onboarding_survives_session_restart(session_factory) -> None:
    onboarding = build_onboarding_session()
    _persist_and_close(session_factory, onboarding=onboarding)

    session = session_factory()
    try:
        loaded = SqlAlchemyOnboardingRepository(session).get(onboarding.onboarding_id)
        assert loaded is not None
        assert loaded.student_id == onboarding.student_id
    finally:
        session.close()


def test_checkpoint_survives_session_restart(session_factory) -> None:
    events = sample_checkpoint_events()
    _persist_and_close(
        session_factory,
        checkpoint_session_id="restart-session",
        checkpoint_events=events,
    )

    session = session_factory()
    try:
        loaded = SqlAlchemyCheckpointRepository(session).load("restart-session")
        assert loaded == events
    finally:
        session.close()
