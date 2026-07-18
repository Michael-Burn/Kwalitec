"""Application-layer exceptions for the Student Digital Twin.

Framework-independent. Raised when Twin evidence or policy rules are violated.
"""

from __future__ import annotations


class StudentTwinError(Exception):
    """Base exception for Student Digital Twin failures."""


class TwinNotFound(StudentTwinError):  # noqa: N818
    """No Twin exists for the requested identity."""


class LearnerNotFound(StudentTwinError):  # noqa: N818
    """No learner exists for the requested identity."""


class EvidenceRejected(StudentTwinError):  # noqa: N818
    """Evidence event failed policy validation."""


class DuplicateEvidence(StudentTwinError):  # noqa: N818
    """Evidence event id already exists in Twin history."""


class IllegalState(StudentTwinError):  # noqa: N818
    """Operation is not lawful for the current Twin state."""


class PolicyViolation(StudentTwinError):  # noqa: N818
    """A Twin policy rejected the operation."""


class SnapshotError(StudentTwinError):  # noqa: N818
    """Snapshot could not be produced."""


class ExplanationError(StudentTwinError):  # noqa: N818
    """Explanation could not be produced."""


class ComparisonError(StudentTwinError):  # noqa: N818
    """Twin comparison could not be produced."""
