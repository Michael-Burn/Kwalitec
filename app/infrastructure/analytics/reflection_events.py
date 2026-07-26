"""PRD-001 Phase C — Reflection analytics event builders + fail-open emit.

Observes Reflection lifecycle **after** authoritative capture succeeds.
Never calculates mastery / readiness / recommendations. Never stores
reflection body text, EducationalState, Twin, or Learning Evidence payloads.

Events
------
``reflection.submitted`` — student reflection content accepted onto the session
``reflection.completed`` — reflection reaches canonical completed posture
"""

from __future__ import annotations

import logging
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

REFLECTION_SUBMITTED = "reflection.submitted"
REFLECTION_COMPLETED = "reflection.completed"

PROCESSING_COMPLETED = "completed"
PROCESSING_STATUSES = frozenset({PROCESSING_COMPLETED})

# Structured Learning Journey / Learning Session reflection (metadata only).
REFLECTION_TYPE_JOURNEY_SESSION = "journey_session"

ALLOWED_REFLECTION_TYPES = frozenset({REFLECTION_TYPE_JOURNEY_SESSION})


def build_reflection_submitted_event(
    *,
    user_id: int,
    reflection_id: str,
    session_id: str,
    reflection_type: str = REFLECTION_TYPE_JOURNEY_SESSION,
    occurred_at: datetime | None = None,
    correlation_id: str | None = None,
    schema_version: int | AnalyticsEventVersion = AnalyticsEventVersion.V1,
) -> AnalyticsEvent:
    """Build a metadata-only ``reflection.submitted`` envelope.

    ``student_id`` in the payload is the privacy-compliant opaque integer
    learner id (same value as envelope ``user_id``) — never email or free text.
    """
    rid = _require_entity_id(reflection_id, "reflection_id")
    sid = _require_entity_id(session_id, "session_id")
    rtype = (reflection_type or "").strip()
    if rtype not in ALLOWED_REFLECTION_TYPES:
        raise ValueError(
            f"Invalid reflection_type: {reflection_type!r}; "
            f"expected one of {sorted(ALLOWED_REFLECTION_TYPES)}"
        )

    payload: dict[str, Any] = {
        "reflection_id": rid,
        "session_id": sid,
        "student_id": int(user_id),
        "reflection_type": rtype,
    }
    return AnalyticsEvent.create(
        REFLECTION_SUBMITTED,
        user_id=user_id,
        payload=payload,
        occurred_at=occurred_at,
        schema_version=schema_version,
        idempotency_key=build_idempotency_key(
            user_id=user_id,
            event_type=REFLECTION_SUBMITTED,
            entity_key=rid,
        ),
        correlation_id=(correlation_id or "").strip() or new_correlation_id(),
    )


def build_reflection_completed_event(
    *,
    user_id: int,
    reflection_id: str,
    processing_status: str = PROCESSING_COMPLETED,
    occurred_at: datetime | None = None,
    correlation_id: str | None = None,
    schema_version: int | AnalyticsEventVersion = AnalyticsEventVersion.V1,
) -> AnalyticsEvent:
    """Build a metadata-only ``reflection.completed`` envelope."""
    rid = _require_entity_id(reflection_id, "reflection_id")
    status = (processing_status or "").strip()
    if status not in PROCESSING_STATUSES:
        raise ValueError(
            f"Invalid processing_status: {processing_status!r}; "
            f"expected one of {sorted(PROCESSING_STATUSES)}"
        )

    payload: dict[str, Any] = {
        "reflection_id": rid,
        "processing_status": status,
    }
    return AnalyticsEvent.create(
        REFLECTION_COMPLETED,
        user_id=user_id,
        payload=payload,
        occurred_at=occurred_at,
        schema_version=schema_version,
        idempotency_key=build_idempotency_key(
            user_id=user_id,
            event_type=REFLECTION_COMPLETED,
            entity_key=rid,
        ),
        correlation_id=(correlation_id or "").strip() or new_correlation_id(),
    )


def emit_reflection_event(
    event: AnalyticsEvent,
    *,
    dispatcher: AnalyticsEventDispatcher | None = None,
) -> DispatchResult:
    """Dispatch a reflection analytics event (fail-open).

    Analytics failures never raise into the reflection workflow.
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


def emit_reflection_submitted(
    *,
    user_id: int,
    reflection_id: str,
    session_id: str,
    reflection_type: str = REFLECTION_TYPE_JOURNEY_SESSION,
    dispatcher: AnalyticsEventDispatcher | None = None,
    correlation_id: str | None = None,
    occurred_at: datetime | None = None,
) -> DispatchResult:
    """Build and emit ``reflection.submitted`` after successful capture."""
    event = build_reflection_submitted_event(
        user_id=user_id,
        reflection_id=reflection_id,
        session_id=session_id,
        reflection_type=reflection_type,
        correlation_id=correlation_id,
        occurred_at=occurred_at,
    )
    return emit_reflection_event(event, dispatcher=dispatcher)


def emit_reflection_completed(
    *,
    user_id: int,
    reflection_id: str,
    processing_status: str = PROCESSING_COMPLETED,
    dispatcher: AnalyticsEventDispatcher | None = None,
    correlation_id: str | None = None,
    occurred_at: datetime | None = None,
) -> DispatchResult:
    """Build and emit ``reflection.completed`` after successful capture."""
    event = build_reflection_completed_event(
        user_id=user_id,
        reflection_id=reflection_id,
        processing_status=processing_status,
        correlation_id=correlation_id,
        occurred_at=occurred_at,
    )
    return emit_reflection_event(event, dispatcher=dispatcher)


def emit_reflection_lifecycle(
    *,
    user_id: int,
    reflection_id: str,
    session_id: str,
    reflection_type: str = REFLECTION_TYPE_JOURNEY_SESSION,
    processing_status: str = PROCESSING_COMPLETED,
    dispatcher: AnalyticsEventDispatcher | None = None,
    correlation_id: str | None = None,
    occurred_at: datetime | None = None,
) -> tuple[DispatchResult, DispatchResult]:
    """Emit submitted then completed for one successful capture transaction.

    Both events share the same ``correlation_id`` so ops can link the pair.
    Failures on either emit are fail-open (returned, never raised).
    """
    when = occurred_at if occurred_at is not None else datetime.now(tz=UTC)
    if when.tzinfo is None:
        when = when.replace(tzinfo=UTC)
    corr = (correlation_id or "").strip() or new_correlation_id()
    submitted = emit_reflection_submitted(
        user_id=user_id,
        reflection_id=reflection_id,
        session_id=session_id,
        reflection_type=reflection_type,
        dispatcher=dispatcher,
        correlation_id=corr,
        occurred_at=when,
    )
    completed = emit_reflection_completed(
        user_id=user_id,
        reflection_id=reflection_id,
        processing_status=processing_status,
        dispatcher=dispatcher,
        correlation_id=corr,
        occurred_at=when,
    )
    return submitted, completed


def _require_entity_id(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()
