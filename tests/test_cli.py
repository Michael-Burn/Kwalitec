"""Tests for the create-admin CLI command."""

from __future__ import annotations

import os

from app.extensions import db
from app.models.user import User


class TestCreateAdminCommand:
    """Test suite for flask --app wsgi.py create-admin."""

    def test_creates_admin_when_no_users_exist(self, runner, ctx):
        """An administrator is created when the users table is empty."""
        os.environ["ADMIN_EMAIL"] = "admin@kwalitec.example"
        os.environ["ADMIN_PASSWORD"] = "securepassword123"

        result = runner.invoke(args=["create-admin"])

        assert result.exit_code == 0
        assert "Administrator created successfully." in result.output

        user = db.session.query(User).filter_by(
            email="admin@kwalitec.example"
        ).first()
        assert user is not None
        assert user.check_password("securepassword123") is True
        assert user.is_active_user is True

    def test_existing_user_skips_creation(self, runner, user, ctx):
        """Should print 'already exists' and exit 0 when a user is present."""
        os.environ["ADMIN_EMAIL"] = "admin@kwalitec.example"
        os.environ["ADMIN_PASSWORD"] = "securepassword123"

        result = runner.invoke(args=["create-admin"])

        assert result.exit_code == 0
        assert "Administrator already exists." in result.output

    def test_missing_admin_email(self, runner, ctx):
        """Should exit non-zero when ADMIN_EMAIL is missing."""
        # Ensure no env leftovers
        os.environ.pop("ADMIN_EMAIL", None)
        os.environ["ADMIN_PASSWORD"] = "securepassword123"

        result = runner.invoke(args=["create-admin"])

        assert result.exit_code != 0
        assert "ADMIN_EMAIL" in result.output

    def test_missing_admin_password(self, runner, ctx):
        """Should exit non-zero when ADMIN_PASSWORD is missing."""
        os.environ["ADMIN_EMAIL"] = "admin@kwalitec.example"
        os.environ.pop("ADMIN_PASSWORD", None)

        result = runner.invoke(args=["create-admin"])

        assert result.exit_code != 0
        assert "ADMIN_PASSWORD" in result.output

    def test_missing_both_env_vars(self, runner, ctx):
        """Should report both missing variables."""
        os.environ.pop("ADMIN_EMAIL", None)
        os.environ.pop("ADMIN_PASSWORD", None)

        result = runner.invoke(args=["create-admin"])

        assert result.exit_code != 0
        assert "ADMIN_EMAIL" in result.output
        assert "ADMIN_PASSWORD" in result.output

    def test_skips_when_users_table_missing(self, runner, ctx):
        """Should exit 0 when the users table does not exist yet.

        This simulates a deploy where create-admin runs before migrations
        have been applied. The command must not crash the deploy.
        """
        os.environ["ADMIN_EMAIL"] = "admin@kwalitec.example"
        os.environ["ADMIN_PASSWORD"] = "securepassword123"

        # Drop all tables to simulate a fresh, unmigrated database
        db.drop_all()

        result = runner.invoke(args=["create-admin"])

        assert result.exit_code == 0
        assert "users table not found" in result.output

        # Recreate tables so the session-scoped app teardown doesn't break
        db.create_all()