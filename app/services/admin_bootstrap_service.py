"""Administrator bootstrap and credential synchronisation.

Used by ``flask create-admin``, ``flask sync-admin``, and production
``StartupService`` for *initial* admin creation only.

Password synchronisation is intentionally **not** invoked from startup —
operators must run ``flask sync-admin`` explicitly.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass

from app.extensions import db
from app.models.user import User
from app.security.roles import Role
from app.services.identity_service import IdentityService

logger = logging.getLogger(__name__)


class AdminBootstrapError(Exception):
    """Raised when required ``ADMIN_EMAIL`` / ``ADMIN_PASSWORD`` are missing."""

    def __init__(self, missing: list[str]) -> None:
        self.missing = list(missing)
        detail = ", ".join(self.missing)
        super().__init__(
            f"Missing required environment variable(s): {detail}. "
            "Set these variables and retry."
        )


@dataclass(frozen=True)
class AdminSyncResult:
    """Outcome of ``AdminBootstrapService.sync_admin``."""

    created: bool
    password_updated: bool
    founder_role_verified: bool
    administrator_role_verified: bool
    student_role_verified: bool
    user_id: int
    email: str


class AdminBootstrapService:
    """Create or synchronise the bootstrap administrator from environment."""

    @staticmethod
    def credentials_from_env() -> tuple[str | None, str | None, list[str]]:
        """Read ``ADMIN_EMAIL`` / ``ADMIN_PASSWORD`` and list missing names.

        Returns:
            ``(email, password, missing)`` where ``email`` is lower/stripped
            when present, and ``missing`` lists absent variable names.
        """
        raw_email = os.getenv("ADMIN_EMAIL")
        raw_password = os.getenv("ADMIN_PASSWORD")
        email = (raw_email or "").strip().lower() or None
        password = (raw_password or "").strip() or None
        missing: list[str] = []
        if not email:
            missing.append("ADMIN_EMAIL")
        if not password:
            missing.append("ADMIN_PASSWORD")
        return email, password, missing

    @staticmethod
    def require_credentials() -> tuple[str, str]:
        """Return normalised ``(email, password)`` or raise ``AdminBootstrapError``."""
        email, password, missing = AdminBootstrapService.credentials_from_env()
        if missing:
            raise AdminBootstrapError(missing)
        assert email is not None and password is not None
        return email, password

    @staticmethod
    def create_admin_user(email: str, password: str) -> User:
        """Create an active administrator and grant Founder RBAC.

        Args:
            email: Normalised administrator email.
            password: Plaintext password (hashed before storage).

        Returns:
            The persisted ``User`` (roles committed via IdentityService).
        """
        user = User(email=email.strip().lower(), is_active_user=True)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()
        IdentityService.ensure_founder_admin(user)
        logger.info("Admin created with Founder RBAC for email=%s", email)
        return user

    @staticmethod
    def create_initial_admin_if_empty() -> User | None:
        """Create the first administrator when the users table is empty.

        Does not synchronise passwords when users already exist (production
        safety). Returns ``None`` when skipped because users already exist.

        Raises:
            AdminBootstrapError: When creation is needed but env vars are missing.
        """
        user_count: int = db.session.query(User).count()
        if user_count > 0:
            logger.info(
                "Admin already exists (%d user(s)) — skipping initial create.",
                user_count,
            )
            return None

        email, password = AdminBootstrapService.require_credentials()
        return AdminBootstrapService.create_admin_user(email, password)

    @staticmethod
    def sync_admin() -> AdminSyncResult:
        """Create or update the administrator matching ``ADMIN_EMAIL``.

        When the user exists, updates the password hash from
        ``ADMIN_PASSWORD`` and ensures Founder RBAC without duplicating role
        rows. When absent, creates the administrator as ``create-admin`` does.

        Raises:
            AdminBootstrapError: When ``ADMIN_EMAIL`` or ``ADMIN_PASSWORD`` is missing.
        """
        email, password = AdminBootstrapService.require_credentials()
        user: User | None = (
            db.session.query(User).filter_by(email=email).first()
        )

        created = False
        password_updated = False

        if user is None:
            user = AdminBootstrapService.create_admin_user(email, password)
            created = True
            password_updated = True
        else:
            user.set_password(password)
            password_updated = True
            IdentityService.ensure_founder_admin(user)

        db.session.refresh(user)
        roles = user.get_roles()
        return AdminSyncResult(
            created=created,
            password_updated=password_updated,
            founder_role_verified=Role.FOUNDER in roles,
            administrator_role_verified=Role.ADMINISTRATOR in roles,
            student_role_verified=Role.STUDENT in roles,
            user_id=int(user.id),
            email=str(user.email),
        )
