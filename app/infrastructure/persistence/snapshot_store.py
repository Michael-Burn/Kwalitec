"""Snapshot persistence — durable projected state without business rules."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class SnapshotRecord:
    """Immutable stored snapshot envelope."""

    snapshot_id: str
    aggregate_name: str
    aggregate_id: str
    schema_version: int
    payload: dict[str, Any]
    created_at: datetime
    correlation_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class SnapshotStore:
    """Append-oriented snapshot store (in-memory foundation).

    Never interprets educational meaning. Repositories decide when to snapshot.
    """

    def __init__(self) -> None:
        self._by_id: dict[str, SnapshotRecord] = {}
        self._by_aggregate: dict[tuple[str, str], list[str]] = {}

    def save(
        self,
        aggregate_name: str,
        aggregate_id: str,
        payload: dict[str, Any],
        *,
        schema_version: int = 1,
        snapshot_id: str | None = None,
        correlation_id: str = "",
        metadata: dict[str, Any] | None = None,
        created_at: datetime | None = None,
    ) -> SnapshotRecord:
        """Persist a snapshot payload."""
        sid = (snapshot_id or "").strip() or uuid4().hex
        if sid in self._by_id:
            raise ValueError(f"duplicate snapshot_id: {sid}")
        when = created_at if created_at is not None else datetime.now(tz=UTC)
        if when.tzinfo is None:
            when = when.replace(tzinfo=UTC)
        record = SnapshotRecord(
            snapshot_id=sid,
            aggregate_name=aggregate_name,
            aggregate_id=aggregate_id,
            schema_version=int(schema_version),
            payload=dict(payload),
            created_at=when,
            correlation_id=(correlation_id or "").strip(),
            metadata=dict(metadata or {}),
        )
        self._by_id[sid] = record
        key = (aggregate_name, aggregate_id)
        self._by_aggregate.setdefault(key, []).append(sid)
        return record

    def get(self, snapshot_id: str) -> SnapshotRecord | None:
        """Load a snapshot by id."""
        return self._by_id.get(snapshot_id)

    def list_for(
        self, aggregate_name: str, aggregate_id: str
    ) -> tuple[SnapshotRecord, ...]:
        """List snapshots for an aggregate in write order."""
        ids = self._by_aggregate.get((aggregate_name, aggregate_id), ())
        return tuple(self._by_id[i] for i in ids if i in self._by_id)

    def latest(
        self, aggregate_name: str, aggregate_id: str
    ) -> SnapshotRecord | None:
        """Return the latest snapshot for an aggregate, if any."""
        items = self.list_for(aggregate_name, aggregate_id)
        return items[-1] if items else None

    def count(self) -> int:
        """Total stored snapshots."""
        return len(self._by_id)
