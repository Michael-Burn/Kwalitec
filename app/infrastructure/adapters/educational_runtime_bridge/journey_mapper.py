"""Journey → Experience opaque DTO mapping (translator only).

Projections may consume StudyPlan / Mission / StudyAttempt / TopicProgress /
Lifecycle / Readiness / Recommendation references via Runtime A. This module
never mutates educational state or invents progress ratios.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.adapters.educational_runtime_bridge.contracts import (
    AUTHORITY_JOURNEY_BRIDGE,
)

# Status labels for Experience topic cards (presentation only).
_STATUS_LABELS: dict[str, str] = {
    "completed": "Completed",
    "current": "Current",
    "upcoming": "Upcoming",
}

# Explicit null recommendation contract when history is not reconstructable.
UNAVAILABLE_RECOMMENDATION: dict[str, Any] = {
    "changed": None,
    "prior_label": None,
    "next_label": None,
    "decision_ids": None,
    "unavailable_reason": "unavailable",
}

NOT_APPLICABLE_RECOMMENDATION: dict[str, Any] = {
    "changed": None,
    "prior_label": None,
    "next_label": None,
    "decision_ids": None,
    "unavailable_reason": "not_applicable",
}


def build_trace_ref(
    *,
    what: str,
    why_summary: str,
    reason_codes: list[str] | tuple[str, ...] | None = None,
    evidence_refs: list[dict[str, str]] | None = None,
    recommendation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a TraceRef block. Never fabricates recommendation deltas."""
    rec = (
        dict(recommendation)
        if recommendation is not None
        else dict(UNAVAILABLE_RECOMMENDATION)
    )
    return {
        "what": str(what or ""),
        "why": {
            "reason_codes": [str(c) for c in (reason_codes or ())],
            "summary": str(why_summary or ""),
        },
        "evidence_refs": [dict(r) for r in (evidence_refs or [])],
        "recommendation": rec,
    }


def map_topic_status(
    *,
    completed: bool,
    is_current: bool,
    stage: str | None = None,
) -> str:
    """Map TopicProgress / current-mission signals to Journey topic status."""
    stage_key = (stage or "").strip().lower()
    if completed or stage_key in {"mastered", "completed"}:
        return "completed"
    if is_current:
        return "current"
    return "upcoming"


def map_topic_card(
    *,
    topic_id: str,
    title: str,
    status: str,
    prerequisite_note: str | None = None,
    trace: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Project one curriculum topic card for Journey."""
    normalised = status if status in _STATUS_LABELS else "upcoming"
    card: dict[str, Any] = {
        "topic_id": str(topic_id),
        "title": str(title or ""),
        "status": normalised,
        "status_label": _STATUS_LABELS[normalised],
    }
    if prerequisite_note:
        card["prerequisite_note"] = str(prerequisite_note)
    if trace is not None:
        card["trace"] = dict(trace)
    return card


def map_timeline_item(
    *,
    event_id: str,
    event_type: str,
    student_id: str,
    occurred_at: str | None,
    summary: str,
    authority: str,
    mission_id: str | None = None,
    topic_code: str | None = None,
    topic_title: str | None = None,
    lifecycle_stage: str | None = None,
    trace: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Project one EducationalTimelineEvent with required TraceRef."""
    return {
        "event_id": str(event_id),
        "event_type": str(event_type),
        "student_id": student_id.strip(),
        "occurred_at": occurred_at,
        "mission_id": None if mission_id is None else str(mission_id),
        "topic_code": topic_code,
        "topic_title": topic_title,
        "lifecycle_stage": lifecycle_stage,
        "summary": str(summary or ""),
        "authority": str(authority or AUTHORITY_JOURNEY_BRIDGE),
        "trace": dict(trace)
        if trace is not None
        else build_trace_ref(
            what=str(summary or event_type),
            why_summary="",
            reason_codes=["unspecified"],
            recommendation=dict(UNAVAILABLE_RECOMMENDATION),
        ),
    }


def empty_authentic_journey(
    *,
    student_id: str,
    error_code: str | None = None,
    fallback_used: bool = False,
) -> dict[str, Any]:
    """Empty authentic Journey projection — never seeded_demo_journey."""
    return {
        "student_id": student_id.strip(),
        "has_journey": False,
        "progress": {
            "overall_progress_ratio": 0.0,
            "estimated_completion_label": "",
            "examination_label": "",
            "current_topic_id": "",
            "current_topic_title": "",
            "lifecycle_stage": "",
        },
        "topics": [],
        "active_missions": [],
        "completed_sessions_summary": {"count": 0, "recent": []},
        "timeline": [],
        "recommendation_focus": None,
        "recommendation_history": None,
        "authority": AUTHORITY_JOURNEY_BRIDGE,
        "next_action_authority": False,
        "error_code": error_code,
        "fallback_used": bool(fallback_used),
    }


def map_journey_to_projection(
    *,
    student_id: str,
    has_journey: bool,
    overall_progress_ratio: float,
    estimated_completion_label: str = "",
    examination_label: str = "",
    current_topic_id: str = "",
    current_topic_title: str = "",
    lifecycle_stage: str = "",
    topics: list[dict[str, Any]] | None = None,
    active_missions: list[dict[str, Any]] | None = None,
    completed_sessions_summary: dict[str, Any] | None = None,
    timeline: list[dict[str, Any]] | None = None,
    recommendation_focus: dict[str, Any] | None = None,
    recommendation_history: list[dict[str, Any]] | None = None,
    fallback_used: bool = False,
    error_code: str | None = None,
) -> dict[str, Any]:
    """Assemble the opaque Journey document for Experience.

    Progress ratios and labels must already come from Runtime A services —
    this function only shapes the DTO.
    """
    ratio = float(overall_progress_ratio)
    if ratio < 0.0:
        ratio = 0.0
    if ratio > 1.0:
        ratio = 1.0

    summary = completed_sessions_summary or {"count": 0, "recent": []}
    return {
        "student_id": student_id.strip(),
        "has_journey": bool(has_journey),
        "progress": {
            "overall_progress_ratio": ratio,
            "estimated_completion_label": str(estimated_completion_label or ""),
            "examination_label": str(examination_label or ""),
            "current_topic_id": str(current_topic_id or ""),
            "current_topic_title": str(current_topic_title or ""),
            "lifecycle_stage": str(lifecycle_stage or ""),
        },
        "topics": [dict(t) for t in (topics or [])],
        "active_missions": [dict(m) for m in (active_missions or [])],
        "completed_sessions_summary": {
            "count": int(summary.get("count") or 0),
            "recent": [dict(r) for r in (summary.get("recent") or [])],
        },
        "timeline": [dict(item) for item in (timeline or [])],
        # Explicit null when Runtime A cannot supply recommendation history.
        "recommendation_focus": (
            None if recommendation_focus is None else dict(recommendation_focus)
        ),
        "recommendation_history": recommendation_history,
        "authority": AUTHORITY_JOURNEY_BRIDGE,
        "next_action_authority": False,
        "error_code": error_code,
        "fallback_used": bool(fallback_used),
    }
