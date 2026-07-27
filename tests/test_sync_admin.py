"""Tests for flask sync-admin and AdminBootstrapService."""

from __future__ import annotations

import os

from app.extensions import db
from app.models.identity import UserCapability, UserRole
from app.models.user import User
from app.security.capabilities import Capability
from app.security.roles import Role
from app.services.admin_bootstrap_service import AdminBootstrapService
from app.services.identity_service import IdentityService


def _set_admin_env(
    email: str = "admin@kwalitec.example",
    password: str = "securepassword123",
) -> None:
    os.environ["ADMIN_EMAIL"] = email
    os.environ["ADMIN_PASSWORD"] = password


def _role_counts(user_id: int) -> dict[str, int]:
    rows = db.session.query(UserRole).filter_by(user_id=user_id).all()
    counts: dict[str, int] = {}
    for row in rows:
        counts[row.role] = counts.get(row.role, 0) + 1
    return counts


def _capability_counts(user_id: int) -> dict[str, int]:
    rows = (
        db.session.query(UserCapability).filter_by(user_id=user_id).all()
    )
    counts: dict[str, int] = {}
    for row in rows:
        counts[row.capability] = counts.get(row.capability, 0) + 1
    return counts


class TestSyncAdminCommand:
    """CLI coverage for ``flask sync-admin``."""

    def test_creates_admin_when_user_absent(self, runner, ctx):
        """Creates administrator when ADMIN_EMAIL is not in the database."""
        _set_admin_env()

        result = runner.invoke(args=["sync-admin"])

        assert result.exit_code == 0
        assert "Administrator created successfully." in result.output

        user = (
            db.session.query(User)
            .filter_by(email="admin@kwalitec.example")
            .first()
        )
        assert user is not None
        assert user.check_password("securepassword123") is True
        assert user.is_active_user is True
        assert Role.FOUNDER in user.get_roles()
        assert Role.ADMINISTRATOR in user.get_roles()
        assert Role.STUDENT in user.get_roles()
        assert Capability.CONSOLE in user.get_capabilities()
        assert Capability.STUDENT_PORTAL in user.get_capabilities()

    def test_updates_password_when_user_exists(self, runner, ctx):
        """Updates password hash when ADMIN_EMAIL already exists."""
        user = User(email="admin@kwalitec.example", is_active_user=True)
        user.set_password("old-password-xyz")
        db.session.add(user)
        db.session.flush()
        IdentityService.ensure_founder_admin(user)
        old_hash = user.password_hash

        _set_admin_env(password="new-synced-password")
        result = runner.invoke(args=["sync-admin"])

        assert result.exit_code == 0
        assert "Administrator synchronised successfully." in result.output
        assert "password updated" in result.output
        assert "founder role verified" in result.output
        assert "administrator role verified" in result.output
        assert "student role verified" in result.output

        db.session.refresh(user)
        assert user.password_hash != old_hash
        assert user.check_password("new-synced-password") is True
        assert user.check_password("old-password-xyz") is False

    def test_roles_remain_correct_after_sync(self, runner, ctx):
        """Founder / administrator / student roles survive synchronisation."""
        user = User(email="admin@kwalitec.example", is_active_user=True)
        user.set_password("initial-password")
        db.session.add(user)
        db.session.flush()
        IdentityService.ensure_founder_admin(user)

        _set_admin_env(password="synced-password")
        result = runner.invoke(args=["sync-admin"])

        assert result.exit_code == 0
        db.session.refresh(user)
        roles = user.get_roles()
        assert Role.FOUNDER in roles
        assert Role.ADMINISTRATOR in roles
        assert Role.STUDENT in roles

    def test_capabilities_remain_correct_after_sync(self, runner, ctx):
        """Console and student portal capabilities survive synchronisation."""
        user = User(email="admin@kwalitec.example", is_active_user=True)
        user.set_password("initial-password")
        db.session.add(user)
        db.session.flush()
        IdentityService.ensure_founder_admin(user)

        _set_admin_env(password="synced-password")
        result = runner.invoke(args=["sync-admin"])

        assert result.exit_code == 0
        db.session.refresh(user)
        caps = user.get_capabilities()
        assert Capability.CONSOLE in caps
        assert Capability.STUDENT_PORTAL in caps
        assert Capability.API in caps

    def test_restores_missing_founder_roles(self, runner, ctx):
        """Grants Founder RBAC when the matching user lacks roles."""
        user = User(email="admin@kwalitec.example", is_active_user=True)
        user.set_password("initial-password")
        db.session.add(user)
        db.session.commit()

        _set_admin_env(password="synced-password")
        result = runner.invoke(args=["sync-admin"])

        assert result.exit_code == 0
        db.session.refresh(user)
        assert Role.FOUNDER in user.get_roles()
        assert Role.ADMINISTRATOR in user.get_roles()
        assert Capability.CONSOLE in user.get_capabilities()
        assert user.check_password("synced-password") is True

    def test_command_is_idempotent(self, runner, ctx):
        """Running sync-admin twice leaves a single consistent admin."""
        _set_admin_env(password="first-pass")
        first = runner.invoke(args=["sync-admin"])
        assert first.exit_code == 0

        user = (
            db.session.query(User)
            .filter_by(email="admin@kwalitec.example")
            .first()
        )
        assert user is not None
        role_counts_before = _role_counts(user.id)
        cap_counts_before = _capability_counts(user.id)

        _set_admin_env(password="second-pass")
        second = runner.invoke(args=["sync-admin"])
        assert second.exit_code == 0
        assert "Administrator synchronised successfully." in second.output

        assert db.session.query(User).count() == 1
        db.session.refresh(user)
        assert user.check_password("second-pass") is True
        assert _role_counts(user.id) == role_counts_before
        assert _capability_counts(user.id) == cap_counts_before

        third = runner.invoke(args=["sync-admin"])
        assert third.exit_code == 0
        assert db.session.query(User).count() == 1
        assert _role_counts(user.id) == role_counts_before

    def test_missing_admin_email(self, runner, ctx):
        """Exits non-zero when ADMIN_EMAIL is missing."""
        os.environ.pop("ADMIN_EMAIL", None)
        os.environ["ADMIN_PASSWORD"] = "securepassword123"

        result = runner.invoke(args=["sync-admin"])

        assert result.exit_code != 0
        assert "ADMIN_EMAIL" in result.output

    def test_missing_admin_password(self, runner, ctx):
        """Exits non-zero when ADMIN_PASSWORD is missing."""
        os.environ["ADMIN_EMAIL"] = "admin@kwalitec.example"
        os.environ.pop("ADMIN_PASSWORD", None)

        result = runner.invoke(args=["sync-admin"])

        assert result.exit_code != 0
        assert "ADMIN_PASSWORD" in result.output

    def test_missing_both_env_vars(self, runner, ctx):
        """Reports both missing variables."""
        os.environ.pop("ADMIN_EMAIL", None)
        os.environ.pop("ADMIN_PASSWORD", None)

        result = runner.invoke(args=["sync-admin"])

        assert result.exit_code != 0
        assert "ADMIN_EMAIL" in result.output
        assert "ADMIN_PASSWORD" in result.output

    def test_duplicate_role_rows_not_created(self, runner, ctx):
        """Repeated sync does not insert duplicate role or capability rows."""
        _set_admin_env()
        runner.invoke(args=["sync-admin"])
        user = (
            db.session.query(User)
            .filter_by(email="admin@kwalitec.example")
            .first()
        )
        assert user is not None

        for _ in range(3):
            result = runner.invoke(args=["sync-admin"])
            assert result.exit_code == 0

        counts = _role_counts(user.id)
        assert counts.get(Role.FOUNDER.value) == 1
        assert counts.get(Role.ADMINISTRATOR.value) == 1
        assert counts.get(Role.STUDENT.value) == 1

        cap_counts = _capability_counts(user.id)
        assert cap_counts.get(Capability.CONSOLE.value) == 1
        assert cap_counts.get(Capability.STUDENT_PORTAL.value) == 1

    def test_password_hash_actually_changes(self, runner, ctx):
        """Password hash changes and check_password matches ADMIN_PASSWORD."""
        user = User(email="admin@kwalitec.example", is_active_user=True)
        user.set_password("stale-local-password")
        db.session.add(user)
        db.session.flush()
        IdentityService.ensure_founder_admin(user)
        previous_hash = user.password_hash

        _set_admin_env(password="env-aligned-password")
        result = runner.invoke(args=["sync-admin"])

        assert result.exit_code == 0
        db.session.refresh(user)
        assert user.password_hash != previous_hash
        assert user.check_password("env-aligned-password") is True

    def test_creates_when_other_users_exist_but_admin_email_absent(
        self, runner, user, ctx
    ):
        """Creates ADMIN_EMAIL even when unrelated users already exist."""
        assert user.email != "admin@kwalitec.example"
        _set_admin_env()

        result = runner.invoke(args=["sync-admin"])

        assert result.exit_code == 0
        assert "Administrator created successfully." in result.output
        admin = (
            db.session.query(User)
            .filter_by(email="admin@kwalitec.example")
            .first()
        )
        assert admin is not None
        assert admin.check_password("securepassword123") is True
        assert db.session.query(User).count() == 2

    def test_skips_when_users_table_missing(self, runner, ctx):
        """Exits non-zero when the users table does not exist."""
        _set_admin_env()
        db.drop_all()

        result = runner.invoke(args=["sync-admin"])

        assert result.exit_code != 0
        assert "users table not found" in result.output

        db.create_all()


class TestAdminBootstrapService:
    """Direct service-level coverage."""

    def test_sync_admin_service_create_and_update(self, ctx):
        _set_admin_env(password="service-pass-1")
        created = AdminBootstrapService.sync_admin()
        assert created.created is True
        assert created.password_updated is True
        assert created.founder_role_verified is True

        _set_admin_env(password="service-pass-2")
        updated = AdminBootstrapService.sync_admin()
        assert updated.created is False
        assert updated.password_updated is True
        assert updated.user_id == created.user_id

        user = db.session.get(User, updated.user_id)
        assert user is not None
        assert user.check_password("service-pass-2") is True

    def test_create_initial_admin_if_empty_skips_when_users_exist(
        self, user, ctx
    ):
        _set_admin_env()
        assert AdminBootstrapService.create_initial_admin_if_empty() is None
        assert db.session.query(User).count() == 1
