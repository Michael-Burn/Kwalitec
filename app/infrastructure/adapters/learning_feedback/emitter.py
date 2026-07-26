"""Fail-open Learning Feedback emitter for Runtime A services (EP-003.4).

Services call these helpers to emit observed behavioural evidence. Emitters
never raise into educational control flows and never alter decisions.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any

from app.infrastructure.adapters.learning_feedback.contracts import (
    CLAIM_OBSERVED_BEHAVIOUR,
    CLAIM_PLAN_INTERACTION,
    CLAIM_PREFERENCE_JOURNAL,
    CLAIM_STUDY_HABIT_SIGNAL,
    FEEDBACK_EVENT_PLAN_COMPLETED,
    FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED,
    FEEDBACK_EVENT_RECOMMENDATION_DISMISSED,
    FEEDBACK_EVENT_RECOVERY_APPLIED,
    FEEDBACK_EVENT_REVISION_ADHERED,
    FEEDBACK_EVENT_REVISION_DEFERRED,
    FEEDBACK_EVENT_SESSION_MISSED,
    FEEDBACK_EVENT_STUDY_CONSISTENCY,
    REASON_FLAG_OFF,
    REASON_FORBIDDEN_INFERENCE,
    REASON_RECORDER_ERROR,
    REASON_SCHEMA_INVALID,
    RECORD_STATUS_FAILED,
    RECORD_STATUS_SKIPPED,
    SOURCE_PLANNING,
    SOURCE_READINESS,
    SOURCE_RECOMMENDATION,
    FeedbackRecordResult,
    LearningFeedbackEvent,
    deterministic_feedback_id,
)

logger = logging.getLogger(__name__)

# Process-local default recorder (set by composition or tests).
_active_recorder: Any | None = None


def bind_learning_feedback_recorder(recorder: Any | None) -> None:
    """Bind the process-local recorder (composition / tests)."""
    global _active_recorder
    _active_recorder = recorder


def get_learning_feedback_recorder() -> Any | None:
    """Return the bound recorder, or construct from flags when unbound."""
    if _active_recorder is not None:
        return _active_recorder
    try:
        from app.application.config.v2_flags import resolve_v2_feature_flags
        from app.infrastructure.adapters.learning_feedback.recorder import (
            build_learning_feedback_recorder,
        )

        flags = resolve_v2_feature_flags()
        recorder = build_learning_feedback_recorder(
            enabled=bool(flags.ENABLE_LEARNING_FEEDBACK)
        )
        # Cache only when ON so flag flips in tests can re-resolve when unbound.
        if recorder is not None:
            bind_learning_feedback_recorder(recorder)
        return recorder
    except Exception:  # noqa: BLE001 — fail-open
        logger.debug("learning_feedback_recorder_resolve_failed", exc_info=True)
        return None


def _now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def _skipped(reason: str, message: str) -> FeedbackRecordResult:
    return FeedbackRecordResult(
        ok=False,
        status=RECORD_STATUS_SKIPPED,
        reason=reason,
        message=message,
    )


def _failed(reason: str, message: str) -> FeedbackRecordResult:
    return FeedbackRecordResult(
        ok=False,
        status=RECORD_STATUS_FAILED,
        reason=reason,
        message=message,
    )


def emit_learning_feedback(
    *,
    student_id: str | int,
    event_type: str,
    source_authority: str,
    claim_boundary: str,
    payload: Mapping[str, Any] | None = None,
    timestamp: str | None = None,
    correlation_id: str = "",
    recorder: Any | None = None,
) -> FeedbackRecordResult:
    """Emit one observed feedback event (fail-open).

    Never raises. Never changes educational decisions.
    """
    try:
        active = recorder if recorder is not None else get_learning_feedback_recorder()
        if active is None or not getattr(active, "enabled", False):
            return _skipped(
                REASON_FLAG_OFF,
                "ENABLE_LEARNING_FEEDBACK is OFF or recorder unavailable",
            )
        ts = (timestamp or "").strip() or _now_iso()
        sid = str(student_id).strip()
        body = dict(payload or {})
        corr = (correlation_id or "").strip()
        feedback_id = deterministic_feedback_id(
            student_id=sid,
            timestamp=ts,
            event_type=str(event_type).strip().lower(),
            source_authority=str(source_authority).strip().lower(),
            claim_boundary=str(claim_boundary).strip().lower(),
            payload=body,
            correlation_id=corr,
        )
        event = LearningFeedbackEvent(
            feedback_id=feedback_id,
            timestamp=ts,
            event_type=str(event_type).strip().lower(),
            source_authority=str(source_authority).strip().lower(),
            claim_boundary=str(claim_boundary).strip().lower(),
            student_id=sid,
            payload=body,
            correlation_id=corr,
        )
        return active.record(event)
    except ValueError as exc:
        logger.warning("learning_feedback_emit_schema_invalid error=%s", exc)
        reason = REASON_SCHEMA_INVALID
        msg = str(exc)
        if "forbidden inference" in msg.lower():
            reason = REASON_FORBIDDEN_INFERENCE
        return _failed(reason, msg)
    except Exception as exc:  # noqa: BLE001 — emitters must not raise
        logger.warning("learning_feedback_emit_failed error=%s", exc)
        return _failed(REASON_RECORDER_ERROR, str(exc))


def emit_recommendation_decision_feedback(
    *,
    user_id: int,
    accepted: bool,
    recommendation_title: str = "",
    recommendation_category: str = "",
    correlation_id: str = "",
    recorder: Any | None = None,
) -> FeedbackRecordResult:
    """Emit preference-journal accept/dismiss evidence (RecommendationService)."""
    event_type = (
        FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED
        if accepted
        else FEEDBACK_EVENT_RECOMMENDATION_DISMISSED
    )
    return emit_learning_feedback(
        student_id=user_id,
        event_type=event_type,
        source_authority=SOURCE_RECOMMENDATION,
        claim_boundary=CLAIM_PREFERENCE_JOURNAL,
        payload={
            "accepted": bool(accepted),
            "recommendation_title": str(recommendation_title or "")[:255],
            "recommendation_category": str(recommendation_category or "")[:100],
        },
        correlation_id=correlation_id,
        recorder=recorder,
    )


def emit_plan_completed_feedback(
    *,
    user_id: int,
    mission_id: int | None = None,
    study_plan_id: int | None = None,
    mission_title: str = "",
    correlation_id: str = "",
    recorder: Any | None = None,
) -> FeedbackRecordResult:
    """Emit plan/mission completion evidence (PlanningService)."""
    return emit_learning_feedback(
        student_id=user_id,
        event_type=FEEDBACK_EVENT_PLAN_COMPLETED,
        source_authority=SOURCE_PLANNING,
        claim_boundary=CLAIM_PLAN_INTERACTION,
        payload={
            "mission_id": mission_id,
            "study_plan_id": study_plan_id,
            "mission_title": str(mission_title or "")[:255],
        },
        correlation_id=correlation_id,
        recorder=recorder,
    )


def emit_planning_recovery_feedback(
    *,
    user_id: int,
    mission_missed_count: int = 0,
    recovery_mode: bool = True,
    correlation_id: str = "",
    recorder: Any | None = None,
) -> list[FeedbackRecordResult]:
    """Emit missed-session + recovery evidence from a plan projection."""
    results: list[FeedbackRecordResult] = []
    missed = max(0, int(mission_missed_count or 0))
    if missed > 0:
        results.append(
            emit_learning_feedback(
                student_id=user_id,
                event_type=FEEDBACK_EVENT_SESSION_MISSED,
                source_authority=SOURCE_PLANNING,
                claim_boundary=CLAIM_OBSERVED_BEHAVIOUR,
                payload={"mission_missed_count": missed},
                correlation_id=correlation_id,
                recorder=recorder,
            )
        )
    if recovery_mode:
        results.append(
            emit_learning_feedback(
                student_id=user_id,
                event_type=FEEDBACK_EVENT_RECOVERY_APPLIED,
                source_authority=SOURCE_PLANNING,
                claim_boundary=CLAIM_PLAN_INTERACTION,
                payload={
                    "recovery_mode": True,
                    "mission_missed_count": missed,
                },
                correlation_id=correlation_id,
                recorder=recorder,
            )
        )
    return results


def emit_revision_feedback(
    *,
    user_id: int,
    adhered: bool,
    slot_count: int = 0,
    correlation_id: str = "",
    recorder: Any | None = None,
) -> FeedbackRecordResult:
    """Emit revision adherence / deferral evidence (PlanningService)."""
    event_type = (
        FEEDBACK_EVENT_REVISION_ADHERED
        if adhered
        else FEEDBACK_EVENT_REVISION_DEFERRED
    )
    return emit_learning_feedback(
        student_id=user_id,
        event_type=event_type,
        source_authority=SOURCE_PLANNING,
        claim_boundary=CLAIM_PLAN_INTERACTION,
        payload={
            "adhered": bool(adhered),
            "revision_slot_count": max(0, int(slot_count or 0)),
        },
        correlation_id=correlation_id,
        recorder=recorder,
    )


def emit_study_consistency_feedback(
    *,
    user_id: int,
    current_streak: int = 0,
    longest_streak: int | None = None,
    correlation_id: str = "",
    recorder: Any | None = None,
) -> FeedbackRecordResult:
    """Emit study consistency observation (ReadinessService)."""
    payload: dict[str, Any] = {
        "current_streak": max(0, int(current_streak or 0)),
    }
    if longest_streak is not None:
        payload["longest_streak"] = max(0, int(longest_streak or 0))
    return emit_learning_feedback(
        student_id=user_id,
        event_type=FEEDBACK_EVENT_STUDY_CONSISTENCY,
        source_authority=SOURCE_READINESS,
        claim_boundary=CLAIM_STUDY_HABIT_SIGNAL,
        payload=payload,
        correlation_id=correlation_id,
        recorder=recorder,
    )
