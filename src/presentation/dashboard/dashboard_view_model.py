"""Immutable view models for the Student Dashboard 2.0 surface.

Presentation containers only. Fields are already-formatted display strings and
Design System components — never domain aggregates or educational decision
objects.
"""

from __future__ import annotations

from dataclasses import dataclass

from presentation.design_system import (
    Badge,
    Button,
    Card,
    ContainerWidth,
    MissionCard,
    PageHeader,
    ProgressBar,
    ProgressCard,
    RecommendationCard,
    Section,
    StatisticTile,
)


@dataclass(frozen=True, slots=True)
class AchievementView:
    """One achievement recognition card (presentation only)."""

    title: str
    message: str
    kind_label: str = ""
    sequence: int = 0
    badge: Badge | None = None
    card: Card | None = None


@dataclass(frozen=True, slots=True)
class UpcomingSessionView:
    """One upcoming study-session preview card."""

    label: str
    detail: str = ""
    day_label: str = ""
    duration_label: str = ""
    kind_label: str = ""
    card: Card | None = None


@dataclass(frozen=True, slots=True)
class QuickActionView:
    """One dashboard quick-action CTA (presentation only)."""

    label: str
    detail: str = ""
    action_key: str = ""
    button: Button | None = None


@dataclass(frozen=True, slots=True)
class StreakView:
    """Current learning-streak chrome (presentation only)."""

    headline: str
    detail: str
    current_days: int = 0
    longest_days: int = 0
    band_label: str = ""
    tile: StatisticTile | None = None
    badge: Badge | None = None


@dataclass(frozen=True, slots=True)
class DashboardViewModel:
    """Student command-centre projection for one dashboard assembly pass.

    Immutable and framework-independent. Composes Design System contracts only.
    Contains no educational engines and no mutable state.
    """

    header: PageHeader
    greeting: Section
    mission_card: MissionCard
    mission_reason: RecommendationCard
    primary_action: Button
    progress_summary: ProgressCard
    progress_bar: ProgressBar
    learning_statistics: tuple[StatisticTile, ...]
    current_streak: StreakView
    achievements: tuple[AchievementView, ...]
    upcoming_sessions: tuple[UpcomingSessionView, ...]
    quick_actions: tuple[QuickActionView, ...]
    container_width: ContainerWidth = ContainerWidth.WIDE
    greeting_text: str = ""
