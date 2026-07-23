"""WorkspacePublisher — publish composed workspace artefacts outbound."""

from __future__ import annotations

from abc import ABC, abstractmethod

from application.student_experience.workspace.models.study_workspace_view_model import (
    StudyWorkspaceViewModel,
)
from application.student_experience.workspace.models.workspace_snapshot import (
    WorkspaceSnapshot,
)


class WorkspacePublisher(ABC):
    """Outbound port for publishing composed workspace views.

    Implementations live in infrastructure. Publishing is notification /
    persistence wiring — never educational reasoning.
    """

    @abstractmethod
    def publish_workspace(self, workspace: StudyWorkspaceViewModel) -> None:
        """Publish a composed ``StudyWorkspaceViewModel``."""

    @abstractmethod
    def publish_snapshot(self, snapshot: WorkspaceSnapshot) -> None:
        """Publish a composed ``WorkspaceSnapshot``."""
