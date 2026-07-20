"""Application-layer exceptions for Learning Session Experience.

Framework-independent. Raised when projection, navigation, or port
collaboration fails — never for educational calculation errors owned
by upstream bounded contexts.
"""

from __future__ import annotations


class SessionExperienceError(Exception):
    """Base exception for Learning Session Experience failures."""


class WorkspaceNotFound(SessionExperienceError):  # noqa: N818
    """No session workspace exists for the requested identity."""


class SessionNotFound(SessionExperienceError):  # noqa: N818
    """No Learning Session experience handle exists for the identity."""


class SessionOwnershipError(SessionExperienceError):  # noqa: N818
    """Authenticated student does not own the requested session."""


class PortUnavailable(SessionExperienceError):  # noqa: N818
    """An injected Session Experience port is unavailable."""


class ProjectionError(SessionExperienceError):  # noqa: N818
    """A session experience projection could not be produced."""


class PolicyViolation(SessionExperienceError):  # noqa: N818
    """A Session Experience policy rejected the operation."""


class NavigationError(SessionExperienceError):  # noqa: N818
    """Session surface navigation failed (branching / skip)."""


class OverviewError(SessionExperienceError):  # noqa: N818
    """Session overview projection could not be produced."""


class ActivityError(SessionExperienceError):  # noqa: N818
    """Activity projection or response workflow failed."""


class ProgressError(SessionExperienceError):  # noqa: N818
    """Progress projection could not be produced."""


class ReflectionError(SessionExperienceError):  # noqa: N818
    """Reflection projection could not be produced."""


class CompletionError(SessionExperienceError):  # noqa: N818
    """Completion / summary projection could not be produced."""
