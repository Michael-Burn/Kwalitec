"""Adaptive Study Workspace — XP-004.

Application-layer composition of Education OS outputs into a focused,
distraction-free study workspace.

Responsibilities
    Project existing educational artefacts into immutable view models.

Non-responsibilities
    Estimate mastery, generate recommendations, generate missions,
    persist data, implement timers, render UI, or call AI.
"""

from __future__ import annotations

from application.student_experience.workspace.enums import (
    FocusPromptKind,
    ObjectiveStatus,
    PriorityLabel,
    QualityIndicatorKind,
    ResourceKind,
    SessionPresence,
    TimerDisplayState,
)
from application.student_experience.workspace.errors import (
    WorkspaceExperienceError,
    WorkspaceInvariantViolation,
)
from application.student_experience.workspace.ids import (
    WorkspaceId,
    WorkspaceSnapshotId,
)
from application.student_experience.workspace.models import (
    CompletionCard,
    CurrentSessionCard,
    FocusCard,
    FocusPrompt,
    MissionCard,
    ObjectiveItem,
    ObjectivesCard,
    ProgressCard,
    QualityIndicator,
    ReflectionCard,
    ResourceItem,
    ResourcesCard,
    SessionTimerCard,
    StudyWorkspaceViewModel,
    WorkspaceSnapshot,
)
from application.student_experience.workspace.ports import (
    WorkspacePublisher,
    WorkspaceResource,
    WorkspaceResourceProvider,
)
from application.student_experience.workspace.study_workspace_service import (
    StudyWorkspaceService,
)
from application.student_experience.workspace.workspace_inputs import WorkspaceInputs

__all__ = [
    # Service
    "StudyWorkspaceService",
    # Inputs
    "WorkspaceInputs",
    # Identity
    "WorkspaceId",
    "WorkspaceSnapshotId",
    # View models
    "StudyWorkspaceViewModel",
    "CurrentSessionCard",
    "MissionCard",
    "ObjectivesCard",
    "ObjectiveItem",
    "ResourcesCard",
    "ResourceItem",
    "ProgressCard",
    "QualityIndicator",
    "FocusCard",
    "FocusPrompt",
    "SessionTimerCard",
    "ReflectionCard",
    "CompletionCard",
    "WorkspaceSnapshot",
    # Enums
    "SessionPresence",
    "PriorityLabel",
    "ObjectiveStatus",
    "FocusPromptKind",
    "QualityIndicatorKind",
    "ResourceKind",
    "TimerDisplayState",
    # Errors
    "WorkspaceExperienceError",
    "WorkspaceInvariantViolation",
    # Ports
    "WorkspacePublisher",
    "WorkspaceResource",
    "WorkspaceResourceProvider",
]
