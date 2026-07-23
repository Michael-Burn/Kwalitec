"""Student Dashboard 2.0 — decision-screen presentation surface (PX-003).

Consumes ``PipelineResult``, ``MissionWorkspaceViewModel``, optional Twin /
evidence / statistics / achievement projections, and optional XP experience
snapshots. Formats already-decided Educational OS outputs into an immutable
dashboard view model composed from the Design System. Never diagnoses,
recommends, persists, orchestrates learning, or invokes AI.
"""

from __future__ import annotations

from presentation.dashboard.achievement_mapper import AchievementMapper
from presentation.dashboard.dashboard_mapper import DashboardMapper
from presentation.dashboard.dashboard_presenter import DashboardPresenter
from presentation.dashboard.dashboard_view_model import (
    AchievementView,
    CoachInsightView,
    DashboardViewModel,
    JourneyStoryView,
    MilestoneView,
    MissionHeroView,
    QuickActionView,
    ReadinessSummaryView,
    StreakView,
    UpcomingSessionView,
)
from presentation.dashboard.mission_card_mapper import MissionCardMapper
from presentation.dashboard.progress_mapper import ProgressMapper
from presentation.dashboard.statistics_mapper import StatisticsMapper
from presentation.dashboard.xp_mapper import XpProjectionMapper

__all__ = [
    "AchievementMapper",
    "AchievementView",
    "CoachInsightView",
    "DashboardMapper",
    "DashboardPresenter",
    "DashboardViewModel",
    "JourneyStoryView",
    "MilestoneView",
    "MissionCardMapper",
    "MissionHeroView",
    "ProgressMapper",
    "QuickActionView",
    "ReadinessSummaryView",
    "StatisticsMapper",
    "StreakView",
    "UpcomingSessionView",
    "XpProjectionMapper",
]
