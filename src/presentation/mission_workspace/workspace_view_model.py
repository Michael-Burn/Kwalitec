"""Immutable view models for the Mission Workspace surface.

Presentation containers only. Fields are already-formatted display strings and
structured presentation snippets — never domain aggregates or educational
decision objects.
"""

from __future__ import annotations

from dataclasses import dataclass

from presentation.provenance import ProvenanceViewModel


@dataclass(frozen=True, slots=True)
class StudyResourceView:
    """One study resource card derived from mission tasks or enrichment tips."""

    label: str
    detail: str = ""
    kind: str = "task"
    estimated_minutes: int | None = None


@dataclass(frozen=True, slots=True)
class ProgressSummaryView:
    """Honest progress summary forwarded from ProgressReport presentation fields."""

    headline: str
    detail: str
    trend_label: str
    confidence_label: str
    metric_lines: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class RecommendationSummaryView:
    """Recommendation summary echoing already-decided recommendation content."""

    headline: str
    detail: str
    category_label: str
    expected_outcome: str = ""


@dataclass(frozen=True, slots=True)
class ReflectionStatusView:
    """Reflection readiness chrome derived from student-experience presentation."""

    label: str
    detail: str
    is_available: bool = True


@dataclass(frozen=True, slots=True)
class SessionProgressView:
    """Session progress counts and labels from SessionSummary / plan facts."""

    completed_missions: int
    planned_minutes: int
    objective_preview: str
    mastery_trend_label: str
    confidence_trend_label: str
    session_count: int = 0
    progress_label: str = ""


@dataclass(frozen=True, slots=True)
class CompletionActionView:
    """One completion / next-step CTA label (presentation only)."""

    label: str
    detail: str = ""
    action_key: str = ""


@dataclass(frozen=True, slots=True)
class MissionWorkspaceViewModel:
    """Primary study workspace projection for one pipeline session.

    Immutable and framework-independent. Safe to serialise or pass to any UI
    adapter. Contains no educational engines and no mutable state.
    """

    greeting: str
    mission_title: str
    mission_objective: str
    mission_explanation: str
    estimated_duration: str
    study_resources: tuple[StudyResourceView, ...]
    progress_summary: ProgressSummaryView
    recommendation_summary: RecommendationSummaryView
    reflection_status: ReflectionStatusView
    session_progress: SessionProgressView
    completion_actions: tuple[CompletionActionView, ...]
    provenance: ProvenanceViewModel | None = None
