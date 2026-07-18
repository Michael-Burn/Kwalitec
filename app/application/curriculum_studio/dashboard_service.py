"""DashboardService — Founder dashboard projection (no persistence)."""

from __future__ import annotations

from app.application.curriculum_studio._registry import StudioRegistry
from app.application.curriculum_studio._snapshots import workspace_snapshot
from app.application.curriculum_studio.dto.dashboard_snapshot import (
    ActivityEntrySnapshot,
    DashboardSnapshot,
)
from app.application.curriculum_studio.dto.workspace_snapshot import (
    WorkspaceSnapshot,
)
from app.application.curriculum_studio.ports.curriculum_management_port import (
    CurriculumManagementPort,
)
from app.application.curriculum_studio.publication_checklist_service import (
    PublicationChecklistService,
)
from app.domain.curriculum_studio.curriculum_workspace import WorkspaceStatus
from app.domain.curriculum_studio.workflow_stage import WorkflowStage


class DashboardService:
    """Project Founder dashboard aggregates from workspaces + Management.

    Projection only. No persistence. No publication authority.
    """

    def __init__(
        self,
        registry: StudioRegistry,
        *,
        management: CurriculumManagementPort | None = None,
    ) -> None:
        self._registry = registry
        self._management = management
        self._checklist = PublicationChecklistService(
            registry, management=management
        )

    def dashboard(self, *, activity_limit: int = 20) -> DashboardSnapshot:
        """Build the Founder Curriculum Studio dashboard projection."""
        workspaces = self._registry.list_workspaces()
        published: list[WorkspaceSnapshot] = []
        drafts: list[WorkspaceSnapshot] = []
        pending_validation: list[WorkspaceSnapshot] = []
        pending_approval: list[WorkspaceSnapshot] = []
        readiness = []
        recent_publications = []

        for ws in workspaces:
            snap = workspace_snapshot(ws)
            pub = self._checklist.checklist(ws.workspace_id)
            readiness.append(pub)

            if (
                ws.status is WorkspaceStatus.PUBLISHED
                or pub.lifecycle_status == "published"
            ):
                published.append(snap)
                recent_publications.append(pub)
            elif ws.status is WorkspaceStatus.ARCHIVED:
                pass
            else:
                drafts.append(snap)

            if (
                ws.current_stage is WorkflowStage.VALIDATION
                and not ws.facts.validation_passed
            ):
                pending_validation.append(snap)
            if (
                ws.current_stage in {
                    WorkflowStage.APPROVAL,
                    WorkflowStage.PREVIEW,
                }
                and not ws.facts.preview_approved
            ):
                pending_approval.append(snap)
            elif (
                ws.facts.validation_passed
                and ws.facts.preview_approved is False
                and ws.status is WorkspaceStatus.DRAFT
            ):
                if snap not in pending_approval:
                    pending_approval.append(snap)

        activity = tuple(
            ActivityEntrySnapshot(
                activity_id=a.activity_id,
                kind=a.kind,
                message=a.message,
                occurred_at=a.occurred_at,
                workspace_id=a.workspace_id,
                subject_code=a.subject_code,
                version_id=a.version_id,
            )
            for a in self._registry.list_activity(limit=activity_limit)
        )

        ready_count = sum(1 for p in readiness if p.ready_to_publish)

        return DashboardSnapshot(
            published_curricula=tuple(published),
            draft_curricula=tuple(drafts),
            pending_validation=tuple(pending_validation),
            pending_approval=tuple(pending_approval),
            recent_publications=tuple(recent_publications[-10:]),
            recent_activity=activity,
            publication_readiness=tuple(readiness),
            published_count=len(published),
            draft_count=len(drafts),
            pending_validation_count=len(pending_validation),
            pending_approval_count=len(pending_approval),
            ready_to_publish_count=ready_count,
        )
