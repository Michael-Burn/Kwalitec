"""PublicationChecklistService — computed publication readiness projection."""

from __future__ import annotations

from app.application.curriculum_studio._ports import as_str
from app.application.curriculum_studio._registry import StudioRegistry
from app.application.curriculum_studio._snapshots import publication_snapshot
from app.application.curriculum_studio.dto.publication_snapshot import (
    PublicationSnapshot,
)
from app.application.curriculum_studio.exceptions import WorkspaceNotFound
from app.application.curriculum_studio.ports.curriculum_management_port import (
    CurriculumManagementPort,
)
from app.domain.curriculum_studio.curriculum_workspace import WorkspaceStatus
from app.domain.curriculum_studio.publication_checklist import (
    PublicationChecklist,
)
from app.domain.curriculum_studio.publication_summary import (
    PublicationLifecycleStatus,
    PublicationSummary,
)


class PublicationChecklistService:
    """Project the computed publication checklist for a workspace.

    Checklist items are never manually toggled. Lifecycle status prefers
    Management ``publication_state`` when a version is linked.
    """

    def __init__(
        self,
        registry: StudioRegistry,
        *,
        management: CurriculumManagementPort | None = None,
    ) -> None:
        self._registry = registry
        self._management = management

    def checklist(self, workspace_id: str) -> PublicationSnapshot:
        """Return the computed publication checklist for a workspace."""
        workspace = self._registry.get_workspace(workspace_id)
        if workspace is None:
            raise WorkspaceNotFound(f"Workspace not found: {workspace_id!r}")
        checklist = PublicationChecklist.compute(workspace.facts)
        rollback = False
        if workspace.version_id:
            record = self._registry.get_version(workspace.version_id)
            rollback = bool(record and record.rollback_eligible)
        status = self._lifecycle_status(workspace, checklist)
        summary = PublicationSummary.create(
            f"pub-{workspace_id}",
            workspace_id,
            workspace.subject_code,
            version_label=workspace.version_label,
            workflow_stage=workspace.current_stage,
            lifecycle_status=status,
            checklist=checklist,
            version_id=workspace.version_id,
            rollback_eligible=rollback,
        )
        return publication_snapshot(summary)

    def _lifecycle_status(self, workspace, checklist) -> PublicationLifecycleStatus:
        """Derive projection status; prefer Management publication_state."""
        if workspace.version_id and self._management is not None:
            try:
                if self._management.is_available():
                    token = self._management.publication_state(
                        workspace.version_id
                    )
                    mapped = _map_management_state(token)
                    if mapped is not None:
                        return mapped
            except Exception:  # noqa: BLE001 — projection must not fail hard
                pass
        if workspace.status is WorkspaceStatus.PUBLISHED:
            return PublicationLifecycleStatus.PUBLISHED
        if workspace.status is WorkspaceStatus.ARCHIVED:
            return PublicationLifecycleStatus.ARCHIVED
        if checklist.ready_to_publish:
            return PublicationLifecycleStatus.READY
        if checklist.blocking_codes:
            return PublicationLifecycleStatus.BLOCKED
        return PublicationLifecycleStatus.DRAFT


def _map_management_state(token: str | None) -> PublicationLifecycleStatus | None:
    if token is None:
        return None
    value = as_str(token).strip().lower()
    if value == "published":
        return PublicationLifecycleStatus.PUBLISHED
    if value == "archived":
        return PublicationLifecycleStatus.ARCHIVED
    if value in {"approved", "preview_ready", "blueprint_assigned", "validated"}:
        return PublicationLifecycleStatus.READY
    if value in {"draft", "uploaded"}:
        return PublicationLifecycleStatus.DRAFT
    return None
