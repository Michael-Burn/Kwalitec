"""Immutable view models for the Student Dashboard decision surface (PX-003).

Presentation containers only. Fields are already-formatted display strings and
Design System components — never domain aggregates or educational decision
objects. Hierarchy: Today's Mission → Readiness / Journey / Coach →
Upcoming milestones / Quick actions.
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
from presentation.provenance import ProvenanceViewModel


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
class MissionHeroView:
    """Primary decision hero — greeting, mission, duration, purpose, CTA."""

    greeting: str
    mission_title: str
    duration_label: str
    purpose: str
    cta_label: str
    action_key: str = "begin_session"
    status_label: str = ""
    mission_card: MissionCard | None = None
    primary_action: Button | None = None
    provenance: ProvenanceViewModel | None = None


@dataclass(frozen=True, slots=True)
class ReadinessSummaryView:
    """Compact readiness summary — category, trend, reason, single action."""

    category_label: str
    trend_label: str
    reason: str
    action_label: str = ""
    action_key: str = ""
    percent_label: str = ""
    available: bool = False
    card: Card | None = None
    provenance: ProvenanceViewModel | None = None


@dataclass(frozen=True, slots=True)
class JourneyStoryView:
    """One learning-journey story — never a timeline or metric grid."""

    story: str
    available: bool = False
    card: Card | None = None
    provenance: ProvenanceViewModel | None = None


@dataclass(frozen=True, slots=True)
class CoachInsightView:
    """Single coach insight — maximum 2–3 sentences."""

    insight: str
    available: bool = False
    card: Card | None = None
    provenance: ProvenanceViewModel | None = None


@dataclass(frozen=True, slots=True)
class MilestoneView:
    """One upcoming milestone (tertiary)."""

    title: str
    detail: str = ""
    days_label: str = ""
    card: Card | None = None


@dataclass(frozen=True, slots=True)
class DashboardViewModel:
    """Student decision-screen projection for one dashboard assembly pass.

    Immutable and framework-independent. Composes Design System contracts only.
    Contains no educational engines and no mutable state.
    """

    header: PageHeader
    hero: MissionHeroView
    readiness: ReadinessSummaryView
    journey: JourneyStoryView
    coach: CoachInsightView
    upcoming_milestones: tuple[MilestoneView, ...]
    quick_actions: tuple[QuickActionView, ...]
    container_width: ContainerWidth = ContainerWidth.WIDE
    # Compatibility / secondary chrome — not rendered as metric grids.
    greeting: Section | None = None
    greeting_text: str = ""
    mission_card: MissionCard | None = None
    mission_reason: RecommendationCard | None = None
    primary_action: Button | None = None
    progress_summary: ProgressCard | None = None
    progress_bar: ProgressBar | None = None
    learning_statistics: tuple[StatisticTile, ...] = ()
    current_streak: StreakView | None = None
    achievements: tuple[AchievementView, ...] = ()
    upcoming_sessions: tuple[UpcomingSessionView, ...] = ()
    revision_provenance: ProvenanceViewModel | None = None
