"""Mission progress mapping — presentation formatting of progress fields.

Forwards ProgressReport and SessionSummary display facts into workspace view
snippets. Does not compute mastery, readiness, velocity, or next actions.
"""

from __future__ import annotations

from typing import Any

from presentation.mission_workspace.workspace_view_model import (
    ProgressSummaryView,
    SessionProgressView,
)

_EMPTY_TREND = "Not available"
_EMPTY_HEADLINE = "Progress summary"
_EMPTY_DETAIL = "No progress detail is available for this session yet."


class MissionProgressMapper:
    """Map pipeline progress artefacts into immutable presentation views."""

    @classmethod
    def map_progress_summary(cls, result: Any) -> ProgressSummaryView:
        """Project progress report text into a ``ProgressSummaryView``.

        Args:
            result: A ``PipelineResult`` (or structural equivalent) exposing
                ``progress_report``.

        Returns:
            Immutable progress summary suitable for workspace rendering.
        """
        report = getattr(result, "progress_report", None)
        if report is None:
            return ProgressSummaryView(
                headline=_EMPTY_HEADLINE,
                detail=_EMPTY_DETAIL,
                trend_label=_EMPTY_TREND,
                confidence_label=_EMPTY_TREND,
                metric_lines=(),
            )

        mastery = getattr(report, "mastery_trend", None)
        confidence = getattr(report, "confidence_trend", None)
        trend_label = _enum_or_text(
            getattr(mastery, "direction", None),
            fallback=_EMPTY_TREND,
        )
        confidence_label = _enum_or_text(
            getattr(confidence, "direction", None),
            fallback=_EMPTY_TREND,
        )
        explanation = _text(
            getattr(report, "educational_explanation", None),
            fallback=_EMPTY_DETAIL,
        )
        headline = _first_sentence(explanation) or _EMPTY_HEADLINE
        metric_lines = tuple(
            _format_metric(metric)
            for metric in _as_tuple(getattr(report, "metrics", ()))
            if metric is not None
        )
        return ProgressSummaryView(
            headline=headline,
            detail=explanation,
            trend_label=_humanise(trend_label),
            confidence_label=_humanise(confidence_label),
            metric_lines=metric_lines,
        )

    @classmethod
    def map_session_progress(cls, result: Any) -> SessionProgressView:
        """Project session summary and plan counts into ``SessionProgressView``.

        Args:
            result: A ``PipelineResult`` (or structural equivalent) exposing
                ``student_experience`` and optionally ``study_plan``.

        Returns:
            Immutable session progress view for workspace rendering.
        """
        experience = getattr(result, "student_experience", None)
        summary = getattr(experience, "session_summary", None) if experience else None
        plan = getattr(result, "study_plan", None)

        session_count = _session_count(plan)
        if summary is None:
            return SessionProgressView(
                completed_missions=0,
                planned_minutes=0,
                objective_preview="",
                mastery_trend_label=_EMPTY_TREND,
                confidence_trend_label=_EMPTY_TREND,
                session_count=session_count,
                progress_label="Session progress not available",
            )

        completed = _safe_int(getattr(summary, "completed_mission_count", 0))
        planned = _safe_int(getattr(summary, "planned_minutes", 0))

        mastery_label = _text(
            getattr(summary, "mastery_trend_label", None),
            fallback=_EMPTY_TREND,
        )
        confidence_label = _text(
            getattr(summary, "confidence_trend_label", None),
            fallback=_EMPTY_TREND,
        )
        objective_preview = _text(
            getattr(summary, "objective_statement", None),
            fallback="",
        )
        progress_label = _progress_label(completed=completed, planned_minutes=planned)
        return SessionProgressView(
            completed_missions=completed,
            planned_minutes=planned,
            objective_preview=objective_preview,
            mastery_trend_label=_humanise(mastery_label),
            confidence_trend_label=_humanise(confidence_label),
            session_count=session_count,
            progress_label=progress_label,
        )


def _session_count(plan: Any) -> int:
    if plan is None:
        return 0
    count = getattr(plan, "session_count", None)
    if callable(count):
        try:
            return _safe_int(count())
        except TypeError:
            return 0
    return _safe_int(count)


def _format_metric(metric: Any) -> str:
    label = _text(getattr(metric, "label", None), fallback="Metric")
    band = _text(getattr(metric, "band", None), fallback="")
    if band:
        return f"{label}: {_humanise(band)}"
    return label


def _progress_label(*, completed: int, planned_minutes: int) -> str:
    if completed == 0:
        mission_part = "No completed missions yet"
    elif completed == 1:
        mission_part = "1 completed mission"
    else:
        mission_part = f"{completed} completed missions"
    if planned_minutes <= 0:
        return mission_part
    return f"{mission_part} · {planned_minutes} min planned"


def _as_tuple(value: Any) -> tuple[Any, ...]:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    try:
        return tuple(value)
    except TypeError:
        return ()


def _safe_int(value: Any) -> int:
    if value is None or isinstance(value, bool):
        return 0
    if isinstance(value, int):
        return max(0, value)
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return 0


def _enum_or_text(value: Any, *, fallback: str) -> str:
    if value is None:
        return fallback
    raw = getattr(value, "value", value)
    return _text(str(raw) if raw is not None else None, fallback=fallback)


def _text(value: str | None, *, fallback: str = "") -> str:
    if value is None:
        return fallback
    cleaned = str(value).strip()
    return cleaned if cleaned else fallback


def _first_sentence(text: str) -> str:
    cleaned = text.strip()
    if not cleaned:
        return ""
    for separator in (". ", "! ", "? "):
        index = cleaned.find(separator)
        if index != -1:
            return cleaned[: index + 1].strip()
    return cleaned


def _humanise(value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        return cleaned
    return cleaned.replace("_", " ").replace("-", " ").strip().capitalize()
