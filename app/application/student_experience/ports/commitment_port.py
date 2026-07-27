"""Ports for Recommendation Commitment persistence + preference-journal writes.

EP-008.3A: Student Experience never imports SQLAlchemy models, learning
feedback infrastructure, or RecommendationService directly — infrastructure
composition binds concrete adapters via the process-local registry below.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Protocol, runtime_checkable


@dataclass
class CommitmentRecord:
    """Mutable mirror of one ``RecommendationCommitment`` persistence row.

    Application code never touches the ORM directly — CommitmentPersistencePort
    adapters translate to/from this shape.
    """

    user_id: int
    recommendation_key: str
    title: str = ""
    state: str = ""
    id: int | None = None
    deferred_reason_code: str = ""
    deferred_reason_note: str = ""
    expected_benefit: str = ""
    review_point: str = ""
    suggested_next_action: str = ""
    session_id: str = ""
    decision_id: int | None = None
    committed_at: datetime | None = None
    deferred_at: datetime | None = None
    session_started_at: datetime | None = None
    completed_at: datetime | None = None
    reflected_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@runtime_checkable
class CommitmentPersistencePort(Protocol):
    """Structural contract for Recommendation Commitment persistence."""

    def find_active(
        self, user_id: int, recommendation_key: str
    ) -> CommitmentRecord | None:
        """Most recent commitment for ``user_id`` + ``recommendation_key``."""

    def find_by_session(
        self, user_id: int, session_id: str
    ) -> CommitmentRecord | None:
        """Most recent commitment for ``user_id`` + ``session_id``."""

    def find_latest_open(self, user_id: int) -> CommitmentRecord | None:
        """Most recent committed / in-session commitment for ``user_id``."""

    def find_latest_completed(self, user_id: int) -> CommitmentRecord | None:
        """Most recent completed (not yet reflected) commitment for ``user_id``."""

    def find_recent(
        self,
        user_id: int,
        *,
        since: datetime,
        states: tuple[str, ...],
        limit: int,
    ) -> tuple[CommitmentRecord, ...]:
        """Recent commitments in ``states`` since ``since``, newest first."""

    def save(self, record: CommitmentRecord) -> CommitmentRecord:
        """Insert (``record.id is None``) or update; return the persisted row."""


@runtime_checkable
class DecisionJournalPort(Protocol):
    """Structural contract for the existing Decision Journal API."""

    def record_decision(
        self,
        user_id: int,
        tip: dict[str, Any],
        *,
        accepted: bool,
        completed: bool,
        outcome_summary: str | None = None,
    ) -> int | None:
        """Record a preference-journal decision; return its identifier."""


@runtime_checkable
class LearningFeedbackPort(Protocol):
    """Structural contract for observational learning-feedback emission."""

    def emit(
        self,
        *,
        student_id: int,
        event_type: str,
        source_authority: str,
        claim_boundary: str,
        payload: dict[str, Any],
    ) -> None:
        """Emit one observational feedback event (fail-open)."""


# Process-local ports (bound by infrastructure composition / tests).
_commitment_persistence: CommitmentPersistencePort | None = None
_decision_journal: DecisionJournalPort | None = None
_learning_feedback: LearningFeedbackPort | None = None


def bind_commitment_persistence_port(
    port: CommitmentPersistencePort | None,
) -> None:
    """Bind the process-local CommitmentPersistencePort."""
    global _commitment_persistence
    _commitment_persistence = port


def get_commitment_persistence_port() -> CommitmentPersistencePort | None:
    """Return the bound CommitmentPersistencePort, or None."""
    return _commitment_persistence


def bind_decision_journal_port(port: DecisionJournalPort | None) -> None:
    """Bind the process-local DecisionJournalPort."""
    global _decision_journal
    _decision_journal = port


def get_decision_journal_port() -> DecisionJournalPort | None:
    """Return the bound DecisionJournalPort, or None."""
    return _decision_journal


def bind_learning_feedback_port(port: LearningFeedbackPort | None) -> None:
    """Bind the process-local LearningFeedbackPort."""
    global _learning_feedback
    _learning_feedback = port


def get_learning_feedback_port() -> LearningFeedbackPort | None:
    """Return the bound LearningFeedbackPort, or None."""
    return _learning_feedback
