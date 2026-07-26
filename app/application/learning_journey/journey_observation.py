"""Fail-open Journey progression observation after durable save (PRD-001 Phase E).

Callers invoke this **only after** ``LearningJourneyRepository.save`` succeeds
(ADR-026). LearningJourneyEngine never persists and must not call this helper
directly for production observation.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


def observe_journey_progressed(
    journey: Any,
    *,
    transition_id: str,
    user_id: int | None = None,
    entity_key: str | None = None,
) -> None:
    """Emit ``journey.progressed`` after successful Journey persistence.

    Fail-open: analytics errors never affect Journey save / progression.

    Args:
        journey: Persisted LearningJourney aggregate (duck-typed).
        transition_id: Canonical JourneyTransitionEvent value string.
        user_id: Optional opaque integer analytics identity. When omitted,
            ``journey.learner_id`` is parsed as int (skipped if non-numeric).
        entity_key: Optional idempotency entity key override.
    """
    try:
        resolved_user_id = user_id
        if resolved_user_id is None:
            learner = str(getattr(journey, "learner_id", "") or "").strip()
            if not learner:
                return
            try:
                resolved_user_id = int(learner)
            except (TypeError, ValueError):
                return

        journey_id = str(getattr(journey, "journey_id", "") or "").strip()
        topic_id = str(getattr(journey, "topic_id", "") or "").strip()
        if not journey_id or not topic_id:
            return

        history = getattr(journey, "history", None)
        entries = getattr(history, "entries", ()) or ()
        key = entity_key or f"{journey_id}:{transition_id}:{len(entries)}"

        from app.infrastructure.analytics.journey_events import emit_journey_progressed

        emit_journey_progressed(
            user_id=int(resolved_user_id),
            journey_id=journey_id,
            curriculum_node_id=topic_id,
            transition_id=transition_id,
            entity_key=key,
        )
    except Exception:  # noqa: BLE001 — analytics must never break Journey
        logger.exception(
            "analytics.emit_failed journey.progressed journey=%s",
            getattr(journey, "journey_id", ""),
        )
