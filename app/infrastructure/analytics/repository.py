"""Analytics event repository contracts and in-memory store.

SQLAlchemy durable adapters live in ``sqlalchemy_store`` and are only used
when explicitly composed — never on educational hot paths while the feature
flag is off (EP-002 default).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Protocol

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
    _payloads: dict[str, str] = field(default_factory=dict)
    _serializer: AnalyticsEventSerializer = field(
        default_factory=AnalyticsEventSerializer
    )

    def append(self, event: AnalyticsEvent, *, payload_json: str) -> bool:
        key = (event.user_id, event.event_type, event.idempotency_key)
        if key in self._keys:
            return False
        self._events[event.event_id] = event
        self._payloads[event.event_id] = payload_json
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
            self._payloads.pop(eid, None)
            self._keys.discard(
                (event.user_id, event.event_type, event.idempotency_key)
            )
        return len(expired_ids)

    def delete_for_user(self, user_id: int) -> int:
        ids = [
            eid
            for eid, e in self._events.items()
            if e.user_id == int(user_id)
        ]
        for eid in ids:
            event = self._events.pop(eid)
            self._payloads.pop(eid, None)
            self._keys.discard(
                (event.user_id, event.event_type, event.idempotency_key)
            )
        return len(ids)

    def list_for_user(self, user_id: int, *, limit: int = 10_000) -> list[dict]:
        events = [
            e
            for e in self._events.values()
            if e.user_id == int(user_id)
        ]
        events.sort(key=lambda e: _as_aware(e.occurred_at))
        out: list[dict[str, Any]] = []
        for event in events[:limit]:
            out.append(self._serializer.to_dict(event))
        return out


def _as_aware(value: datetime) -> datetime:
    from datetime import UTC

    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value
