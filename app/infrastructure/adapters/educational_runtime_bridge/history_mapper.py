"""History → Experience opaque DTO mapping (translator only).

Projections may consume Mission / StudyAttempt / TopicProgress / Lifecycle /
Readiness / Recommendation references via Runtime A. This module never mutates
educational state or invents historical sessions.
"""

from __future__ import annotations

from typing import Any

from .contracts import (
    AUTHORITY_HISTORY_BRIDGE,
)
from .journey_mapper import (
    UNAVAILABLE_RECOMMENDATION,
    build_trace_ref,
)

# Explicit null contracts when durable series cannot be reconstructed.
UNAVAILABLE_SERIES: dict[str, Any] = {
    "points": None,
    "unavailable_reason": "unavailable",
}

DEFAULT_PAGE_LIMIT = 20
HARD_MAX_PAGE_LIMIT = 100


def clamp_limit(limit: int | None) -> int:
    """Apply default and hard-max pagination limits."""
    if limit is None:
        return DEFAULT_PAGE_LIMIT
    value = int(limit)
    if value < 0:
        return 0
    return min(value, HARD_MAX_PAGE_LIMIT)


def map_completed_session(
    *,
    session_id: str,
    mission_id: str,
    topic_title: str,
    completed_at: str | None,
    study_minutes: int | None,
    lifecycle_stage: str | None = None,
    trace: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Project one completed session card for History."""
    card: dict[str, Any] = {
        "session_id": str(session_id),
        "mission_id": str(mission_id),
        "topic_title": str(topic_title or ""),
        "completed_at": completed_at or "",
        "study_minutes": int(study_minutes or 0),
    }
    if lifecycle_stage:
        card["lifecycle_stage"] = str(lifecycle_stage)
    if trace is not None:
        card["trace"] = dict(trace)
    return card


def map_readiness_point(
    *,
    recorded_at: str,
    exam_readiness: float,
    label: str = "",
) -> dict[str, Any]:
    """Project one readiness progression sample (Runtime A values only)."""
    score = float(exam_readiness)
    if score < 0.0:
        score = 0.0
    if score > 1.0:
        score = 1.0
    return {
        "recorded_at": str(recorded_at),
        "exam_readiness": score,
        "label": str(label or ""),
    }


def map_achievement(
    *,
    achievement_id: str,
    title: str,
    earned_at: str = "",
    description: str = "",
) -> dict[str, Any]:
    """Project one progress milestone card."""
    return {
        "achievement_id": str(achievement_id),
        "title": str(title or ""),
        "earned_at": str(earned_at or ""),
        "description": str(description or ""),
    }


def map_page_meta(
    *,
    limit: int,
    offset: int,
    has_more: bool,
    next_offset: int | None = None,
    cursor: str | None = None,
    next_cursor: str | None = None,
) -> dict[str, Any]:
    """Canonical pagination contract."""
    page: dict[str, Any] = {
        "limit": int(limit),
        "offset": int(offset),
        "has_more": bool(has_more),
    }
    if next_offset is not None:
        page["next_offset"] = int(next_offset)
    if cursor is not None:
        page["cursor"] = cursor
    if next_cursor is not None:
        page["next_cursor"] = next_cursor
    return page


def empty_authentic_history(
    *,
    student_id: str,
    error_code: str | None = None,
    fallback_used: bool = False,
    limit: int = DEFAULT_PAGE_LIMIT,
    offset: int = 0,
) -> dict[str, Any]:
    """Empty authentic History projection — never Twin demo insights."""
    return {
        "student_id": student_id.strip(),
        "completed_sessions": [],
        "total_study_minutes": 0,
        "readiness_progression": None,
        "readiness_progression_meta": dict(UNAVAILABLE_SERIES),
        "mastered_topics": [],
        "revision_history": [],
        "recent_achievements": [],
        "session_count": 0,
        "mastered_count": 0,
        "recommendation_history": None,
        "recommendation_history_meta": {
            "unavailable_reason": "unavailable",
        },
        "page": map_page_meta(
            limit=limit, offset=offset, has_more=False, next_offset=None
        ),
        "authority": AUTHORITY_HISTORY_BRIDGE,
        "error_code": error_code,
        "fallback_used": bool(fallback_used),
    }


def map_history_to_projection(
    *,
    student_id: str,
    completed_sessions: list[dict[str, Any]] | None = None,
    total_study_minutes: int = 0,
    readiness_progression: list[dict[str, Any]] | None = None,
    readiness_unavailable_reason: str | None = "unavailable",
    mastered_topics: list[str] | None = None,
    revision_history: list[str] | None = None,
    recent_achievements: list[dict[str, Any]] | None = None,
    recommendation_history: list[dict[str, Any]] | None = None,
    page: dict[str, Any] | None = None,
    fallback_used: bool = False,
    error_code: str | None = None,
) -> dict[str, Any]:
    """Assemble the opaque History document for Experience.

    Counts and labels must already come from Runtime A — this only shapes DTOs.
    Missing recommendation / readiness series use explicit null contracts.
    """
    sessions = [dict(s) for s in (completed_sessions or [])]
    mastered = [str(t) for t in (mastered_topics or []) if str(t).strip()]
    minutes = int(total_study_minutes)
    if minutes < 0:
        minutes = 0

    readiness: list[dict[str, Any]] | None
    readiness_meta: dict[str, Any] | None
    if readiness_progression is None:
        readiness = None
        readiness_meta = {
            "points": None,
            "unavailable_reason": readiness_unavailable_reason or "unavailable",
        }
    else:
        readiness = [dict(p) for p in readiness_progression]
        readiness_meta = None

    return {
        "student_id": student_id.strip(),
        "completed_sessions": sessions,
        "total_study_minutes": minutes,
        "readiness_progression": readiness,
        "readiness_progression_meta": readiness_meta,
        "mastered_topics": mastered,
        "revision_history": [
            str(r) for r in (revision_history or []) if str(r).strip()
        ],
        "recent_achievements": [dict(a) for a in (recent_achievements or [])],
        "session_count": len(sessions),
        "mastered_count": len(mastered),
        # Explicit null when Runtime A cannot supply recommendation history.
        "recommendation_history": recommendation_history,
        "recommendation_history_meta": (
            None
            if recommendation_history is not None
            else {"unavailable_reason": "unavailable"}
        ),
        "page": dict(page)
        if page is not None
        else map_page_meta(limit=DEFAULT_PAGE_LIMIT, offset=0, has_more=False),
        "authority": AUTHORITY_HISTORY_BRIDGE,
        "error_code": error_code,
        "fallback_used": bool(fallback_used),
    }


def session_trace_for_mission(
    *,
    topic_title: str,
    mission_id: str,
    attempt_ids: list[str] | None = None,
) -> dict[str, Any]:
    """Build TraceRef for a completed History session card."""
    evidence_refs = [{"kind": "mission", "id": str(mission_id)}]
    for aid in attempt_ids or ():
        evidence_refs.append({"kind": "attempt", "id": str(aid)})
    return build_trace_ref(
        what=f"Completed session: {topic_title}",
        why_summary="Mission marked Completed after evidence path",
        reason_codes=["session_completed"],
        evidence_refs=evidence_refs,
        recommendation=dict(UNAVAILABLE_RECOMMENDATION),
    )
