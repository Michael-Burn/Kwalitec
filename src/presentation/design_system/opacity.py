"""Opacity tokens — DX-006A DESIGN_TOKEN_SPEC."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True, slots=True)
class OpacityValue:
    """Named opacity role."""

    value: float
    css_var: str


class OpacityToken(str, Enum):
    DISABLED = "disabled"
    MUTED = "muted"
    SKELETON_MIN = "skeleton-min"
    SKELETON_MAX = "skeleton-max"


OPACITY: Mapping[OpacityToken, OpacityValue] = {
    OpacityToken.DISABLED: OpacityValue(0.5, "--opacity-disabled"),
    OpacityToken.MUTED: OpacityValue(0.7, "--opacity-muted"),
    OpacityToken.SKELETON_MIN: OpacityValue(0.55, "--opacity-skeleton-min"),
    OpacityToken.SKELETON_MAX: OpacityValue(1.0, "--opacity-skeleton-max"),
}


def opacity(token: OpacityToken) -> OpacityValue:
    """Resolve an opacity token."""
    return OPACITY[token]
