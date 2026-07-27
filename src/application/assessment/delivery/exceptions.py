"""Application-layer delivery errors (not educational validation)."""

from __future__ import annotations


class AssessmentDeliveryError(Exception):
    """Base error for assessment delivery orchestration failures."""


class SessionNotFoundError(AssessmentDeliveryError):
    """Raised when a session id cannot be resolved."""


class SessionOwnershipError(AssessmentDeliveryError):
    """Raised when a student attempts to access another learner's session."""


class SessionStateError(AssessmentDeliveryError):
    """Raised when an action is unlawful for the current session status."""


class QuestionUnavailableError(AssessmentDeliveryError):
    """Raised when a question is not part of the session or catalogue."""


class InvalidResponseFormatError(AssessmentDeliveryError):
    """Raised when a response payload fails format validation."""


class DuplicateSubmissionError(AssessmentDeliveryError):
    """Raised when a response would unlawfully duplicate a committed attempt."""


class ExpiredSessionError(AssessmentDeliveryError):
    """Raised when the session time budget has elapsed."""
