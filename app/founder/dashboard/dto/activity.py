"""Activity feed DTOs for Founder Dashboard (FOS-004)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ActivityItem:
    """One activity line item (display-only)."""

    kind: str
    label: str


@dataclass(frozen=True)
class ActivitySection:
    """Recent activity panel for the Founder Dashboard."""

    recently_indexed: tuple[str, ...]
    recently_completed_capabilities: tuple[str, ...]
    recent_internal_alpha_weeks: tuple[str, ...]
    items: tuple[ActivityItem, ...]
