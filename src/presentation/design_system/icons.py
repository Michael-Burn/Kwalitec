"""Iconography contract — Lucide exclusively (UX-001).

Icons support labels; they never replace accessible text.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True, slots=True)
class IconSizeValue:
    """Approved Lucide icon size."""

    px: int
    css_var: str


class IconSize(str, Enum):
    """Allowed Lucide sizes."""

    SM = "sm"  # 20
    MD = "md"  # 24
    LG = "lg"  # 32


class IconName(str, Enum):
    """Curated Lucide names used by V3 components.

    Expand only when a new component needs a glyph — do not invent libraries.
    """

    ALERT_CIRCLE = "alert-circle"
    ALERT_TRIANGLE = "alert-triangle"
    CHECK = "check"
    CHECK_CIRCLE = "check-circle"
    CHEVRON_DOWN = "chevron-down"
    CHEVRON_RIGHT = "chevron-right"
    CLOCK = "clock"
    INFO = "info"
    LOADER = "loader"
    PLUS = "plus"
    TARGET = "target"
    TRENDING_UP = "trending-up"
    X = "x"
    INBOX = "inbox"
    BOOK_OPEN = "book-open"
    FLAG = "flag"
    LAYERS = "layers"


ICON_SIZES: Mapping[IconSize, IconSizeValue] = {
    IconSize.SM: IconSizeValue(20, "--icon-size-sm"),
    IconSize.MD: IconSizeValue(24, "--icon-size-md"),
    IconSize.LG: IconSizeValue(32, "--icon-size-lg"),
}

ICON_LIBRARY = "lucide"
ICON_STROKE_WIDTH = 1.75
ICON_VIEWBOX = "0 0 24 24"


@dataclass(frozen=True, slots=True)
class IconSpec:
    """Presentation-only icon descriptor."""

    name: IconName
    size: IconSize = IconSize.MD
    decorative: bool = True
    label: str = ""

    @property
    def library(self) -> str:
        return ICON_LIBRARY

    @property
    def stroke_width(self) -> float:
        return ICON_STROKE_WIDTH

    def size_px(self) -> int:
        return ICON_SIZES[self.size].px
