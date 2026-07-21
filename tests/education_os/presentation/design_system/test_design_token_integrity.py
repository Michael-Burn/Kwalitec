"""Design token integrity — every value tokenised and brand-aligned."""

from __future__ import annotations

from presentation.design_system import (
    BRAND_COLOURS,
    SEMANTIC_COLOURS,
    SPACING,
    TOKENS,
    TYPE_STYLES,
    BrandColour,
    SemanticColour,
    SpacingToken,
    TypeRole,
    get_tokens,
)
from presentation.design_system.colours import (
    UI_FORBIDDEN_BRAND_COLOURS,
    is_ui_chrome_safe,
)
from presentation.design_system.spacing import (
    ALLOWED_SPACING_PX,
    assert_spacing_integrity,
)
from presentation.design_system.typography import (
    CANONICAL_TYPE_SIZES_PX,
    FONT_FAMILY_SANS,
)


def test_get_tokens_returns_canonical_catalogue() -> None:
    tokens = get_tokens()
    assert tokens is TOKENS
    assert tokens.icon_library == "lucide"


def test_brand_primary_blue_matches_bi000() -> None:
    assert BRAND_COLOURS[BrandColour.PRIMARY_BLUE].hex.upper() == "#3B4FB8"
    assert SEMANTIC_COLOURS[SemanticColour.PRIMARY].hex.upper() == "#3B4FB8"


def test_gold_is_not_a_ui_chrome_semantic() -> None:
    assert BrandColour.GOLD in UI_FORBIDDEN_BRAND_COLOURS
    assert not is_ui_chrome_safe(BrandColour.GOLD)
    warning = SEMANTIC_COLOURS[SemanticColour.WARNING].hex.upper()
    assert warning != BRAND_COLOURS[BrandColour.GOLD].hex.upper()


def test_required_semantic_colours_present() -> None:
    required = {
        SemanticColour.PRIMARY,
        SemanticColour.SECONDARY,
        SemanticColour.SUCCESS,
        SemanticColour.WARNING,
        SemanticColour.DANGER,
        SemanticColour.INFO,
        SemanticColour.SURFACE,
        SemanticColour.BACKGROUND,
        SemanticColour.BORDER,
        SemanticColour.TEXT,
        SemanticColour.MUTED,
    }
    assert required <= set(SEMANTIC_COLOURS)


def test_spacing_scale_is_eight_point_grid() -> None:
    assert_spacing_integrity()
    for value in SPACING.values():
        assert value.px in ALLOWED_SPACING_PX


def test_spacing_tokens_cover_ux001_scale() -> None:
    pixels = {value.px for value in SPACING.values()}
    assert {4, 8, 12, 16, 24, 32, 48, 64, 96, 128} <= pixels
    assert SpacingToken.XS in SPACING


def test_typography_roles_and_inter_family() -> None:
    for role in TypeRole:
        assert role in TYPE_STYLES
    assert TYPE_STYLES[TypeRole.DISPLAY].size_px == 40
    assert TYPE_STYLES[TypeRole.HEADING].size_px == 28
    assert TYPE_STYLES[TypeRole.SUBHEADING].size_px == 20
    assert TYPE_STYLES[TypeRole.BODY].size_px == 16
    assert TYPE_STYLES[TypeRole.CAPTION].size_px == 14
    assert "Inter" in TYPE_STYLES[TypeRole.BODY].family
    assert TYPE_STYLES[TypeRole.BODY].family == FONT_FAMILY_SANS
    sizes = {style.size_px for style in TYPE_STYLES.values()}
    assert sizes <= CANONICAL_TYPE_SIZES_PX | {14}  # mono also 14


def test_css_custom_properties_are_complete() -> None:
    props = TOKENS.css_custom_properties()
    assert "--primary" in props
    assert "--space-lg" in props
    assert "--radius-lg" in props
    assert "--shadow-sm" in props
    assert props["--primary"].upper() == "#3B4FB8"


def test_no_duplicate_semantic_css_vars() -> None:
    vars_ = [value.css_var for value in SEMANTIC_COLOURS.values()]
    assert len(vars_) == len(set(vars_))
