"""PRD-001 Phase E — Twin evolution observation (hash + metadata).

Observes Twin succession **after** TwinRepository durable persist succeeds.
Never recalculates Twin state. Never stores Twin / Educational State /
Learning Evidence / recommendation payloads.

Event
-----
``twin.evolved`` — durable Twin snapshot succession (hash + metadata)
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

TWIN_EVOLVED = "twin.evolved"

# Canonical evolution_reason enum (metadata only — not Twin math).
EVOLUTION_BIRTH = "birth"
EVOLUTION_SUCCESSOR = "successor"

EVOLUTION_REASONS = frozenset({EVOLUTION_BIRTH, EVOLUTION_SUCCESSOR})

# SHA-256 hex digest (64 lowercase hex chars).
_SNAPSHOT_HASH_RE = re.compile(r"^[0-9a-f]{64}$")


def build_twin_evolved_event(
    *,
    user_id: int,
    twin_snapshot_id: str,
    twin_version: str,
    evolution_reason: str,
    snapshot_hash: str,
    occurred_at: datetime | None = None,
    correlation_id: str | None = None,
    schema_version: int | AnalyticsEventVersion = AnalyticsEventVersion.V1,
) -> AnalyticsEvent:
    """Build a hash + metadata ``twin.evolved`` envelope.

    Payload contains only opaque snapshot identity, version string,
    canonical ``evolution_reason``, and ``snapshot_hash``. Twin payload is
    forbidden.
    """
    sid = _require_entity_id(twin_snapshot_id, "twin_snapshot_id")
    version = _require_entity_id(twin_version, "twin_version")
    reason = _require_evolution_reason(evolution_reason)
    digest = _require_snapshot_hash(snapshot_hash)

    payload: dict[str, Any] = {
        "twin_snapshot_id": sid,
        "twin_version": version,
        "evolution_reason": reason,
        "snapshot_hash": digest,
    }
    return AnalyticsEvent.create(
        TWIN_EVOLVED,
        user_id=user_id,
        payload=payload,
        occurred_at=occurred_at,
        schema_version=schema_version,
        idempotency_key=build_idempotency_key(
            user_id=user_id,
            event_type=TWIN_EVOLVED,
            entity_key=sid,
        ),
        correlation_id=(correlation_id or "").strip() or new_correlation_id(),
    )


def emit_twin_event(
    event: AnalyticsEvent,
    *,
    dispatcher: AnalyticsEventDispatcher | None = None,
) -> DispatchResult:
    """Dispatch a Twin analytics event (fail-open).

    Analytics failures never raise into Twin persistence.
    """
    try:
        active = dispatcher if dispatcher is not None else AnalyticsEventDispatcher()
        return active.dispatch(event)
    except Exception:  # noqa: BLE001 — fail-open for Twin UX
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


def emit_twin_evolved(
    *,
    user_id: int,
    twin_snapshot_id: str,
    twin_version: str,
    evolution_reason: str,
    snapshot_hash: str,
    dispatcher: AnalyticsEventDispatcher | None = None,
    correlation_id: str | None = None,
    occurred_at: datetime | None = None,
) -> DispatchResult:
    """Build and emit ``twin.evolved`` after successful Twin persist."""
    when = occurred_at if occurred_at is not None else datetime.now(tz=UTC)
    if when.tzinfo is None:
        when = when.replace(tzinfo=UTC)
    event = build_twin_evolved_event(
        user_id=user_id,
        twin_snapshot_id=twin_snapshot_id,
        twin_version=twin_version,
        evolution_reason=evolution_reason,
        snapshot_hash=snapshot_hash,
        correlation_id=correlation_id,
        occurred_at=when,
    )
    return emit_twin_event(event, dispatcher=dispatcher)


def _require_entity_id(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _require_evolution_reason(value: str) -> str:
    reason = (value or "").strip()
    if reason not in EVOLUTION_REASONS:
        raise ValueError(
            "evolution_reason must be one of: " + ", ".join(sorted(EVOLUTION_REASONS))
        )
    return reason


def _require_snapshot_hash(value: str) -> str:
    digest = (value or "").strip().lower()
    if not _SNAPSHOT_HASH_RE.fullmatch(digest):
        raise ValueError(
            "snapshot_hash must be a 64-character lowercase SHA-256 hex digest"
        )
    return digest
