"""Founder / Console access helpers — RBAC with legacy allowlist bridge (PR-001).

Primary authorization is durable ``UserRole`` / ``UserCapability`` rows.
``ADMIN_EMAIL`` ∪ ``FOUNDER_EMAILS`` remains a bootstrap bridge: matching
emails are treated as Founder and synced onto the user record when checked.
"""

from __future__ import annotations

import os
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from flask import abort, current_app
from flask_login import current_user, login_required

from app.security.authorization import (
    user_has_capability,
    user_has_permission,
    user_has_role,
)
from app.security.capabilities import Capability
from app.security.permissions import Permission
from app.security.roles import Role

F = TypeVar("F", bound=Callable[..., Any])


def founder_emails() -> frozenset[str]:
    """Return normalised bootstrap Founder email addresses.

    Sources (merged):
    - ``ADMIN_EMAIL`` (canonical bootstrap administrator)
    - ``FOUNDER_EMAILS`` comma-separated list
    - ``FOUNDER_EMAILS`` app config (tests)
    """
    emails: set[str] = set()
    admin = (os.getenv("ADMIN_EMAIL") or "").strip().lower()
    if admin:
        emails.add(admin)

    env_founders = (os.getenv("FOUNDER_EMAILS") or "").strip()
    if env_founders:
        emails.update(e.strip().lower() for e in env_founders.split(",") if e.strip())

    try:
        cfg = current_app.config.get("FOUNDER_EMAILS")
    except RuntimeError:
        cfg = None
    if isinstance(cfg, str) and cfg.strip():
        emails.update(e.strip().lower() for e in cfg.split(",") if e.strip())
    elif isinstance(cfg, list | tuple | set | frozenset):
        emails.update(str(e).strip().lower() for e in cfg if str(e).strip())

    return frozenset(emails)


def _email_on_legacy_allowlist(user: Any) -> bool:
    email = str(getattr(user, "email", "") or "").strip().lower()
    return bool(email) and email in founder_emails()


def is_founder_user(user: Any | None = None) -> bool:
    """Return whether ``user`` may access Founder / Console surfaces.

    Order of checks:
    1. Durable Founder role
    2. Console capability + console.access permission (admin / staff)
    3. Legacy email allowlist (bootstrap; syncs Founder role when possible)
    """
    candidate = user if user is not None else current_user
    if candidate is None or not getattr(candidate, "is_authenticated", False):
        return False

    if user_has_role(candidate, Role.FOUNDER):
        return True

    if user_has_capability(candidate, Capability.CONSOLE) and user_has_permission(
        candidate, Permission.CONSOLE_ACCESS
    ):
        return True

    if _email_on_legacy_allowlist(candidate):
        try:
            from app.services.identity_service import IdentityService

            IdentityService.sync_legacy_founder_allowlist(
                candidate, founder_emails()
            )
        except Exception:  # noqa: BLE001 — access check must not fail closed on sync
            pass
        return True

    return False


def founder_required(view: F) -> F:
    """Require authentication and Founder / Console access (RBAC).

    Prefer ``permission_required(Permission.CONSOLE_ACCESS)`` for new routes.
    """

    @wraps(view)
    @login_required
    def wrapped(*args: Any, **kwargs: Any):
        if not is_founder_user(current_user):
            abort(403)
        return view(*args, **kwargs)

    return wrapped  # type: ignore[return-value]
