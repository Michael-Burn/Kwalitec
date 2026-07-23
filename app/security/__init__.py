"""Identity, RBAC, and authorization primitives (PR-001).

Templates must not contain authorization logic — use injected helpers
(``can``, ``has_role``, ``has_capability``) that delegate here.
"""

from app.security.authorization import (
    AuthorizationError,
    assert_permission,
    assert_resource_owner,
    user_capabilities,
    user_has_capability,
    user_has_permission,
    user_has_role,
    user_permissions,
    user_roles,
)
from app.security.capabilities import ROLE_DEFAULT_CAPABILITIES, Capability
from app.security.guards import capability_required, permission_required, role_required
from app.security.permissions import ROLE_PERMISSIONS, Permission
from app.security.roles import Role

__all__ = [
    "AuthorizationError",
    "Capability",
    "Permission",
    "ROLE_DEFAULT_CAPABILITIES",
    "ROLE_PERMISSIONS",
    "Role",
    "assert_permission",
    "assert_resource_owner",
    "capability_required",
    "permission_required",
    "role_required",
    "user_capabilities",
    "user_has_capability",
    "user_has_permission",
    "user_has_role",
    "user_permissions",
    "user_roles",
]
