"""Service-layer authorization helpers (PR-001).

Routes and services call these with an explicit user. Templates must not
embed authorization branches beyond calling injected helpers.
"""

from __future__ import annotations

from typing import Any

from app.security.capabilities import Capability, normalize_capability
from app.security.permissions import (
    Permission,
    normalize_permission,
    permissions_for_roles,
)
from app.security.roles import Role, normalize_role


class AuthorizationError(PermissionError):
    """Raised when a service refuses an unauthorized operation."""


def user_roles(user: Any | None) -> frozenset[Role]:
    """Return roles assigned to ``user`` (empty when anonymous/unset)."""
    if user is None or not getattr(user, "is_authenticated", False):
        return frozenset()
    getter = getattr(user, "get_roles", None)
    if callable(getter):
        return frozenset(r for r in getter() if isinstance(r, Role))
    raw = getattr(user, "roles", None) or ()
    roles: set[Role] = set()
    for item in raw:
        role = normalize_role(getattr(item, "role", item))
        if role is not None:
            roles.add(role)
    return frozenset(roles)


def user_capabilities(user: Any | None) -> frozenset[Capability]:
    """Return portal capabilities assigned to ``user``."""
    if user is None or not getattr(user, "is_authenticated", False):
        return frozenset()
    getter = getattr(user, "get_capabilities", None)
    if callable(getter):
        return frozenset(c for c in getter() if isinstance(c, Capability))
    raw = getattr(user, "capabilities", None) or ()
    caps: set[Capability] = set()
    for item in raw:
        cap = normalize_capability(getattr(item, "capability", item))
        if cap is not None:
            caps.add(cap)
    return frozenset(caps)


def user_permissions(user: Any | None) -> frozenset[Permission]:
    """Return the effective permission set for ``user``."""
    return permissions_for_roles(user_roles(user))


def user_has_role(user: Any | None, role: str | Role) -> bool:
    """Return whether ``user`` holds ``role``."""
    target = normalize_role(role)
    if target is None:
        return False
    return target in user_roles(user)


def user_has_permission(user: Any | None, permission: str | Permission) -> bool:
    """Return whether ``user`` is granted ``permission``."""
    target = normalize_permission(permission)
    if target is None:
        return False
    return target in user_permissions(user)


def user_has_capability(user: Any | None, capability: str | Capability) -> bool:
    """Return whether ``user`` holds portal ``capability``."""
    target = normalize_capability(capability)
    if target is None:
        return False
    return target in user_capabilities(user)


def assert_permission(
    user: Any | None,
    permission: str | Permission,
    *,
    message: str | None = None,
) -> None:
    """Raise ``AuthorizationError`` when ``user`` lacks ``permission``."""
    if not user_has_permission(user, permission):
        raise AuthorizationError(
            message
            or f"Missing permission: {normalize_permission(permission) or permission}"
        )


def assert_resource_owner(
    user: Any | None,
    resource_user_id: int | None,
    *,
    message: str = "Resource does not belong to the current user",
) -> None:
    """Raise ``AuthorizationError`` when ``user`` does not own the resource.

    Founders and administrators may bypass ownership for support workflows
    when they hold ``users.manage``.
    """
    if user is None or not getattr(user, "is_authenticated", False):
        raise AuthorizationError(message)
    if resource_user_id is None:
        raise AuthorizationError(message)
    if int(getattr(user, "id", -1)) == int(resource_user_id):
        return
    if user_has_permission(user, Permission.USERS_MANAGE):
        return
    raise AuthorizationError(message)
