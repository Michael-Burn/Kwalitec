"""Spacing scale — 8-point grid (UX-001).

Never invent spacing outside this catalogue.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True, slots=True)
class SpacingValue:
    """One spacing step in pixels and rem (16px root)."""

    px: int
    rem: str
    css_var: str


class SpacingToken(str, Enum):
    """Named spacing steps."""

    NONE = "none"
    XS = "xs"  # 4
    SM = "sm"  # 8
    MD = "md"  # 12
    LG = "lg"  # 16
    XL = "xl"  # 24
    XXL = "2xl"  # 32
    XXXL = "3xl"  # 48
    XXXXL = "4xl"  # 64
    XXXXXL = "5xl"  # 96
    XXXXXXL = "6xl"  # 128


SPACING: Mapping[SpacingToken, SpacingValue] = {
    SpacingToken.NONE: SpacingValue(0, "0", "--space-none"),
    SpacingToken.XS: SpacingValue(4, "0.25rem", "--space-xs"),
    SpacingToken.SM: SpacingValue(8, "0.5rem", "--space-sm"),
    SpacingToken.MD: SpacingValue(12, "0.75rem", "--space-md"),
    SpacingToken.LG: SpacingValue(16, "1rem", "--space-lg"),
    SpacingToken.XL: SpacingValue(24, "1.5rem", "--space-xl"),
    SpacingToken.XXL: SpacingValue(32, "2rem", "--space-2xl"),
    SpacingToken.XXXL: SpacingValue(48, "3rem", "--space-3xl"),
    SpacingToken.XXXXL: SpacingValue(64, "4rem", "--space-4xl"),
    SpacingToken.XXXXXL: SpacingValue(96, "6rem", "--space-5xl"),
    SpacingToken.XXXXXXL: SpacingValue(128, "8rem", "--space-6xl"),
}

# Canonical allowed pixel values from UX-001.
ALLOWED_SPACING_PX: frozenset[int] = frozenset(
    {0, 4, 8, 12, 16, 24, 32, 48, 64, 96, 128}
)


def space(token: SpacingToken) -> SpacingValue:
    """Resolve a spacing token."""
    return SPACING[token]


def assert_spacing_integrity() -> None:
    """Raise AssertionError if the scale drifts from the 8-point grid."""
    for token, value in SPACING.items():
        if value.px not in ALLOWED_SPACING_PX:
            raise AssertionError(f"{token} has non-canonical px={value.px}")
