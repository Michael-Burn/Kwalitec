"""PublicationService — orchestrate approve/publish via Curriculum Management."""

from __future__ import annotations

from app.application.curriculum_studio._ports import as_str, require_management
from app.application.curriculum_studio._registry import StudioRegistry
from app.application.curriculum_studio.dto.publication_snapshot import (
    PublicationSnapshot,
)
from app.application.curriculum_studio.exceptions import (
    PublicationError,
    WorkspaceNotFound,
)
from app.application.curriculum_studio.ports.curriculum_management_port import (
    CurriculumManagementPort,
)
from app.application.curriculum_studio.publication_checklist_service import (
    PublicationChecklistService,
)
from app.domain.curriculum_studio.curriculum_workspace import WorkspaceStatus
from app.domain.curriculum_studio.publication_checklist import (
    WorkspacePublicationFacts,
)
from app.domain.curriculum_studio.version_history import StudioVersionStatus


class PublicationService:
    """Orchestrate Founder publication use-cases through Management.

    Studio never owns publication state. Management ``publish`` /
    ``archive`` / ``approve`` are the authority. Studio syncs workspace
    projection status and checklist facts after successful port calls.
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

    def checklist(self, workspace_id: str) -> PublicationSnapshot:
        """Return the computed publication checklist for a workspace."""
        return self._checklist.checklist(workspace_id)

    def assert_ready(self, workspace_id: str) -> PublicationSnapshot:
        """Raise when the workspace checklist is not ready to publish."""
        snap = self.checklist(workspace_id)
        if not snap.ready_to_publish:
            raise PublicationError(
                f"Not ready to publish {workspace_id}: "
                f"blocking={list(snap.blocking_codes)}"
            )
        return snap

    def approve(
        self,
        workspace_id: str,
        *,
        actor_id: str | None = None,
        occurred_at: str = "",
        reason: str = "",
    ) -> PublicationSnapshot:
        """Approve Curriculum — Management authority."""
        mgmt = require_management(self._management, action="approve")
        workspace = self._require_workspace(workspace_id)
        if not workspace.version_id:
            raise PublicationError("Approval requires an assigned version")
        mgmt.approve(
            workspace.version_id,
            actor_id=actor_id,
            occurred_at=occurred_at,
            reason=reason or "founder_approval",
        )
        facts = WorkspacePublicationFacts.create(
            cmp_uploaded=workspace.facts.cmp_uploaded,
            official_syllabus_uploaded=workspace.facts.official_syllabus_uploaded,
            validation_passed=workspace.facts.validation_passed,
            blueprint_assigned=workspace.facts.blueprint_assigned,
            preview_approved=True,
            version_assigned=workspace.facts.version_assigned,
            rollback_snapshot_created=workspace.facts.rollback_snapshot_created,
        )
        self._registry.put_workspace(workspace.with_facts(facts))
        self._registry.record_activity(
            "approved",
            f"Approved {workspace_id}",
            workspace_id=workspace_id,
            subject_code=workspace.subject_code,
            version_id=workspace.version_id,
            occurred_at=occurred_at,
        )
        return self.checklist(workspace_id)

    def publish(
        self,
        workspace_id: str,
        *,
        occurred_at: str = "",
        actor_id: str | None = None,
    ) -> PublicationSnapshot:
        """Publish Curriculum — Management authority."""
        mgmt = require_management(self._management, action="publish")
        workspace = self._require_workspace(workspace_id)
        self.assert_ready(workspace_id)
        if not workspace.version_id:
            raise PublicationError("Publication requires an assigned version")
        result = mgmt.publish(
            workspace.version_id,
            actor_id=actor_id,
            occurred_at=occurred_at,
        )
        state = as_str(
            result.get("publication_state")
            or mgmt.publication_state(workspace.version_id)
            or "published"
        ).lower()
        if state != "published":
            raise PublicationError(
                f"Management did not publish {workspace.version_id}: {state}"
            )
        # Mirror projection only — not authority
        self._mirror_version_status(
            workspace.version_id,
            StudioVersionStatus.PUBLISHED,
            published_at=occurred_at or "published",
        )
        self._registry.put_workspace(
            workspace.with_status(WorkspaceStatus.PUBLISHED)
        )
        self._registry.record_activity(
            "published",
            f"Published {workspace_id}",
            workspace_id=workspace_id,
            subject_code=workspace.subject_code,
            version_id=workspace.version_id,
            occurred_at=occurred_at,
        )
        return self.checklist(workspace_id)

    def archive(
        self,
        workspace_id: str,
        *,
        occurred_at: str = "",
        actor_id: str | None = None,
    ) -> PublicationSnapshot:
        """Archive Version — Management authority."""
        mgmt = require_management(self._management, action="archive")
        workspace = self._require_workspace(workspace_id)
        if not workspace.version_id:
            raise PublicationError("Archive requires an assigned version")
        # Prefer archive_version when published via Management state
        state = as_str(mgmt.publication_state(workspace.version_id) or "")
        if state == "published" or workspace.status is WorkspaceStatus.PUBLISHED:
            mgmt.archive(
                workspace.version_id,
                actor_id=actor_id,
                occurred_at=occurred_at,
            )
        else:
            raise PublicationError(
                f"Archive requires published workspace; got {workspace.status.value}"
            )
        self._mirror_version_status(
            workspace.version_id,
            StudioVersionStatus.ARCHIVED,
            archived_at=occurred_at or "archived",
        )
        self._registry.put_workspace(
            workspace.with_status(WorkspaceStatus.ARCHIVED)
        )
        self._registry.record_activity(
            "archived",
            f"Archived {workspace_id}",
            workspace_id=workspace_id,
            subject_code=workspace.subject_code,
            version_id=workspace.version_id,
            occurred_at=occurred_at,
        )
        return self.checklist(workspace_id)

    def update_facts(
        self,
        workspace_id: str,
        *,
        cmp_uploaded: bool | None = None,
        official_syllabus_uploaded: bool | None = None,
        validation_passed: bool | None = None,
        blueprint_assigned: bool | None = None,
        preview_approved: bool | None = None,
        version_assigned: bool | None = None,
        rollback_snapshot_created: bool | None = None,
    ) -> PublicationSnapshot:
        """Update publication facts (inputs only — checklist is recomputed).

        Intended for port-sync and test seeding. Prefer use-case methods
        that set facts after successful port responses.
        """
        workspace = self._require_workspace(workspace_id)
        f = workspace.facts
        facts = WorkspacePublicationFacts.create(
            cmp_uploaded=_or(cmp_uploaded, f.cmp_uploaded),
            official_syllabus_uploaded=_or(
                official_syllabus_uploaded, f.official_syllabus_uploaded
            ),
            validation_passed=_or(validation_passed, f.validation_passed),
            blueprint_assigned=_or(blueprint_assigned, f.blueprint_assigned),
            preview_approved=_or(preview_approved, f.preview_approved),
            version_assigned=_or(version_assigned, f.version_assigned),
            rollback_snapshot_created=_or(
                rollback_snapshot_created, f.rollback_snapshot_created
            ),
        )
        self._registry.put_workspace(workspace.with_facts(facts))
        return self.checklist(workspace_id)

    def _mirror_version_status(
        self,
        version_id: str,
        status: StudioVersionStatus,
        *,
        published_at: str | None = None,
        archived_at: str | None = None,
    ) -> None:
        record = self._registry.get_version(version_id)
        if record is None:
            return
        updated = record.with_status(
            status,
            published_at=published_at,
            archived_at=archived_at,
            rollback_snapshot_id=(
                record.rollback_snapshot_id
                or (
                    f"rb-{version_id}"
                    if status is StudioVersionStatus.PUBLISHED
                    else None
                )
            ),
        )
        self._registry.put_version(updated)

    def _require_workspace(self, workspace_id: str):
        workspace = self._registry.get_workspace(workspace_id)
        if workspace is None:
            raise WorkspaceNotFound(f"Workspace not found: {workspace_id!r}")
        return workspace


def _or(override: bool | None, current: bool) -> bool:
    return current if override is None else bool(override)
