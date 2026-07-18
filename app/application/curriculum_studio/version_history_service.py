"""VersionHistoryService — version lifecycle via Curriculum Management."""

from __future__ import annotations

from app.application.curriculum_studio._ports import as_str, require_management
from app.application.curriculum_studio._registry import StudioRegistry
from app.application.curriculum_studio._snapshots import (
    version_record_snapshot,
    version_snapshot,
)
from app.application.curriculum_studio.dto.version_snapshot import (
    VersionRecordSnapshot,
    VersionSnapshot,
)
from app.application.curriculum_studio.exceptions import (
    VersionError,
    VersionNotFound,
    WorkspaceNotFound,
)
from app.application.curriculum_studio.ports.curriculum_management_port import (
    CurriculumManagementPort,
)
from app.domain.curriculum_studio.curriculum_workspace import CurriculumWorkspace
from app.domain.curriculum_studio.publication_checklist import (
    WorkspacePublicationFacts,
)
from app.domain.curriculum_studio.version_history import (
    StudioVersionStatus,
    VersionHistory,
    VersionRecord,
)


class VersionHistoryService:
    """View and orchestrate version history through Management.

    Version lifecycle belongs to Curriculum Management.
    Studio mirrors records for Founder UX linkage only.
    """

    def __init__(
        self,
        registry: StudioRegistry,
        *,
        management: CurriculumManagementPort | None = None,
    ) -> None:
        self._registry = registry
        self._management = management

    def assign_version(
        self,
        workspace_id: str,
        version_label: str,
        *,
        version_id: str | None = None,
        created_at: str = "",
        parent_version_id: str | None = None,
        notes: str = "",
    ) -> VersionRecordSnapshot:
        """Assign a Management version to a workspace and mirror locally."""
        workspace = self._require_workspace(workspace_id)
        mgmt = require_management(self._management, action="assign_version")
        summary = mgmt.create_version(
            workspace.subject_code,
            version_label,
            version_id=version_id,
            parent_version_id=parent_version_id,
            notes=notes,
        )
        vid = as_str(summary.get("version_id") or version_id)
        if not vid:
            raise VersionError("Management create_version returned no version_id")
        if self._registry.get_version(vid) is not None:
            raise VersionError(f"Version already exists: {vid!r}")
        record = VersionRecord.create(
            vid,
            workspace_id,
            workspace.subject_code,
            as_str(summary.get("version_label") or version_label),
            status=StudioVersionStatus.DRAFT,
            created_at=created_at or as_str(summary.get("created_at")),
            parent_version_id=parent_version_id,
            notes=notes,
        )
        self._registry.put_version(record)
        facts = WorkspacePublicationFacts.create(
            cmp_uploaded=workspace.facts.cmp_uploaded,
            official_syllabus_uploaded=workspace.facts.official_syllabus_uploaded,
            validation_passed=workspace.facts.validation_passed,
            blueprint_assigned=workspace.facts.blueprint_assigned,
            preview_approved=workspace.facts.preview_approved,
            version_assigned=True,
            rollback_snapshot_created=workspace.facts.rollback_snapshot_created,
        )
        updated = CurriculumWorkspace.create(
            workspace.workspace_id,
            workspace.subject_code,
            subject_title=workspace.subject_title,
            version_label=record.version_label,
            version_id=vid,
            status=workspace.status,
            workflow=workspace.workflow,
            facts=facts,
            section_ids=workspace.section_ids,
            topic_ids=workspace.topic_ids,
            objective_ids=workspace.objective_ids,
            prerequisite_edges=workspace.prerequisite_edges,
            metadata=workspace.metadata,
            estimated_workload_hours=workspace.estimated_workload_hours,
            notes=workspace.notes,
        )
        self._registry.put_workspace(updated)
        self._registry.record_activity(
            "version_assigned",
            f"Assigned version {vid}",
            workspace_id=workspace_id,
            subject_code=workspace.subject_code,
            version_id=vid,
        )
        return version_record_snapshot(record)

    def create_rollback_snapshot(
        self,
        version_id: str,
        *,
        snapshot_id: str | None = None,
    ) -> VersionRecordSnapshot:
        """Attach a rollback snapshot id (Management-backed when available)."""
        record = self._require_version(version_id)
        sid = snapshot_id or f"rb-{version_id}"
        # Management may encode rollback eligibility on version summary
        if self._management is not None and self._management.is_available():
            summary = self._management.get_version_summary(version_id) or {}
            if summary.get("rollback_snapshot_id"):
                sid = as_str(summary["rollback_snapshot_id"])
        updated = VersionRecord.create(
            record.version_id,
            record.workspace_id,
            record.subject_code,
            record.version_label,
            status=record.status,
            created_at=record.created_at,
            published_at=record.published_at,
            archived_at=record.archived_at,
            parent_version_id=record.parent_version_id,
            rollback_snapshot_id=sid,
            notes=record.notes,
        )
        self._registry.put_version(updated)
        workspace = self._registry.get_workspace(record.workspace_id)
        if workspace is not None and workspace.version_id == version_id:
            facts = WorkspacePublicationFacts.create(
                cmp_uploaded=workspace.facts.cmp_uploaded,
                official_syllabus_uploaded=(
                    workspace.facts.official_syllabus_uploaded
                ),
                validation_passed=workspace.facts.validation_passed,
                blueprint_assigned=workspace.facts.blueprint_assigned,
                preview_approved=workspace.facts.preview_approved,
                version_assigned=workspace.facts.version_assigned,
                rollback_snapshot_created=True,
            )
            self._registry.put_workspace(workspace.with_facts(facts))
        return version_record_snapshot(updated)

    def archive_version(
        self,
        version_id: str,
        *,
        archived_at: str = "",
    ) -> VersionRecordSnapshot:
        """Archive Version — Management authority."""
        mgmt = require_management(self._management, action="archive_version")
        record = self._require_version(version_id)
        summary = mgmt.archive_version(version_id, occurred_at=archived_at)
        status_token = as_str(
            summary.get("status")
            or summary.get("publication_state")
            or "archived"
        ).lower()
        if status_token != "archived":
            raise VersionError(
                f"Management did not archive {version_id}: {status_token}"
            )
        updated = record.with_status(
            StudioVersionStatus.ARCHIVED,
            archived_at=archived_at or "archived",
        )
        self._registry.put_version(updated)
        self._registry.record_activity(
            "version_archived",
            f"Archived version {version_id}",
            workspace_id=record.workspace_id,
            subject_code=record.subject_code,
            version_id=version_id,
            occurred_at=archived_at,
        )
        return version_record_snapshot(updated)

    def rollback_version(
        self,
        version_id: str,
        *,
        occurred_at: str = "",
    ) -> VersionRecordSnapshot:
        """Rollback Version — Management authority."""
        mgmt = require_management(self._management, action="rollback_version")
        record = self._require_version(version_id)
        summary = mgmt.rollback_version(version_id, occurred_at=occurred_at)
        if not as_str(summary.get("version_id") or version_id):
            raise VersionError(f"Rollback failed for {version_id}")
        self._registry.record_activity(
            "version_rollback",
            f"Rolled back to {version_id}",
            workspace_id=record.workspace_id,
            subject_code=record.subject_code,
            version_id=version_id,
            occurred_at=occurred_at,
        )
        # Re-project from Management summary when present
        refreshed = self._registry.get_version(version_id) or record
        return version_record_snapshot(refreshed)

    def get_version(self, version_id: str) -> VersionRecordSnapshot:
        """Return a single version record snapshot (local mirror or Management)."""
        local = self._registry.get_version(version_id)
        if local is not None:
            return version_record_snapshot(local)
        if self._management is not None and self._management.is_available():
            summary = self._management.get_version_summary(version_id)
            if summary is not None:
                return _record_from_summary(summary)
        raise VersionNotFound(f"Version not found: {version_id!r}")

    def history(self, subject_code: str) -> VersionSnapshot:
        """View Version History — prefer Management list; fall back to mirror."""
        code = subject_code.strip().upper()
        if self._management is not None and self._management.is_available():
            try:
                summaries = self._management.list_versions(code)
                if summaries:
                    records = tuple(
                        _record_from_summary(s, fallback_subject=code)
                        for s in summaries
                    )
                    published = sum(1 for r in records if r.status == "published")
                    drafts = sum(1 for r in records if r.status == "draft")
                    archived = sum(1 for r in records if r.status == "archived")
                    current = next(
                        (r.version_id for r in records if r.status == "published"),
                        None,
                    )
                    return VersionSnapshot(
                        subject_code=code,
                        version_count=len(records),
                        published_count=published,
                        draft_count=drafts,
                        archived_count=archived,
                        current_published_id=current,
                        records=records,
                    )
            except Exception:  # noqa: BLE001
                pass
        history = self._registry.get_history(code) or VersionHistory.create(code)
        return version_snapshot(history)

    def rollback_eligible(
        self, subject_code: str
    ) -> tuple[VersionRecordSnapshot, ...]:
        """Return rollback-eligible version snapshots for a subject."""
        snap = self.history(subject_code)
        return tuple(r for r in snap.records if r.rollback_eligible)

    # Compatibility aliases used by older tests / facade
    def publish_version(
        self,
        version_id: str,
        *,
        published_at: str = "",
        actor_id: str | None = None,
    ) -> VersionRecordSnapshot:
        """Publish a version via Management (compatibility)."""
        record = self._require_version(version_id)
        mgmt = require_management(self._management, action="publish_version")
        mgmt.publish(version_id, actor_id=actor_id, occurred_at=published_at)
        updated = record.with_status(
            StudioVersionStatus.PUBLISHED,
            published_at=published_at or "published",
            rollback_snapshot_id=record.rollback_snapshot_id
            or f"rb-{version_id}",
        )
        self._registry.put_version(updated)
        return version_record_snapshot(updated)

    def _require_workspace(self, workspace_id: str):
        workspace = self._registry.get_workspace(workspace_id)
        if workspace is None:
            raise WorkspaceNotFound(f"Workspace not found: {workspace_id!r}")
        return workspace

    def _require_version(self, version_id: str) -> VersionRecord:
        record = self._registry.get_version(version_id)
        if record is None:
            raise VersionNotFound(f"Version not found: {version_id!r}")
        return record


