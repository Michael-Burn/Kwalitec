"""Semantic and brand colour tokens for the V3 design system.

Values align with BI-000 / ``brand.css`` / ``tokens.css``. Gold is brand-only
(achievement, logo) and must not appear as a UI chrome semantic.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True, slots=True)
class ColourValue:
    """A single colour with hex and optional CSS custom-property name."""

    hex: str
    css_var: str
    description: str = ""


class BrandColour(str, Enum):
    """Official brand palette (BI-000)."""

    PRIMARY_BLUE = "primary_blue"
    PRIMARY_DARK = "primary_dark"
    DEEP_NAVY = "deep_navy"
    MIDNIGHT = "midnight"
    GOLD = "gold"
    GOLD_HOVER = "gold_hover"
    WHITE = "white"
    TEXT_SECONDARY_ON_DARK = "text_secondary_on_dark"
    DIVIDER_DARK = "divider_dark"


class SemanticColour(str, Enum):
    """UI semantic roles — prefer these in components."""

    PRIMARY = "primary"
    PRIMARY_HOVER = "primary_hover"
    SECONDARY = "secondary"
    SUCCESS = "success"
    WARNING = "warning"
    DANGER = "danger"
    INFO = "info"
    SURFACE = "surface"
    SURFACE_ALT = "surface_alt"
    SURFACE_ELEVATED = "surface_elevated"
    BACKGROUND = "background"
    BORDER = "border"
    BORDER_SUBTLE = "border_subtle"
    TEXT = "text"
    TEXT_SECONDARY = "text_secondary"
    MUTED = "muted"
    TEXT_INVERSE = "text_inverse"
    ON_PRIMARY = "on_primary"
    ON_SUCCESS = "on_success"
    ON_DANGER = "on_danger"
    SUCCESS_BG = "success_bg"
    WARNING_BG = "warning_bg"
    DANGER_BG = "danger_bg"
    INFO_BG = "info_bg"
    FOCUS_RING = "focus_ring"


BRAND_COLOURS: Mapping[BrandColour, ColourValue] = {
    BrandColour.PRIMARY_BLUE: ColourValue(
        "#3B4FB8", "--brand-primary-blue", "Primary Blue"
    ),
    BrandColour.PRIMARY_DARK: ColourValue(
        "#0D1B2A", "--brand-primary-dark", "Primary Dark"
    ),
    BrandColour.DEEP_NAVY: ColourValue("#0A1628", "--brand-deep-navy", "Deep Navy"),
    BrandColour.MIDNIGHT: ColourValue("#020D24", "--brand-midnight", "Midnight"),
    BrandColour.GOLD: ColourValue("#E8B02B", "--brand-gold", "Gold (achievement only)"),
    BrandColour.GOLD_HOVER: ColourValue("#F0C040", "--brand-gold-hover", "Gold hover"),
    BrandColour.WHITE: ColourValue("#FFFFFF", "--brand-white", "White"),
    BrandColour.TEXT_SECONDARY_ON_DARK: ColourValue(
        "#8B93A7", "--brand-text-secondary", "Text secondary on dark"
    ),
    BrandColour.DIVIDER_DARK: ColourValue("#1E2A3D", "--brand-divider", "Dark divider"),
}

# Light-theme semantic defaults (UX-001 / tokens.css).
SEMANTIC_COLOURS: Mapping[SemanticColour, ColourValue] = {
    SemanticColour.PRIMARY: ColourValue("#3B4FB8", "--primary", "Primary action"),
    SemanticColour.PRIMARY_HOVER: ColourValue(
        "#2F3F96", "--primary-hover", "Primary hover"
    ),
    SemanticColour.SECONDARY: ColourValue("#475569", "--secondary", "Secondary chrome"),
    SemanticColour.SUCCESS: ColourValue("#0F766E", "--success", "Success"),
    SemanticColour.WARNING: ColourValue("#A16207", "--warning", "Warning (not gold)"),
    SemanticColour.DANGER: ColourValue("#C81E1E", "--danger", "Danger"),
    SemanticColour.INFO: ColourValue("#3B4FB8", "--info", "Info"),
    SemanticColour.SURFACE: ColourValue("#FFFFFF", "--surface", "Surface"),
    SemanticColour.SURFACE_ALT: ColourValue(
        "#F4F6F9", "--surface-alt", "Alternate surface"
    ),
    SemanticColour.SURFACE_ELEVATED: ColourValue(
        "#FFFFFF", "--surface-elevated", "Elevated surface"
    ),
    SemanticColour.BACKGROUND: ColourValue(
        "#F4F6F9", "--background", "Page background"
    ),
    SemanticColour.BORDER: ColourValue("#D5DAE3", "--border", "Border"),
    SemanticColour.BORDER_SUBTLE: ColourValue(
        "#E6E9EF", "--border-subtle", "Subtle border"
    ),
    SemanticColour.TEXT: ColourValue("#1E2430", "--text-primary", "Primary text"),
    SemanticColour.TEXT_SECONDARY: ColourValue(
        "#4A5568", "--text-secondary", "Secondary text"
    ),
    SemanticColour.MUTED: ColourValue("#5C6570", "--text-muted", "Muted text"),
    SemanticColour.TEXT_INVERSE: ColourValue(
        "#F8FAFC", "--text-inverse", "Inverse text"
    ),
    SemanticColour.ON_PRIMARY: ColourValue(
        "#F8FAFC", "--on-primary", "Text on primary"
    ),
    SemanticColour.ON_SUCCESS: ColourValue(
        "#F8FAFC", "--on-success", "Text on success"
    ),
    SemanticColour.ON_DANGER: ColourValue("#F8FAFC", "--on-danger", "Text on danger"),
    SemanticColour.SUCCESS_BG: ColourValue(
        "#E6F7F5", "--success-bg", "Success background"
    ),
    SemanticColour.WARNING_BG: ColourValue(
        "rgba(161, 98, 7, 0.12)", "--warning-bg", "Warning background"
    ),
    SemanticColour.DANGER_BG: ColourValue(
        "#FEF1F1", "--danger-bg", "Danger background"
    ),
    SemanticColour.INFO_BG: ColourValue(
        "rgba(59, 79, 184, 0.1)", "--info-bg", "Info background"
    ),
    SemanticColour.FOCUS_RING: ColourValue(
        "rgba(59, 79, 184, 0.28)", "--focus-ring", "Focus ring colour"
    ),
}

# Colours forbidden as UI chrome semantics (UX-001).
UI_FORBIDDEN_BRAND_COLOURS: frozenset[BrandColour] = frozenset(
    {BrandColour.GOLD, BrandColour.GOLD_HOVER}
)


def colour(token: SemanticColour | BrandColour) -> ColourValue:
    """Resolve a colour token to its value."""
    if isinstance(token, SemanticColour):
        return SEMANTIC_COLOURS[token]
    return BRAND_COLOURS[token]


def is_ui_chrome_safe(token: BrandColour) -> bool:
    """Return False when a brand colour must not drive UI chrome."""
    return token not in UI_FORBIDDEN_BRAND_COLOURS
