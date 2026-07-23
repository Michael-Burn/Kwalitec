"""Account portal capabilities — one identity, multiple portals (PR-001).

Capabilities gate *which product surfaces* an account may enter.
Permissions gate *what* they may do inside those surfaces.
"""

from __future__ import annotations

from enum import StrEnum

from app.security.roles import Role


class Capability(StrEnum):
    """Portal / surface capabilities attached to an account."""

    STUDENT_PORTAL = "student_portal"
    CONSOLE = "console"
    ORGANIZATION_PORTAL = "organization_portal"  # reserved — future
    API = "api"  # reserved — future


ROLE_DEFAULT_CAPABILITIES: dict[Role, frozenset[Capability]] = {
    Role.FOUNDER: frozenset(
        {Capability.STUDENT_PORTAL, Capability.CONSOLE, Capability.API}
    ),
    Role.ADMINISTRATOR: frozenset(
        {Capability.STUDENT_PORTAL, Capability.CONSOLE}
    ),
    Role.CONTENT_MANAGER: frozenset(
        {Capability.STUDENT_PORTAL, Capability.CONSOLE}
    ),
    Role.SUPPORT: frozenset({Capability.STUDENT_PORTAL, Capability.CONSOLE}),
    Role.RESEARCH: frozenset({Capability.STUDENT_PORTAL, Capability.CONSOLE}),
    Role.STUDENT: frozenset({Capability.STUDENT_PORTAL}),
}


def normalize_capability(value: str | Capability) -> Capability | None:
    """Return a ``Capability`` for a stored string, or ``None`` if unknown."""
    if isinstance(value, Capability):
        return value
    code = str(value or "").strip().lower()
    if not code:
        return None
    try:
        return Capability(code)
    except ValueError:
        return None


def default_capabilities_for_roles(
    roles: frozenset[Role] | set[Role],
) -> frozenset[Capability]:
    """Union default portal capabilities for the given roles."""
    caps: set[Capability] = set()
    for role in roles:
        caps.update(ROLE_DEFAULT_CAPABILITIES.get(role, frozenset()))
    return frozenset(caps)