def _record_from_summary(
    summary: dict,
    *,
    fallback_subject: str = "",
) -> VersionRecordSnapshot:
    status = as_str(
        summary.get("status") or summary.get("publication_state") or "draft"
    )
    rollback_id = summary.get("rollback_snapshot_id")
    rollback_eligible = bool(
        summary.get("rollback_eligible")
        or (
            rollback_id
            and status.lower() in {"published", "archived"}
        )
    )
    return VersionRecordSnapshot(
        version_id=as_str(summary.get("version_id")),
        workspace_id=as_str(summary.get("workspace_id")),
        subject_code=as_str(
            summary.get("subject_code") or fallback_subject
        ).upper(),
        version_label=as_str(summary.get("version_label")),
        status=status.lower(),
        created_at=as_str(summary.get("created_at")),
        published_at=(
            None
            if summary.get("published_at") is None
            else as_str(summary.get("published_at"))
        ),
        archived_at=(
            None
            if summary.get("archived_at") is None
            else as_str(summary.get("archived_at"))
        ),
        parent_version_id=(
            None
            if summary.get("parent_version_id") is None
            else as_str(summary.get("parent_version_id"))
        ),
        rollback_snapshot_id=(
            None if rollback_id is None else as_str(rollback_id)
        ),
        rollback_eligible=rollback_eligible,
        notes=as_str(summary.get("notes")),
    )


# Backwards-compatible alias
VersionService = VersionHistoryService
