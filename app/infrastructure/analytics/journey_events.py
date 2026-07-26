"""PRD-001 Phase E — Journey progression observation (metadata only).

Observes Learning Journey progression **after** durable repository save
succeeds. Never recalculates journey state. Never stores Journey narrative,
Educational State, Twin, Learning Evidence, or recommendation payloads.

Event
-----
``journey.progressed`` — lawful journey transition after persistence

Production emit remains deferred until a durable LearningJourneyRepository
adapter exists (ADR-026). Builders and the Application observe helper are
shipped so adapters can call them after ``save``.
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

JOURNEY_PROGRESSED = "journey.progressed"

# Canonical transition identifiers (metadata catalogue — mirrors JourneyTransitionEvent
# values without importing domain modules into analytics).
ALLOWED_TRANSITION_IDS = frozenset(
    {
        "start_journey",
        "pause_journey",
        "resume_journey",
        "settle_active",
        "completion_criteria_met",
        "confirm_topic_complete",
        "continue_journey",
        "defer_journey",
        "abandon_journey",
        "reactivate_journey",
        "archive_journey",
    }
)


def build_journey_progressed_event(
    *,
    user_id: int,
    journey_id: str,
    curriculum_node_id: str,
    transition_id: str,
    occurred_at: datetime | None = None,
    correlation_id: str | None = None,
    schema_version: int | AnalyticsEventVersion = AnalyticsEventVersion.V1,
    entity_key: str | None = None,
) -> AnalyticsEvent:
    """Build a metadata-only ``journey.progressed`` envelope.

    Payload contains journey identifier, curriculum node identifier, and
    transition identifier only.
    """
    jid = _require_entity_id(journey_id, "journey_id")
    node = _require_entity_id(curriculum_node_id, "curriculum_node_id")
    transition = _require_transition_id(transition_id)
    key = (entity_key or "").strip() or f"{jid}:{transition}:{node}"

    payload: dict[str, Any] = {
        "journey_id": jid,
        "curriculum_node_id": node,
        "transition_id": transition,
    }
    return AnalyticsEvent.create(
        JOURNEY_PROGRESSED,
        user_id=user_id,
        payload=payload,
        occurred_at=occurred_at,
        schema_version=schema_version,
        idempotency_key=build_idempotency_key(
            user_id=user_id,
            event_type=JOURNEY_PROGRESSED,
            entity_key=key,
        ),
        correlation_id=(correlation_id or "").strip() or new_correlation_id(),
    )


def emit_journey_event(
    event: AnalyticsEvent,
    *,
    dispatcher: AnalyticsEventDispatcher | None = None,
) -> DispatchResult:
    """Dispatch a Journey analytics event (fail-open).

    Analytics failures never raise into Journey persistence / progression.
    """
    try:
        active = dispatcher if dispatcher is not None else AnalyticsEventDispatcher()
        return active.dispatch(event)
    except Exception:  # noqa: BLE001 — fail-open for Journey UX
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


def emit_journey_progressed(
    *,
    user_id: int,
    journey_id: str,
    curriculum_node_id: str,
    transition_id: str,
    dispatcher: AnalyticsEventDispatcher | None = None,
    correlation_id: str | None = None,
    occurred_at: datetime | None = None,
    entity_key: str | None = None,
) -> DispatchResult:
    """Build and emit ``journey.progressed`` after successful Journey persist."""
    when = occurred_at if occurred_at is not None else datetime.now(tz=UTC)
    if when.tzinfo is None:
        when = when.replace(tzinfo=UTC)
    event = build_journey_progressed_event(
        user_id=user_id,
        journey_id=journey_id,
        curriculum_node_id=curriculum_node_id,
        transition_id=transition_id,
        correlation_id=correlation_id,
        occurred_at=when,
        entity_key=entity_key,
    )
    return emit_journey_event(event, dispatcher=dispatcher)


def _require_entity_id(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _require_transition_id(value: str) -> str:
    transition = (value or "").strip()
    if transition not in ALLOWED_TRANSITION_IDS:
        raise ValueError(
            "transition_id must be a canonical Journey transition identifier"
        )
    return transition
