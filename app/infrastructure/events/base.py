"""Canonical Version 2 integration event envelope."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class IntegrationEvent:
    """Immutable integration event envelope.

    Every Version 2 integration event carries identity, time, schema version,
    source, payload, and causal linkage fields.
    """

    event_type: str
    payload: dict[str, Any]
    event_id: str = field(default_factory=lambda: uuid4().hex)
    occurred_at: datetime = field(
        default_factory=lambda: datetime.now(tz=UTC)
    )
    event_version: int = 1
    source: str = "infrastructure"
    correlation_id: str = ""
    causation_id: str = ""

    @classmethod
    def create(
        cls,
        event_type: str,
        payload: dict[str, Any] | None = None,
        *,
        event_id: str | None = None,
        occurred_at: datetime | None = None,
        event_version: int = 1,
        source: str = "infrastructure",
        correlation_id: str = "",
        causation_id: str = "",
    ) -> IntegrationEvent:
        """Construct a validated integration event."""
        etype = (event_type or "").strip()
        if not etype:
            raise ValueError("event_type is required")
        if event_version < 1:
            raise ValueError("event_version must be >= 1")
        src = (source or "").strip() or "infrastructure"
        when = occurred_at if occurred_at is not None else datetime.now(tz=UTC)
        if when.tzinfo is None:
            when = when.replace(tzinfo=UTC)
        eid = (event_id or "").strip() or uuid4().hex
        return cls(
            event_type=etype,
            payload=dict(payload or {}),
            event_id=eid,
            occurred_at=when,
            event_version=int(event_version),
            source=src,
            correlation_id=(correlation_id or "").strip(),
            causation_id=(causation_id or "").strip(),
        )

    def with_correlation(
        self,
        *,
        correlation_id: str | None = None,
        causation_id: str | None = None,
    ) -> IntegrationEvent:
        """Return a copy with updated causal linkage."""
        return IntegrationEvent(
            event_type=self.event_type,
            payload=dict(self.payload),
            event_id=self.event_id,
            occurred_at=self.occurred_at,
            event_version=self.event_version,
            source=self.source,
            correlation_id=(
                correlation_id
                if correlation_id is not None
                else self.correlation_id
            ),
            causation_id=(
                causation_id if causation_id is not None else self.causation_id
            ),
        )
