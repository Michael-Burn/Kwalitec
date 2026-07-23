"""StudyWorkspaceService — compose Education OS outputs into Study Workspace.

Projection only. Never estimates mastery, generates recommendations,
generates missions, schedules work, persists data, implements timers,
renders UI, or invokes AI.
"""

from __future__ import annotations

from application.student_experience.workspace.ids import (
    WorkspaceId,
    WorkspaceSnapshotId,
)
from application.student_experience.workspace.models.study_workspace_view_model import (
    StudyWorkspaceViewModel,
)
from application.student_experience.workspace.models.workspace_snapshot import (
    WorkspaceSnapshot,
)
from application.student_experience.workspace.ports.workspace_publisher import (
    WorkspacePublisher,
)
from application.student_experience.workspace.ports.workspace_resource_provider import (
    WorkspaceResource,
    WorkspaceResourceProvider,
)
from application.student_experience.workspace.workspace_composer import (
    compose_snapshot,
    compose_workspace,
)
from application.student_experience.workspace.workspace_inputs import WorkspaceInputs


class StudyWorkspaceService:
    """Application service composing the Adaptive Study Workspace.

    Consumes Education OS artefacts and optional presentation ports.
    Returns immutable view models suitable for UI binding.
    """

    def __init__(
        self,
        *,
        workspace_publisher: WorkspacePublisher | None = None,
        workspace_resource_provider: WorkspaceResourceProvider | None = None,
    ) -> None:
        self._publisher = workspace_publisher
        self._resources = workspace_resource_provider

    def build_workspace(
        self,
        inputs: WorkspaceInputs,
        *,
        workspace_id: WorkspaceId | str | None = None,
    ) -> StudyWorkspaceViewModel:
        """Compose the full Adaptive Study Workspace view model.

        Args:
            inputs: Caller-supplied Education OS artefacts and ``as_of`` time.
            workspace_id: Optional identity for the composed workspace.
                Defaults to a deterministic id derived from student and time.

        Returns:
            Immutable ``StudyWorkspaceViewModel``.
        """
        resolved_id = self._resolve_workspace_id(inputs, workspace_id)
        resources = self._load_resources(inputs)
        return compose_workspace(
            inputs,
            workspace_id=resolved_id,
            resources=resources,
        )

    def refresh_workspace(
        self,
        inputs: WorkspaceInputs,
        *,
        workspace_id: WorkspaceId | str | None = None,
    ) -> StudyWorkspaceViewModel:
        """Rebuild the workspace and publish it when a publisher is configured.

        Args:
            inputs: Caller-supplied Education OS artefacts and ``as_of`` time.
            workspace_id: Optional identity for the composed workspace.

        Returns:
            Freshly composed ``StudyWorkspaceViewModel``.
        """
        workspace = self.build_workspace(inputs, workspace_id=workspace_id)
        if self._publisher is not None:
            self._publisher.publish_workspace(workspace)
            snapshot = self.build_snapshot(workspace)
            self._publisher.publish_snapshot(snapshot)
        return workspace

    def build_snapshot(
        self,
        workspace: StudyWorkspaceViewModel,
        *,
        snapshot_id: WorkspaceSnapshotId | str | None = None,
    ) -> WorkspaceSnapshot:
        """Project a composed workspace into a compact snapshot.

        Args:
            workspace: Previously composed ``StudyWorkspaceViewModel``.
            snapshot_id: Optional snapshot identity. Defaults to a
                deterministic id derived from the workspace identity and time.

        Returns:
            Immutable ``WorkspaceSnapshot``.
        """
        resolved = self._resolve_snapshot_id(workspace, snapshot_id)
        return compose_snapshot(workspace, snapshot_id=resolved)

    def _load_resources(
        self, inputs: WorkspaceInputs
    ) -> tuple[WorkspaceResource, ...]:
        if self._resources is None:
            return ()
        mission_id = None
        session_id = None
        if inputs.mission_execution is not None:
            mission_id = str(inputs.mission_execution.mission_id)
        elif inputs.mission_plan is not None and inputs.mission_plan.missions:
            mission_id = str(inputs.mission_plan.missions[0].mission_id)
        if inputs.current_session is not None:
            session_id = inputs.current_session.session_id.value
        return self._resources.list_resources(
            inputs.student_id,
            mission_id=mission_id,
            session_id=session_id,
        )

    @staticmethod
    def _resolve_workspace_id(
        inputs: WorkspaceInputs, workspace_id: WorkspaceId | str | None
    ) -> WorkspaceId:
        if isinstance(workspace_id, WorkspaceId):
            return workspace_id
        if isinstance(workspace_id, str) and workspace_id.strip():
            return WorkspaceId(workspace_id.strip())
        stamp = inputs.as_of.strftime("%Y%m%dT%H%M%S")
        return WorkspaceId(f"workspace:{inputs.student_id}:{stamp}")

    @staticmethod
    def _resolve_snapshot_id(
        workspace: StudyWorkspaceViewModel,
        snapshot_id: WorkspaceSnapshotId | str | None,
    ) -> WorkspaceSnapshotId:
        if isinstance(snapshot_id, WorkspaceSnapshotId):
            return snapshot_id
        if isinstance(snapshot_id, str) and snapshot_id.strip():
            return WorkspaceSnapshotId(snapshot_id.strip())
        stamp = workspace.composed_at.strftime("%Y%m%dT%H%M%S")
        return WorkspaceSnapshotId(
            f"wsnap:{workspace.workspace_id.value}:{stamp}"
        )
