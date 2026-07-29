"""PreviewService — Founder gate preview via Management; optional EP surface."""

from __future__ import annotations

from app.application.curriculum_studio._ports import (
    optional_platform,
    require_management,
)
from app.application.curriculum_studio._registry import StudioRegistry
from app.application.curriculum_studio._snapshots import preview_snapshot
from app.application.curriculum_studio.dto.preview_snapshot import PreviewSnapshot
from app.application.curriculum_studio.exceptions import (
    PreviewError,
    WorkspaceNotFound,
)
from app.application.curriculum_studio.ports.curriculum_management_port import (
    CurriculumManagementPort,
)
from app.application.curriculum_studio.ports.education_platform_port import (
    EducationPlatformPort,
)
from app.application.curriculum_studio.structure_preparation_service import (
    StructurePreparationService,
)
from app.domain.curriculum_studio.preview_summary import (
    PreviewNode,
    PreviewReadiness,
    PreviewSummary,
)
from app.domain.curriculum_studio.publication_checklist import (
    WorkspacePublicationFacts,
)


class PreviewService:
    """Display Founder publication-gate preview from Curriculum Management.

    Optional student-surface from Education Platform is display-only.
    Preview never publishes and never mutates Management publication state
    except via explicit approve/reject port calls.
    """

    def __init__(
        self,
        registry: StudioRegistry,
        *,
        management: CurriculumManagementPort | None = None,
        education_platform: EducationPlatformPort | None = None,
    ) -> None:
        self._registry = registry
        self._management = management
        self._platform = education_platform
        self._structure = StructurePreparationService(
            registry, management=management
        )

    def preview(self, workspace_id: str) -> PreviewSnapshot:
        """Generate Preview — prefer prepared structure; advance Management gate."""
        workspace = self._require_workspace(workspace_id)
        hierarchy: list[PreviewNode] = []
        objectives = workspace.objective_ids
        prerequisites = workspace.prerequisite_edges
        workload = workspace.estimated_workload_hours

        # PI-002R: Founder-facing hierarchy comes from the same prepared
        # structure used at validation (CIP / Foundation / workspace).
        structure_hierarchy = self._hierarchy_from_structure(workspace_id, workspace)

        if workspace.version_id and self._management is not None:
            try:
                if self._management.is_available():
                    payload = self._management.preview_version(
                        workspace.version_id
                    )
                    mgmt_hierarchy = _nodes_from_payload(payload)
                    # Prefer prepared structure when present so Preview matches
                    # the curriculum the Founder validated.
                    if structure_hierarchy:
                        hierarchy = structure_hierarchy
                    else:
                        hierarchy = mgmt_hierarchy
                    if payload.get("objectives") and not objectives:
                        objectives = tuple(
                            str(o) for o in payload["objectives"]
                        )
                    if payload.get("prerequisites"):
                        prerequisites = tuple(
                            (str(a), str(b))
                            for a, b in payload["prerequisites"]
                        )
                    if payload.get("estimated_workload_hours") is not None:
                        workload = float(payload["estimated_workload_hours"])
            except Exception:  # noqa: BLE001 — fall back to workspace projection
                hierarchy = []

        if not hierarchy:
            hierarchy = structure_hierarchy

        # Optional student-surface (display only — does not alter readiness)
        platform = optional_platform(self._platform)
        if platform is not None:
            try:
                platform.student_surface(
                    subject_code=workspace.subject_code,
                    version_id=workspace.version_id,
                )
            except Exception:  # noqa: BLE001
                pass

        summary = PreviewSummary.create(
            f"prev-{workspace_id}",
            workspace_id,
            hierarchy=hierarchy,
            objectives=objectives,
            prerequisites=prerequisites,
            estimated_workload_hours=workload,
            validation_passed=workspace.facts.validation_passed,
            publication_ready=workspace.ready_to_publish,
            readiness=(
                PreviewReadiness.APPROVED
                if workspace.facts.preview_approved
                else None
            ),
            subject_code=workspace.subject_code,
            version_label=workspace.version_label,
        )
        return preview_snapshot(summary)

    def build_for_review(self, workspace_id: str) -> PreviewSnapshot:
        """Build preview and require meaningful curriculum content.

        Raises:
            PreviewError: When hierarchy is empty (contradictory success banned).
        """
        # Prefer freshly synced extraction when Management preview is thin.
        try:
            self._structure.prepare_for_validation(workspace_id)
        except Exception:  # noqa: BLE001 — preview still attempts existing structure
            pass
        snap = self.preview(workspace_id)
        if snap.node_count <= 0:
            raise PreviewError(
                f"Preview has no curriculum topics for {workspace_id}. "
                "Complete extraction and validation before building preview."
            )
        return snap

    def approve(
        self,
        workspace_id: str,
        *,
        require_validation: bool = True,
        actor_id: str | None = None,
        occurred_at: str = "",
        reason: str = "",
    ) -> PreviewSnapshot:
        """Approve Curriculum preview — Management authority when version linked."""
        workspace = self._require_workspace(workspace_id)
        if require_validation and not workspace.facts.validation_passed:
            raise PreviewError(
                f"Preview approval requires validation for {workspace_id}"
            )
        snap = self.build_for_review(workspace_id)
        if snap.node_count <= 0:
            raise PreviewError(
                f"Preview approval requires hierarchy for {workspace_id}"
            )

        if workspace.version_id and self._management is not None:
            mgmt = require_management(self._management, action="approve_preview")
            # Ensure Management preview exists (advances PREVIEW_READY), then approve
            mgmt.preview_version(workspace.version_id)
            mgmt.approve(
                workspace.version_id,
                actor_id=actor_id,
                occurred_at=occurred_at,
                reason=reason or "preview_approved",
            )

        workspace = self._require_workspace(workspace_id)
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
            "preview_approved",
            f"Preview approved for {workspace_id}",
            workspace_id=workspace_id,
            subject_code=workspace.subject_code,
            version_id=workspace.version_id,
            occurred_at=occurred_at,
        )
        return self.preview(workspace_id)

    def reject(
        self,
        workspace_id: str,
        *,
        actor_id: str | None = None,
        occurred_at: str = "",
        reason: str = "",
    ) -> PreviewSnapshot:
        """Reject preview approval (clears fact; notifies Management when linked)."""
        workspace = self._require_workspace(workspace_id)
        if workspace.version_id and self._management is not None:
            try:
                if self._management.is_available():
                    self._management.reject(
                        workspace.version_id,
                        actor_id=actor_id,
                        occurred_at=occurred_at,
                        reason=reason or "preview_rejected",
                    )
            except Exception:  # noqa: BLE001
                pass
        facts = WorkspacePublicationFacts.create(
            cmp_uploaded=workspace.facts.cmp_uploaded,
            official_syllabus_uploaded=workspace.facts.official_syllabus_uploaded,
            validation_passed=workspace.facts.validation_passed,
            blueprint_assigned=workspace.facts.blueprint_assigned,
            preview_approved=False,
            version_assigned=workspace.facts.version_assigned,
            rollback_snapshot_created=workspace.facts.rollback_snapshot_created,
        )
        self._registry.put_workspace(workspace.with_facts(facts))
        snap = self.preview(workspace_id)
        summary = PreviewSummary.create(
            snap.preview_id,
            snap.workspace_id,
            hierarchy=tuple(
                PreviewNode.create(
                    n.node_id,
                    n.title,
                    kind=n.kind,
                    parent_id=n.parent_id,
                    order_index=n.order_index,
                )
                for n in snap.hierarchy
            ),
            objectives=snap.objectives,
            prerequisites=snap.prerequisites,
            estimated_workload_hours=snap.estimated_workload_hours,
            validation_passed=snap.validation_passed,
            publication_ready=False,
            readiness=PreviewReadiness.REJECTED,
            subject_code=snap.subject_code,
            version_label=snap.version_label,
        )
        return preview_snapshot(summary)

    def _hierarchy_from_structure(
        self, workspace_id: str, workspace
    ) -> list[PreviewNode]:
        nodes: list[PreviewNode] = []
        order = 0
        for node_id, title, kind in self._structure.hierarchy_nodes(workspace_id):
            nodes.append(
                PreviewNode.create(
                    node_id,
                    title,
                    kind=kind,
                    order_index=order,
                )
            )
            order += 1
        if nodes:
            return nodes
        for section_id in workspace.section_ids:
            nodes.append(
                PreviewNode.create(
                    section_id,
                    section_id,
                    kind="section",
                    order_index=order,
                )
            )
            order += 1
        for topic_id in workspace.topic_ids:
            nodes.append(
                PreviewNode.create(
                    topic_id,
                    topic_id,
                    kind="topic",
                    order_index=order,
                )
            )
            order += 1
        return nodes

    def _require_workspace(self, workspace_id: str):
        workspace = self._registry.get_workspace(workspace_id)
        if workspace is None:
            raise WorkspaceNotFound(f"Workspace not found: {workspace_id!r}")
        return workspace


