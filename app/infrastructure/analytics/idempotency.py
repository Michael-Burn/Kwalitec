"""Idempotency key strategy for analytics events (PRD-001 §9).

Unique per ``(user_id, event_type, entity_key)`` where ``entity_key`` is the
authoritative domain id for the lifecycle point (session_id, reflection_id,
milestone_id, snapshot_id, twin_snapshot_id, …).
"""

from __future__ import annotations


def build_idempotency_key(
    *,
    user_id: int,
    event_type: str,
    entity_key: str,
) -> str:
    """Build a stable idempotency key for an analytics emit.

    Args:
        user_id: Owning student id.
        event_type: Allowlisted event type.
        entity_key: Domain entity id string (required, non-empty).

    Returns:
        Deterministic key string ``{user_id}:{event_type}:{entity_key}``.
    """
    etype = (event_type or "").strip()
    entity = (entity_key or "").strip()
    if not etype:
        raise ValueError("event_type is required for idempotency_key")
    if not entity:
        raise ValueError("entity_key is required for idempotency_key")
    if user_id is None or int(user_id) < 1:
        raise ValueError("user_id must be a positive integer")
    return f"{int(user_id)}:{etype}:{entity}"
