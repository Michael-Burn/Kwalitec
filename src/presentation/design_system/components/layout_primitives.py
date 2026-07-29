"""L2 layout primitives — Page, Container, Stack, Grid, Toolbar, Table, List."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from presentation.design_system.colours import SemanticColour
from presentation.design_system.components.base import (
    AccessibilityContract,
    StyleContract,
)
from presentation.design_system.layout import ContainerWidth
from presentation.design_system.radius import RadiusToken
from presentation.design_system.spacing import SpacingToken
from presentation.design_system.typography import TypeRole


class StackDirection(str, Enum):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


@dataclass(frozen=True, slots=True)
class Page:
    """Page shell content region — one H1 owned by PageHeader / caller."""

    title: str = ""

    def style(self) -> StyleContract:
        return StyleContract(
            background=SemanticColour.BACKGROUND,
            foreground=SemanticColour.TEXT,
            typography=TypeRole.BODY,
            padding_x=SpacingToken.XL,
            padding_y=SpacingToken.XXL,
            gap=SpacingToken.XXXL,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="main",
            label_required=False,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.BACKGROUND,
        )


@dataclass(frozen=True, slots=True)
class ContentContainer:
    """Max-width content container."""

    width: ContainerWidth = ContainerWidth.CONTENT

    def style(self) -> StyleContract:
        return StyleContract(
            extras=(("container", self.width.value),),
            padding_x=SpacingToken.LG,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(role="", label_required=False)


@dataclass(frozen=True, slots=True)
class Stack:
    """Flex stack — vertical by default."""

    direction: StackDirection = StackDirection.VERTICAL
    gap: SpacingToken = SpacingToken.LG

    def style(self) -> StyleContract:
        return StyleContract(
            gap=self.gap,
            extras=(("direction", self.direction.value),),
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(role="", label_required=False)


@dataclass(frozen=True, slots=True)
class Inline:
    """Horizontal inline cluster."""

    gap: SpacingToken = SpacingToken.SM

    def style(self) -> StyleContract:
        return StyleContract(
            gap=self.gap,
            extras=(("direction", StackDirection.HORIZONTAL.value),),
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(role="", label_required=False)


@dataclass(frozen=True, slots=True)
class LayoutGrid:
    """Responsive column grid region."""

    columns: int = 12
    gap: SpacingToken = SpacingToken.LG

    def style(self) -> StyleContract:
        return StyleContract(
            gap=self.gap,
            extras=(("columns", str(self.columns)),),
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(role="", label_required=False)


@dataclass(frozen=True, slots=True)
class Panel:
    """Bordered content panel — justified grouping only."""

    title: str = ""

    def style(self) -> StyleContract:
        return StyleContract(
            background=SemanticColour.SURFACE,
            foreground=SemanticColour.TEXT,
            border=SemanticColour.BORDER_SUBTLE,
            typography=TypeRole.SECTION,
            padding_x=SpacingToken.XL,
            padding_y=SpacingToken.XL,
            gap=SpacingToken.LG,
            radius=RadiusToken.LG,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="region",
            label_required=bool(self.title),
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.SURFACE,
        )


@dataclass(frozen=True, slots=True)
class Toolbar:
    """Quiet action / filter toolbar — never hosts a second Primary."""

    label: str = "Toolbar"

    def style(self) -> StyleContract:
        return StyleContract(
            foreground=SemanticColour.TEXT,
            typography=TypeRole.SUPPORT,
            gap=SpacingToken.SM,
            padding_y=SpacingToken.SM,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="toolbar",
            label_required=True,
            keyboard_focusable=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.BACKGROUND,
        )


@dataclass(frozen=True, slots=True)
class SearchBar:
    """Search header chrome — pairs with SearchInput."""

    label: str = "Search"

    def style(self) -> StyleContract:
        return StyleContract(
            background=SemanticColour.SURFACE,
            foreground=SemanticColour.TEXT,
            border=SemanticColour.BORDER,
            typography=TypeRole.BODY,
            padding_x=SpacingToken.LG,
            padding_y=SpacingToken.SM,
            gap=SpacingToken.SM,
            radius=RadiusToken.MD,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="search",
            label_required=True,
            keyboard_focusable=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.SURFACE,
        )


@dataclass(frozen=True, slots=True)
class DataTable:
    """Table for catalogues — prefer over card walls."""

    caption: str = ""
    column_labels: tuple[str, ...] = ()

    def style(self) -> StyleContract:
        return StyleContract(
            background=SemanticColour.SURFACE,
            foreground=SemanticColour.TEXT,
            border=SemanticColour.BORDER_SUBTLE,
            typography=TypeRole.BODY,
            gap=SpacingToken.SM,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="table",
            label_required=bool(self.caption),
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.SURFACE,
        )


@dataclass(frozen=True, slots=True)
class DataList:
    """List for queues and recent rows."""

    label: str = ""
    ordered: bool = False

    def style(self) -> StyleContract:
        return StyleContract(
            foreground=SemanticColour.TEXT,
            typography=TypeRole.BODY,
            gap=SpacingToken.SM,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="list",
            label_required=bool(self.label),
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.BACKGROUND,
        )


@dataclass(frozen=True, slots=True)
class PrimaryActionStrip:
    """Hosts the single Primary and optional quiet Text/Ghost escape."""

    primary_label: str
    primary_href: str = ""
    secondary_label: str = ""
    secondary_href: str = ""

    def style(self) -> StyleContract:
        return StyleContract(
            gap=SpacingToken.LG,
            padding_y=SpacingToken.SM,
            typography=TypeRole.BODY,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="group",
            label_required=True,
            keyboard_focusable=True,
            contrast_fg=SemanticColour.ON_PRIMARY,
            contrast_bg=SemanticColour.PRIMARY,
        )
