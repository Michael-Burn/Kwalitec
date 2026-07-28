"""Exceptions for Learning Evidence Engine application services."""

from __future__ import annotations

from app.domain.learning_evidence.invariants import EvidenceInvariantError


class LearningEvidenceError(Exception):
    """Base error for learning evidence services."""


class InstanceNotFoundError(LearningEvidenceError):
    """Requested Student Curriculum Instance does not exist."""


class EvidenceNotFoundError(LearningEvidenceError):
    """Requested evidence event does not exist."""


class EvidenceGateError(LearningEvidenceError):
    """Evidence integrity invariant or gate failed."""

    def __init__(self, message: str, *, cause: Exception | None = None) -> None:
        super().__init__(message)
        self.cause = cause


def gate_from_invariant(exc: EvidenceInvariantError) -> EvidenceGateError:
    return EvidenceGateError(str(exc), cause=exc)
