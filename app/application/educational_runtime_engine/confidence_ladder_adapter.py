"""Domain H confidence → Spacing calendar nudge (sole bridge).

This module is the only place that may connect a sitting's Domain H
``confidence_rating`` to a scheduling effect. It reduces the rating to a
calendar-only ``ladder_step_delta`` in ``{-1, 0, +1}`` and never feeds
confidence into Twin, Estimated Knowledge, mastery, recommendations, or
the Decision Engine.

The Spacing Scheduler remains unaware that confidence exists: it only
receives the integer ladder delta.
"""

from __future__ import annotations

from typing import Any


def confidence_rating_to_ladder_step_delta(
    confidence_rating: int | None,
) -> int:
    """Map Domain H confidence (1-5 or missing) to a ladder step delta.

    Locked table:
    - missing / invalid → 0 (no change)
    - 1–2 → -1 (one step shorter)
    - 3 → 0 (no change)
    - 4–5 → +1 (one step longer)
    """
    if confidence_rating is None:
        return 0
    try:
        rating = int(confidence_rating)
    except (TypeError, ValueError):
        return 0
    if rating in (1, 2):
        return -1
    if rating == 3:
        return 0
    if rating in (4, 5):
        return 1
    return 0


def load_sitting_confidence_rating(
    *,
    user_id: int,
    mission_instance_id: str,
) -> int | None:
    """Read Domain H ``confidence_rating`` from the sitting's session handle.

    Join: ``lsr.mission`` pointer ``{user_id}::{mission_instance_id}`` →
    ``session_id`` → ``lsr.handle`` document. Missing pointer, handle, or
    rating returns ``None`` (no nudge). Fail-open on store errors.
    """
    mid = (mission_instance_id or "").strip()
    if not mid:
        return None
    try:
        from app.infrastructure.adapters.learning_session.persistence import (
            NS_MISSION,
            LearningSessionPersistenceAdapter,
        )
        from app.infrastructure.session.composition import (
            build_production_session_experience,
        )

        composition, _service = build_production_session_experience(
            seed_demo_learners=False
        )
        adapter = LearningSessionPersistenceAdapter(store=composition.store)
        sid = str(user_id)
        ptr = adapter.store.get(NS_MISSION, f"{sid}::{mid}")
        if not isinstance(ptr, dict):
            return None
        session_id = str(ptr.get("session_id") or "").strip()
        if not session_id:
            return None
        doc = adapter.load(session_id=session_id)
        if not isinstance(doc, dict):
            return None
        return _coerce_domain_h_rating(doc.get("confidence_rating"))
    except Exception:
        return None


def ladder_step_delta_for_completed_sitting(
    *,
    user_id: int,
    mission_instance_id: str,
) -> int:
    """Sole confidence→scheduling translation for a completed sitting."""
    rating = load_sitting_confidence_rating(
        user_id=user_id,
        mission_instance_id=mission_instance_id,
    )
    return confidence_rating_to_ladder_step_delta(rating)


def _coerce_domain_h_rating(raw: Any) -> int | None:
    if raw is None:
        return None
    try:
        rating = int(raw)
    except (TypeError, ValueError):
        return None
    if 1 <= rating <= 5:
        return rating
    return None
