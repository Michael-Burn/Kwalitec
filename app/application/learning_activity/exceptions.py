"""Application-layer exceptions for the Learning Activity Engine.

Framework-independent. Raised when sequencing, transition, progression,
completion, evidence, or reflection rules are violated.
"""

from __future__ import annotations


class LearningActivityEngineError(Exception):
    """Base exception for Learning Activity Engine failures."""


class ActivityNotFound(LearningActivityEngineError):  # noqa: N818
    """No Learning Activity exists for the requested identity."""


class InvalidActivityState(LearningActivityEngineError):  # noqa: N818
    """Operation is unlawful for the activity's current lifecycle state."""


class ActivityAlreadyCompleted(LearningActivityEngineError):  # noqa: N818
    """Activity has already reached a completed educational outcome."""


class ActivityAlreadySkipped(LearningActivityEngineError):  # noqa: N818
    """Activity has already been skipped."""


class SequenceIntegrityError(LearningActivityEngineError):  # noqa: N818
    """Activity sequence violates structural integrity invariants."""


class PlanningError(LearningActivityEngineError):  # noqa: N818
    """Activity plan could not be constructed from the supplied inputs."""


class TransitionError(LearningActivityEngineError):  # noqa: N818
    """Requested activity transition is not lawful."""


class ValidationError(LearningActivityEngineError):  # noqa: N818
    """Activity engine validation failed."""


class EvidenceRoutingError(LearningActivityEngineError):  # noqa: N818
    """Evidence could not be routed to the requested activity."""


class ReflectionRoutingError(LearningActivityEngineError):  # noqa: N818
    """Reflection could not be associated with the requested activity."""


class CompletionEvaluationError(LearningActivityEngineError):  # noqa: N818
    """Activity / sequence completion could not be evaluated."""
