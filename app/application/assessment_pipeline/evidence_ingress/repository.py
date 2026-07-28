"""Submission registry for evidence ingress duplicate protection.

No database schema changes — port + in-memory adapter for AP-002D1.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True, slots=True)
class EvidenceSubmissionRecord:
    """Record of an accepted evidence bundle at the ingress boundary."""

    bundle_id: str
    twin_id: str
    session_id: str
    correlation_id: str
    reasoning_request_id: str
    accepted_at: datetime


class EvidenceSubmissionRepository(ABC):
    """Tracks accepted evidence bundle identifiers for duplicate protection."""

    @abstractmethod
    def get(self, bundle_id: str) -> EvidenceSubmissionRecord | None:
        """Return prior acceptance record, or None."""

    @abstractmethod
    def save(self, record: EvidenceSubmissionRecord) -> None:
        """Persist an acceptance record (insert)."""

    @abstractmethod
    def exists(self, bundle_id: str) -> bool:
        """True when bundle_id was already accepted."""


class InMemoryEvidenceSubmissionRepository(EvidenceSubmissionRepository):
    """Process-local submission registry (tests + bootstrap wiring)."""

    def __init__(self) -> None:
        self._records: dict[str, EvidenceSubmissionRecord] = {}

    def get(self, bundle_id: str) -> EvidenceSubmissionRecord | None:
        return self._records.get(bundle_id)

    def save(self, record: EvidenceSubmissionRecord) -> None:
        self._records[record.bundle_id] = record

    def exists(self, bundle_id: str) -> bool:
        return bundle_id in self._records


def utc_now_naive() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)
