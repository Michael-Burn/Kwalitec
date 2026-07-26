"""Canonical educational event stream for Journey + History.

Both bridges project from the same Mission / StudyAttempt stream.
Ordering and event ids must remain identical — do not duplicate sort logic.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from .journey_mapper import (
    NOT_APPLICABLE_RECOMMENDATION,
    UNAVAILABLE_RECOMMENDATION,
    build_trace_ref,
    map_timeline_item,
)


def timeline_sort_key(item: dict[str, Any]) -> tuple:
    """Stable reverse-chronological key: occurred_at then event_id."""
    return (item.get("occurred_at") or "", item.get("event_id") or "")


def order_timeline_items(
    items: list[dict[str, Any]], *, limit: int | None = None
) -> list[dict[str, Any]]:
    """Order timeline items reverse-chronologically with a stable secondary key."""
    ordered = sorted(items, key=timeline_sort_key, reverse=True)
    if limit is None:
        return ordered
    if limit <= 0:
        return []
    return ordered[:limit]


def iso_date(value: Any) -> str | None:
    """Normalise date/datetime values to ISO date strings."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def project_canonical_timeline_from_missions(
    *,
    student_id: str,
    missions: list[Any],
    attempts_by_mission: dict[Any, list[Any]],
    lifecycle_stage: str = "",
    limit: int | None = None,
) -> list[dict[str, Any]]:
    """Project EducationalTimelineEvents from Runtime A Mission + Attempt rows.

    Translator only — does not invent events or recalculate educational state.
    """
    items: list[dict[str, Any]] = []
    for mission in missions:
        status = str(getattr(mission, "status", "") or "")
        occurred = iso_date(getattr(mission, "mission_date", None))
        mid = str(mission.id)
        title = str(mission.title or "")
        attempts = list(attempts_by_mission.get(mission.id, []))

        if status == "Completed":
            attempt_ids = [str(a.id) for a in attempts]
            evidence_refs = [{"kind": "mission", "id": mid}]
            evidence_refs.extend(
                {"kind": "attempt", "id": aid} for aid in attempt_ids
            )
            items.append(
                map_timeline_item(
                    event_id=f"session-completed-{mid}",
                    event_type="SessionCompleted",
                    student_id=student_id,
                    occurred_at=occurred,
                    summary=f"Completed session: {title}",
                    authority="study_session_service",
                    mission_id=mid,
                    topic_title=title,
                    lifecycle_stage=lifecycle_stage or None,
                    trace=build_trace_ref(
                        what=f"Completed session: {title}",
                        why_summary=(
                            "Mission marked Completed after evidence path"
                        ),
                        reason_codes=["session_completed"],
                        evidence_refs=evidence_refs,
                        recommendation=dict(UNAVAILABLE_RECOMMENDATION),
                    ),
                )
            )
            for attempt in attempts:
                items.append(
                    map_timeline_item(
                        event_id=f"evidence-{attempt.id}",
                        event_type="EvidenceCommitted",
                        student_id=student_id,
                        occurred_at=iso_date(getattr(attempt, "study_date", None))
                        or occurred,
                        summary=f"Evidence recorded for: {title}",
                        authority="evidence_authority",
                        mission_id=mid,
                        topic_title=title,
                        lifecycle_stage=lifecycle_stage or None,
                        trace=build_trace_ref(
                            what=f"Evidence recorded for: {title}",
                            why_summary="StudyAttempt accepted as evidence",
                            reason_codes=["evidence_committed"],
                            evidence_refs=[
                                {"kind": "attempt", "id": str(attempt.id)},
                                {"kind": "mission", "id": mid},
                            ],
                            recommendation=dict(UNAVAILABLE_RECOMMENDATION),
                        ),
                    )
                )
        elif status == "In Progress":
            items.append(
                map_timeline_item(
                    event_id=f"session-started-{mid}",
                    event_type="SessionStarted",
                    student_id=student_id,
                    occurred_at=occurred,
                    summary=f"Session in progress: {title}",
                    authority="study_session_service",
                    mission_id=mid,
                    topic_title=title,
                    lifecycle_stage=lifecycle_stage or None,
                    trace=build_trace_ref(
                        what=f"Session in progress: {title}",
                        why_summary="Mission status In Progress",
                        reason_codes=["session_started"],
                        evidence_refs=[{"kind": "mission", "id": mid}],
                        recommendation=dict(NOT_APPLICABLE_RECOMMENDATION),
                    ),
                )
            )
        elif status == "Pending":
            items.append(
                map_timeline_item(
                    event_id=f"mission-ensured-{mid}",
                    event_type="MissionEnsured",
                    student_id=student_id,
                    occurred_at=occurred,
                    summary=f"Mission ready: {title}",
                    authority="planning_service",
                    mission_id=mid,
                    topic_title=title,
                    lifecycle_stage=lifecycle_stage or None,
                    trace=build_trace_ref(
                        what=f"Mission ready: {title}",
                        why_summary="Mission ensured by Planning",
                        reason_codes=["mission_ensured"],
                        evidence_refs=[{"kind": "mission", "id": mid}],
                        recommendation=dict(NOT_APPLICABLE_RECOMMENDATION),
                    ),
                )
            )

    return order_timeline_items(items, limit=limit)
