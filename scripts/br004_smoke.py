"""BR-004 smoke: adapters + CRUD + rollback (no pytest, no alembic import)."""

from __future__ import annotations

import re
import sys
import traceback
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

failures: list[str] = []
FIXED_NOW = datetime(2026, 7, 20, 12, 0, tzinfo=UTC)


def check(name: str, fn) -> None:
    try:
        fn()
        print(f"PASS {name}", flush=True)
    except Exception as exc:  # noqa: BLE001
        failures.append(name)
        print(f"FAIL {name}: {exc}", flush=True)
        traceback.print_exc()


def test_files() -> None:
    base = ROOT / "src" / "infrastructure" / "persistence"
    for name in (
        "user_repository.py",
        "twin_repository.py",
        "evidence_repository.py",
        "onboarding_repository.py",
        "checkpoint_repository.py",
        "sqlalchemy_uow.py",
        "migrations/versions/202607200002_add_br004_product_persistence.py",
        "sqlalchemy/models/user_account.py",
        "sqlalchemy/models/auth_token.py",
        "sqlalchemy/models/onboarding_session.py",
        "sqlalchemy/models/session_checkpoint.py",
        "mappers/user_mapper.py",
        "mappers/onboarding_mapper.py",
        "mappers/checkpoint_mapper.py",
        "dto/user.py",
        "dto/onboarding.py",
    ):
        assert (base / name).is_file(), name


def test_migration_revision_text() -> None:
    path = (
        ROOT
        / "src"
        / "infrastructure"
        / "persistence"
        / "migrations"
        / "versions"
        / "202607200002_add_br004_product_persistence.py"
    )
    text = path.read_text(encoding="utf-8")
    assert re.search(r'revision\s*=\s*"202607200002"', text)
    assert re.search(r'down_revision\s*=\s*"202607200001"', text)
    for table in (
        "eos_user_accounts",
        "eos_auth_tokens",
        "eos_onboarding_sessions",
        "eos_session_checkpoints",
    ):
        assert table in text, table


def test_interfaces() -> None:
    from application.auth.ports import AuthTokenRepository, UserAccountRepository
    from application.onboarding.ports import OnboardingRepository
    from infrastructure.persistence.onboarding_repository import (
        SqlAlchemyOnboardingRepository,
    )
    from infrastructure.persistence.user_repository import (
        SqlAlchemyAuthTokenRepository,
        SqlAlchemyUserRepository,
    )

    assert issubclass(SqlAlchemyUserRepository, UserAccountRepository)
    assert issubclass(SqlAlchemyAuthTokenRepository, AuthTokenRepository)
    assert issubclass(SqlAlchemyOnboardingRepository, OnboardingRepository)


def test_crud_and_rollback() -> None:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session, sessionmaker
    from sqlalchemy.pool import StaticPool

    from domain.auth.auth_token import AuthToken
    from domain.auth.email_address import EmailAddress
    from domain.auth.enums import AuthTokenPurpose
    from domain.auth.ids import UserId
    from domain.auth.user_account import UserAccount
    from domain.onboarding.enums import OnboardingStep
    from domain.onboarding.ids import OnboardingId, StudentId
    from domain.onboarding.onboarding_session import OnboardingSession
    from domain.onboarding.step_payloads import WelcomePayload
    from infrastructure.persistence.checkpoint_repository import (
        SqlAlchemyCheckpointRepository,
    )
    from infrastructure.persistence.onboarding_repository import (
        SqlAlchemyOnboardingRepository,
    )
    from infrastructure.persistence.sqlalchemy.base import metadata
    from infrastructure.persistence.sqlalchemy.models.auth_token import AuthTokenModel
    from infrastructure.persistence.sqlalchemy.models.onboarding_session import (
        OnboardingSessionModel,
    )
    from infrastructure.persistence.sqlalchemy.models.session_checkpoint import (
        SessionCheckpointModel,
    )
    from infrastructure.persistence.sqlalchemy.models.user_account import (
        UserAccountModel,
    )
    from infrastructure.persistence.user_repository import (
        SqlAlchemyAuthTokenRepository,
        SqlAlchemyUserRepository,
    )

    _ = (AuthTokenModel, OnboardingSessionModel, SessionCheckpointModel, UserAccountModel)

    eng = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    metadata.create_all(eng)
    factory = sessionmaker(bind=eng, expire_on_commit=False, class_=Session)

    account = UserAccount.register(
        user_id=UserId("user-001"),
        email=EmailAddress("student@example.com"),
        password_hash="hashed",
        now=FIXED_NOW,
    ).mark_email_verified(now=FIXED_NOW)
    token = AuthToken(
        user_id=account.user_id,
        purpose=AuthTokenPurpose.EMAIL_VERIFICATION,
        token_hash="tok-hash",
        expires_at=FIXED_NOW + timedelta(hours=24),
        created_at=FIXED_NOW,
    )
    onboarding = OnboardingSession.start(
        onboarding_id=OnboardingId("onb-001"),
        student_id=StudentId("stu-001"),
        now=FIXED_NOW,
    ).autosave(
        OnboardingStep.WELCOME,
        WelcomePayload(acknowledged=True),
        now=FIXED_NOW,
    )
    events = [{"type": "started", "at": FIXED_NOW.isoformat()}]

    with factory() as session:
        SqlAlchemyUserRepository(session).save(account)
        SqlAlchemyAuthTokenRepository(session).save(token)
        SqlAlchemyOnboardingRepository(session).save(onboarding)
        SqlAlchemyCheckpointRepository(session).save("sess-1", events)
        session.commit()

    with factory() as session:
        assert SqlAlchemyUserRepository(session).get_by_id(account.user_id) is not None
        assert (
            SqlAlchemyAuthTokenRepository(session).find_usable(
                purpose=AuthTokenPurpose.EMAIL_VERIFICATION,
                token_hash="tok-hash",
                now=FIXED_NOW,
            )
            is not None
        )
        assert (
            SqlAlchemyOnboardingRepository(session).get(onboarding.onboarding_id)
            is not None
        )
        assert SqlAlchemyCheckpointRepository(session).load("sess-1") == events

    with factory() as session:
        other = UserAccount.register(
            user_id=UserId("user-rollback"),
            email=EmailAddress("rollback@example.com"),
            password_hash="hashed",
            now=FIXED_NOW,
        )
        SqlAlchemyUserRepository(session).save(other)
        session.rollback()
    with factory() as session:
        assert (
            SqlAlchemyUserRepository(session).get_by_email(
                EmailAddress("rollback@example.com")
            )
            is None
        )
    eng.dispose()


def test_product_uow_mocks() -> None:
    from sqlalchemy.orm import Session

    from infrastructure.persistence.sqlalchemy_uow import SqlAlchemyProductUnitOfWork
    from infrastructure.persistence.user_repository import SqlAlchemyUserRepository

    session = Mock(spec=Session)
    with SqlAlchemyProductUnitOfWork(Mock(return_value=session)) as uow:
        assert isinstance(uow.users, SqlAlchemyUserRepository)
        assert uow.checkpoints is not None
        uow.commit()


def main() -> int:
    print("BR-004 smoke starting...", flush=True)
    check("files", test_files)
    check("migration_revision_text", test_migration_revision_text)
    check("interfaces", test_interfaces)
    check("crud_and_rollback", test_crud_and_rollback)
    check("product_uow_mocks", test_product_uow_mocks)
    if failures:
        print(f"FAILED: {failures}", flush=True)
        return 1
    print("all smoke passed", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
