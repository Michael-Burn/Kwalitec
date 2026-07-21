"""Elevation / shadow tokens — soft, restrained (UX-001)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True, slots=True)
class ElevationValue:
    """Box-shadow contract for a depth level."""

    shadow: str
    css_var: str
    description: str = ""


class ElevationToken(str, Enum):
    """Named elevation levels."""

    NONE = "none"
    SM = "sm"
    MD = "md"
    LG = "lg"
    XL = "xl"
    FOCUS = "focus"


ELEVATION: Mapping[ElevationToken, ElevationValue] = {
    ElevationToken.NONE: ElevationValue("none", "--shadow-none", "Flat"),
    ElevationToken.SM: ElevationValue(
        "0 1px 2px rgba(13, 27, 42, 0.05)",
        "--shadow-sm",
        "Subtle card edge",
    ),
    ElevationToken.MD: ElevationValue(
        "0 1px 2px rgba(13, 27, 42, 0.05), 0 2px 10px rgba(13, 27, 42, 0.07)",
        "--shadow-md",
        "Default card lift",
    ),
    ElevationToken.LG: ElevationValue(
        "0 4px 18px rgba(13, 27, 42, 0.09), 0 2px 4px rgba(13, 27, 42, 0.04)",
        "--shadow-lg",
        "Modal / elevated panel",
    ),
    ElevationToken.XL: ElevationValue(
        "0 10px 32px rgba(13, 27, 42, 0.12)",
        "--shadow-xl",
        "High emphasis overlay",
    ),
    ElevationToken.FOCUS: ElevationValue(
        "0 0 0 3px rgba(59, 79, 184, 0.28)",
        "--focus-ring",
        "Keyboard focus ring",
    ),
}


def elevation(token: ElevationToken) -> ElevationValue:
    """Resolve an elevation token."""
    return ELEVATION[token]
