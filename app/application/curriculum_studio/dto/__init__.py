"""Curriculum Studio DTO package."""

from __future__ import annotations

from app.application.curriculum_studio.dto.dashboard_snapshot import (
    ActivityEntrySnapshot,
    DashboardSnapshot,
)
from app.application.curriculum_studio.dto.preview_snapshot import (
    PreviewNodeSnapshot,
    PreviewSnapshot,
)
from app.application.curriculum_studio.dto.publication_snapshot import (
    ChecklistItemSnapshot,
    PublicationSnapshot,
)
from app.application.curriculum_studio.dto.subject_snapshot import SubjectSnapshot
from app.application.curriculum_studio.dto.validation_snapshot import (
    ValidationFindingSnapshot,
    ValidationSnapshot,
)
from app.application.curriculum_studio.dto.version_snapshot import (
    VersionRecordSnapshot,
    VersionSnapshot,
)
from app.application.curriculum_studio.dto.workflow_snapshot import (
    WorkflowSnapshot,
    WorkflowTransitionSnapshot,
)
from app.application.curriculum_studio.dto.workspace_snapshot import (
    WorkspaceSnapshot,
)

__all__ = [
    "ActivityEntrySnapshot",
    "ChecklistItemSnapshot",
    "DashboardSnapshot",
    "PreviewNodeSnapshot",
    "PreviewSnapshot",
    "PublicationSnapshot",
    "SubjectSnapshot",
    "ValidationFindingSnapshot",
    "ValidationSnapshot",
    "VersionRecordSnapshot",
    "VersionSnapshot",
    "WorkflowSnapshot",
    "WorkflowTransitionSnapshot",
    "WorkspaceSnapshot",
]
