"""Motion tokens — purposeful, reduced-motion aware (UX-001)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True, slots=True)
class MotionValue:
    """Duration + easing for one motion role."""

    duration_ms: int
    easing: str
    css_var: str
    description: str = ""


class MotionToken(str, Enum):
    """Named motion roles."""

    FAST = "fast"
    BASE = "base"
    SLOW = "slow"
    PRESS = "press"
    LIFT = "lift"
    SKELETON = "skeleton"
    PAGE = "page"
    SIDEBAR = "sidebar"
    TOOLTIP = "tooltip"


MOTION: Mapping[MotionToken, MotionValue] = {
    MotionToken.FAST: MotionValue(
        150, "ease-out", "--transition-fast", "Micro feedback"
    ),
    MotionToken.BASE: MotionValue(200, "ease-out", "--transition-base", "Default UI"),
    MotionToken.SLOW: MotionValue(
        250, "ease-out", "--transition-slow", "Panels / toasts"
    ),
    MotionToken.PRESS: MotionValue(
        100, "ease-out", "--transition-press", "Button press scale"
    ),
    MotionToken.LIFT: MotionValue(
        200, "ease-out", "--transition-lift", "Hover lift 2px"
    ),
    MotionToken.SKELETON: MotionValue(
        1200, "ease-out", "--transition-skeleton", "Skeleton pulse"
    ),
    # UX-001 / PX-004 — continuous navigation without abrupt page cuts.
    MotionToken.PAGE: MotionValue(
        250, "ease-out", "--transition-page", "Page enter / surface continuity"
    ),
    MotionToken.SIDEBAR: MotionValue(
        220, "ease-out", "--transition-sidebar", "Sidebar open / close"
    ),
    MotionToken.TOOLTIP: MotionValue(
        120, "ease-out", "--transition-tooltip", "Tooltip appear"
    ),
}

# UX-001 button press / hover transforms (tokenised, not free-form).
HOVER_LIFT_PX = 2
PRESS_SCALE = 0.98
DISABLED_OPACITY = 0.5
REDUCED_MOTION_POLICY = "respect-prefers-reduced-motion"


def motion(token: MotionToken) -> MotionValue:
    """Resolve a motion token."""
    return MOTION[token]
