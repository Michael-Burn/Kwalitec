"""PublicationService — orchestrate approve/publish via Curriculum Management."""

from __future__ import annotations

import logging

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

logger = logging.getLogger(__name__)


class PublicationService:
    """Orchestrate Founder publication use-cases through Management.

    Studio never owns publication state. Management ``publish`` /
    ``archive`` / ``approve`` are the authority. Studio syncs workspace
    projection status and checklist facts after successful port calls.
    After Management publish, Foundation is bridged so Subject Catalogue
    can show Ready (student-facing SSOT package).
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
        if not workspace.facts.validation_passed:
            raise PublicationError(
                "Approval requires successful validation"
            )
        # Advance Management to PREVIEW_READY when still at BLUEPRINT_ASSIGNED.
        try:
            mgmt.preview_version(workspace.version_id)
        except Exception as exc:
            raise PublicationError(
                "Approval requires a successful preview with curriculum "
                f"content: {exc}"
            ) from exc
        mgmt.approve(
            workspace.version_id,
            actor_id=actor_id,
            occurred_at=occurred_at,
            reason=reason or "founder_approval",
        )
        workspace = self._require_workspace(workspace_id)
        facts = WorkspacePublicationFacts.create(
            cmp_uploaded=workspace.facts.cmp_uploaded,
            official_syllabus_uploaded=workspace.facts.official_syllabus_uploaded,
            validation_passed=workspace.facts.validation_passed,
            blueprint_assigned=True,
            preview_built=True,
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
        """Publish Curriculum — Management authority + Foundation Ready bridge."""
        mgmt = require_management(self._management, action="publish")
        workspace = self._require_workspace(workspace_id)
        self._ensure_rollback_snapshot(workspace_id)
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
        workspace = self._require_workspace(workspace_id)
        self._registry.put_workspace(
            workspace.with_status(WorkspaceStatus.PUBLISHED)
        )
        # Student Subject Catalogue Ready depends on Foundation packages.
        try:
            from app.application.platform_integration.publication_bridge import (
                PublicationBridgeService,
            )

            PublicationBridgeService(self._registry).publish_to_catalogue(
                workspace_id, actor_id=actor_id or ""
            )
        except PublicationError as exc:
            detail = str(exc).lower()
            # Unit paths without Foundation documents still publish via Management.
            if "no foundation" in detail:
                logger.warning("Ready bridge skipped: %s", exc)
            else:
                raise
        except RuntimeError as exc:
            # Outside Flask app context (pure unit tests).
            logger.warning("Ready bridge skipped (no app context): %s", exc)
        except Exception as exc:
            logger.exception("Foundation Ready bridge failed")
            raise PublicationError(
                "Curriculum was approved in Studio but could not become Ready "
                f"in the Subject Catalogue: {exc}"
            ) from exc
        self._registry.record_activity(
            "published",
            f"Published {workspace_id}",
            workspace_id=workspace_id,
            subject_code=workspace.subject_code,
            version_id=workspace.version_id,
            occurred_at=occurred_at,
        )
        return self.checklist(workspace_id)

    def _ensure_rollback_snapshot(self, workspace_id: str) -> None:
        """Create rollback snapshot when missing (safety gate, not a bypass)."""
        workspace = self._require_workspace(workspace_id)
        if workspace.facts.rollback_snapshot_created:
            return
        if not workspace.version_id:
            raise PublicationError("Publication requires an assigned version")
        from app.application.curriculum_studio.version_history_service import (
            VersionHistoryService,
        )

        VersionHistoryService(
            self._registry, management=self._management
        ).create_rollback_snapshot(workspace.version_id)

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
        preview_built: bool | None = None,
        preview_approved: bool | None = None,
        version_assigned: bool | None = None,
        rollback_snapshot_created: bool | None = None,
    ) -> PublicationSnapshot:
        """Update publication facts (inputs only — checklist is recomputed).

        Intended for port-sync and test seeding. Prefer use-case methods
        that set facts after successful port responses.
        """
        from app.application.curriculum_studio.fact_updates import (
            copy_publication_facts,
        )

        workspace = self._require_workspace(workspace_id)
        facts = copy_publication_facts(
            workspace.facts,
            cmp_uploaded=cmp_uploaded,
            official_syllabus_uploaded=official_syllabus_uploaded,
            validation_passed=validation_passed,
            blueprint_assigned=blueprint_assigned,
            preview_built=preview_built,
            preview_approved=preview_approved,
            version_assigned=version_assigned,
            rollback_snapshot_created=rollback_snapshot_created,
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
