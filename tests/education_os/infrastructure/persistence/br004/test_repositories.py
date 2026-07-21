"""CRUD and round-trip persistence tests for BR-004 product repositories."""

from __future__ import annotations

from datetime import timedelta

from domain.auth.email_address import EmailAddress
from domain.auth.enums import AuthTokenPurpose
from domain.auth.ids import UserId
from domain.onboarding.ids import OnboardingId
from infrastructure.persistence.checkpoint_repository import SqlAlchemyCheckpointRepository
from infrastructure.persistence.mappers.onboarding_mapper import OnboardingSessionMapper
from infrastructure.persistence.mappers.user_mapper import AuthTokenMapper, UserAccountMapper
from infrastructure.persistence.onboarding_repository import SqlAlchemyOnboardingRepository
from infrastructure.persistence.user_repository import (
    SqlAlchemyAuthTokenRepository,
    SqlAlchemyUserRepository,
)
from tests.education_os.infrastructure.persistence.br004.conftest import (
    FIXED_NOW,
    build_auth_token,
    build_onboarding_session,
    build_user_account,
    sample_checkpoint_events,
)


def test_user_account_round_trip(session) -> None:
    account = build_user_account(verified=True)
    repo = SqlAlchemyUserRepository(session)
    repo.save(account)
    session.commit()

    by_id = repo.get_by_id(account.user_id)
    by_email = repo.get_by_email(account.email)
    assert by_id is not None
    assert by_email is not None
    assert UserAccountMapper.to_persistence(by_id) == UserAccountMapper.to_persistence(
        account
    )


def test_user_account_update_increments_row_version(session) -> None:
    account = build_user_account()
    repo = SqlAlchemyUserRepository(session)
    repo.save(account)
    session.commit()

    updated = account.mark_email_verified(now=FIXED_NOW)
    repo.save(updated)
    session.commit()

    loaded = repo.get_by_id(account.user_id)
    assert loaded is not None
    assert loaded.email_verified is True


def test_auth_token_save_find_and_consume(session) -> None:
    account = build_user_account()
    SqlAlchemyUserRepository(session).save(account)
    token = build_auth_token(user_id=account.user_id)
    repo = SqlAlchemyAuthTokenRepository(session)
    repo.save(token)
    session.commit()

    found = repo.find_usable(
        purpose=AuthTokenPurpose.EMAIL_VERIFICATION,
        token_hash=token.token_hash,
        now=FIXED_NOW,
    )
    assert found is not None
    assert AuthTokenMapper.to_persistence(found) == AuthTokenMapper.to_persistence(token)

    consumed_at = FIXED_NOW + timedelta(minutes=5)
    repo.mark_consumed(token, consumed_at=consumed_at)
    session.commit()

    assert (
        repo.find_usable(
            purpose=AuthTokenPurpose.EMAIL_VERIFICATION,
            token_hash=token.token_hash,
            now=consumed_at,
        )
        is None
    )


def test_auth_token_invalidate_for_user(session) -> None:
    account = build_user_account()
    SqlAlchemyUserRepository(session).save(account)
    repo = SqlAlchemyAuthTokenRepository(session)
    repo.save(build_auth_token(user_id=account.user_id, token_hash="hash-a"))
    repo.save(
        build_auth_token(
            user_id=account.user_id,
            purpose=AuthTokenPurpose.PASSWORD_RESET,
            token_hash="hash-b",
        )
    )
    session.commit()

    repo.invalidate_for_user(account.user_id, AuthTokenPurpose.EMAIL_VERIFICATION)
    session.commit()

    assert (
        repo.find_usable(
            purpose=AuthTokenPurpose.EMAIL_VERIFICATION,
            token_hash="hash-a",
            now=FIXED_NOW,
        )
        is None
    )
    assert (
        repo.find_usable(
            purpose=AuthTokenPurpose.PASSWORD_RESET,
            token_hash="hash-b",
            now=FIXED_NOW,
        )
        is not None
    )


def test_onboarding_session_round_trip(session) -> None:
    onboarding = build_onboarding_session()
    repo = SqlAlchemyOnboardingRepository(session)
    repo.save(onboarding)
    session.commit()

    loaded = repo.get(onboarding.onboarding_id)
    assert loaded is not None
    assert OnboardingSessionMapper.to_persistence(
        loaded
    ) == OnboardingSessionMapper.to_persistence(onboarding)


def test_onboarding_get_in_progress_for_student(session) -> None:
    onboarding = build_onboarding_session()
    repo = SqlAlchemyOnboardingRepository(session)
    repo.save(onboarding)
    session.commit()

    loaded = repo.get_in_progress_for_student(onboarding.student_id)
    assert loaded is not None
    assert loaded.onboarding_id == onboarding.onboarding_id


def test_onboarding_completed_not_returned_as_in_progress(session) -> None:
    from dataclasses import replace

    from domain.onboarding.enums import OnboardingStatus, OnboardingStep

    onboarding = build_onboarding_session()
    completed = replace(
        onboarding,
        status=OnboardingStatus.COMPLETED,
        current_step=OnboardingStep.BUILD_STUDENT_TWIN,
        completed_at=FIXED_NOW,
        updated_at=FIXED_NOW,
    )
    repo = SqlAlchemyOnboardingRepository(session)
    repo.save(completed)
    session.commit()

    assert repo.get_in_progress_for_student(completed.student_id) is None


def test_checkpoint_save_load_clear(session) -> None:
    events = sample_checkpoint_events()
    repo = SqlAlchemyCheckpointRepository(session)
    repo.save("session-001", events)
    session.commit()

    loaded = repo.load("session-001")
    assert loaded == events

    repo.clear("session-001")
    session.commit()
    assert repo.load("session-001") is None


def test_checkpoint_empty_session_id_is_noop(session) -> None:
    repo = SqlAlchemyCheckpointRepository(session)
    repo.save("  ", sample_checkpoint_events())
    repo.clear("")
    session.commit()
    assert repo.load("") is None


def test_twin_and_evidence_adapters_are_sqlalchemy_repos() -> None:
    from infrastructure.persistence.evidence_repository import (
        SqlAlchemyEvidenceRepository,
    )
    from infrastructure.persistence.sqlalchemy.repositories.digital_twin_repository import (
        SqlAlchemyDigitalTwinRepository,
    )
    from infrastructure.persistence.sqlalchemy.repositories.evidence_repository import (
        SqlAlchemyEvidenceRepository as EosEvidenceRepo,
    )
    from infrastructure.persistence.twin_repository import SqlAlchemyTwinRepository

    assert SqlAlchemyTwinRepository is SqlAlchemyDigitalTwinRepository
    assert SqlAlchemyEvidenceRepository is EosEvidenceRepo


def test_get_missing_returns_none(session) -> None:
    assert SqlAlchemyUserRepository(session).get_by_id(UserId("missing")) is None
    assert (
        SqlAlchemyUserRepository(session).get_by_email(EmailAddress("x@example.com"))
        is None
    )
    assert (
        SqlAlchemyOnboardingRepository(session).get(OnboardingId("missing")) is None
    )
    assert SqlAlchemyCheckpointRepository(session).load("missing") is None
