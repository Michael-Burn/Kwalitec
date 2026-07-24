"""Analytics event serialization utilities."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from app.infrastructure.analytics.audit import AuditMetadata
from app.infrastructure.analytics.contracts import AnalyticsEvent
from app.infrastructure.analytics.versioning import AnalyticsEventVersion

REQUIRED_KEYS = (
    "event_id",
    "event_type",
    "user_id",
    "occurred_at",
    "schema_version",
    "idempotency_key",
    "correlation_id",
    "payload",
)


class AnalyticsEventSerializer:
    """Serialize / deserialize :class:`AnalyticsEvent` envelopes."""

    def to_dict(self, event: AnalyticsEvent) -> dict[str, Any]:
        """Convert an event to a plain dict (ISO timestamps)."""
        return {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "user_id": event.user_id,
            "occurred_at": event.occurred_at.isoformat(),
            "schema_version": int(event.schema_version),
            "idempotency_key": event.idempotency_key,
            "correlation_id": event.correlation_id,
            "payload": dict(event.payload),
            "audit": event.audit.to_dict(),
        }

    def to_json(self, event: AnalyticsEvent) -> str:
        """Serialize an event to a compact JSON string."""
        return json.dumps(
            self.to_dict(event), separators=(",", ":"), sort_keys=True
        )

    def from_dict(self, data: dict[str, Any]) -> AnalyticsEvent:
        """Deserialize a dict into an AnalyticsEvent."""
        missing = [k for k in REQUIRED_KEYS if k not in data]
        if missing:
            raise ValueError(f"event dict missing keys: {missing}")
        occurred = data["occurred_at"]
        if isinstance(occurred, str):
            occurred_at = datetime.fromisoformat(occurred)
        elif isinstance(occurred, datetime):
            occurred_at = occurred
        else:
            raise ValueError("occurred_at must be str or datetime")

        audit_raw = data.get("audit") or {}
        audit = AuditMetadata(
            source=str(audit_raw.get("source") or "analytics"),
            emitted_at=(
                datetime.fromisoformat(audit_raw["emitted_at"])
                if audit_raw.get("emitted_at")
                else None
            ),
            flag_enabled=bool(audit_raw.get("flag_enabled", False)),
            sink=str(audit_raw.get("sink") or "null"),
            notes=str(audit_raw.get("notes") or ""),
        )
        return AnalyticsEvent.create(
            str(data["event_type"]),
            user_id=int(data["user_id"]),
            payload=dict(data.get("payload") or {}),
            event_id=str(data["event_id"]),
            occurred_at=occurred_at,
            schema_version=AnalyticsEventVersion.coerce(data["schema_version"]),
            idempotency_key=str(data.get("idempotency_key") or ""),
            correlation_id=str(data.get("correlation_id") or ""),
            audit=audit,
        )

    def from_json(self, raw: str) -> AnalyticsEvent:
        """Deserialize a JSON string into an AnalyticsEvent."""
        return self.from_dict(json.loads(raw))
