"""Confidence and difficulty scale chrome for Reflection Workspace.

Qualitative self-report options only. Never scores mastery, diagnoses
understanding, or invents educational meaning from a selected level.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from presentation.design_system import Chip, Tone


class ConfidenceLevel(StrEnum):
    """Student-reported confidence band (presentation vocabulary)."""

    NOT_CONFIDENT = "not_confident"
    SLIGHTLY = "slightly"
    MODERATELY = "moderately"
    CONFIDENT = "confident"
    VERY_CONFIDENT = "very_confident"


class DifficultyLevel(StrEnum):
    """Student-reported perceived difficulty (presentation vocabulary)."""

    VERY_EASY = "very_easy"
    EASY = "easy"
    ABOUT_RIGHT = "about_right"
    HARD = "hard"
    VERY_HARD = "very_hard"


_CONFIDENCE_LABELS: dict[ConfidenceLevel, str] = {
    ConfidenceLevel.NOT_CONFIDENT: "Not confident",
    ConfidenceLevel.SLIGHTLY: "Slightly confident",
    ConfidenceLevel.MODERATELY: "Moderately confident",
    ConfidenceLevel.CONFIDENT: "Confident",
    ConfidenceLevel.VERY_CONFIDENT: "Very confident",
}

_DIFFICULTY_LABELS: dict[DifficultyLevel, str] = {
    DifficultyLevel.VERY_EASY: "Very easy",
    DifficultyLevel.EASY: "Easy",
    DifficultyLevel.ABOUT_RIGHT: "About right",
    DifficultyLevel.HARD: "Hard",
    DifficultyLevel.VERY_HARD: "Very hard",
}

_CONFIDENCE_ORDER: tuple[ConfidenceLevel, ...] = (
    ConfidenceLevel.NOT_CONFIDENT,
    ConfidenceLevel.SLIGHTLY,
    ConfidenceLevel.MODERATELY,
    ConfidenceLevel.CONFIDENT,
    ConfidenceLevel.VERY_CONFIDENT,
)

_DIFFICULTY_ORDER: tuple[DifficultyLevel, ...] = (
    DifficultyLevel.VERY_EASY,
    DifficultyLevel.EASY,
    DifficultyLevel.ABOUT_RIGHT,
    DifficultyLevel.HARD,
    DifficultyLevel.VERY_HARD,
)


@dataclass(frozen=True, slots=True)
class ScaleOptionView:
    """One selectable option on a qualitative scale."""

    key: str
    label: str
    selected: bool = False
    chip: Chip | None = None


@dataclass(frozen=True, slots=True)
class ConfidenceScaleView:
    """Immutable scale chrome for confidence or difficulty capture."""

    prompt: str
    options: tuple[ScaleOptionView, ...]
    selected_key: str = ""
    selected_label: str = ""
    scale_kind: str = "confidence"


class ConfidenceScale:
    """Build Design System chip scales for reflection self-report fields."""

    @classmethod
    def confidence(
        cls,
        *,
        prompt: str = "How confident do you feel about this session?",
        selected: str | ConfidenceLevel | None = None,
    ) -> ConfidenceScaleView:
        """Render the confidence self-report scale."""
        allowed = {level.value for level in _CONFIDENCE_ORDER}
        selected_key = _normalise_key(selected, allowed=allowed)
        options = tuple(
            _option(
                key=level.value,
                label=_CONFIDENCE_LABELS[level],
                selected=level.value == selected_key,
            )
            for level in _CONFIDENCE_ORDER
        )
        fallback_prompt = "How confident do you feel about this session?"
        return ConfidenceScaleView(
            prompt=_text(prompt, fallback=fallback_prompt),
            options=options,
            selected_key=selected_key,
            selected_label=_CONFIDENCE_LABELS.get(
                ConfidenceLevel(selected_key), ""
            )
            if selected_key
            else "",
            scale_kind="confidence",
        )

    @classmethod
    def difficulty(
        cls,
        *,
        prompt: str = "How difficult did this session feel?",
        selected: str | DifficultyLevel | None = None,
    ) -> ConfidenceScaleView:
        """Render the perceived-difficulty self-report scale."""
        selected_key = _normalise_key(
            selected, allowed={level.value for level in _DIFFICULTY_ORDER}
        )
        options = tuple(
            _option(
                key=level.value,
                label=_DIFFICULTY_LABELS[level],
                selected=level.value == selected_key,
            )
            for level in _DIFFICULTY_ORDER
        )
        return ConfidenceScaleView(
            prompt=_text(prompt, fallback="How difficult did this session feel?"),
            options=options,
            selected_key=selected_key,
            selected_label=_DIFFICULTY_LABELS.get(
                DifficultyLevel(selected_key), ""
            )
            if selected_key
            else "",
            scale_kind="difficulty",
        )

    @classmethod
    def confidence_label(cls, key: str | ConfidenceLevel | None) -> str:
        """Return the display label for a confidence key, or empty."""
        normalised = _normalise_key(
            key, allowed={level.value for level in _CONFIDENCE_ORDER}
        )
        if not normalised:
            return ""
        return _CONFIDENCE_LABELS[ConfidenceLevel(normalised)]

    @classmethod
    def difficulty_label(cls, key: str | DifficultyLevel | None) -> str:
        """Return the display label for a difficulty key, or empty."""
        normalised = _normalise_key(
            key, allowed={level.value for level in _DIFFICULTY_ORDER}
        )
        if not normalised:
            return ""
        return _DIFFICULTY_LABELS[DifficultyLevel(normalised)]


def _option(*, key: str, label: str, selected: bool) -> ScaleOptionView:
    return ScaleOptionView(
        key=key,
        label=label,
        selected=selected,
        chip=Chip(
            label=label,
            selected=selected,
            tone=Tone.PRIMARY if selected else Tone.NEUTRAL,
        ),
    )


def _normalise_key(
    value: str | ConfidenceLevel | DifficultyLevel | None,
    *,
    allowed: set[str],
) -> str:
    if value is None:
        return ""
    raw = getattr(value, "value", value)
    cleaned = str(raw).strip().lower().replace(" ", "_").replace("-", "_")
    return cleaned if cleaned in allowed else ""


def _text(value: str | None, *, fallback: str = "") -> str:
    if value is None:
        return fallback
    cleaned = str(value).strip()
    return cleaned if cleaned else fallback
