"""Aggregate design token catalogue for Version 3.

Every visual value used by V3 surfaces should resolve through this module.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from presentation.design_system.colours import (
    BRAND_COLOURS,
    SEMANTIC_COLOURS,
    BrandColour,
    ColourValue,
    SemanticColour,
)
from presentation.design_system.elevation import (
    ELEVATION,
    ElevationToken,
    ElevationValue,
)
from presentation.design_system.icons import (
    ICON_LIBRARY,
    ICON_SIZES,
    ICON_STROKE_WIDTH,
    IconSize,
    IconSizeValue,
)
from presentation.design_system.motion import (
    DISABLED_OPACITY,
    HOVER_LIFT_PX,
    MOTION,
    PRESS_SCALE,
    REDUCED_MOTION_POLICY,
    MotionToken,
    MotionValue,
)
from presentation.design_system.radius import RADIUS, RadiusToken, RadiusValue
from presentation.design_system.spacing import SPACING, SpacingToken, SpacingValue
from presentation.design_system.typography import TYPE_STYLES, TypeRole, TypeStyle


@dataclass(frozen=True, slots=True)
class DesignTokens:
    """Immutable snapshot of the full token catalogue."""

    colours: Mapping[SemanticColour, ColourValue]
    brand_colours: Mapping[BrandColour, ColourValue]
    spacing: Mapping[SpacingToken, SpacingValue]
    typography: Mapping[TypeRole, TypeStyle]
    elevation: Mapping[ElevationToken, ElevationValue]
    radius: Mapping[RadiusToken, RadiusValue]
    icon_sizes: Mapping[IconSize, IconSizeValue]
    motion: Mapping[MotionToken, MotionValue]
    icon_library: str
    icon_stroke_width: float
    hover_lift_px: int
    press_scale: float
    disabled_opacity: float
    reduced_motion_policy: str

    def semantic_hex(self, token: SemanticColour) -> str:
        return self.colours[token].hex

    def space_px(self, token: SpacingToken) -> int:
        return self.spacing[token].px

    def type_style(self, role: TypeRole) -> TypeStyle:
        return self.typography[role]

    def css_custom_properties(self) -> dict[str, str]:
        """Flat map of CSS custom-property name → value (framework-agnostic)."""
        props: dict[str, str] = {}
        for value in self.colours.values():
            props[value.css_var] = value.hex
        for value in self.brand_colours.values():
            props[value.css_var] = value.hex
        for value in self.spacing.values():
            props[value.css_var] = value.rem
        for style in self.typography.values():
            props[style.css_var_size] = style.size_rem
            props[style.css_var_weight] = str(style.weight)
        for value in self.elevation.values():
            props[value.css_var] = value.shadow
        for value in self.radius.values():
            props[value.css_var] = value.rem
        for value in self.icon_sizes.values():
            props[value.css_var] = f"{value.px}px"
        for value in self.motion.values():
            props[value.css_var] = f"{value.duration_ms}ms {value.easing}"
        return props


TOKENS = DesignTokens(
    colours=SEMANTIC_COLOURS,
    brand_colours=BRAND_COLOURS,
    spacing=SPACING,
    typography=TYPE_STYLES,
    elevation=ELEVATION,
    radius=RADIUS,
    icon_sizes=ICON_SIZES,
    motion=MOTION,
    icon_library=ICON_LIBRARY,
    icon_stroke_width=ICON_STROKE_WIDTH,
    hover_lift_px=HOVER_LIFT_PX,
    press_scale=PRESS_SCALE,
    disabled_opacity=DISABLED_OPACITY,
    reduced_motion_policy=REDUCED_MOTION_POLICY,
)


def get_tokens() -> DesignTokens:
    """Return the canonical V3 design token catalogue."""
    return TOKENS
