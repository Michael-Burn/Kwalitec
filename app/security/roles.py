"""Canonical application roles (PR-001).

One identity may hold multiple roles. Role names are stored as stable
string codes on ``user_roles.role``.
"""

from __future__ import annotations

from enum import StrEnum


class Role(StrEnum):
    """Named roles for Kwalitec RBAC."""

    FOUNDER = "founder"
    ADMINISTRATOR = "administrator"
    CONTENT_MANAGER = "content_manager"
    SUPPORT = "support"
    RESEARCH = "research"
    STUDENT = "student"


ALL_ROLES: frozenset[Role] = frozenset(Role)


def normalize_role(value: str | Role) -> Role | None:
    """Return a ``Role`` for a stored/config string, or ``None`` if unknown."""
    if isinstance(value, Role):
        return value
    code = str(value or "").strip().lower()
    if not code:
        return None
    try:
        return Role(code)
    except ValueError:
        return None
