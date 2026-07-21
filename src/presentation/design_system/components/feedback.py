"""Overlay and feedback components — Modal, Toast, Empty/Loading/Skeleton."""

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


class ToastTone(str, Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    DANGER = "danger"


_TOAST_FG = {
    ToastTone.INFO: SemanticColour.INFO,
    ToastTone.SUCCESS: SemanticColour.SUCCESS,
    ToastTone.WARNING: SemanticColour.WARNING,
    ToastTone.DANGER: SemanticColour.DANGER,
}
_TOAST_BG = {
    ToastTone.INFO: SemanticColour.INFO_BG,
    ToastTone.SUCCESS: SemanticColour.SUCCESS_BG,
    ToastTone.WARNING: SemanticColour.WARNING_BG,
    ToastTone.DANGER: SemanticColour.DANGER_BG,
}


@dataclass(frozen=True, slots=True)
class Modal:
    """Dialog chrome — title/body/actions are presentation strings only."""

    title: str
    body: str = ""
    primary_action_label: str = ""
    secondary_action_label: str = ""
    dismissible: bool = True

    def style(self) -> StyleContract:
        return StyleContract(
            background=SemanticColour.SURFACE_ELEVATED,
            foreground=SemanticColour.TEXT,
            border=SemanticColour.BORDER_SUBTLE,
            typography=TypeRole.HEADING,
            padding_x=SpacingToken.XXL,
            padding_y=SpacingToken.XXL,
            gap=SpacingToken.LG,
            radius=RadiusToken.LG,
            elevation=ElevationToken.LG,
            motion=MotionToken.SLOW,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="dialog",
            label_required=True,
            keyboard_focusable=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.SURFACE_ELEVATED,
        )


@dataclass(frozen=True, slots=True)
class Toast:
    """Transient feedback message."""

    message: str
    tone: ToastTone = ToastTone.INFO
    dismissible: bool = True

    def style(self) -> StyleContract:
        return StyleContract(
            background=_TOAST_BG[self.tone],
            foreground=_TOAST_FG[self.tone],
            typography=TypeRole.BODY,
            padding_x=SpacingToken.LG,
            padding_y=SpacingToken.MD,
            radius=RadiusToken.MD,
            elevation=ElevationToken.MD,
            motion=MotionToken.SLOW,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="status",
            label_required=True,
            contrast_fg=_TOAST_FG[self.tone],
            contrast_bg=_TOAST_BG[self.tone],
            min_contrast_ratio=3.0,
        )


@dataclass(frozen=True, slots=True)
class EmptyState:
    """Calm empty surface — never invent fake actions."""

    title: str
    description: str = ""
    action_label: str = ""
    icon: IconSpec = field(
        default_factory=lambda: IconSpec(
            name=IconName.INBOX, decorative=False, label="Empty"
        )
    )

    def style(self) -> StyleContract:
        return StyleContract(
            background=SemanticColour.SURFACE,
            foreground=SemanticColour.TEXT,
            typography=TypeRole.HEADING,
            padding_x=SpacingToken.XXL,
            padding_y=SpacingToken.XXXL,
            gap=SpacingToken.MD,
            radius=RadiusToken.LG,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="status",
            label_required=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.SURFACE,
        )


@dataclass(frozen=True, slots=True)
class LoadingState:
    """Indeterminate loading chrome with accessible label."""

    label: str = "Loading"
    icon: IconSpec = field(
        default_factory=lambda: IconSpec(name=IconName.LOADER, decorative=True)
    )

    def style(self) -> StyleContract:
        return StyleContract(
            foreground=SemanticColour.MUTED,
            typography=TypeRole.CAPTION,
            gap=SpacingToken.SM,
            motion=MotionToken.SKELETON,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="status",
            label_required=True,
            reduced_motion_safe=True,
        )


class SkeletonVariant(str, Enum):
    TEXT = "text"
    TITLE = "title"
    AVATAR = "avatar"
    BUTTON = "button"
    CARD = "card"
    BAR = "bar"


@dataclass(frozen=True, slots=True)
class Skeleton:
    """Layout-preserving placeholder — never flash empty (UX-001)."""

    variant: SkeletonVariant = SkeletonVariant.TEXT
    label: str = "Loading content"

    def style(self) -> StyleContract:
        return StyleContract(
            background=SemanticColour.BORDER,
            foreground=SemanticColour.BORDER,
            radius=(
                RadiusToken.FULL
                if self.variant == SkeletonVariant.AVATAR
                else RadiusToken.SM
            ),
            motion=MotionToken.SKELETON,
            extras=(("variant", self.variant.value),),
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="status",
            label_required=True,
            reduced_motion_safe=True,
        )
