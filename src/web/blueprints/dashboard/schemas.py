"""Request validation for the Dashboard API."""

from __future__ import annotations

from typing import Any

from application.errors import ApplicationError
from application.queries.get_dashboard import GetDashboard
from application.queries.get_progress_summary import GetProgressSummary
from application.queries.get_recommendations import GetRecommendations
from application.queries.get_timeline import GetTimeline
from application.queries.get_todays_mission import GetTodaysMission
from application.read_models.serialization import to_dashboard_json


def serialize_read_model(read_model: Any) -> dict[str, Any] | None:
    """Serialize a read model (or ``None``) into a JSON-ready payload."""
    if read_model is None:
        return None
    return to_dashboard_json(read_model)


def parse_get_dashboard(args: Any) -> GetDashboard:
    data = _as_mapping(args)
    return GetDashboard(
        student_id=_require_str(data, "student_id"),
        episode_id=_optional_str(data, "episode_id"),
    )


def parse_get_todays_mission(args: Any) -> GetTodaysMission:
    data = _as_mapping(args)
    return GetTodaysMission(
        student_id=_require_str(data, "student_id"),
        episode_id=_require_str(data, "episode_id"),
    )


def parse_get_progress(args: Any) -> GetProgressSummary:
    data = _as_mapping(args)
    return GetProgressSummary(student_id=_require_str(data, "student_id"))


def parse_get_recommendations(args: Any) -> GetRecommendations:
    data = _as_mapping(args)
    return GetRecommendations(
        student_id=_require_str(data, "student_id"),
        episode_id=_optional_str(data, "episode_id"),
    )


def parse_get_timeline(args: Any) -> GetTimeline:
    data = _as_mapping(args)
    return GetTimeline(student_id=_require_str(data, "student_id"))


def _as_mapping(args: Any) -> dict[str, Any]:
    if args is None:
        return {}
    if hasattr(args, "to_dict"):
        return dict(args.to_dict())  # type: ignore[no-untyped-call]
    if isinstance(args, dict):
        return args
    try:
        return dict(args)
    except (TypeError, ValueError) as exc:
        raise ApplicationError("query parameters must be a mapping") from exc


def _require_str(data: dict[str, Any], field: str) -> str:
    value = data.get(field)
    if isinstance(value, list):
        value = value[0] if value else None
    if not isinstance(value, str) or not value.strip():
        raise ApplicationError(f"missing or invalid field: {field}")
    return value.strip()


def _optional_str(data: dict[str, Any], field: str) -> str | None:
    if field not in data or data[field] is None:
        return None
    value = data[field]
    if isinstance(value, list):
        value = value[0] if value else None
    if value is None:
        return None
    if not isinstance(value, str):
        raise ApplicationError(f"invalid field: {field}")
    cleaned = value.strip()
    return cleaned or None
