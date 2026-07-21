"""Card components — Card, Mission Card, Recommendation Card, Progress Card."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from presentation.design_system.colours import SemanticColour
from presentation.design_system.components.base import (
    AccessibilityContract,
    StyleContract,
)
from presentation.design_system.elevation import ElevationToken
from presentation.design_system.icons import IconName, IconSpec
from presentation.design_system.motion import MotionToken
from presentation.design_system.radius import RadiusToken
from presentation.design_system.spacing import SpacingToken
from presentation.design_system.typography import TypeRole


class CardVariant(str, Enum):
    DEFAULT = "default"
    MISSION = "mission"
    RECOMMENDATION = "recommendation"
    PROGRESS = "progress"


@dataclass(frozen=True, slots=True)
class Card:
    """Generic information container."""

    title: str
    body: str = ""
    eyebrow: str = ""
    variant: CardVariant = CardVariant.DEFAULT
    emphasized: bool = False

    def style(self) -> StyleContract:
        border = (
            SemanticColour.PRIMARY
            if self.emphasized
            or self.variant
            in {
                CardVariant.MISSION,
                CardVariant.RECOMMENDATION,
            }
            else SemanticColour.BORDER_SUBTLE
        )
        return StyleContract(
            background=SemanticColour.SURFACE,
            foreground=SemanticColour.TEXT,
            border=border,
            typography=TypeRole.SUBHEADING,
            padding_x=SpacingToken.XL,
            padding_y=SpacingToken.XL,
            gap=SpacingToken.MD,
            radius=RadiusToken.LG,
            elevation=ElevationToken.SM,
            motion=MotionToken.BASE,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="region",
            label_required=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.SURFACE,
        )


@dataclass(frozen=True, slots=True)
class MissionCard(Card):
    """Mission-focused card chrome — presentation fields only."""

    duration_label: str = ""
    status_label: str = ""
    icon: IconSpec = field(default_factory=lambda: IconSpec(name=IconName.TARGET))

    def __post_init__(self) -> None:
        object.__setattr__(self, "variant", CardVariant.MISSION)
        object.__setattr__(self, "emphasized", True)


@dataclass(frozen=True, slots=True)
class RecommendationCard(Card):
    """Recommendation card chrome — already-decided content only."""

    reason_label: str = ""
    category_label: str = ""
    icon: IconSpec = field(default_factory=lambda: IconSpec(name=IconName.FLAG))

    def __post_init__(self) -> None:
        object.__setattr__(self, "variant", CardVariant.RECOMMENDATION)
        object.__setattr__(self, "emphasized", True)


@dataclass(frozen=True, slots=True)
class ProgressCard(Card):
    """Progress summary card — display metrics only."""

    metric_label: str = ""
    trend_label: str = ""
    icon: IconSpec = field(default_factory=lambda: IconSpec(name=IconName.TRENDING_UP))

    def __post_init__(self) -> None:
        object.__setattr__(self, "variant", CardVariant.PROGRESS)
