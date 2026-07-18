"""Application-layer exceptions for the Learning Journey Engine.

Framework-independent. Raised by engine orchestration when domain
invariants or educational progression rules are violated.
"""

from __future__ import annotations


class LearningJourneyEngineError(Exception):
    """Base exception for Learning Journey Engine failures."""


class JourneyNotFound(LearningJourneyEngineError):  # noqa: N818
    """No Learning Journey exists for the requested identity."""


class InvalidJourneyState(LearningJourneyEngineError):  # noqa: N818
    """Operation is unlawful for the journey's current lifecycle state."""


class InvalidProgression(LearningJourneyEngineError):  # noqa: N818
    """Requested progression violates educational progression rules."""


class JourneyAlreadyCompleted(LearningJourneyEngineError):  # noqa: N818
    """Journey has already reached a completed (Topic Complete) outcome."""


class SessionOrderingViolation(LearningJourneyEngineError):  # noqa: N818
    """Session sequence ordering is inconsistent or out of educational order."""
