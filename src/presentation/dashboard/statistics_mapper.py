"""Statistics mapping — learning statistics and streak chrome.

Forwards already-decided Twin / evidence / statistics display facts into
Design System tiles. Does not diagnose, score mastery, or invent metrics.
"""

from __future__ import annotations

from typing import Any

from presentation.dashboard.dashboard_view_model import StreakView
from presentation.design_system import Badge, StatisticTile, Tone
from presentation.mission_workspace.workspace_view_model import (
    MissionWorkspaceViewModel,
)

_EMPTY_VALUE = "Not available"
_STREAK_HEADLINE = "Current streak"
_STREAK_EMPTY = "No active study streak yet."


class StatisticsMapper:
    """Map Twin / evidence / study statistics into dashboard tiles."""

    @classmethod
    def map_learning_statistics(
        cls,
        *,
        statistics: Any = None,
        twin: Any = None,
        evidence_history: Any = None,
        workspace: MissionWorkspaceViewModel | None = None,
        result: Any = None,
    ) -> tuple[StatisticTile, ...]:
        """Project learning statistics into ``StatisticTile`` chrome."""
        tiles: list[StatisticTile] = []

        sessions = _first_int(
            statistics,
            "sessions_completed",
            "completed_sessions",
            "session_count",
        )
        if sessions is None and workspace is not None:
            session = getattr(workspace, "session_progress", None)
            candidate = _safe_int(getattr(session, "completed_missions", None))
            if candidate > 0:
                sessions = candidate
        if sessions is not None:
            tiles.append(
                StatisticTile(
                    label="Sessions completed",
                    value=str(sessions),
                    detail="Completed learning sessions",
                )
            )

        minutes = _first_int(
            statistics,
            "total_minutes",
            "study_minutes",
            "planned_minutes",
        )
        if minutes is None and workspace is not None:
            session = getattr(workspace, "session_progress", None)
            candidate = _safe_int(getattr(session, "planned_minutes", None))
            if candidate > 0:
                minutes = candidate
        if minutes is None and result is not None:
            experience = getattr(result, "student_experience", None)
            summary = (
                getattr(experience, "session_summary", None) if experience else None
            )
            candidate = _safe_int(getattr(summary, "planned_minutes", None))
            if candidate > 0:
                minutes = candidate
        if minutes is not None:
            tiles.append(
                StatisticTile(
                    label="Study minutes",
                    value=str(minutes),
                    detail="Recorded or planned focus time",
                )
            )

        concepts = _first_int(
            statistics,
            "concepts_practiced",
            "concept_count",
            "concepts",
        )
        if concepts is None and twin is not None:
            states = getattr(twin, "concept_states", None)
            if states is not None:
                concepts = len(_as_tuple(states))
        if concepts is not None:
            tiles.append(
                StatisticTile(
                    label="Concepts tracked",
                    value=str(concepts),
                    detail="Concepts remembered in your learning profile",
                )
            )

        evidence_count = _first_int(
            statistics,
            "evidence_count",
            "evidence_records",
        )
        if evidence_count is None:
            evidence_count = _evidence_count(evidence_history, twin)
        if evidence_count is not None:
            tiles.append(
                StatisticTile(
                    label="Evidence records",
                    value=str(evidence_count),
                    detail="Captured learning evidence",
                )
            )

        mastery_label = _twin_mastery_label(twin) or _text(
            getattr(statistics, "mastery_label", None)
        )
        if mastery_label:
            tiles.append(
                StatisticTile(
                    label="Mastery posture",
                    value=_humanise(mastery_label),
                    detail="Forwarded from your learning profile",
                )
            )

        confidence_label = _twin_confidence_label(twin) or _text(
            getattr(statistics, "confidence_label", None)
        )
        if confidence_label:
            tiles.append(
                StatisticTile(
                    label="Confidence posture",
                    value=_humanise(confidence_label),
                    detail="Forwarded from your learning profile",
                )
            )

        if not tiles:
            tiles.append(
                StatisticTile(
                    label="Learning statistics",
                    value=_EMPTY_VALUE,
                    detail="Statistics will appear as you study",
                )
            )
        return tuple(tiles)

    @classmethod
    def map_streak(
        cls,
        *,
        statistics: Any = None,
        result: Any = None,
        twin: Any = None,
    ) -> StreakView:
        """Project current streak facts into a ``StreakView``."""
        experience = getattr(result, "student_experience", None) if result else None
        streak = getattr(experience, "streak", None) if experience else None

        current = _first_int(statistics, "current_streak_days", "streak_days")
        longest = _first_int(statistics, "longest_streak_days", "longest_streak")
        band = ""
        detail = ""

        if streak is not None:
            if current is None:
                current = _safe_int(getattr(streak, "current_days", None))
            if longest is None:
                longest = _safe_int(getattr(streak, "longest_days", None))
            band = _enum_or_text(getattr(streak, "band", None))
            detail = _text(getattr(streak, "explanation", None))

        if current is None:
            current = _safe_int(getattr(twin, "current_streak_days", None))
        if longest is None:
            longest = _safe_int(getattr(twin, "longest_streak_days", None))

        current = current or 0
        longest = max(longest or 0, current)
        if not detail:
            if current <= 0:
                detail = _STREAK_EMPTY
            elif current == 1:
                detail = "1 day of consecutive study activity."
            else:
                detail = f"{current} days of consecutive study activity."

        value = f"{current} day" if current == 1 else f"{current} days"
        if current <= 0:
            value = "0 days"
        band_label = _humanise(band) if band else ""
        tone = Tone.SUCCESS if current >= 3 else Tone.NEUTRAL
        badge = None
        if band_label or current:
            badge = Badge(label=band_label or "Streak", tone=tone)
        tile = StatisticTile(
            label=_STREAK_HEADLINE,
            value=value,
            detail=detail,
        )
        return StreakView(
            headline=_STREAK_HEADLINE,
            detail=detail,
            current_days=current,
            longest_days=longest,
            band_label=band_label,
            tile=tile,
            badge=badge,
        )


