"""PRD-001 Phase B — Study Session analytics event builders + fail-open emit.

Observes Study Session lifecycle **after** educational persistence succeeds.
Never calculates mastery / readiness / recommendations. Never stores
EducationalState, Twin, Learning Evidence, or free-text reflection bodies.

Canonical abandonment form (PRD-001 §7.4): ``session.completed`` with
``completion_status=abandoned_after_start``. There is no separate
``session.cancelled`` event type.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta
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

SESSION_STARTED = "session.started"
SESSION_COMPLETED = "session.completed"

COMPLETION_COMPLETED = "completed"
COMPLETION_ABANDONED_AFTER_START = "abandoned_after_start"

COMPLETION_STATUSES = frozenset(
    {COMPLETION_COMPLETED, COMPLETION_ABANDONED_AFTER_START}
)


def session_entity_key(mission_id: int) -> str:
    """Stable session entity key — LXP Study Session is 1:1 with Mission."""
    return f"mission:{int(mission_id)}"


def build_session_started_event(
    *,
    user_id: int,
    mission_id: int,
    curriculum_node_id: int | str | None = None,
    occurred_at: datetime | None = None,
    correlation_id: str | None = None,
    schema_version: int | AnalyticsEventVersion = AnalyticsEventVersion.V1,
) -> AnalyticsEvent:
    """Build a metadata-only ``session.started`` envelope."""
    session_id = session_entity_key(mission_id)
    payload: dict[str, Any] = {
        "session_id": session_id,
        "mission_id": int(mission_id),
    }
    if curriculum_node_id is not None and str(curriculum_node_id).strip():
        payload["curriculum_node_id"] = (
            int(curriculum_node_id)
            if isinstance(curriculum_node_id, int)
            or str(curriculum_node_id).isdigit()
            else str(curriculum_node_id).strip()
        )
    return AnalyticsEvent.create(
        SESSION_STARTED,
        user_id=user_id,
        payload=payload,
        occurred_at=occurred_at,
        schema_version=schema_version,
        idempotency_key=build_idempotency_key(
            user_id=user_id,
            event_type=SESSION_STARTED,
            entity_key=session_id,
        ),
        correlation_id=(correlation_id or "").strip() or new_correlation_id(),
    )


def build_session_completed_event(
    *,
    user_id: int,
    mission_id: int,
    completion_status: str,
    topic_id: int | None = None,
    started_at: datetime | None = None,
    duration_seconds: int | None = None,
    abandon_reason: str | None = None,
    occurred_at: datetime | None = None,
    correlation_id: str | None = None,
    schema_version: int | AnalyticsEventVersion = AnalyticsEventVersion.V1,
) -> AnalyticsEvent:
    """Build a metadata-only ``session.completed`` envelope.

    ``completion_status`` must be ``completed`` or ``abandoned_after_start``
    (canonical abandoned / cancelled lifecycle — PRD-001 §7.4).
    """
    status = (completion_status or "").strip()
    if status not in COMPLETION_STATUSES:
        raise ValueError(
            f"Invalid completion_status: {completion_status!r}; "
            f"expected one of {sorted(COMPLETION_STATUSES)}"
        )

    when = occurred_at if occurred_at is not None else datetime.now(tz=UTC)
    if when.tzinfo is None:
        when = when.replace(tzinfo=UTC)

    session_id = session_entity_key(mission_id)
    payload: dict[str, Any] = {
        "session_id": session_id,
        "mission_id": int(mission_id),
        "completion_status": status,
    }

    effective_started = started_at
    if (
        effective_started is None
        and duration_seconds is not None
        and duration_seconds >= 0
    ):
        effective_started = when - timedelta(seconds=int(duration_seconds))
    if effective_started is not None:
        if effective_started.tzinfo is None:
            effective_started = effective_started.replace(tzinfo=UTC)
        payload["started_at"] = effective_started.astimezone(UTC).isoformat().replace(
            "+00:00", "Z"
        )

    if duration_seconds is not None and duration_seconds >= 0:
        payload["duration_seconds"] = int(duration_seconds)

    if topic_id is not None:
        payload["topic_id"] = int(topic_id)

    if status == COMPLETION_ABANDONED_AFTER_START and abandon_reason:
        reason = str(abandon_reason).strip()[:128]
        if reason:
            payload["abandon_reason"] = reason

    return AnalyticsEvent.create(
        SESSION_COMPLETED,
        user_id=user_id,
        payload=payload,
        occurred_at=when,
        schema_version=schema_version,
        idempotency_key=build_idempotency_key(
            user_id=user_id,
            event_type=SESSION_COMPLETED,
            entity_key=session_id,
        ),
        correlation_id=(correlation_id or "").strip() or new_correlation_id(),
    )


def emit_session_event(
    event: AnalyticsEvent,
    *,
    dispatcher: AnalyticsEventDispatcher | None = None,
) -> DispatchResult:
    """Dispatch a session analytics event (fail-open).

    Analytics failures never raise into the educational workflow.
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


def emit_session_started(
    *,
    user_id: int,
    mission_id: int,
    curriculum_node_id: int | str | None = None,
    dispatcher: AnalyticsEventDispatcher | None = None,
    correlation_id: str | None = None,
) -> DispatchResult:
    """Build and emit ``session.started`` after a successful session start."""
    event = build_session_started_event(
        user_id=user_id,
        mission_id=mission_id,
        curriculum_node_id=curriculum_node_id,
        correlation_id=correlation_id,
    )
    return emit_session_event(event, dispatcher=dispatcher)


def emit_session_completed(
    *,
    user_id: int,
    mission_id: int,
    completion_status: str,
    topic_id: int | None = None,
    started_at: datetime | None = None,
    duration_seconds: int | None = None,
    abandon_reason: str | None = None,
    dispatcher: AnalyticsEventDispatcher | None = None,
    correlation_id: str | None = None,
) -> DispatchResult:
    """Build and emit ``session.completed`` after a successful session close."""
    event = build_session_completed_event(
        user_id=user_id,
        mission_id=mission_id,
        completion_status=completion_status,
        topic_id=topic_id,
        started_at=started_at,
        duration_seconds=duration_seconds,
        abandon_reason=abandon_reason,
        correlation_id=correlation_id,
    )
    return emit_session_event(event, dispatcher=dispatcher)
