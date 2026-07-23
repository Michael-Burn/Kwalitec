"""Presentation/application telemetry — ALPHA-001.

Records product-surface events for Internal Alpha observability.
Never writes educational scores, Twin state, or recommendation payloads.
No analytics fields belong on domain models.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from app.extensions import db
from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.models.alpha_infrastructure import PresentationEvent

logger = logging.getLogger(__name__)

EVENT_DASHBOARD_OPENED = "dashboard_opened"
EVENT_MISSION_STARTED = "mission_started"
EVENT_MISSION_COMPLETED = "mission_completed"
EVENT_REFLECTION_COMPLETED = "reflection_completed"
EVENT_COACH_OPENED = "coach_opened"
EVENT_JOURNEY_OPENED = "journey_opened"
EVENT_READINESS_OPENED = "readiness_opened"
EVENT_PROVENANCE_EXPANDED = "provenance_expanded"
EVENT_FEEDBACK_SUBMITTED = "feedback_submitted"

ALLOWED_EVENTS = frozenset(
    {
        EVENT_DASHBOARD_OPENED,
        EVENT_MISSION_STARTED,
        EVENT_MISSION_COMPLETED,
        EVENT_REFLECTION_COMPLETED,
        EVENT_COACH_OPENED,
        EVENT_JOURNEY_OPENED,
        EVENT_READINESS_OPENED,
        EVENT_PROVENANCE_EXPANDED,
        EVENT_FEEDBACK_SUBMITTED,
    }
)

# Client-emitted interaction events (CSRF-protected ingest endpoint).
CLIENT_EVENTS = frozenset(
    {
        EVENT_COACH_OPENED,
        EVENT_READINESS_OPENED,
        EVENT_PROVENANCE_EXPANDED,
    }
)


class PresentationTelemetryService:
    """Persist and query presentation-layer telemetry events."""

    @staticmethod
    def record(
        event_type: str,
        *,
        user_id: int | None = None,
        resource_type: str | None = None,
        resource_id: str | int | None = None,
        path: str | None = None,
        context: dict[str, Any] | None = None,
        correlation_id: str | None = None,
        commit: bool = True,
    ) -> PresentationEvent | None:
        """Record one allowed presentation event. Returns None if rejected."""
        normalised = (event_type or "").strip().lower()
        if normalised not in ALLOWED_EVENTS:
            logger.warning("Rejected unknown presentation event: %s", event_type)
            return None

        corr = (correlation_id or "").strip() or CorrelationContext.get_correlation_id()
        context_json = None
        if context:
            # Keep context small and non-educational (paths, surface names only).
            safe = {
                str(k)[:64]: str(v)[:256]
                for k, v in list(context.items())[:12]
                if v is not None
            }
            if safe:
                context_json = json.dumps(safe, separators=(",", ":"))

        event = PresentationEvent(
            user_id=user_id,
            event_type=normalised,
            resource_type=(resource_type or None),
            resource_id=str(resource_id) if resource_id is not None else None,
            path=(path or None),
            correlation_id=corr or None,
            context_json=context_json,
        )
        db.session.add(event)
        if commit:
            try:
                db.session.commit()
            except Exception:  # noqa: BLE001
                db.session.rollback()
                logger.exception("Failed to persist presentation event %s", normalised)
                return None
        logger.info(
            "presentation_event type=%s user=%s correlation_id=%s",
            normalised,
            user_id,
            corr or "-",
        )
        return event

    @staticmethod
    def recent(
        *,
        limit: int = 50,
        event_type: str | None = None,
        user_id: int | None = None,
    ) -> list[PresentationEvent]:
        """Return recent events for founder support tooling."""
        query = PresentationEvent.query.order_by(PresentationEvent.created_at.desc())
        if event_type:
            query = query.filter_by(event_type=event_type.strip().lower())
        if user_id is not None:
            query = query.filter_by(user_id=user_id)
        return list(query.limit(max(1, min(limit, 200))).all())

    @staticmethod
    def count_by_type(*, limit_types: int = 20) -> list[tuple[str, int]]:
        """Aggregate counts by event type for support overview."""
        rows = (
            db.session.query(
                PresentationEvent.event_type,
                db.func.count(PresentationEvent.id),
            )
            .group_by(PresentationEvent.event_type)
            .order_by(db.func.count(PresentationEvent.id).desc())
            .limit(max(1, min(limit_types, 50)))
            .all()
        )
        return [(str(event_type), int(count)) for event_type, count in rows]
