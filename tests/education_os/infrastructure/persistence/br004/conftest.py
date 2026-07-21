"""Shared fixtures and builders for BR-004 persistence tests."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from domain.auth.auth_token import AuthToken
from domain.auth.email_address import EmailAddress
from domain.auth.enums import AuthTokenPurpose
from domain.auth.ids import UserId
from domain.auth.user_account import UserAccount
from domain.onboarding.enums import OnboardingStep
from domain.onboarding.ids import OnboardingId, StudentId
from domain.onboarding.onboarding_session import OnboardingSession
from domain.onboarding.step_payloads import WelcomePayload
from infrastructure.persistence.sqlalchemy.base import metadata
from infrastructure.persistence.sqlalchemy.models.auth_token import AuthTokenModel
from infrastructure.persistence.sqlalchemy.models.onboarding_session import (
    OnboardingSessionModel,
)
from infrastructure.persistence.sqlalchemy.models.session_checkpoint import (
    SessionCheckpointModel,
)
from infrastructure.persistence.sqlalchemy.models.user_account import UserAccountModel

# Register BR-004 models on metadata without importing the educational model package.
_ = (
    AuthTokenModel,
    OnboardingSessionModel,
    SessionCheckpointModel,
    UserAccountModel,
)

FIXED_NOW = datetime(2026, 7, 20, 12, 0, tzinfo=UTC)


@pytest.fixture()
def engine():
    from sqlalchemy.pool import StaticPool

    eng = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    metadata.create_all(eng)
    yield eng
    eng.dispose()


@pytest.fixture()
def session_factory(engine):
    return sessionmaker(bind=engine, expire_on_commit=False, class_=Session)


@pytest.fixture()
def session(session_factory):
    with session_factory() as sess:
        yield sess
        sess.rollback()


def build_user_account(*, verified: bool = False) -> UserAccount:
    account = UserAccount.register(
        user_id=UserId("user-001"),
        email=EmailAddress("student@example.com"),
        password_hash="hashed-password-value",
        now=FIXED_NOW,
    )
    if verified:
        return account.mark_email_verified(now=FIXED_NOW)
    return account


def build_auth_token(
    *,
    user_id: UserId | None = None,
    purpose: AuthTokenPurpose = AuthTokenPurpose.EMAIL_VERIFICATION,
    token_hash: str = "sha256-token-hash",
) -> AuthToken:
    uid = user_id or UserId("user-001")
    return AuthToken(
        user_id=uid,
        purpose=purpose,
        token_hash=token_hash,
        expires_at=FIXED_NOW + timedelta(hours=24),
        created_at=FIXED_NOW,
    )


def build_onboarding_session() -> OnboardingSession:
    session = OnboardingSession.start(
        onboarding_id=OnboardingId("onb-001"),
        student_id=StudentId("stu-001"),
        now=FIXED_NOW,
    )
    return session.autosave(
        OnboardingStep.WELCOME,
        WelcomePayload(acknowledged=True),
        now=FIXED_NOW,
    )


def sample_checkpoint_events() -> list[dict[str, object]]:
    return [
        {"type": "session_started", "at": FIXED_NOW.isoformat()},
        {"type": "step_completed", "step": "welcome", "at": FIXED_NOW.isoformat()},
    ]
