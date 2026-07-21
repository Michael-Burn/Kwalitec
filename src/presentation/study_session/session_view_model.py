"""Immutable view models for the Study Session Runner surface.

Presentation containers only. Fields are already-formatted display strings and
Design System components — never domain aggregates or educational decision
objects.
"""

from __future__ import annotations

from dataclasses import dataclass

from presentation.design_system import (
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
    Stepper,
    Timeline,
)
from presentation.mission_workspace.workspace_view_model import CompletionActionView


@dataclass(frozen=True, slots=True)
class SessionSectionView:
    """One ordered section in the guided session runner."""

    key: str
    title: str
    body: str = ""
    eyebrow: str = ""


@dataclass(frozen=True, slots=True)
class LearningResourceView:
    """One learning-resource card for the session runner."""

    label: str
    detail: str = ""
    kind: str = "task"
    estimated_minutes: int | None = None
    card: Card | None = None


@dataclass(frozen=True, slots=True)
class WorkedExampleView:
    """One worked-example presentation snippet."""

    label: str
    detail: str = ""
    card: Card | None = None


@dataclass(frozen=True, slots=True)
class CompletionSummaryView:
    """Completion checklist and summary chrome (presentation only)."""

    headline: str
    detail: str
    checklist: tuple[str, ...] = ()
    actions: tuple[CompletionActionView, ...] = ()


@dataclass(frozen=True, slots=True)
class NextStepView:
    """Next-step CTA projected from already-decided recommendation content."""

    headline: str
    detail: str
    category_label: str = ""
    action_key: str = ""
    action_label: str = ""
    card: RecommendationCard | None = None
    primary_button: Button | None = None


@dataclass(frozen=True, slots=True)
class StudySessionViewModel:
    """Guided study experience for one mission / session.

    Immutable and framework-independent. Composes Design System contracts only.
    Contains no educational engines and no mutable state.
    """

    header: PageHeader
    mission_card: MissionCard
    objective: Section
    explanation: Section
    duration: StatisticTile
    resources: tuple[LearningResourceView, ...]
    worked_examples: tuple[WorkedExampleView, ...]
    progress_bar: ProgressBar
    progress_card: ProgressCard
    study_notes: Section
    reflection: Section
    completion: CompletionSummaryView
    next_step: NextStepView
    timeline: Timeline
    stepper: Stepper
    sections: tuple[SessionSectionView, ...]
    container_width: ContainerWidth = ContainerWidth.CONTENT
    greeting: str = ""
