"""Shared component primitives — token-only style contracts.

Components declare visual intent via design tokens. They never contain
business logic, educational logic, or framework-specific markup.
"""

from __future__ import annotations

from dataclasses import dataclass

from presentation.design_system.colours import SemanticColour
from presentation.design_system.elevation import ElevationToken
from presentation.design_system.motion import MotionToken
from presentation.design_system.radius import RadiusToken
from presentation.design_system.spacing import SpacingToken
from presentation.design_system.typography import TypeRole


@dataclass(frozen=True, slots=True)
class StyleContract:
    """Token references that a renderer must honour — no raw visual literals."""

    background: SemanticColour | None = None
    foreground: SemanticColour | None = None
    border: SemanticColour | None = None
    typography: TypeRole | None = None
    padding_x: SpacingToken | None = None
    padding_y: SpacingToken | None = None
    gap: SpacingToken | None = None
    radius: RadiusToken | None = None
    elevation: ElevationToken | None = None
    motion: MotionToken | None = None
    extras: tuple[tuple[str, str], ...] = ()

    def token_names(self) -> frozenset[str]:
        """Flatten referenced token enum values for integrity checks."""
        names: set[str] = set()
        for value in (
            self.background,
            self.foreground,
            self.border,
            self.typography,
            self.padding_x,
            self.padding_y,
            self.gap,
            self.radius,
            self.elevation,
            self.motion,
        ):
            if value is not None:
                names.add(value.value)
        names.update(value for _, value in self.extras)
        return frozenset(names)


@dataclass(frozen=True, slots=True)
class AccessibilityContract:
    """Accessibility expectations attached to a component."""

    role: str = ""
    label_required: bool = False
    keyboard_focusable: bool = False
    contrast_fg: SemanticColour | None = None
    contrast_bg: SemanticColour | None = None
    min_contrast_ratio: float = 4.5
    reduced_motion_safe: bool = True
