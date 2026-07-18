"""Evidence persistence — append-only evidence records.

No scoring. No Twin algorithms. Store + retrieve only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class EvidenceRecord:
    """Append-only evidence persistence record."""

    record_id: str
    learner_id: str
    subject_id: str
    evidence_type: str
    payload: dict[str, Any]
    recorded_at: datetime
    correlation_id: str = ""
    causation_id: str = ""
    source: str = "infrastructure"
    metadata: dict[str, Any] = field(default_factory=dict)


class EvidenceStore:
    """Append-only evidence store (in-memory foundation)."""

    def __init__(self) -> None:
        self._records: dict[str, EvidenceRecord] = {}
        self._by_learner: dict[str, list[str]] = {}

    def append(
        self,
        *,
        learner_id: str,
        subject_id: str,
        evidence_type: str,
        payload: dict[str, Any] | None = None,
        record_id: str | None = None,
        recorded_at: datetime | None = None,
        correlation_id: str = "",
        causation_id: str = "",
        source: str = "infrastructure",
        metadata: dict[str, Any] | None = None,
    ) -> EvidenceRecord:
        """Append an evidence record. Duplicate ids raise ValueError."""
        lid = (learner_id or "").strip()
        sid = (subject_id or "").strip()
        etype = (evidence_type or "").strip()
        if not lid or not sid or not etype:
            raise ValueError("learner_id, subject_id, evidence_type required")
        rid = (record_id or "").strip() or uuid4().hex
        if rid in self._records:
            raise ValueError(f"duplicate evidence record_id: {rid}")
        when = recorded_at if recorded_at is not None else datetime.now(tz=UTC)
        if when.tzinfo is None:
            when = when.replace(tzinfo=UTC)
        record = EvidenceRecord(
            record_id=rid,
            learner_id=lid,
            subject_id=sid,
            evidence_type=etype,
            payload=dict(payload or {}),
            recorded_at=when,
            correlation_id=(correlation_id or "").strip(),
            causation_id=(causation_id or "").strip(),
            source=(source or "").strip() or "infrastructure",
            metadata=dict(metadata or {}),
        )
        self._records[rid] = record
        self._by_learner.setdefault(lid, []).append(rid)
        return record

    def get(self, record_id: str) -> EvidenceRecord | None:
        """Load one evidence record."""
        return self._records.get(record_id)

    def list_for_learner(
        self, learner_id: str, *, subject_id: str | None = None
    ) -> tuple[EvidenceRecord, ...]:
        """List evidence for a learner (optionally subject-scoped)."""
        ids = self._by_learner.get(learner_id, ())
        records = [self._records[i] for i in ids if i in self._records]
        if subject_id is not None:
            records = [r for r in records if r.subject_id == subject_id]
        return tuple(records)

    def count(self) -> int:
        """Total evidence records."""
        return len(self._records)
