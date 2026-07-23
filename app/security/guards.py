"""Flask route guards for RBAC and portal capabilities (PR-001)."""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from flask import abort
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


def permission_required(
    *permissions: str | Permission,
    require_all: bool = True,
) -> Callable[[F], F]:
    """Require authentication and one/all of the given permissions."""

    def decorator(view: F) -> F:
        @wraps(view)
        @login_required
        def wrapped(*args: Any, **kwargs: Any):
            if require_all:
                allowed = all(
                    user_has_permission(current_user, permission)
                    for permission in permissions
                )
            else:
                allowed = any(
                    user_has_permission(current_user, permission)
                    for permission in permissions
                )
            if not allowed:
                abort(403)
            return view(*args, **kwargs)

        return wrapped  # type: ignore[return-value]

    return decorator


def role_required(*roles: str | Role, require_all: bool = False) -> Callable[[F], F]:
    """Require authentication and one/all of the given roles."""

    def decorator(view: F) -> F:
        @wraps(view)
        @login_required
        def wrapped(*args: Any, **kwargs: Any):
            if require_all:
                allowed = all(user_has_role(current_user, role) for role in roles)
            else:
                allowed = any(user_has_role(current_user, role) for role in roles)
            if not allowed:
                abort(403)
            return view(*args, **kwargs)

        return wrapped  # type: ignore[return-value]

    return decorator


def capability_required(
    *capabilities: str | Capability,
    require_all: bool = True,
) -> Callable[[F], F]:
    """Require authentication and one/all of the given portal capabilities."""

    def decorator(view: F) -> F:
        @wraps(view)
        @login_required
        def wrapped(*args: Any, **kwargs: Any):
            if require_all:
                allowed = all(
                    user_has_capability(current_user, capability)
                    for capability in capabilities
                )
            else:
                allowed = any(
                    user_has_capability(current_user, capability)
                    for capability in capabilities
                )
            if not allowed:
                abort(403)
            return view(*args, **kwargs)

        return wrapped  # type: ignore[return-value]

    return decorator
