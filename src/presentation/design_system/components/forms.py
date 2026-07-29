"""Form control primitives — Input, Textarea, Checkbox, Radio, Select, Toggle."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from presentation.design_system.colours import SemanticColour
from presentation.design_system.components.base import (
    AccessibilityContract,
    StyleContract,
)
from presentation.design_system.motion import MotionToken
from presentation.design_system.radius import RadiusToken
from presentation.design_system.spacing import SpacingToken
from presentation.design_system.typography import TypeRole


class FieldState(str, Enum):
    DEFAULT = "default"
    ERROR = "error"
    DISABLED = "disabled"


@dataclass(frozen=True, slots=True)
class Input:
    """Single-line text field chrome."""

    name: str
    label: str
    value: str = ""
    placeholder: str = ""
    state: FieldState = FieldState.DEFAULT
    error_message: str = ""
    required: bool = False

    def style(self) -> StyleContract:
        border = (
            SemanticColour.DANGER
            if self.state == FieldState.ERROR
            else SemanticColour.BORDER
        )
        return StyleContract(
            background=SemanticColour.SURFACE,
            foreground=SemanticColour.TEXT,
            border=border,
            typography=TypeRole.BODY,
            padding_x=SpacingToken.LG,
            padding_y=SpacingToken.SM,
            radius=RadiusToken.MD,
            motion=MotionToken.FAST,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="textbox",
            label_required=True,
            keyboard_focusable=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.SURFACE,
        )


@dataclass(frozen=True, slots=True)
class Textarea:
    """Multi-line text field chrome."""

    name: str
    label: str
    value: str = ""
    rows: int = 4
    state: FieldState = FieldState.DEFAULT
    error_message: str = ""

    def style(self) -> StyleContract:
        return Input(
            name=self.name,
            label=self.label,
            state=self.state,
        ).style()

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="textbox",
            label_required=True,
            keyboard_focusable=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.SURFACE,
        )


@dataclass(frozen=True, slots=True)
class Checkbox:
    """Binary checkbox chrome."""

    name: str
    label: str
    checked: bool = False
    disabled: bool = False

    def style(self) -> StyleContract:
        return StyleContract(
            foreground=SemanticColour.TEXT,
            typography=TypeRole.BODY,
            gap=SpacingToken.SM,
            motion=MotionToken.FAST,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="checkbox",
            label_required=True,
            keyboard_focusable=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.SURFACE,
        )


@dataclass(frozen=True, slots=True)
class Radio:
    """Single-select radio chrome."""

    name: str
    label: str
    value: str
    checked: bool = False
    disabled: bool = False

    def style(self) -> StyleContract:
        return Checkbox(name=self.name, label=self.label).style()

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="radio",
            label_required=True,
            keyboard_focusable=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.SURFACE,
        )


@dataclass(frozen=True, slots=True)
class Select:
    """Select / dropdown chrome."""

    name: str
    label: str
    options: tuple[str, ...] = ()
    selected: str = ""
    state: FieldState = FieldState.DEFAULT

    def style(self) -> StyleContract:
        return Input(name=self.name, label=self.label, state=self.state).style()

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="combobox",
            label_required=True,
            keyboard_focusable=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.SURFACE,
        )


@dataclass(frozen=True, slots=True)
class Toggle:
    """On/off switch chrome."""

    name: str
    label: str
    on: bool = False
    disabled: bool = False

    def style(self) -> StyleContract:
        return StyleContract(
            background=SemanticColour.PRIMARY if self.on else SemanticColour.BORDER,
            foreground=SemanticColour.ON_PRIMARY if self.on else SemanticColour.TEXT,
            typography=TypeRole.SUPPORT,
            gap=SpacingToken.SM,
            radius=RadiusToken.FULL,
            motion=MotionToken.FAST,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="switch",
            label_required=True,
            keyboard_focusable=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.SURFACE,
        )


@dataclass(frozen=True, slots=True)
class SearchInput:
    """Search field chrome — composes Input semantics."""

    name: str = "q"
    label: str = "Search"
    value: str = ""
    placeholder: str = "Search"

    def style(self) -> StyleContract:
        return Input(name=self.name, label=self.label, value=self.value).style()

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="searchbox",
            label_required=True,
            keyboard_focusable=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.SURFACE,
        )


@dataclass(frozen=True, slots=True)
class Spinner:
    """Indeterminate spinner primitive."""

    label: str = "Loading"

    def style(self) -> StyleContract:
        return StyleContract(
            foreground=SemanticColour.PRIMARY,
            typography=TypeRole.SUPPORT,
            motion=MotionToken.SKELETON,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="status",
            label_required=True,
            reduced_motion_safe=True,
        )


@dataclass(frozen=True, slots=True)
class ErrorState:
    """Inline or section error surface — Reason + recovery path."""

    title: str
    description: str = ""
    action_label: str = ""

    def style(self) -> StyleContract:
        return StyleContract(
            background=SemanticColour.DANGER_BG,
            foreground=SemanticColour.DANGER,
            border=SemanticColour.DANGER,
            typography=TypeRole.SECTION,
            padding_x=SpacingToken.XL,
            padding_y=SpacingToken.LG,
            gap=SpacingToken.SM,
            radius=RadiusToken.LG,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="alert",
            label_required=True,
            contrast_fg=SemanticColour.DANGER,
            contrast_bg=SemanticColour.DANGER_BG,
            min_contrast_ratio=3.0,
        )
