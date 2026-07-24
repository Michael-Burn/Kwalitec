"""Outbox contracts and in-memory sink (approved write path).

Phase A: enqueue only. Durable SQL outbox persistence is available via the
repository adapter; the dispatcher never writes educational tables.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Protocol
from uuid import uuid4

from app.infrastructure.analytics.contracts import AnalyticsEvent
from app.infrastructure.analytics.serialization import AnalyticsEventSerializer


@dataclass(frozen=True)
class OutboxRecord:
    """One pending analytics outbox row."""

    outbox_id: str
    event_id: str
    event_type: str
    user_id: int
    idempotency_key: str
    payload_json: str
    created_at: datetime
    attempts: int = 0
    status: str = "pending"  # pending | processed | failed


class AnalyticsOutboxPort(Protocol):
    """Port for enqueueing analytics events (approved write contract)."""

    name: str

    def enqueue(self, event: AnalyticsEvent, *, payload_json: str) -> OutboxRecord:
        """Enqueue a validated serialized event. Idempotent on key."""
        ...

    def pending(self) -> tuple[OutboxRecord, ...]:
        """Return pending outbox records in enqueue order."""
        ...


@dataclass
class MemoryOutboxSink:
    """In-process outbox for unit tests and flag-on dry runs without DB."""

    name: str = "memory_outbox"
    _records: list[OutboxRecord] = field(default_factory=list)
    _keys: set[tuple[int, str, str]] = field(default_factory=set)

    def enqueue(self, event: AnalyticsEvent, *, payload_json: str) -> OutboxRecord:
        key = (event.user_id, event.event_type, event.idempotency_key)
        if key in self._keys:
            # Idempotent no-op: return the existing record.
            for existing in self._records:
                if (
                    existing.user_id == event.user_id
                    and existing.event_type == event.event_type
                    and existing.idempotency_key == event.idempotency_key
                ):
                    return existing
        record = OutboxRecord(
            outbox_id=uuid4().hex,
            event_id=event.event_id,
            event_type=event.event_type,
            user_id=event.user_id,
            idempotency_key=event.idempotency_key,
            payload_json=payload_json,
            created_at=datetime.now(tz=UTC),
        )
        self._records.append(record)
        self._keys.add(key)
        return record

    def pending(self) -> tuple[OutboxRecord, ...]:
        return tuple(r for r in self._records if r.status == "pending")


@dataclass
class NullOutboxSink:
    """No-op sink used when the feature flag is off."""

    name: str = "null"

    def enqueue(self, event: AnalyticsEvent, *, payload_json: str) -> OutboxRecord:
        return OutboxRecord(
            outbox_id="",
            event_id=event.event_id,
            event_type=event.event_type,
            user_id=event.user_id,
            idempotency_key=event.idempotency_key,
            payload_json=payload_json,
            created_at=datetime.now(tz=UTC),
            status="skipped",
        )

    def pending(self) -> tuple[OutboxRecord, ...]:
        return ()


def serialize_for_outbox(
    event: AnalyticsEvent,
    serializer: AnalyticsEventSerializer | None = None,
) -> str:
    """Serialize an event for outbox storage."""
    ser = serializer or AnalyticsEventSerializer()
    return ser.to_json(event)
