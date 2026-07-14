"""Weekly briefing metadata DTOs for Founder Dashboard (FSI-002)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WeeklyBriefSection:
    """Current weekly brief metadata for dashboard display.

    Metadata only — the dashboard does not render full brief body sections.
    """

    available: bool
    week: str
    generated_at: str
    snapshot_version: str
    recommendation_version: str
    report_version: str
