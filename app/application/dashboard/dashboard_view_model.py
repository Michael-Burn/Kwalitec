"""Dashboard ViewModel — closed immutable presentation artefact.

Maps the Educational Experience Contract into presentation-only fields the
dashboard surface may render. Never carries Decision, Recommendation, Mission,
ReadinessState, Twin, or Curriculum domain objects.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.dashboard.recommendation_card_builder import (
    RecommendationCardViewModel,
)


@dataclass(frozen=True)
class MissionCardViewModel:
    """Today's Mission presentation cargo — display only."""

    title: str
    summary: str | None
    task_count: int
    task_headlines: tuple[str, ...]
    duration_display: str | None
    warning: str | None
    show_open_button: bool


@dataclass(frozen=True)
class ReadinessSummaryViewModel:
    """Readiness posture presentation — forwarded honesty, never recomputed."""

    overall_posture: str
    warrant_posture: str
    cold_start: bool
    honesty_cue: str | None


@dataclass(frozen=True)
class ProgressSummaryViewModel:
    """Non-selecting progress cues — never next-action authority."""

    overall_posture: str
    warrant_posture: str
    cold_start: bool
    progress_cues: tuple[str, ...]


@dataclass(frozen=True)
class NavigationAffordancesViewModel:
    """Finished-path CTA visibility — no dead-button theatre."""

    can_start_recommendation: bool
    can_open_mission: bool
    can_view_explanation: bool
    can_view_readiness: bool
    can_view_progress: bool


@dataclass(frozen=True)
class FeatureVisibilityViewModel:
    """Feature-flag inclusion snapshot — gates presentation, not truth."""

    recommendations: bool
    missions: bool
    explainability: bool
    progress: bool


@dataclass(frozen=True)
class DashboardViewModel:
    """Closed Dashboard presentation artefact for one assembly pass.

    Sparse / empty sections are lawful. Fabricated educational certainty is not.
    """

    recommendation_card: RecommendationCardViewModel | None
    mission_card: MissionCardViewModel | None
    readiness_summary: ReadinessSummaryViewModel | None
    progress_summary: ProgressSummaryViewModel | None
    warnings: tuple[str, ...]
    empty_states: tuple[str, ...]
    navigation: NavigationAffordancesViewModel
    feature_visibility: FeatureVisibilityViewModel
