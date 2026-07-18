"""Application-layer exceptions for Student Experience.

Framework-independent. Raised when projection, navigation, or port
collaboration fails — never for educational calculation errors owned
by upstream bounded contexts.
"""

from __future__ import annotations


class StudentExperienceError(Exception):
    """Base exception for Student Experience failures."""


class WorkspaceNotFound(StudentExperienceError):  # noqa: N818
    """No experience workspace exists for the requested identity."""


class SessionNotFound(StudentExperienceError):  # noqa: N818
    """No experience session handle exists for the requested identity."""


class PortUnavailable(StudentExperienceError):  # noqa: N818
    """An injected Student Experience port is unavailable."""


class ProjectionError(StudentExperienceError):  # noqa: N818
    """A student experience projection could not be produced."""


class ExplanationError(StudentExperienceError):  # noqa: N818
    """A student-safe explanation could not be produced."""


class PolicyViolation(StudentExperienceError):  # noqa: N818
    """A Student Experience policy rejected the operation."""


class NavigationError(StudentExperienceError):  # noqa: N818
    """Experience surface navigation failed."""


class ProfileError(StudentExperienceError):  # noqa: N818
    """Profile projection could not be produced."""


class HistoryError(StudentExperienceError):  # noqa: N818
    """History projection could not be produced."""


class JourneyError(StudentExperienceError):  # noqa: N818
    """Journey projection could not be produced."""


class RevisionError(StudentExperienceError):  # noqa: N818
    """Revision projection could not be produced."""


class HomeError(StudentExperienceError):  # noqa: N818
    """Home projection could not be produced."""
