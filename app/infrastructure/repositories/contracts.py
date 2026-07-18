"""Repository contracts — persistence boundaries without business rules."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Repository(ABC):
    """Base repository contract."""

    @property
    @abstractmethod
    def repository_id(self) -> str:
        """Stable repository identity."""

    @abstractmethod
    def is_available(self) -> bool:
        """True when the repository can accept work."""


class SnapshotRepository(Repository):
    """Contract for aggregate snapshot persistence."""

    @abstractmethod
    def save_snapshot(
        self,
        aggregate_name: str,
        aggregate_id: str,
        payload: dict[str, Any],
        *,
        schema_version: int = 1,
        correlation_id: str = "",
    ) -> dict[str, Any]:
        """Persist a snapshot; return opaque acknowledgement."""

    @abstractmethod
    def load_latest(
        self, aggregate_name: str, aggregate_id: str
    ) -> dict[str, Any] | None:
        """Load the latest snapshot payload envelope, or None."""


class EvidenceRepository(Repository):
    """Contract for append-only evidence persistence."""

    @abstractmethod
    def append_evidence(
        self,
        *,
        learner_id: str,
        subject_id: str,
        evidence_type: str,
        payload: dict[str, Any] | None = None,
        correlation_id: str = "",
        causation_id: str = "",
    ) -> dict[str, Any]:
        """Append evidence; return opaque acknowledgement."""

    @abstractmethod
    def list_evidence(
        self, learner_id: str, *, subject_id: str | None = None
    ) -> tuple[dict[str, Any], ...]:
        """List evidence records as opaque dicts."""


class AggregateRepository(Repository):
    """Generic key-value aggregate document repository."""

    @abstractmethod
    def get(self, aggregate_id: str) -> dict[str, Any] | None:
        """Load an aggregate document, or None."""

    @abstractmethod
    def save(
        self,
        aggregate_id: str,
        document: dict[str, Any],
        *,
        expected_version: int | None = None,
    ) -> dict[str, Any]:
        """Save an aggregate document; return opaque ack with version."""

    @abstractmethod
    def delete(self, aggregate_id: str) -> bool:
        """Delete an aggregate document. Returns True when removed."""

    @abstractmethod
    def list_ids(self) -> tuple[str, ...]:
        """List known aggregate ids."""
