"""Accessibility checks for design-system colour and component contracts."""

from __future__ import annotations

import pytest

from presentation.design_system import (
    SEMANTIC_COLOURS,
    SemanticColour,
    contrast_ratio,
    danger_button,
    meets_contrast,
    primary_button,
    secondary_button,
)
from presentation.design_system.contrast import parse_hex


def test_parse_hex_rejects_rgba() -> None:
    assert parse_hex("#1E2430") == (30, 36, 48)
    assert parse_hex("rgba(59, 79, 184, 0.28)") is None


@pytest.mark.parametrize(
    ("fg", "bg", "minimum"),
    [
        (SemanticColour.TEXT, SemanticColour.SURFACE, 4.5),
        (SemanticColour.TEXT, SemanticColour.BACKGROUND, 4.5),
        (SemanticColour.ON_PRIMARY, SemanticColour.PRIMARY, 4.5),
        (SemanticColour.ON_DANGER, SemanticColour.DANGER, 4.5),
        (SemanticColour.TEXT_SECONDARY, SemanticColour.SURFACE, 4.5),
    ],
)
def test_core_text_pairs_meet_wcag_aa(
    fg: SemanticColour, bg: SemanticColour, minimum: float
) -> None:
    fg_hex = SEMANTIC_COLOURS[fg].hex
    bg_hex = SEMANTIC_COLOURS[bg].hex
    ratio = contrast_ratio(fg_hex, bg_hex)
    assert ratio is not None
    assert ratio >= minimum
    assert meets_contrast(fg_hex, bg_hex, minimum=minimum)


def test_primary_and_danger_buttons_declare_contrast_pairs() -> None:
    for factory in (primary_button, danger_button, secondary_button):
        button = factory("Action")
        a11y = button.accessibility()
        assert a11y.keyboard_focusable
        assert a11y.label_required
        assert a11y.contrast_fg is not None
        assert a11y.contrast_bg is not None
        fg = SEMANTIC_COLOURS[a11y.contrast_fg].hex
        bg = SEMANTIC_COLOURS[a11y.contrast_bg].hex
        if parse_hex(fg) and parse_hex(bg):
            assert meets_contrast(fg, bg, minimum=a11y.min_contrast_ratio)


def test_muted_on_surface_is_readable() -> None:
    """Muted text must remain above AA for large/secondary use (3:1 floor)."""
    ratio = contrast_ratio(
        SEMANTIC_COLOURS[SemanticColour.MUTED].hex,
        SEMANTIC_COLOURS[SemanticColour.SURFACE].hex,
    )
    assert ratio is not None
    assert ratio >= 3.0


def test_focus_ring_token_present() -> None:
    assert SemanticColour.FOCUS_RING in SEMANTIC_COLOURS
