"""Mission Workspace — primary study-session presentation surface.

Consumes ``PipelineResult`` only. Formats already-decided Educational OS
outputs into an immutable view model. Never diagnoses, recommends, persists,
or invokes AI.
"""

from __future__ import annotations

from presentation.mission_workspace.mission_progress_mapper import (
    MissionProgressMapper,
)
from presentation.mission_workspace.workspace_presenter import WorkspacePresenter
from presentation.mission_workspace.workspace_view_model import (
    CompletionActionView,
    MissionWorkspaceViewModel,
    ProgressSummaryView,
    RecommendationSummaryView,
    ReflectionStatusView,
    SessionProgressView,
    StudyResourceView,
)

__all__ = [
    "CompletionActionView",
    "MissionProgressMapper",
    "MissionWorkspaceViewModel",
    "ProgressSummaryView",
    "RecommendationSummaryView",
    "ReflectionStatusView",
    "SessionProgressView",
    "StudyResourceView",
    "WorkspacePresenter",
]
