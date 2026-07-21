"""Border-radius tokens — inputs 12px, cards 16px (UX-001)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True, slots=True)
class RadiusValue:
    """One corner-radius step."""

    px: int
    rem: str
    css_var: str


class RadiusToken(str, Enum):
    """Named radius steps."""

    NONE = "none"
    SM = "sm"  # 8 — badges / chips
    MD = "md"  # 12 — inputs / buttons
    LG = "lg"  # 16 — cards
    XL = "xl"  # 16 — large panels (alias)
    FULL = "full"  # pills / progress tracks


RADIUS: Mapping[RadiusToken, RadiusValue] = {
    RadiusToken.NONE: RadiusValue(0, "0", "--radius-none"),
    RadiusToken.SM: RadiusValue(8, "0.5rem", "--radius-sm"),
    RadiusToken.MD: RadiusValue(12, "0.75rem", "--radius-md"),
    RadiusToken.LG: RadiusValue(16, "1rem", "--radius-lg"),
    RadiusToken.XL: RadiusValue(16, "1rem", "--radius-xl"),
    RadiusToken.FULL: RadiusValue(9999, "9999px", "--radius-full"),
}


def radius(token: RadiusToken) -> RadiusValue:
    """Resolve a radius token."""
    return RADIUS[token]
