"""Study Session Runner — guided mission study presentation surface.

Consumes ``PipelineResult`` and/or ``MissionWorkspaceViewModel``. Formats
already-decided Educational OS outputs into an immutable study-session view
model composed from the Design System. Never diagnoses, recommends, persists,
orchestrates learning, or invokes AI.
"""

from __future__ import annotations

from presentation.study_session.completion_mapper import CompletionMapper
from presentation.study_session.resource_mapper import ResourceMapper
from presentation.study_session.session_presenter import SessionPresenter
from presentation.study_session.session_timeline import (
    SECTION_ORDER,
    SessionTimeline,
)
from presentation.study_session.session_view_model import (
    CompletionSummaryView,
    LearningResourceView,
    NextStepView,
    SessionSectionView,
    StudySessionViewModel,
    WorkedExampleView,
)

__all__ = [
    "SECTION_ORDER",
    "CompletionMapper",
    "CompletionSummaryView",
    "LearningResourceView",
    "NextStepView",
    "ResourceMapper",
    "SessionPresenter",
    "SessionSectionView",
    "SessionTimeline",
    "StudySessionViewModel",
    "WorkedExampleView",
]
