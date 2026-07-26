"""Input normalization for Adaptive Input Assembler (MS-003 A1).

Normalizes collector payloads into deterministic plain data suitable for
AdaptiveInputBundle. Does not estimate missing educational values or
derive new scores.
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import date, datetime
from typing import Any


def _canonical_scalar(value: Any) -> Any:
    if value is None or isinstance(value, bool | int | float | str):
        return value
    if isinstance(value, datetime | date):
        return value.isoformat()
    return str(value)


def normalize_mapping(value: Mapping[str, Any] | None) -> dict[str, Any]:
    """Normalize a mapping into a plain dict with string keys (sorted insert)."""
    if not value:
        return {}
    result: dict[str, Any] = {}
    for key in sorted(value.keys(), key=lambda k: str(k)):
        result[str(key)] = normalize_value(value[key])
    return result


def normalize_value(value: Any) -> Any:
    """Recursively normalize values without inventing educational content."""
    if value is None or isinstance(value, bool | int | float | str):
        return value
    if isinstance(value, datetime | date):
        return value.isoformat()
    if isinstance(value, Mapping):
        return normalize_mapping(value)
    if isinstance(value, list | tuple):
        return [normalize_value(item) for item in value]
    return _canonical_scalar(value)


def normalize_list_of_mappings(
    rows: list[Mapping[str, Any]] | tuple[Mapping[str, Any], ...] | None,
    *,
    sort_keys: tuple[str, ...] = (),
) -> list[dict[str, Any]]:
    """Normalize a list of row mappings and optionally sort by stable keys."""
    if not rows:
        return []
    normalized = [normalize_mapping(row) for row in rows]
    if sort_keys:
        normalized.sort(
            key=lambda row: tuple(str(row.get(k) or "") for k in sort_keys)
        )
    return normalized


def normalize_evidence(payload: Any) -> dict[str, Any]:
    """Normalize evidence collector payload."""
    if not isinstance(payload, Mapping):
        return {"attempt_count": 0, "authorised_count": 0, "attempts": []}
    attempts = normalize_list_of_mappings(
        payload.get("attempts") or [],
        sort_keys=("study_date", "attempt_id"),
    )
    return {
        "attempt_count": int(payload.get("attempt_count") or len(attempts)),
        "authorised_count": int(payload.get("authorised_count") or 0),
        "attempts": attempts,
    }


def normalize_topic_progress(payload: Any) -> list[dict[str, Any]]:
    """Normalize topic progress list."""
    if not isinstance(payload, list | tuple):
        return []
    return normalize_list_of_mappings(
        list(payload),
        sort_keys=("topic_id", "topic_progress_id"),
    )


def normalize_study_attempts(payload: Any) -> list[dict[str, Any]]:
    """Normalize study attempt list."""
    if not isinstance(payload, list | tuple):
        return []
    return normalize_list_of_mappings(
        list(payload),
        sort_keys=("study_date", "attempt_id"),
    )


def normalize_mission(payload: Any) -> dict[str, Any]:
    """Normalize mission history payload."""
    if not isinstance(payload, Mapping):
        return {"today": None, "history": [], "history_count": 0}
    history = normalize_list_of_mappings(
        payload.get("history") or [],
        sort_keys=("mission_date", "mission_id"),
    )
    today = payload.get("today")
    return {
        "today": None if today is None else normalize_mapping(today),
        "history": history,
        "history_count": int(payload.get("history_count") or len(history)),
    }


def normalize_readiness(payload: Any) -> dict[str, Any]:
    """Normalize readiness pass-through aggregates."""
    if not isinstance(payload, Mapping):
        return {
            "overall": {},
            "coverage": {},
            "review_backlog": {},
            "streaks": {},
            "current_streak": None,
            "longest_streak": None,
        }
    streaks = normalize_mapping(payload.get("streaks"))
    current = payload.get("current_streak")
    longest = payload.get("longest_streak")
    if current is None and streaks:
        current = streaks.get("current_streak")
    if longest is None and streaks:
        longest = streaks.get("longest_streak")
    return {
        "overall": normalize_mapping(payload.get("overall")),
        "coverage": normalize_mapping(payload.get("coverage")),
        "review_backlog": normalize_mapping(payload.get("review_backlog")),
        "streaks": streaks,
        "current_streak": current,
        "longest_streak": longest,
    }


def normalize_curriculum(payload: Any) -> dict[str, Any]:
    """Normalize curriculum context."""
    if not isinstance(payload, Mapping):
        return {
            "curriculum_id": "",
            "exam_name": "",
            "version": "",
            "leaves": [],
            "leaf_count": 0,
        }
    leaves = normalize_list_of_mappings(
        payload.get("leaves") or [],
        sort_keys=("order", "topic_id"),
    )
    return {
        "curriculum_id": str(payload.get("curriculum_id") or ""),
        "exam_name": str(payload.get("exam_name") or ""),
        "version": str(payload.get("version") or ""),
        "leaves": leaves,
        "leaf_count": int(payload.get("leaf_count") or len(leaves)),
    }


def normalize_student_goals(payload: Any) -> dict[str, Any]:
    """Normalize student goals from StudyPlan."""
    if not isinstance(payload, Mapping):
        return {}
    return normalize_mapping(payload)


def normalize_lifecycle_stage(payload: Any) -> str:
    """Normalize lifecycle stage string."""
    if isinstance(payload, Mapping):
        return str(payload.get("stage") or "").strip().lower()
    return str(payload or "").strip().lower()
