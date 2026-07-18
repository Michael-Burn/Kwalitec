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

    def preview(self, workspace_id: str) -> PreviewSnapshot:
        """Generate Preview — prefer Management gate preview; fallback structural."""
        workspace = self._require_workspace(workspace_id)
        hierarchy: list[PreviewNode] = []
        objectives = workspace.objective_ids
        prerequisites = workspace.prerequisite_edges
        workload = workspace.estimated_workload_hours

        if workspace.version_id and self._management is not None:
            try:
                if self._management.is_available():
                    payload = self._management.preview_version(
                        workspace.version_id
                    )
                    hierarchy = _nodes_from_payload(payload)
                    if payload.get("objectives"):
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
            order = 0
            for section_id in workspace.section_ids:
                hierarchy.append(
                    PreviewNode.create(
                        section_id,
                        section_id,
                        kind="section",
                        order_index=order,
                    )
                )
                order += 1
            for topic_id in workspace.topic_ids:
                hierarchy.append(
                    PreviewNode.create(
                        topic_id,
                        topic_id,
                        kind="topic",
                        order_index=order,
                    )
                )
                order += 1

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
        if not workspace.section_ids and not workspace.topic_ids:
            # Allow Management preview content to satisfy hierarchy
            if workspace.version_id and self._management is not None:
                try:
                    payload = require_management(
                        self._management, action="approve_preview"
                    ).preview_version(workspace.version_id)
                    if not payload.get("nodes") and not payload.get("hierarchy"):
                        raise PreviewError(
                            f"Preview approval requires hierarchy for {workspace_id}"
                        )
                except PreviewError:
                    raise
                except Exception as exc:
                    raise PreviewError(
                        f"Preview approval requires hierarchy for {workspace_id}"
                    ) from exc
            else:
                raise PreviewError(
                    f"Preview approval requires hierarchy for {workspace_id}"
                )

        if workspace.version_id and self._management is not None:
            mgmt = require_management(self._management, action="approve_preview")
            # Ensure Management preview exists, then approve gate
            mgmt.preview_version(workspace.version_id)
            mgmt.approve(
                workspace.version_id,
                actor_id=actor_id,
                occurred_at=occurred_at,
                reason=reason or "preview_approved",
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

    def _require_workspace(self, workspace_id: str):
        workspace = self._registry.get_workspace(workspace_id)
        if workspace is None:
            raise WorkspaceNotFound(f"Workspace not found: {workspace_id!r}")
        return workspace


def _nodes_from_payload(payload: dict) -> list[PreviewNode]:
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
    return nodes