def _evidence_count(evidence_history: Any, twin: Any) -> int | None:
    if evidence_history is not None:
        count = getattr(evidence_history, "count", None)
        if callable(count):
            try:
                return _safe_int(count())
            except TypeError:
                pass
        elif count is not None:
            return _safe_int(count)
        records = getattr(evidence_history, "records", None)
        if records is None:
            records = getattr(evidence_history, "entries", None)
        if records is not None:
            return len(_as_tuple(records))
    if twin is not None:
        history = getattr(twin, "evidence_history", None)
        if history is not None:
            return len(_as_tuple(history))
    return None


def _twin_mastery_label(twin: Any) -> str:
    if twin is None:
        return ""
    mastery = getattr(twin, "mastery", None)
    if mastery is not None:
        band = getattr(mastery, "band", mastery)
        return _enum_or_text(band)
    return _text(
        getattr(twin, "mastery_band", None) or getattr(twin, "mastery_label", None)
    )


def _twin_confidence_label(twin: Any) -> str:
    if twin is None:
        return ""
    confidence = getattr(twin, "confidence", None)
    if confidence is not None:
        overall = getattr(confidence, "overall", confidence)
        return _enum_or_text(overall)
    return _text(
        getattr(twin, "confidence_label", None)
        or getattr(twin, "confidence_level", None)
    )


def _first_int(source: Any, *attrs: str) -> int | None:
    if source is None:
        return None
    for attr in attrs:
        if hasattr(source, attr):
            raw = getattr(source, attr)
            if raw is None:
                continue
            return _safe_int(raw)
    return None


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


def _enum_or_text(value: Any) -> str:
    if value is None:
        return ""
    raw = getattr(value, "value", value)
    return _text(str(raw) if raw is not None else None)


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
