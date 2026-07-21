"""Student Dashboard 2.0 — command-centre presentation surface.

Consumes ``PipelineResult``, ``MissionWorkspaceViewModel``, and optional Twin /
evidence / statistics / achievement projections. Formats already-decided
Educational OS outputs into an immutable dashboard view model composed from the
Design System. Never diagnoses, recommends, persists, orchestrates learning, or
invokes AI.
"""

from __future__ import annotations

from presentation.dashboard.achievement_mapper import AchievementMapper
from presentation.dashboard.dashboard_mapper import DashboardMapper
from presentation.dashboard.dashboard_presenter import DashboardPresenter
from presentation.dashboard.dashboard_view_model import (
    AchievementView,
    DashboardViewModel,
    QuickActionView,
    StreakView,
    UpcomingSessionView,
)
from presentation.dashboard.mission_card_mapper import MissionCardMapper
from presentation.dashboard.progress_mapper import ProgressMapper
from presentation.dashboard.statistics_mapper import StatisticsMapper

__all__ = [
    "AchievementMapper",
    "AchievementView",
    "DashboardMapper",
    "DashboardPresenter",
    "DashboardViewModel",
    "MissionCardMapper",
    "ProgressMapper",
    "QuickActionView",
    "StatisticsMapper",
    "StreakView",
    "UpcomingSessionView",
]
