"""Immutable view models for Adaptive Study Workspace."""

from __future__ import annotations

from application.student_experience.workspace.models.completion_card import (
    CompletionCard,
)
from application.student_experience.workspace.models.current_session_card import (
    CurrentSessionCard,
)
from application.student_experience.workspace.models.focus_card import (
    FocusCard,
    FocusPrompt,
)
from application.student_experience.workspace.models.mission_card import MissionCard
from application.student_experience.workspace.models.objectives_card import (
    ObjectiveItem,
    ObjectivesCard,
)
from application.student_experience.workspace.models.progress_card import (
    ProgressCard,
    QualityIndicator,
)
from application.student_experience.workspace.models.reflection_card import (
    ReflectionCard,
)
from application.student_experience.workspace.models.resources_card import (
    ResourceItem,
    ResourcesCard,
)
from application.student_experience.workspace.models.session_timer_card import (
    SessionTimerCard,
)
from application.student_experience.workspace.models.study_workspace_view_model import (
    StudyWorkspaceViewModel,
)
from application.student_experience.workspace.models.workspace_snapshot import (
    WorkspaceSnapshot,
)

__all__ = [
    "CompletionCard",
    "CurrentSessionCard",
    "FocusCard",
    "FocusPrompt",
    "MissionCard",
    "ObjectiveItem",
    "ObjectivesCard",
    "ProgressCard",
    "QualityIndicator",
    "ReflectionCard",
    "ResourceItem",
    "ResourcesCard",
    "SessionTimerCard",
    "StudyWorkspaceViewModel",
    "WorkspaceSnapshot",
]
