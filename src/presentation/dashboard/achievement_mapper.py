"""Achievement mapping — recognition chrome for the dashboard.

Forwards already-recognised achievement presentation facts into Design System
cards. Does not invent achievements, declare mastery, or alter educational
decisions.
"""

from __future__ import annotations

from typing import Any

from presentation.dashboard.dashboard_view_model import AchievementView
from presentation.design_system import Badge, Card, CardVariant, Tone

_EMPTY_TITLE = "No achievements yet"
_EMPTY_MESSAGE = "Achievements will appear as you build study continuity."


class AchievementMapper:
    """Map achievement collections into dashboard achievement views."""

    @classmethod
    def map_achievements(
        cls,
        achievements: Any = None,
        *,
        result: Any = None,
    ) -> tuple[AchievementView, ...]:
        """Project achievements into immutable ``AchievementView`` chrome."""
        items = _resolve_achievements(achievements=achievements, result=result)
        views: list[AchievementView] = []
        for index, item in enumerate(items, start=1):
            if item is None:
                continue
            title = _text(getattr(item, "title", None), fallback="Achievement")
            message = _text(
                getattr(item, "message", None) or getattr(item, "detail", None),
                fallback="",
            )
            kind = _enum_or_text(getattr(item, "kind", None))
            sequence = _safe_int(getattr(item, "sequence", None)) or index
            kind_label = _humanise(kind) if kind else ""
            badge = Badge(
                label=kind_label or "Achievement",
                tone=Tone.SUCCESS if kind else Tone.NEUTRAL,
            )
            card = Card(
                title=title,
                body=message,
                eyebrow=kind_label or "Achievement",
                variant=CardVariant.DEFAULT,
            )
            views.append(
                AchievementView(
                    title=title,
                    message=message,
                    kind_label=kind_label,
                    sequence=sequence,
                    badge=badge,
                    card=card,
                )
            )

        if not views:
            return (
                AchievementView(
                    title=_EMPTY_TITLE,
                    message=_EMPTY_MESSAGE,
                    kind_label="",
                    sequence=0,
                    badge=Badge(label="Achievements", tone=Tone.NEUTRAL),
                    card=Card(
                        title=_EMPTY_TITLE,
                        body=_EMPTY_MESSAGE,
                        eyebrow="Achievements",
                        variant=CardVariant.DEFAULT,
                    ),
                ),
            )
        return tuple(views)


def _resolve_achievements(*, achievements: Any, result: Any) -> tuple[Any, ...]:
    if achievements is not None:
        if isinstance(achievements, tuple | list):
            return tuple(achievements)
        items = getattr(achievements, "achievements", None)
        if items is not None:
            return _as_tuple(items)
        items = getattr(achievements, "items", None)
        if items is not None:
            return _as_tuple(items)
        try:
            return tuple(achievements)
        except TypeError:
            return ()

    experience = getattr(result, "student_experience", None) if result else None
    return _as_tuple(getattr(experience, "achievements", ()))


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
