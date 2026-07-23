"""Permission codes and role → permission matrix (PR-001)."""

from __future__ import annotations

from enum import StrEnum

from app.security.roles import Role


class Permission(StrEnum):
    """Fine-grained permissions checked by guards and services."""

    # Portal / surface access
    STUDENT_PORTAL = "student.portal"
    CONSOLE_ACCESS = "console.access"

    # Console domains
    CONSOLE_OPS = "console.ops"
    CONSOLE_SETTINGS = "console.settings"
    CONSOLE_HEALTH = "console.health"
    CONSOLE_SEARCH = "console.search"

    # Content
    CURRICULUM_MANAGE = "curriculum.manage"
    CONTENT_EDIT = "content.edit"

    # Support / feedback
    SUPPORT_VIEW = "support.view"
    FEEDBACK_VIEW = "feedback.view"
    FEEDBACK_MANAGE = "feedback.manage"

    # Research
    RESEARCH_VIEW = "research.view"
    RESEARCH_MANAGE = "research.manage"

    # Identity / admin
    USERS_MANAGE = "users.manage"
    ROLES_MANAGE = "roles.manage"

    # Future surfaces (capability-gated; permission reserved)
    ORGANIZATION_PORTAL = "organization.portal"
    API_ACCESS = "api.access"


# Founder inherits every permission.
_ALL_PERMISSIONS: frozenset[Permission] = frozenset(Permission)

ROLE_PERMISSIONS: dict[Role, frozenset[Permission]] = {
    Role.FOUNDER: _ALL_PERMISSIONS,
    Role.ADMINISTRATOR: frozenset(
        {
            Permission.STUDENT_PORTAL,
            Permission.CONSOLE_ACCESS,
            Permission.CONSOLE_OPS,
            Permission.CONSOLE_SETTINGS,
            Permission.CONSOLE_HEALTH,
            Permission.CONSOLE_SEARCH,
            Permission.CURRICULUM_MANAGE,
            Permission.CONTENT_EDIT,
            Permission.SUPPORT_VIEW,
            Permission.FEEDBACK_VIEW,
            Permission.FEEDBACK_MANAGE,
            Permission.RESEARCH_VIEW,
            Permission.USERS_MANAGE,
            Permission.ROLES_MANAGE,
        }
    ),
    Role.CONTENT_MANAGER: frozenset(
        {
            Permission.STUDENT_PORTAL,
            Permission.CONSOLE_ACCESS,
            Permission.CONSOLE_SEARCH,
            Permission.CURRICULUM_MANAGE,
            Permission.CONTENT_EDIT,
        }
    ),
    Role.SUPPORT: frozenset(
        {
            Permission.STUDENT_PORTAL,
            Permission.CONSOLE_ACCESS,
            Permission.CONSOLE_SEARCH,
            Permission.SUPPORT_VIEW,
            Permission.FEEDBACK_VIEW,
            Permission.FEEDBACK_MANAGE,
        }
    ),
    Role.RESEARCH: frozenset(
        {
            Permission.STUDENT_PORTAL,
            Permission.CONSOLE_ACCESS,
            Permission.CONSOLE_SEARCH,
            Permission.RESEARCH_VIEW,
            Permission.RESEARCH_MANAGE,
            Permission.FEEDBACK_VIEW,
        }
    ),
    Role.STUDENT: frozenset(
        {
            Permission.STUDENT_PORTAL,
        }
    ),
}


def permissions_for_roles(roles: frozenset[Role] | set[Role]) -> frozenset[Permission]:
    """Union permissions granted by the given roles."""
    granted: set[Permission] = set()
    for role in roles:
        granted.update(ROLE_PERMISSIONS.get(role, frozenset()))
    return frozenset(granted)


def normalize_permission(value: str | Permission) -> Permission | None:
    """Return a ``Permission`` for a string code, or ``None`` if unknown."""
    if isinstance(value, Permission):
        return value
    code = str(value or "").strip().lower()
    if not code:
        return None
    try:
        return Permission(code)
    except ValueError:
        return None
