"""Fail-open Personal Learning Profile consumer for Runtime A (EP-004.1).

RecommendationService, ReadinessService, and PlanningService may resolve
profile attributes through this surface without depending on aggregator or
store implementation details. Never educational authority.
"""

from __future__ import annotations

import logging
from collections.abc import Sequence
from typing import Any

from app.infrastructure.adapters.personal_learning_profile.contracts import (
    REASON_FLAG_OFF,
    REASON_STORE_ERROR,
    RESOLVE_STATUS_FAILED,
    RESOLVE_STATUS_SKIPPED,
    PersonalLearningProfile,
    ProfileResolveResult,
)

logger = logging.getLogger(__name__)

_active_store: Any | None = None


def bind_personal_learning_profile_store(store: Any | None) -> None:
    """Bind the process-local profile store (composition / tests)."""
    global _active_store
    _active_store = store


def get_personal_learning_profile_store() -> Any | None:
    """Return the bound store, or construct from flags when unbound."""
    if _active_store is not None:
        return _active_store
    try:
        from app.application.config.v2_flags import resolve_v2_feature_flags
        from app.infrastructure.adapters.personal_learning_profile.store import (
            build_personal_learning_profile_store,
        )

        flags = resolve_v2_feature_flags()
        store = build_personal_learning_profile_store(
            enabled=bool(flags.ENABLE_PERSONAL_LEARNING_PROFILE)
        )
        if store is not None:
            bind_personal_learning_profile_store(store)
        return store
    except Exception:  # noqa: BLE001 — fail-open
        logger.debug(
            "personal_learning_profile_store_resolve_failed", exc_info=True
        )
        return None


def _skipped(reason: str, message: str) -> ProfileResolveResult:
    return ProfileResolveResult(
        ok=False,
        status=RESOLVE_STATUS_SKIPPED,
        reason=reason,
        message=message,
    )


def _failed(reason: str, message: str) -> ProfileResolveResult:
    return ProfileResolveResult(
        ok=False,
        status=RESOLVE_STATUS_FAILED,
        reason=reason,
        message=message,
    )


def _load_feedback_events(student_id: str) -> list[Any]:
    """Pull Learning Feedback buffer events for the student (fail-open)."""
    try:
        from app.infrastructure.adapters.learning_feedback import (
            get_learning_feedback_recorder,
        )

        recorder = get_learning_feedback_recorder()
        if recorder is None:
            return []
        return list(recorder.list_events(student_id=student_id, limit=0) or [])
    except Exception:  # noqa: BLE001 — fail-open
        logger.debug(
            "personal_learning_profile_feedback_load_failed", exc_info=True
        )
        return []


def resolve_personal_learning_profile(
    *,
    student_id: str | int,
    events: Sequence[Any] | None = None,
    declared_session_minutes: int | None = None,
    as_of: str | None = None,
    store: Any | None = None,
) -> ProfileResolveResult:
    """Resolve a Personal Learning Profile for consumer services (fail-open).

    Never raises. Never changes educational decisions. Returns skipped when
    the feature flag is OFF or the store is unavailable.
    """
    try:
        active = (
            store if store is not None else get_personal_learning_profile_store()
        )
        if active is None or not getattr(active, "enabled", False):
            return _skipped(
                REASON_FLAG_OFF,
                "ENABLE_PERSONAL_LEARNING_PROFILE is OFF or store unavailable",
            )
        sid = str(student_id).strip()
        source_events = (
            list(events) if events is not None else _load_feedback_events(sid)
        )
        return active.resolve(
            sid,
            events=source_events,
            declared_session_minutes=declared_session_minutes,
            as_of=as_of,
        )
    except Exception as exc:  # noqa: BLE001 — consumers must not raise
        logger.warning(
            "personal_learning_profile_consumer_failed error=%s", exc
        )
        return _failed(REASON_STORE_ERROR, str(exc))


def consume_personal_learning_profile(
    *,
    student_id: str | int,
    events: Sequence[Any] | None = None,
    declared_session_minutes: int | None = None,
    as_of: str | None = None,
    store: Any | None = None,
) -> dict[str, Any] | None:
    """Stable consumer view for Runtime A services (Protocol-friendly).

    Returns None when flag OFF / resolve skipped / failed — services must
    continue without profile inputs (fail-open). Never delegates authority.
    """
    result = resolve_personal_learning_profile(
        student_id=student_id,
        events=events,
        declared_session_minutes=declared_session_minutes,
        as_of=as_of,
        store=store,
    )
    if not result.ok or result.profile is None:
        return None
    return result.profile.consumer_view()


def get_cached_personal_learning_profile(
    student_id: str | int,
    *,
    store: Any | None = None,
) -> PersonalLearningProfile | None:
    """Return cached profile without re-aggregation (fail-open)."""
    try:
        active = (
            store if store is not None else get_personal_learning_profile_store()
        )
        if active is None:
            return None
        return active.get_cached(student_id)
    except Exception:  # noqa: BLE001 — fail-open
        logger.debug(
            "personal_learning_profile_cache_read_failed", exc_info=True
        )
        return None
