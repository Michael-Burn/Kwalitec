"""Responsive layout contracts."""

from __future__ import annotations

import pytest

from presentation.design_system.layout import (
    BREAKPOINTS,
    CONTAINERS,
    DESKTOP_GRID,
    GRIDS,
    MOBILE_GRID,
    TABLET_GRID,
    Breakpoint,
    ContainerWidth,
    breakpoint_at_width,
    columns_at_width,
    container,
    grid_for,
)
from presentation.design_system.spacing import SPACING, SpacingToken


def test_grids_exist_for_mobile_tablet_desktop() -> None:
    assert GRIDS[Breakpoint.MOBILE] is MOBILE_GRID
    assert GRIDS[Breakpoint.TABLET] is TABLET_GRID
    assert GRIDS[Breakpoint.DESKTOP] is DESKTOP_GRID
    assert MOBILE_GRID.columns == 4
    assert TABLET_GRID.columns == 8
    assert DESKTOP_GRID.columns == 12


def test_grid_gutters_and_margins_use_spacing_tokens() -> None:
    for grid in GRIDS.values():
        assert grid.gutter in SpacingToken
        assert grid.margin in SpacingToken
        assert grid.gutter in SPACING
        assert grid.margin in SPACING


@pytest.mark.parametrize(
    ("width", "expected_bp", "expected_cols"),
    [
        (320, Breakpoint.MOBILE, 4),
        (767, Breakpoint.MOBILE, 4),
        (768, Breakpoint.TABLET, 8),
        (1023, Breakpoint.TABLET, 8),
        (1024, Breakpoint.DESKTOP, 12),
        (1440, Breakpoint.DESKTOP, 12),
    ],
)
def test_breakpoint_and_columns_at_width(
    width: int, expected_bp: Breakpoint, expected_cols: int
) -> None:
    assert breakpoint_at_width(width) is expected_bp
    assert columns_at_width(width) == expected_cols


def test_container_widths() -> None:
    narrow = container(ContainerWidth.NARROW)
    content = container(ContainerWidth.CONTENT)
    wide = container(ContainerWidth.WIDE)
    full = container(ContainerWidth.FULL)
    assert narrow.max_width_rem == "44rem"
    assert content.max_width_px == 960
    assert wide.max_width_px == 1152
    assert full.max_width_px is None
    assert set(CONTAINERS) == set(ContainerWidth)


def test_breakpoint_media_queries_documented() -> None:
    assert BREAKPOINTS[Breakpoint.MOBILE].min_width_px == 0
    assert BREAKPOINTS[Breakpoint.TABLET].min_width_px == 768
    assert BREAKPOINTS[Breakpoint.DESKTOP].min_width_px == 1024
    assert "768" in BREAKPOINTS[Breakpoint.TABLET].css_media


def test_grid_for_matches_catalogue() -> None:
    assert grid_for(Breakpoint.DESKTOP).columns == 12
