"""Timeline, Stepper, and Accordion navigation/structure components."""

from __future__ import annotations

from dataclasses import dataclass

from presentation.design_system.colours import SemanticColour
from presentation.design_system.components.base import (
    AccessibilityContract,
    StyleContract,
)
from presentation.design_system.radius import RadiusToken
from presentation.design_system.spacing import SpacingToken
from presentation.design_system.typography import TypeRole


@dataclass(frozen=True, slots=True)
class TimelineItem:
    """One timeline entry — labels only."""

    title: str
    detail: str = ""
    timestamp_label: str = ""
    active: bool = False


@dataclass(frozen=True, slots=True)
class Timeline:
    """Vertical timeline of presentation events."""

    items: tuple[TimelineItem, ...]
    label: str = "Timeline"

    def style(self) -> StyleContract:
        return StyleContract(
            foreground=SemanticColour.TEXT,
            border=SemanticColour.BORDER,
            typography=TypeRole.BODY,
            gap=SpacingToken.LG,
            padding_y=SpacingToken.MD,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="list",
            label_required=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.BACKGROUND,
        )


@dataclass(frozen=True, slots=True)
class StepperStep:
    """One step in a wizard/stepper."""

    label: str
    description: str = ""
    complete: bool = False
    current: bool = False


@dataclass(frozen=True, slots=True)
class Stepper:
    """Ordered step indicator — no form logic."""

    steps: tuple[StepperStep, ...]
    label: str = "Progress"

    def style(self) -> StyleContract:
        return StyleContract(
            foreground=SemanticColour.TEXT,
            typography=TypeRole.CAPTION,
            gap=SpacingToken.SM,
            radius=RadiusToken.FULL,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="list",
            label_required=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.BACKGROUND,
        )

    def current_index(self) -> int | None:
        for index, step in enumerate(self.steps):
            if step.current:
                return index
        return None


@dataclass(frozen=True, slots=True)
class AccordionPanel:
    """One expandable panel — open state is presentation only."""

    title: str
    body: str
    open: bool = False


@dataclass(frozen=True, slots=True)
class Accordion:
    """Stacked expandable sections."""

    panels: tuple[AccordionPanel, ...]
    label: str = "Sections"
    allow_multiple: bool = False

    def style(self) -> StyleContract:
        return StyleContract(
            background=SemanticColour.SURFACE,
            foreground=SemanticColour.TEXT,
            border=SemanticColour.BORDER_SUBTLE,
            typography=TypeRole.SUBHEADING,
            padding_x=SpacingToken.LG,
            padding_y=SpacingToken.LG,
            gap=SpacingToken.SM,
            radius=RadiusToken.MD,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="region",
            label_required=True,
            keyboard_focusable=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.SURFACE,
        )
