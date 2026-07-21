"""Section and Page Header layout components."""

from __future__ import annotations

from dataclasses import dataclass

from presentation.design_system.colours import SemanticColour
from presentation.design_system.components.base import (
    AccessibilityContract,
    StyleContract,
)
from presentation.design_system.spacing import SpacingToken
from presentation.design_system.typography import TypeRole


@dataclass(frozen=True, slots=True)
class Section:
    """One-purpose page section: headline + optional supporting copy."""

    title: str
    description: str = ""
    eyebrow: str = ""

    def style(self) -> StyleContract:
        return StyleContract(
            foreground=SemanticColour.TEXT,
            typography=TypeRole.HEADING,
            padding_y=SpacingToken.XXL,
            gap=SpacingToken.SM,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="region",
            label_required=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.BACKGROUND,
        )


@dataclass(frozen=True, slots=True)
class PageHeader:
    """Page-level title block — display typography."""

    title: str
    description: str = ""
    eyebrow: str = ""

    def style(self) -> StyleContract:
        return StyleContract(
            foreground=SemanticColour.TEXT,
            typography=TypeRole.DISPLAY,
            padding_y=SpacingToken.XXXL,
            gap=SpacingToken.MD,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="banner",
            label_required=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.BACKGROUND,
        )
