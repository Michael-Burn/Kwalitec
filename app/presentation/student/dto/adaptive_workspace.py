"""Adaptive Study Workspace DTOs (KWP-013).

Presentation projection only — composes existing Educational Intelligence
surfaces into one coherent student workspace. No engine redesign.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WorkspaceMorningBrief:
    """Single adaptive summary answering where I am and what today continues."""

    greeting: str = ""
    momentum_line: str = ""
    yesterday_line: str = ""
    today_line: str = ""
    estimated_study_label: str = ""
    has_brief: bool = False


@dataclass(frozen=True)
class WorkspaceSessionPlan:
    """Today's session plan — duration, objective, status (presentation only)."""

    objective: str = ""
    duration_label: str = ""
    status_label: str = ""
    after_completion: str = ""
    has_plan: bool = False


@dataclass(frozen=True)
class WorkspaceCurrentFocus:
    """Combined Strategy / Diagnostics / Difficulty explanation.

    ``curriculum_why`` (KWP-014) explains why the topic matters inside the
    qualification using explicit curriculum relationships.
    """

    topic_title: str = ""
    guidance: str = ""
    detail: str = ""
    curriculum_why: str = ""
    has_focus: bool = False


@dataclass(frozen=True)
class WorkspaceProgressNarrative:
    """Educational progress story — not isolated metrics."""

    headline: str = ""
    body: str = ""
    has_narrative: bool = False


@dataclass(frozen=True)
class WorkspaceForecastSummary:
    """One concise Readiness Forecast projection (KWP-012 reuse)."""

    title: str = ""
    guidance: str = ""
    href: str = ""
    has_forecast: bool = False


@dataclass(frozen=True)
class WorkspaceJourneyHighlights:
    """One milestone, one pattern, one recent improvement (KWP-011 reuse)."""

    milestone: str = ""
    pattern: str = ""
    improvement: str = ""
    href: str = ""
    has_highlights: bool = False


@dataclass(frozen=True)
class WorkspaceQuickAction:
    """Workspace quick action — Begin / Review / Resume / Journey / Forecast."""

    label: str
    href: str = ""
    detail: str = ""
    kind: str = "link"
    # kind: link | start_form | primary_mission


@dataclass(frozen=True)
class WorkspaceLearningEpisode:
    """Authored Learning Episode projection (KWP-015) — presentation only."""

    educational_context: str = ""
    learning_objective: str = ""
    concept_focus: tuple[str, ...] = ()
    activity_labels: tuple[str, ...] = ()
    success_criteria: tuple[str, ...] = ()
    estimated_duration_label: str = ""
    connection: str = ""
    sequence: int = 1
    has_episode: bool = False


@dataclass(frozen=True)
class WorkspaceTomorrowPreview:
    """Tomorrow's Mission preview (KWP-015) — presentation only."""

    topic_title: str = ""
    continuity_line: str = ""
    estimated_duration_label: str = ""
    start_early_available: bool = False
    start_early_label: str = "Start Early"
    start_early_detail: str = ""
    has_preview: bool = False


@dataclass(frozen=True)
class WorkspaceExtraStudyOffer:
    """Extra study offer when spare capacity remains (KWP-015)."""

    label: str
    detail: str = ""
    kind: str = ""
    href: str = ""


@dataclass(frozen=True)
class WorkspaceMissionComposition:
    """Authored mission arc for workspace (KWP-015).

    Morning Brief → Learning Episode(s) → Checkpoint → Reflection →
    Tomorrow Preview. Presentation projection only.
    """

    mission_narrative: str = ""
    episodes: tuple[WorkspaceLearningEpisode, ...] = ()
    checkpoint_prompt: str = ""
    reflection_prompt: str = ""
    tomorrow_preview: WorkspaceTomorrowPreview | None = None
    extra_study: tuple[WorkspaceExtraStudyOffer, ...] = ()
    total_duration_label: str = ""
    has_composition: bool = False
    # V1S-005 DF-003: calm quiet copy when authoring fails (never silent omit).
    composition_quiet_reason: str = ""


@dataclass(frozen=True)
class AdaptiveStudyWorkspace:
    """Unified Adaptive Study Workspace projection (KWP-013 / KWP-015).

    Layout order (student-facing):
    Morning Brief → Today's Mission → Learning Episode(s) → Session Plan →
    Current Focus → Study Signals → Recent Progress → Tomorrow Preview →
    Extra Study → Forecast → Journey Highlights → Quick Actions.
    """

    morning_brief: WorkspaceMorningBrief | None = None
    session_plan: WorkspaceSessionPlan | None = None
    current_focus: WorkspaceCurrentFocus | None = None
    progress_narrative: WorkspaceProgressNarrative | None = None
    forecast: WorkspaceForecastSummary | None = None
    journey_highlights: WorkspaceJourneyHighlights | None = None
    mission_composition: WorkspaceMissionComposition | None = None
    quick_actions: tuple[WorkspaceQuickAction, ...] = ()
    page_question: str = "What should I do now?"
    enabled: bool = False
