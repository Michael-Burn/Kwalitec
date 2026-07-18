"""Application-layer exceptions for the Learning Session Runtime.

Framework-independent. Raised when lifecycle, planning, evidence,
reflection, or completion rules are violated.
"""

from __future__ import annotations


class LearningSessionRuntimeError(Exception):
    """Base exception for Learning Session Runtime failures."""


class SessionNotFound(LearningSessionRuntimeError):  # noqa: N818
    """No Learning Session exists for the requested identity."""


class InvalidSessionState(LearningSessionRuntimeError):  # noqa: N818
    """Operation is unlawful for the session's current lifecycle phase."""


class SessionAlreadyCompleted(LearningSessionRuntimeError):  # noqa: N818
    """Session has already reached a completed educational outcome."""


class SessionAlreadyArchived(LearningSessionRuntimeError):  # noqa: N818
    """Session has been archived and no longer accepts educational work."""


class ReflectionRequired(LearningSessionRuntimeError):  # noqa: N818
    """Reflection is owed before the requested educational step may proceed."""


class EvidenceCollectionError(LearningSessionRuntimeError):  # noqa: N818
    """Evidence could not be attributed to the session under current rules."""


class PlanningError(LearningSessionRuntimeError):  # noqa: N818
    """Session plan could not be constructed from the supplied inputs."""


class CompletionEvaluationError(LearningSessionRuntimeError):  # noqa: N818
    """Session completion could not be evaluated under current rules."""
