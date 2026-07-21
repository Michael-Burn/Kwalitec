"""Statistic tile and progress indicators."""

from __future__ import annotations

from dataclasses import dataclass

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


def _clamp_percent(value: float) -> float:
    if value < 0:
        return 0.0
    if value > 100:
        return 100.0
    return float(value)


@dataclass(frozen=True, slots=True)
class StatisticTile:
    """Single metric display — value must already be formatted."""

    label: str
    value: str
    detail: str = ""

    def style(self) -> StyleContract:
        return StyleContract(
            background=SemanticColour.SURFACE,
            foreground=SemanticColour.TEXT,
            border=SemanticColour.BORDER_SUBTLE,
            typography=TypeRole.HEADING,
            padding_x=SpacingToken.XL,
            padding_y=SpacingToken.XL,
            gap=SpacingToken.XS,
            radius=RadiusToken.LG,
            elevation=ElevationToken.SM,
            motion=MotionToken.FAST,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="group",
            label_required=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.SURFACE,
        )


@dataclass(frozen=True, slots=True)
class ProgressBar:
    """Linear progress track — percentage is display input only."""

    label: str
    percent: float
    value_text: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "percent", _clamp_percent(self.percent))

    def style(self) -> StyleContract:
        return StyleContract(
            background=SemanticColour.BORDER_SUBTLE,
            foreground=SemanticColour.PRIMARY,
            radius=RadiusToken.FULL,
            motion=MotionToken.SLOW,
            extras=(("track_height", SpacingToken.XS.value),),
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="progressbar",
            label_required=True,
            contrast_fg=SemanticColour.PRIMARY,
            contrast_bg=SemanticColour.BORDER_SUBTLE,
            min_contrast_ratio=3.0,
        )


@dataclass(frozen=True, slots=True)
class ProgressRing:
    """Circular progress indicator — percentage is display input only."""

    label: str
    percent: float
    size_token: SpacingToken = SpacingToken.XXXXL
    value_text: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "percent", _clamp_percent(self.percent))

    def style(self) -> StyleContract:
        return StyleContract(
            background=SemanticColour.BORDER_SUBTLE,
            foreground=SemanticColour.PRIMARY,
            typography=TypeRole.CAPTION,
            motion=MotionToken.SLOW,
            extras=(("size", self.size_token.value),),
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="progressbar",
            label_required=True,
            contrast_fg=SemanticColour.PRIMARY,
            contrast_bg=SemanticColour.SURFACE,
            min_contrast_ratio=3.0,
        )
