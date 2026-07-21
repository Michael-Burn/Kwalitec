"""Responsive layout tokens — grids, containers, breakpoints.

Framework-independent layout contracts for V3 surfaces.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum

from presentation.design_system.spacing import SpacingToken


class Breakpoint(str, Enum):
    """Responsive breakpoints (min-width)."""

    MOBILE = "mobile"
    TABLET = "tablet"
    DESKTOP = "desktop"


class ContainerWidth(str, Enum):
    """Named content container widths."""

    NARROW = "narrow"  # reading column
    CONTENT = "content"  # default page
    WIDE = "wide"  # shell / dashboard
    FULL = "full"


@dataclass(frozen=True, slots=True)
class BreakpointValue:
    """Min-width breakpoint in pixels."""

    min_width_px: int
    css_media: str


@dataclass(frozen=True, slots=True)
class GridSpec:
    """Column grid for one breakpoint band."""

    columns: int
    gutter: SpacingToken
    margin: SpacingToken
    max_width: ContainerWidth


@dataclass(frozen=True, slots=True)
class ContainerSpec:
    """Max content width for a named container."""

    max_width_px: int | None
    max_width_rem: str | None
    css_var: str


BREAKPOINTS: Mapping[Breakpoint, BreakpointValue] = {
    Breakpoint.MOBILE: BreakpointValue(0, "(max-width: 767px)"),
    Breakpoint.TABLET: BreakpointValue(
        768, "(min-width: 768px) and (max-width: 1023px)"
    ),
    Breakpoint.DESKTOP: BreakpointValue(1024, "(min-width: 1024px)"),
}

CONTAINERS: Mapping[ContainerWidth, ContainerSpec] = {
    ContainerWidth.NARROW: ContainerSpec(704, "44rem", "--container-narrow"),
    ContainerWidth.CONTENT: ContainerSpec(960, "60rem", "--container-content"),
    ContainerWidth.WIDE: ContainerSpec(1152, "72rem", "--container-wide"),
    ContainerWidth.FULL: ContainerSpec(None, None, "--container-full"),
}

# Grids requested by V3-002.
MOBILE_GRID = GridSpec(
    columns=4,
    gutter=SpacingToken.MD,
    margin=SpacingToken.LG,
    max_width=ContainerWidth.FULL,
)
TABLET_GRID = GridSpec(
    columns=8,
    gutter=SpacingToken.LG,
    margin=SpacingToken.XL,
    max_width=ContainerWidth.CONTENT,
)
DESKTOP_GRID = GridSpec(
    columns=12,
    gutter=SpacingToken.XL,
    margin=SpacingToken.XXL,
    max_width=ContainerWidth.WIDE,
)

GRIDS: Mapping[Breakpoint, GridSpec] = {
    Breakpoint.MOBILE: MOBILE_GRID,
    Breakpoint.TABLET: TABLET_GRID,
    Breakpoint.DESKTOP: DESKTOP_GRID,
}


def grid_for(breakpoint: Breakpoint) -> GridSpec:
    """Return the column grid for a breakpoint."""
    return GRIDS[breakpoint]


def container(width: ContainerWidth) -> ContainerSpec:
    """Resolve a container width token."""
    return CONTAINERS[width]


def columns_at_width(viewport_px: int) -> int:
    """Deterministic column count for a viewport width in pixels."""
    if viewport_px < BREAKPOINTS[Breakpoint.TABLET].min_width_px:
        return MOBILE_GRID.columns
    if viewport_px < BREAKPOINTS[Breakpoint.DESKTOP].min_width_px:
        return TABLET_GRID.columns
    return DESKTOP_GRID.columns


def breakpoint_at_width(viewport_px: int) -> Breakpoint:
    """Resolve which breakpoint band a viewport falls into."""
    if viewport_px < BREAKPOINTS[Breakpoint.TABLET].min_width_px:
        return Breakpoint.MOBILE
    if viewport_px < BREAKPOINTS[Breakpoint.DESKTOP].min_width_px:
        return Breakpoint.TABLET
    return Breakpoint.DESKTOP
