"""Identity service — assign roles and portal capabilities (PR-001).

One User identity may hold multiple roles and portal capabilities.
Does not create duplicate accounts for Console vs Student Portal.
"""

from __future__ import annotations

import logging
from typing import Any

from app.extensions import db
from app.security.capabilities import (
    Capability,
    default_capabilities_for_roles,
    normalize_capability,
)
from app.security.roles import Role, normalize_role

logger = logging.getLogger(__name__)


class IdentityService:
    """Manage durable role and capability assignments on a User."""

    @staticmethod
    def ensure_student_defaults(user: Any) -> None:
        """Ensure a learner identity has Student role + student portal."""
        IdentityService.grant_role(user, Role.STUDENT, commit=False)
        IdentityService.grant_capability(
            user, Capability.STUDENT_PORTAL, commit=False
        )
        db.session.commit()

    @staticmethod
    def ensure_founder_admin(user: Any) -> None:
        """Bootstrap Founder + Administrator with console access."""
        IdentityService.grant_role(user, Role.FOUNDER, commit=False)
        IdentityService.grant_role(user, Role.ADMINISTRATOR, commit=False)
        IdentityService.grant_role(user, Role.STUDENT, commit=False)
        for role in (Role.FOUNDER, Role.ADMINISTRATOR, Role.STUDENT):
            for cap in default_capabilities_for_roles({role}):
                IdentityService.grant_capability(user, cap, commit=False)
        db.session.commit()

    @staticmethod
    def grant_role(user: Any, role: str | Role, *, commit: bool = True) -> bool:
        """Assign ``role`` to ``user``. Returns True when a row was added."""
        from app.models.identity import UserRole

        resolved = normalize_role(role)
        if resolved is None:
            raise ValueError(f"Unknown role: {role}")
        existing = (
            db.session.query(UserRole)
            .filter_by(user_id=user.id, role=resolved.value)
            .first()
        )
        if existing is not None:
            return False
        db.session.add(UserRole(user_id=user.id, role=resolved.value))
        if commit:
            db.session.commit()
        logger.info("Granted role=%s user_id=%s", resolved.value, user.id)
        return True

    @staticmethod
    def revoke_role(user: Any, role: str | Role, *, commit: bool = True) -> bool:
        """Remove ``role`` from ``user``. Returns True when a row was deleted."""
        from app.models.identity import UserRole

        resolved = normalize_role(role)
        if resolved is None:
            raise ValueError(f"Unknown role: {role}")
        deleted = (
            db.session.query(UserRole)
            .filter_by(user_id=user.id, role=resolved.value)
            .delete()
        )
        if commit and deleted:
            db.session.commit()
        return bool(deleted)

    @staticmethod
    def grant_capability(
        user: Any,
        capability: str | Capability,
        *,
        commit: bool = True,
    ) -> bool:
        """Assign portal ``capability`` to ``user``."""
        from app.models.identity import UserCapability

        resolved = normalize_capability(capability)
        if resolved is None:
            raise ValueError(f"Unknown capability: {capability}")
        existing = (
            db.session.query(UserCapability)
            .filter_by(user_id=user.id, capability=resolved.value)
            .first()
        )
        if existing is not None:
            return False
        db.session.add(
            UserCapability(user_id=user.id, capability=resolved.value)
        )
        if commit:
            db.session.commit()
        logger.info(
            "Granted capability=%s user_id=%s", resolved.value, user.id
        )
        return True

    @staticmethod
    def revoke_capability(
        user: Any,
        capability: str | Capability,
        *,
        commit: bool = True,
    ) -> bool:
        """Remove portal ``capability`` from ``user``."""
        from app.models.identity import UserCapability

        resolved = normalize_capability(capability)
        if resolved is None:
            raise ValueError(f"Unknown capability: {capability}")
        deleted = (
            db.session.query(UserCapability)
            .filter_by(user_id=user.id, capability=resolved.value)
            .delete()
        )
        if commit and deleted:
            db.session.commit()
        return bool(deleted)

    @staticmethod
    def sync_legacy_founder_allowlist(
        user: Any, founder_emails: frozenset[str]
    ) -> bool:
        """If email is on the legacy allowlist and lacks Founder, grant it.

        Used during the PR-001 transition so existing deployments keep working
        until operators assign durable roles. Returns True when roles changed.
        """
        email = str(getattr(user, "email", "") or "").strip().lower()
        if not email or email not in founder_emails:
            return False
        from app.security.authorization import user_has_role

        if user_has_role(user, Role.FOUNDER):
            return False
        IdentityService.ensure_founder_admin(user)
        return True
