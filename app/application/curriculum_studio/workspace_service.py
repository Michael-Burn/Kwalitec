"""WorkspaceService — Founder workspace session and source upload orchestration."""

from __future__ import annotations

from app.application.curriculum_studio._ports import (
    require_ingestion,
    require_management,
)
from app.application.curriculum_studio._registry import StudioRegistry
from app.application.curriculum_studio._snapshots import workspace_snapshot
from app.application.curriculum_studio.dto.workspace_snapshot import (
    WorkspaceSnapshot,
)
from app.application.curriculum_studio.exceptions import (
    WorkspaceAlreadyExists,
    WorkspaceNotFound,
)
from app.application.curriculum_studio.ports.curriculum_ingestion_port import (
    CurriculumIngestionPort,
)
from app.application.curriculum_studio.ports.curriculum_management_port import (
    CurriculumManagementPort,
)
from app.domain.curriculum_studio.curriculum_workspace import CurriculumWorkspace
from app.domain.curriculum_studio.publication_checklist import (
    WorkspacePublicationFacts,
)


class WorkspaceService:
    """Open and update Founder workspaces; upload sources via ports.

    Workspace identity is Studio-owned. Asset refs belong to Management.
    Document ingestion belongs to Ingestion.
    """

    def __init__(
        self,
        registry: StudioRegistry,
        *,
        management: CurriculumManagementPort | None = None,
        ingestion: CurriculumIngestionPort | None = None,
    ) -> None:
        self._registry = registry
        self._management = management
        self._ingestion = ingestion

    def open_workspace(
        self,
        workspace_id: str,
        subject_code: str,
        *,
        subject_title: str = "",
        version_label: str = "",
        version_id: str | None = None,
        section_ids: list[str] | tuple[str, ...] | None = None,
        topic_ids: list[str] | tuple[str, ...] | None = None,
        objective_ids: list[str] | tuple[str, ...] | None = None,
        prerequisite_edges: (
            list[tuple[str, str]] | tuple[tuple[str, str], ...] | None
        ) = None,
        estimated_workload_hours: float | None = None,
        facts: WorkspacePublicationFacts | None = None,
        notes: str = "",
    ) -> WorkspaceSnapshot:
        """Open Workspace — create a Founder operating session."""
        if self._registry.has_workspace(workspace_id):
            raise WorkspaceAlreadyExists(
                f"Workspace already exists: {workspace_id!r}"
            )
        workspace = CurriculumWorkspace.create(
            workspace_id,
            subject_code,
            subject_title=subject_title,
            version_label=version_label,
            version_id=version_id,
            section_ids=section_ids,
            topic_ids=topic_ids,
            objective_ids=objective_ids,
            prerequisite_edges=prerequisite_edges,
            estimated_workload_hours=estimated_workload_hours,
            facts=facts,
            notes=notes,
        )
        self._registry.put_workspace(workspace)
        self._registry.record_activity(
            "workspace_opened",
            f"Opened workspace {workspace_id}",
            workspace_id=workspace_id,
            subject_code=workspace.subject_code,
            version_id=version_id,
        )
        return workspace_snapshot(workspace)

    def get_workspace(self, workspace_id: str) -> WorkspaceSnapshot:
        """Return a workspace snapshot."""
        return workspace_snapshot(self._require_workspace(workspace_id))

    def list_workspaces(self) -> tuple[WorkspaceSnapshot, ...]:
        """List all registered workspace snapshots."""
        return tuple(
            workspace_snapshot(w) for w in self._registry.list_workspaces()
        )

    def update_structure(
        self,
        workspace_id: str,
        *,
        section_ids: list[str] | tuple[str, ...] | None = None,
        topic_ids: list[str] | tuple[str, ...] | None = None,
        objective_ids: list[str] | tuple[str, ...] | None = None,
        prerequisite_edges: (
            list[tuple[str, str]] | tuple[tuple[str, str], ...] | None
        ) = None,
        estimated_workload_hours: float | None = None,
        subject_title: str | None = None,
        notes: str | None = None,
    ) -> WorkspaceSnapshot:
        """Update structural projection fields on a workspace."""
        workspace = self._require_workspace(workspace_id)
        updated = CurriculumWorkspace.create(
            workspace.workspace_id,
            workspace.subject_code,
            subject_title=(
                workspace.subject_title
                if subject_title is None
                else subject_title
            ),
            version_label=workspace.version_label,
            version_id=workspace.version_id,
            status=workspace.status,
            workflow=workspace.workflow,
            facts=workspace.facts,
            section_ids=(
                workspace.section_ids if section_ids is None else section_ids
            ),
            topic_ids=workspace.topic_ids if topic_ids is None else topic_ids,
            objective_ids=(
                workspace.objective_ids
                if objective_ids is None
                else objective_ids
            ),
            prerequisite_edges=(
                workspace.prerequisite_edges
                if prerequisite_edges is None
                else prerequisite_edges
            ),
            metadata=workspace.metadata,
            estimated_workload_hours=(
                workspace.estimated_workload_hours
                if estimated_workload_hours is None
                else estimated_workload_hours
            ),
            notes=workspace.notes if notes is None else notes,
        )
        self._registry.put_workspace(updated)
        return workspace_snapshot(updated)

    def upload_sources(
        self,
        workspace_id: str,
        *,
        version_id: str | None = None,
        cmp_reference: str | None = None,
        syllabus_reference: str | None = None,
        start_ingestion: bool = True,
    ) -> WorkspaceSnapshot:
        """Upload Curriculum Sources — asset refs via Management; ingest via port."""
        mgmt = require_management(self._management, action="upload_sources")
        workspace = self._require_workspace(workspace_id)
        vid = version_id or workspace.version_id
        if not vid:
            raise WorkspaceNotFound(
                f"Workspace {workspace_id!r} has no version_id for source upload"
            )
        sources: list[dict] = []
        cmp_ok = workspace.facts.cmp_uploaded
        syl_ok = workspace.facts.official_syllabus_uploaded
        if cmp_reference:
            mgmt.add_asset_ref(vid, kind="cmp", reference=cmp_reference)
            sources.append({"kind": "cmp", "reference": cmp_reference})
            cmp_ok = True
        if syllabus_reference:
            mgmt.add_asset_ref(
                vid, kind="syllabus", reference=syllabus_reference
            )
            sources.append(
                {"kind": "syllabus", "reference": syllabus_reference}
            )
            syl_ok = True
        if start_ingestion and sources:
            ing = require_ingestion(self._ingestion, action="upload_sources")
            job = ing.start_ingestion(
                subject_code=workspace.subject_code,
                sources=sources,
            )
            job_id = str(job.get("job_id") or "")
            if job_id:
                self._registry.set_ingestion_job(workspace_id, job_id)
        facts = WorkspacePublicationFacts.create(
            cmp_uploaded=cmp_ok,
            official_syllabus_uploaded=syl_ok,
            validation_passed=workspace.facts.validation_passed,
            blueprint_assigned=workspace.facts.blueprint_assigned,
            preview_approved=workspace.facts.preview_approved,
            version_assigned=workspace.facts.version_assigned,
            rollback_snapshot_created=workspace.facts.rollback_snapshot_created,
        )
        updated = workspace.with_facts(facts)
        self._registry.put_workspace(updated)
        self._registry.record_activity(
            "sources_uploaded",
            f"Uploaded sources for {workspace_id}",
            workspace_id=workspace_id,
            subject_code=workspace.subject_code,
            version_id=vid,
        )
        return workspace_snapshot(updated)

    def assign_blueprint(
        self,
        workspace_id: str,
        *,
        section_id: str,
        blueprint_profile_id: str,
        version_id: str | None = None,
    ) -> WorkspaceSnapshot:
        """Assign blueprint via Management and sync checklist fact."""
        workspace = self._require_workspace(workspace_id)
        vid = version_id or workspace.version_id
        if not vid:
            raise WorkspaceNotFound(
                f"Workspace {workspace_id!r} has no version_id for blueprint"
            )
        mgmt = require_management(self._management, action="assign_blueprint")
        mgmt.assign_blueprint(
            vid,
            section_id=section_id,
            blueprint_profile_id=blueprint_profile_id,
        )
        facts = WorkspacePublicationFacts.create(
            cmp_uploaded=workspace.facts.cmp_uploaded,
            official_syllabus_uploaded=workspace.facts.official_syllabus_uploaded,
            validation_passed=workspace.facts.validation_passed,
            blueprint_assigned=True,
            preview_approved=workspace.facts.preview_approved,
            version_assigned=workspace.facts.version_assigned,
            rollback_snapshot_created=workspace.facts.rollback_snapshot_created,
        )
        updated = workspace.with_facts(facts)
        self._registry.put_workspace(updated)
        return workspace_snapshot(updated)

    def _require_workspace(self, workspace_id: str) -> CurriculumWorkspace:
        workspace = self._registry.get_workspace(workspace_id)
        if workspace is None:
            raise WorkspaceNotFound(f"Workspace not found: {workspace_id!r}")
        return workspace
