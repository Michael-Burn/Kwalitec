"""Progress mapping — progress summary and bar chrome for the dashboard.

Forwards already-decided workspace / statistics progress facts into Design
System progress components. Does not compute mastery, readiness, or velocity.
"""

from __future__ import annotations

from typing import Any

from presentation.design_system import ProgressBar, ProgressCard
from presentation.mission_workspace.workspace_view_model import (
    MissionWorkspaceViewModel,
)

_DEFAULT_TITLE = "Progress"
_DEFAULT_BODY = "No progress detail is available yet."
_DEFAULT_METRIC = "Progress not available"
_DEFAULT_TREND = "Not available"


class ProgressMapper:
    """Map workspace / statistics progress fields into dashboard chrome."""

    @classmethod
    def map_progress_card(
        cls,
        workspace: MissionWorkspaceViewModel | None,
        *,
        statistics: Any = None,
    ) -> ProgressCard:
        """Project progress summary into a ``ProgressCard``."""
        summary = getattr(workspace, "progress_summary", None) if workspace else None
        session = getattr(workspace, "session_progress", None) if workspace else None

        title = _text(getattr(summary, "headline", None), fallback=_DEFAULT_TITLE)
        body = _text(getattr(summary, "detail", None), fallback=_DEFAULT_BODY)
        metric = _text(
            getattr(session, "progress_label", None)
            or getattr(summary, "headline", None),
            fallback=_DEFAULT_METRIC,
        )
        trend = _text(
            getattr(session, "mastery_trend_label", None)
            or getattr(summary, "trend_label", None),
            fallback=_DEFAULT_TREND,
        )

        if body == _DEFAULT_BODY and statistics is not None:
            cue = _text(
                getattr(statistics, "progress_detail", None)
                or getattr(statistics, "summary", None)
            )
            if cue:
                body = cue

        return ProgressCard(
            title=title or _DEFAULT_TITLE,
            body=body or _DEFAULT_BODY,
            eyebrow="Progress",
            metric_label=metric,
            trend_label=_humanise(trend) if trend else _DEFAULT_TREND,
        )

    @classmethod
    def map_progress_bar(
        cls,
        workspace: MissionWorkspaceViewModel | None,
        *,
        statistics: Any = None,
    ) -> ProgressBar:
        """Project a display percent into a ``ProgressBar`` (forwarded only)."""
        session = getattr(workspace, "session_progress", None) if workspace else None
        summary = getattr(workspace, "progress_summary", None) if workspace else None
        label = _text(
            getattr(session, "progress_label", None)
            or getattr(summary, "headline", None),
            fallback=_DEFAULT_METRIC,
        )
        percent = _display_percent(workspace=workspace, statistics=statistics)
        value_text = f"{int(percent)}%" if percent > 0 else label
        return ProgressBar(label=label, percent=percent, value_text=value_text)


def _display_percent(
    *,
    workspace: MissionWorkspaceViewModel | None,
    statistics: Any,
) -> float:
    """Forward an already-supplied display percent; never invent mastery."""
    for source in (statistics, workspace):
        if source is None:
            continue
        for attr in ("progress_percent", "completion_percent", "percent"):
            raw = getattr(source, attr, None)
            value = _safe_percent(raw)
            if value is not None:
                return value

    if statistics is not None:
        completed = _safe_int(
            getattr(statistics, "sessions_completed", None)
            or getattr(statistics, "completed_sessions", None)
        )
        planned = _safe_int(
            getattr(statistics, "sessions_planned", None)
            or getattr(statistics, "planned_sessions", None)
        )
        if planned > 0:
            return min(100.0, round(100.0 * completed / planned, 1))

    session = getattr(workspace, "session_progress", None) if workspace else None
    if session is not None:
        completed = _safe_int(getattr(session, "completed_missions", None))
        session_count = _safe_int(getattr(session, "session_count", None))
        if session_count > 0:
            return min(100.0, round(100.0 * completed / session_count, 1))
    return 0.0


def _safe_percent(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if number < 0:
        return 0.0
    if number > 100:
        return 100.0
    return number


def _safe_int(value: Any) -> int:
    if value is None or isinstance(value, bool):
        return 0
    if isinstance(value, int):
        return max(0, value)
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return 0


def _text(value: Any, *, fallback: str = "") -> str:
    if value is None:
        return fallback
    cleaned = str(value).strip()
    return cleaned if cleaned else fallback


def _humanise(value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        return cleaned
    return cleaned.replace("_", " ").replace("-", " ").strip().capitalize()
