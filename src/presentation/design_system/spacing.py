"""Spacing scale — 8-point grid (DX-001 / DX-006A).

Product UI allows only: 4, 8, 16, 24, 32, 48, 64.
Legacy 12 / 96 / 128 remain as transitional aliases for unmigrated pages.
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
    XS = "xs"  # 4 — space.1
    SM = "sm"  # 8 — space.2
    MD = "md"  # 12 — LEGACY only; not for DX-006B components
    LG = "lg"  # 16 — space.3
    XL = "xl"  # 24 — space.4
    XXL = "2xl"  # 32 — space.5
    XXXL = "3xl"  # 48 — space.6
    XXXXL = "4xl"  # 64 — space.7
    XXXXXL = "5xl"  # 96 — LEGACY only
    XXXXXXL = "6xl"  # 128 — LEGACY only


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

# Full catalogue including transitional aliases (CSS / legacy pages).
ALLOWED_SPACING_PX: frozenset[int] = frozenset(
    {0, 4, 8, 12, 16, 24, 32, 48, 64, 96, 128}
)

# DX-006A product UI law — new / migrated components must use only these.
PRODUCT_SPACING_PX: frozenset[int] = frozenset({0, 4, 8, 16, 24, 32, 48, 64})

LEGACY_SPACING_TOKENS: frozenset[SpacingToken] = frozenset(
    {
        SpacingToken.MD,
        SpacingToken.XXXXXL,
        SpacingToken.XXXXXXL,
    }
)


def space(token: SpacingToken) -> SpacingValue:
    """Resolve a spacing token."""
    return SPACING[token]


def assert_spacing_integrity() -> None:
    """Raise AssertionError if the scale drifts from the 8-point grid."""
    for token, value in SPACING.items():
        if value.px not in ALLOWED_SPACING_PX:
            raise AssertionError(f"{token} has non-canonical px={value.px}")


def assert_product_spacing(token: SpacingToken) -> None:
    """Raise AssertionError if a token is forbidden in DX-006B components."""
    if token in LEGACY_SPACING_TOKENS:
        raise AssertionError(
            f"{token} ({SPACING[token].px}px) is legacy-only; "
            "use 4/8/16/24/32/48/64 for DX-006A product UI"
        )
    if SPACING[token].px not in PRODUCT_SPACING_PX:
        raise AssertionError(f"{token} px={SPACING[token].px} not in product scale")


def is_product_spacing(token: SpacingToken) -> bool:
    """Return True when the token is legal for DX-006B shared components."""
    return token not in LEGACY_SPACING_TOKENS and SPACING[token].px in PRODUCT_SPACING_PX
