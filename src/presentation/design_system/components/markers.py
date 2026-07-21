"""Badge, Chip, Tag, and Divider markers."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from presentation.design_system.colours import SemanticColour
from presentation.design_system.components.base import (
    AccessibilityContract,
    StyleContract,
)
from presentation.design_system.radius import RadiusToken
from presentation.design_system.spacing import SpacingToken
from presentation.design_system.typography import TypeRole


class Tone(str, Enum):
    NEUTRAL = "neutral"
    PRIMARY = "primary"
    SUCCESS = "success"
    WARNING = "warning"
    DANGER = "danger"
    INFO = "info"


_TONE_FG: dict[Tone, SemanticColour] = {
    Tone.NEUTRAL: SemanticColour.TEXT_SECONDARY,
    Tone.PRIMARY: SemanticColour.PRIMARY,
    Tone.SUCCESS: SemanticColour.SUCCESS,
    Tone.WARNING: SemanticColour.WARNING,
    Tone.DANGER: SemanticColour.DANGER,
    Tone.INFO: SemanticColour.INFO,
}

_TONE_BG: dict[Tone, SemanticColour] = {
    Tone.NEUTRAL: SemanticColour.SURFACE_ALT,
    Tone.PRIMARY: SemanticColour.INFO_BG,
    Tone.SUCCESS: SemanticColour.SUCCESS_BG,
    Tone.WARNING: SemanticColour.WARNING_BG,
    Tone.DANGER: SemanticColour.DANGER_BG,
    Tone.INFO: SemanticColour.INFO_BG,
}


@dataclass(frozen=True, slots=True)
class Badge:
    """Compact status badge — educational meaning only; no gamification."""

    label: str
    tone: Tone = Tone.NEUTRAL

    def style(self) -> StyleContract:
        return StyleContract(
            background=_TONE_BG[self.tone],
            foreground=_TONE_FG[self.tone],
            typography=TypeRole.CAPTION,
            padding_x=SpacingToken.SM,
            padding_y=SpacingToken.XS,
            radius=RadiusToken.SM,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="status",
            label_required=True,
            contrast_fg=_TONE_FG[self.tone],
            contrast_bg=_TONE_BG[self.tone],
            min_contrast_ratio=3.0,
        )


@dataclass(frozen=True, slots=True)
class Chip:
    """Selectable or filter chip chrome (presentation state only)."""

    label: str
    selected: bool = False
    tone: Tone = Tone.NEUTRAL

    def style(self) -> StyleContract:
        return StyleContract(
            background=(
                SemanticColour.PRIMARY if self.selected else _TONE_BG[self.tone]
            ),
            foreground=(
                SemanticColour.ON_PRIMARY if self.selected else _TONE_FG[self.tone]
            ),
            border=SemanticColour.BORDER
            if not self.selected
            else SemanticColour.PRIMARY,
            typography=TypeRole.CAPTION,
            padding_x=SpacingToken.LG,
            padding_y=SpacingToken.SM,
            radius=RadiusToken.FULL,
        )

    def accessibility(self) -> AccessibilityContract:
        style = self.style()
        return AccessibilityContract(
            role="button",
            label_required=True,
            keyboard_focusable=True,
            contrast_fg=style.foreground,
            contrast_bg=style.background or SemanticColour.SURFACE,
        )


@dataclass(frozen=True, slots=True)
class Tag:
    """Non-interactive classification tag."""

    label: str
    tone: Tone = Tone.NEUTRAL

    def style(self) -> StyleContract:
        return StyleContract(
            background=_TONE_BG[self.tone],
            foreground=_TONE_FG[self.tone],
            border=SemanticColour.BORDER_SUBTLE,
            typography=TypeRole.CAPTION,
            padding_x=SpacingToken.SM,
            padding_y=SpacingToken.XS,
            radius=RadiusToken.SM,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="",
            label_required=True,
            contrast_fg=_TONE_FG[self.tone],
            contrast_bg=_TONE_BG[self.tone],
            min_contrast_ratio=3.0,
        )


@dataclass(frozen=True, slots=True)
class Divider:
    """Horizontal or vertical rule."""

    orientation: str = "horizontal"
    tone: Tone = Tone.NEUTRAL

    def style(self) -> StyleContract:
        return StyleContract(
            border=SemanticColour.BORDER_SUBTLE,
            extras=(("orientation", self.orientation),),
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(role="separator", label_required=False)
