"""Confidence and difficulty scale rendering (V3-005)."""

from __future__ import annotations

from presentation.design_system import Chip
from presentation.reflection import (
    ConfidenceLevel,
    ConfidenceScale,
    DifficultyLevel,
)


def test_confidence_scale_renders_all_options() -> None:
    scale = ConfidenceScale.confidence()

    assert scale.scale_kind == "confidence"
    assert scale.prompt
    assert len(scale.options) == 5
    assert [option.key for option in scale.options] == [
        ConfidenceLevel.NOT_CONFIDENT.value,
        ConfidenceLevel.SLIGHTLY.value,
        ConfidenceLevel.MODERATELY.value,
        ConfidenceLevel.CONFIDENT.value,
        ConfidenceLevel.VERY_CONFIDENT.value,
    ]
    assert all(isinstance(option.chip, Chip) for option in scale.options)
    assert all(not option.selected for option in scale.options)
    assert scale.selected_key == ""
    assert scale.selected_label == ""


def test_confidence_scale_selects_level() -> None:
    scale = ConfidenceScale.confidence(selected=ConfidenceLevel.VERY_CONFIDENT)

    assert scale.selected_key == ConfidenceLevel.VERY_CONFIDENT.value
    assert scale.selected_label == "Very confident"
    selected = [option for option in scale.options if option.selected]
    assert len(selected) == 1
    assert selected[0].label == "Very confident"
    assert selected[0].chip is not None
    assert selected[0].chip.selected is True


def test_difficulty_scale_renders_and_selects() -> None:
    scale = ConfidenceScale.difficulty(selected="about_right")

    assert scale.scale_kind == "difficulty"
    assert len(scale.options) == 5
    assert scale.selected_key == DifficultyLevel.ABOUT_RIGHT.value
    assert scale.selected_label == "About right"
    assert sum(1 for option in scale.options if option.selected) == 1


def test_invalid_selection_is_ignored() -> None:
    confidence = ConfidenceScale.confidence(selected="mastered")
    difficulty = ConfidenceScale.difficulty(selected=99)  # type: ignore[arg-type]

    assert confidence.selected_key == ""
    assert confidence.selected_label == ""
    assert difficulty.selected_key == ""
    assert difficulty.selected_label == ""


def test_label_helpers() -> None:
    assert ConfidenceScale.confidence_label("confident") == "Confident"
    assert ConfidenceScale.confidence_label(None) == ""
    assert ConfidenceScale.difficulty_label(DifficultyLevel.HARD) == "Hard"
    assert ConfidenceScale.difficulty_label("unknown") == ""


def test_scale_options_are_keyboard_focusable_chips() -> None:
    scale = ConfidenceScale.confidence(selected="moderately")
    for option in scale.options:
        assert option.chip is not None
        a11y = option.chip.accessibility()
        assert a11y.role == "button"
        assert a11y.keyboard_focusable
        assert a11y.label_required
