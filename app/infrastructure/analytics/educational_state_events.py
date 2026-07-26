"""PRD-001 Phase D — Educational State snapshot observation (hash + metadata).

Observes Educational State **after** EducationalStateService assembles a
snapshot. Never recalculates Educational State. Never stores Educational
State / Twin / Learning Evidence / recommendation payloads.

Event
-----
``educational_state.snapshot`` — material ESS assembly change (hash + metadata)
"""

from __future__ import annotations

import logging
import re
from datetime import UTC, datetime
from typing import Any

from app.infrastructure.analytics.contracts import AnalyticsEvent
from app.infrastructure.analytics.correlation import new_correlation_id
from app.infrastructure.analytics.dispatcher import (
    AnalyticsEventDispatcher,
    DispatchResult,
    DispatchStatus,
)
from app.infrastructure.analytics.idempotency import build_idempotency_key
from app.infrastructure.analytics.versioning import AnalyticsEventVersion

logger = logging.getLogger(__name__)

EDUCATIONAL_STATE_SNAPSHOT = "educational_state.snapshot"

# SHA-256 hex digest (64 lowercase hex chars).
_CONTENT_HASH_RE = re.compile(r"^[0-9a-f]{64}$")


def build_educational_state_snapshot_event(
    *,
    user_id: int,
    snapshot_id: str,
    content_hash: str,
    occurred_at: datetime | None = None,
    correlation_id: str | None = None,
    schema_version: int | AnalyticsEventVersion = AnalyticsEventVersion.V1,
) -> AnalyticsEvent:
    """Build a hash + metadata ``educational_state.snapshot`` envelope.

    Payload contains only ``snapshot_id`` and ``content_hash`` (PRD-001 §7.4).
    Envelope carries ``user_id`` (privacy-compliant student identifier),
    ``schema_version``, ``occurred_at`` (timestamp), and ``correlation_id``.
    """
    sid = _require_entity_id(snapshot_id, "snapshot_id")
    digest = _require_content_hash(content_hash)

    payload: dict[str, Any] = {
        "snapshot_id": sid,
        "content_hash": digest,
    }
    return AnalyticsEvent.create(
        EDUCATIONAL_STATE_SNAPSHOT,
        user_id=user_id,
        payload=payload,
        occurred_at=occurred_at,
        schema_version=schema_version,
        idempotency_key=build_idempotency_key(
            user_id=user_id,
            event_type=EDUCATIONAL_STATE_SNAPSHOT,
            entity_key=sid,
        ),
        correlation_id=(correlation_id or "").strip() or new_correlation_id(),
    )


def emit_educational_state_event(
    event: AnalyticsEvent,
    *,
    dispatcher: AnalyticsEventDispatcher | None = None,
) -> DispatchResult:
    """Dispatch an Educational State analytics event (fail-open).

    Analytics failures never raise into Educational State assembly.
    """
    try:
        active = dispatcher if dispatcher is not None else AnalyticsEventDispatcher()
        return active.dispatch(event)
    except Exception:  # noqa: BLE001 — fail-open for learning UX
        logger.exception(
            "analytics.emit_failed event_id=%s type=%s",
            getattr(event, "event_id", ""),
            getattr(event, "event_type", ""),
        )
        return DispatchResult(
            status=DispatchStatus.FAILED,
            event_id=getattr(event, "event_id", ""),
            errors=("analytics.emit_failed",),
        )


def emit_educational_state_snapshot(
    *,
    user_id: int,
    snapshot_id: str,
    content_hash: str,
    dispatcher: AnalyticsEventDispatcher | None = None,
    correlation_id: str | None = None,
    occurred_at: datetime | None = None,
) -> DispatchResult:
    """Build and emit ``educational_state.snapshot`` after material ESS change."""
    when = occurred_at if occurred_at is not None else datetime.now(tz=UTC)
    if when.tzinfo is None:
        when = when.replace(tzinfo=UTC)
    event = build_educational_state_snapshot_event(
        user_id=user_id,
        snapshot_id=snapshot_id,
        content_hash=content_hash,
        correlation_id=correlation_id,
        occurred_at=when,
    )
    return emit_educational_state_event(event, dispatcher=dispatcher)


def _require_entity_id(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _require_content_hash(value: str) -> str:
    digest = (value or "").strip().lower()
    if not _CONTENT_HASH_RE.fullmatch(digest):
        raise ValueError(
            "content_hash must be a 64-character lowercase SHA-256 hex digest"
        )
    return digest