def _nodes_from_payload(payload: dict) -> list[PreviewNode]:
    """Map Management preview payloads into PreviewNode hierarchy.

    Management returns section_refs / assignment_sections rather than
    hierarchy/nodes — both shapes are accepted.
    """
    raw = payload.get("hierarchy") or payload.get("nodes") or ()
    nodes: list[PreviewNode] = []
    for idx, item in enumerate(raw):
        if isinstance(item, dict):
            nodes.append(
                PreviewNode.create(
                    str(item.get("node_id") or item.get("id") or f"n-{idx}"),
                    str(item.get("title") or item.get("node_id") or f"n-{idx}"),
                    kind=str(item.get("kind") or "topic"),
                    parent_id=(
                        None
                        if item.get("parent_id") is None
                        else str(item.get("parent_id"))
                    ),
                    order_index=int(item.get("order_index") or idx),
                )
            )
        else:
            nodes.append(
                PreviewNode.create(str(item), str(item), kind="topic", order_index=idx)
            )
    if nodes:
        return nodes

    # Management PreviewSnapshot shape (opaque_dict)
    section_refs = list(payload.get("section_refs") or ())
    assignment_sections = list(payload.get("assignment_sections") or ())
    asset_labels = list(payload.get("asset_labels") or ())
    order = 0
    seen: set[str] = set()
    for ref in (*section_refs, *assignment_sections):
        token = str(ref).strip()
        if not token or token in seen:
            continue
        seen.add(token)
        nodes.append(
            PreviewNode.create(token, token, kind="section", order_index=order)
        )
        order += 1
    if not nodes:
        for label in asset_labels:
            token = str(label).strip()
            if not token or token in seen:
                continue
            seen.add(token)
            nodes.append(
                PreviewNode.create(token, token, kind="topic", order_index=order)
            )
            order += 1
    return nodes
