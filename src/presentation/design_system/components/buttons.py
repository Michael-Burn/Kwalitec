"""Button components — Primary, Secondary, Danger, Ghost (UX-001)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from presentation.design_system.colours import SemanticColour
from presentation.design_system.components.base import (
    AccessibilityContract,
    StyleContract,
)
from presentation.design_system.elevation import ElevationToken
from presentation.design_system.motion import MotionToken
from presentation.design_system.radius import RadiusToken
from presentation.design_system.spacing import SpacingToken
from presentation.design_system.typography import TypeRole


class ButtonVariant(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    DANGER = "danger"
    GHOST = "ghost"


@dataclass(frozen=True, slots=True)
class Button:
    """Tokenised button style contract. Content is presentation-only."""

    label: str
    variant: ButtonVariant = ButtonVariant.PRIMARY
    disabled: bool = False
    icon_name: str = ""

    def style(self) -> StyleContract:
        return _STYLES[self.variant]

    def accessibility(self) -> AccessibilityContract:
        style = self.style()
        return AccessibilityContract(
            role="button",
            label_required=True,
            keyboard_focusable=True,
            contrast_fg=style.foreground,
            contrast_bg=style.background or SemanticColour.SURFACE,
            min_contrast_ratio=4.5,
        )


_STYLES: dict[ButtonVariant, StyleContract] = {
    ButtonVariant.PRIMARY: StyleContract(
        background=SemanticColour.PRIMARY,
        foreground=SemanticColour.ON_PRIMARY,
        border=SemanticColour.PRIMARY,
        typography=TypeRole.BODY,
        padding_x=SpacingToken.XL,
        padding_y=SpacingToken.MD,
        radius=RadiusToken.MD,
        elevation=ElevationToken.NONE,
        motion=MotionToken.BASE,
        extras=(("hover_background", SemanticColour.PRIMARY_HOVER.value),),
    ),
    ButtonVariant.SECONDARY: StyleContract(
        background=SemanticColour.SURFACE,
        foreground=SemanticColour.TEXT,
        border=SemanticColour.BORDER,
        typography=TypeRole.BODY,
        padding_x=SpacingToken.XL,
        padding_y=SpacingToken.MD,
        radius=RadiusToken.MD,
        elevation=ElevationToken.NONE,
        motion=MotionToken.BASE,
    ),
    ButtonVariant.DANGER: StyleContract(
        background=SemanticColour.DANGER,
        foreground=SemanticColour.ON_DANGER,
        border=SemanticColour.DANGER,
        typography=TypeRole.BODY,
        padding_x=SpacingToken.XL,
        padding_y=SpacingToken.MD,
        radius=RadiusToken.MD,
        elevation=ElevationToken.NONE,
        motion=MotionToken.BASE,
    ),
    ButtonVariant.GHOST: StyleContract(
        background=None,
        foreground=SemanticColour.PRIMARY,
        border=None,
        typography=TypeRole.BODY,
        padding_x=SpacingToken.LG,
        padding_y=SpacingToken.SM,
        radius=RadiusToken.MD,
        elevation=ElevationToken.NONE,
        motion=MotionToken.FAST,
        extras=(("hover_background", SemanticColour.INFO_BG.value),),
    ),
}


def primary_button(label: str, *, disabled: bool = False) -> Button:
    return Button(label=label, variant=ButtonVariant.PRIMARY, disabled=disabled)


def secondary_button(label: str, *, disabled: bool = False) -> Button:
    return Button(label=label, variant=ButtonVariant.SECONDARY, disabled=disabled)


def danger_button(label: str, *, disabled: bool = False) -> Button:
    return Button(label=label, variant=ButtonVariant.DANGER, disabled=disabled)


def ghost_button(label: str, *, disabled: bool = False) -> Button:
    return Button(label=label, variant=ButtonVariant.GHOST, disabled=disabled)
