"""Outbox contracts, memory sink, and durable port (EP-002).

Phase A shipped enqueue-only. EP-002 adds claim / retry / dead-letter /
cleanup on the durable port. The dispatcher never writes educational tables.
Feature flag ``ANALYTICS_EVENTS_V1`` remains OFF by default.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Protocol
from uuid import uuid4

from app.infrastructure.analytics.contracts import AnalyticsEvent
from app.infrastructure.analytics.serialization import AnalyticsEventSerializer
from app.infrastructure.analytics.status import (
    DEFAULT_MAX_ATTEMPTS,
    DEFAULT_PROCESSED_RETENTION_DAYS,
    OUTBOX_DEAD_LETTER,
    OUTBOX_FAILED,
    OUTBOX_PENDING,
    OUTBOX_PROCESSED,
    OUTBOX_PROCESSING,
    OUTBOX_SKIPPED,
)


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
    status: str = OUTBOX_PENDING
    last_error: str | None = None
    updated_at: datetime | None = None


class AnalyticsOutboxPort(Protocol):
    """Port for enqueueing analytics events (approved write contract)."""

    name: str

    def enqueue(self, event: AnalyticsEvent, *, payload_json: str) -> OutboxRecord:
        """Enqueue a validated serialized event. Idempotent on key."""
        ...

    def pending(self) -> tuple[OutboxRecord, ...]:
        """Return pending outbox records in enqueue order."""
        ...


class DurableOutboxPort(AnalyticsOutboxPort, Protocol):
    """Durable outbox with retry, dead-letter, replay, and cleanup."""

    def claim_batch(
        self,
        *,
        limit: int = 100,
        max_attempts: int = DEFAULT_MAX_ATTEMPTS,
    ) -> tuple[OutboxRecord, ...]:
        """Claim pending / retryable failed rows for processing."""
        ...

    def mark_processed(self, outbox_id: str) -> None:
        """Mark a claimed row as processed."""
        ...

    def mark_failed(self, outbox_id: str, *, error: str) -> None:
        """Increment attempts and mark failed (retryable if under max)."""
        ...

    def mark_dead_letter(self, outbox_id: str, *, error: str) -> None:
        """Move a row to dead-letter (no automatic retry)."""
        ...

    def requeue(
        self,
        outbox_id: str,
        *,
        reset_attempts: bool = False,
    ) -> bool:
        """Requeue a failed / dead-letter row to pending. Returns False if missing."""
        ...

    def count_by_status(self) -> dict[str, int]:
        """Return counts keyed by status."""
        ...

    def delete_processed(
        self,
        *,
        older_than: datetime | None = None,
        limit: int = 1000,
    ) -> int:
        """Delete processed rows older than cutoff; return deleted count."""
        ...

    def get(self, outbox_id: str) -> OutboxRecord | None:
        """Fetch one outbox row by id."""
        ...

    def list_dead_letters(self, *, limit: int = 100) -> tuple[OutboxRecord, ...]:
        """List dead-letter rows for replay tooling."""
        ...


@dataclass
class MemoryOutboxSink:
    """In-process durable outbox for unit tests and flag-on dry runs without DB."""

    name: str = "memory_outbox"
    _records: list[OutboxRecord] = field(default_factory=list)
    _keys: set[tuple[int, str, str]] = field(default_factory=set)

    def enqueue(self, event: AnalyticsEvent, *, payload_json: str) -> OutboxRecord:
        key = (event.user_id, event.event_type, event.idempotency_key)
        if key in self._keys:
            for existing in self._records:
                if (
                    existing.user_id == event.user_id
                    and existing.event_type == event.event_type
                    and existing.idempotency_key == event.idempotency_key
                ):
                    return existing
        now = datetime.now(tz=UTC)
        record = OutboxRecord(
            outbox_id=uuid4().hex,
            event_id=event.event_id,
            event_type=event.event_type,
            user_id=event.user_id,
            idempotency_key=event.idempotency_key,
            payload_json=payload_json,
            created_at=now,
            updated_at=now,
            status=OUTBOX_PENDING,
        )
        self._records.append(record)
        self._keys.add(key)
        return record

    def pending(self) -> tuple[OutboxRecord, ...]:
        return tuple(r for r in self._records if r.status == OUTBOX_PENDING)

    def claim_batch(
        self,
        *,
        limit: int = 100,
        max_attempts: int = DEFAULT_MAX_ATTEMPTS,
    ) -> tuple[OutboxRecord, ...]:
        claimed: list[OutboxRecord] = []
        for i, record in enumerate(self._records):
            if len(claimed) >= limit:
                break
            retryable = record.status == OUTBOX_PENDING or (
                record.status == OUTBOX_FAILED and record.attempts < max_attempts
            )
            if not retryable:
                continue
            updated = OutboxRecord(
                outbox_id=record.outbox_id,
                event_id=record.event_id,
                event_type=record.event_type,
                user_id=record.user_id,
                idempotency_key=record.idempotency_key,
                payload_json=record.payload_json,
                created_at=record.created_at,
                attempts=record.attempts,
                status=OUTBOX_PROCESSING,
                last_error=record.last_error,
                updated_at=datetime.now(tz=UTC),
            )
            self._records[i] = updated
            claimed.append(updated)
        return tuple(claimed)

    def mark_processed(self, outbox_id: str) -> None:
        self._update(
            outbox_id,
            status=OUTBOX_PROCESSED,
            attempts_delta=0,
            error=None,
        )

    def mark_failed(self, outbox_id: str, *, error: str) -> None:
        self._update(
            outbox_id,
            status=OUTBOX_FAILED,
            attempts_delta=1,
            error=error[:512],
        )

    def mark_dead_letter(self, outbox_id: str, *, error: str) -> None:
        self._update(
            outbox_id,
            status=OUTBOX_DEAD_LETTER,
            attempts_delta=1,
            error=error[:512],
        )

    def requeue(self, outbox_id: str, *, reset_attempts: bool = False) -> bool:
        for i, record in enumerate(self._records):
            if record.outbox_id != outbox_id:
                continue
            if record.status not in {
                OUTBOX_FAILED,
                OUTBOX_DEAD_LETTER,
                OUTBOX_PROCESSING,
            }:
                return False
            self._records[i] = OutboxRecord(
                outbox_id=record.outbox_id,
                event_id=record.event_id,
                event_type=record.event_type,
                user_id=record.user_id,
                idempotency_key=record.idempotency_key,
                payload_json=record.payload_json,
                created_at=record.created_at,
                attempts=0 if reset_attempts else record.attempts,
                status=OUTBOX_PENDING,
                last_error=None,
                updated_at=datetime.now(tz=UTC),
            )
            return True
        return False

    def count_by_status(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for record in self._records:
            counts[record.status] = counts.get(record.status, 0) + 1
        return counts

    def delete_processed(
        self,
        *,
        older_than: datetime | None = None,
        limit: int = 1000,
    ) -> int:
        cutoff = older_than
        if cutoff is None:
            cutoff = datetime.now(tz=UTC) - timedelta(
                days=DEFAULT_PROCESSED_RETENTION_DAYS
            )
        if cutoff.tzinfo is None:
            cutoff = cutoff.replace(tzinfo=UTC)
        keep: list[OutboxRecord] = []
        deleted = 0
        for record in self._records:
            updated = record.updated_at or record.created_at
            if updated.tzinfo is None:
                updated = updated.replace(tzinfo=UTC)
            if (
                deleted < limit
                and record.status == OUTBOX_PROCESSED
                and updated < cutoff
            ):
                deleted += 1
                self._keys.discard(
                    (record.user_id, record.event_type, record.idempotency_key)
                )
                continue
            keep.append(record)
        self._records = keep
        return deleted

    def get(self, outbox_id: str) -> OutboxRecord | None:
        for record in self._records:
            if record.outbox_id == outbox_id:
                return record
        return None

    def list_dead_letters(self, *, limit: int = 100) -> tuple[OutboxRecord, ...]:
        rows = [r for r in self._records if r.status == OUTBOX_DEAD_LETTER]
        return tuple(rows[:limit])

    def delete_for_user(self, user_id: int) -> int:
        keep: list[OutboxRecord] = []
        deleted = 0
        for record in self._records:
            if record.user_id == int(user_id):
                deleted += 1
                self._keys.discard(
                    (record.user_id, record.event_type, record.idempotency_key)
                )
                continue
            keep.append(record)
        self._records = keep
        return deleted

    def _update(
        self,
        outbox_id: str,
        *,
        status: str,
        attempts_delta: int,
        error: str | None,
    ) -> None:
        for i, record in enumerate(self._records):
            if record.outbox_id != outbox_id:
                continue
            self._records[i] = OutboxRecord(
                outbox_id=record.outbox_id,
                event_id=record.event_id,
                event_type=record.event_type,
                user_id=record.user_id,
                idempotency_key=record.idempotency_key,
                payload_json=record.payload_json,
                created_at=record.created_at,
                attempts=record.attempts + attempts_delta,
                status=status,
                last_error=error if error is not None else record.last_error,
                updated_at=datetime.now(tz=UTC),
            )
            return


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
            status=OUTBOX_SKIPPED,
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
