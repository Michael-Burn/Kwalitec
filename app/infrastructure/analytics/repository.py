"""Analytics event repository contracts and in-memory store.

SQLAlchemy durable adapters live in ``sqlalchemy_store`` and are only used
when explicitly composed — never on educational hot paths in Phase A.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol

from app.infrastructure.analytics.contracts import AnalyticsEvent
from app.infrastructure.analytics.serialization import AnalyticsEventSerializer


class AnalyticsEventRepository(Protocol):
    """Append-only analytics event store contract."""

    def append(self, event: AnalyticsEvent, *, payload_json: str) -> bool:
        """Append event. Returns False when idempotent duplicate."""
        ...

    def get_by_event_id(self, event_id: str) -> AnalyticsEvent | None:
        """Fetch by event_id or None."""
        ...


@dataclass
class MemoryAnalyticsEventStore:
    """In-memory append-only store for unit tests."""

    _events: dict[str, AnalyticsEvent] = field(default_factory=dict)
    _keys: set[tuple[int, str, str]] = field(default_factory=set)
    _serializer: AnalyticsEventSerializer = field(
        default_factory=AnalyticsEventSerializer
    )

    def append(self, event: AnalyticsEvent, *, payload_json: str) -> bool:
        key = (event.user_id, event.event_type, event.idempotency_key)
        if key in self._keys:
            return False
        # payload_json retained only to exercise the contract; envelope is source.
        _ = payload_json
        self._events[event.event_id] = event
        self._keys.add(key)
        return True

    def get_by_event_id(self, event_id: str) -> AnalyticsEvent | None:
        return self._events.get(event_id)

    def count_expired(self, *, cutoff: datetime) -> int:
        return sum(
            1
            for e in self._events.values()
            if _as_aware(e.occurred_at) < _as_aware(cutoff)
        )

    def delete_expired(self, *, cutoff: datetime, limit: int) -> int:
        expired_ids = [
            eid
            for eid, e in self._events.items()
            if _as_aware(e.occurred_at) < _as_aware(cutoff)
        ][:limit]
        for eid in expired_ids:
            event = self._events.pop(eid)
            self._keys.discard(
                (event.user_id, event.event_type, event.idempotency_key)
            )
        return len(expired_ids)


def _as_aware(value: datetime) -> datetime:
    from datetime import UTC

    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value
