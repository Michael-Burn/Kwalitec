"""Analytics event envelope contract (PRD-001 Phase A).

Immutable observation record. Payload is metadata-only; educational
authorities remain authoritative for mastery / readiness / next action.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from app.infrastructure.analytics.audit import AuditMetadata
from app.infrastructure.analytics.versioning import AnalyticsEventVersion


@dataclass(frozen=True)
class AnalyticsEvent:
    """Canonical analytics event envelope (AnalyticsEvent interface).

    Attributes:
        event_type: Allowlisted type string (registry-enforced at dispatch).
        user_id: Owning student id.
        payload: Metadata-only fields (no free-text reflection / exam PII).
        event_id: Stable UUID hex identity.
        occurred_at: Event time (timezone-aware UTC preferred).
        schema_version: Integer schema version for this event type.
        idempotency_key: Replay / duplicate protection key.
        correlation_id: Cross-request linkage.
        audit: Emit-path audit metadata.
    """

    event_type: str
    user_id: int
    payload: dict[str, Any]
    event_id: str = field(default_factory=lambda: uuid4().hex)
    occurred_at: datetime = field(
        default_factory=lambda: datetime.now(tz=UTC)
    )
    schema_version: AnalyticsEventVersion = AnalyticsEventVersion.V1
    idempotency_key: str = ""
    correlation_id: str = ""
    audit: AuditMetadata = field(default_factory=AuditMetadata)

    @classmethod
    def create(
        cls,
        event_type: str,
        *,
        user_id: int,
        payload: dict[str, Any] | None = None,
        event_id: str | None = None,
        occurred_at: datetime | None = None,
        schema_version: int | AnalyticsEventVersion = AnalyticsEventVersion.V1,
        idempotency_key: str = "",
        correlation_id: str = "",
        audit: AuditMetadata | None = None,
    ) -> AnalyticsEvent:
        """Construct a minimally validated analytics event envelope.

        Full allowlist / payload-size checks run in
        :class:`AnalyticsEventValidator` at dispatch time.
        """
        etype = (event_type or "").strip()
        if not etype:
            raise ValueError("event_type is required")
        if user_id is None or int(user_id) < 1:
            raise ValueError("user_id must be a positive integer")
        version = AnalyticsEventVersion.coerce(schema_version)
        when = occurred_at if occurred_at is not None else datetime.now(tz=UTC)
        if when.tzinfo is None:
            when = when.replace(tzinfo=UTC)
        eid = (event_id or "").strip() or uuid4().hex
        return cls(
            event_type=etype,
            user_id=int(user_id),
            payload=dict(payload or {}),
            event_id=eid,
            occurred_at=when,
            schema_version=version,
            idempotency_key=(idempotency_key or "").strip(),
            correlation_id=(correlation_id or "").strip(),
            audit=audit if audit is not None else AuditMetadata(),
        )
