"""DTO projections from Curriculum Studio domain objects."""

from __future__ import annotations

from app.application.curriculum_studio.dto.preview_snapshot import (
    PreviewNodeSnapshot,
    PreviewSnapshot,
)
from app.application.curriculum_studio.dto.publication_snapshot import (
    ChecklistItemSnapshot,
    PublicationSnapshot,
)
from app.application.curriculum_studio.dto.validation_snapshot import (
    ValidationFindingSnapshot,
    ValidationSnapshot,
)
from app.application.curriculum_studio.dto.version_snapshot import (
    VersionRecordSnapshot,
    VersionSnapshot,
)
from app.application.curriculum_studio.dto.workflow_snapshot import (
    WorkflowSnapshot,
    WorkflowTransitionSnapshot,
)
from app.application.curriculum_studio.dto.workspace_snapshot import (
    WorkspaceSnapshot,
)
from app.domain.curriculum_studio.curriculum_workspace import CurriculumWorkspace
from app.domain.curriculum_studio.preview_summary import PreviewSummary
from app.domain.curriculum_studio.publication_summary import PublicationSummary
from app.domain.curriculum_studio.studio_workflow import StudioWorkflow
from app.domain.curriculum_studio.validation_summary import ValidationSummary
from app.domain.curriculum_studio.version_history import (
    VersionHistory,
    VersionRecord,
)
from app.domain.curriculum_studio.workflow_stage import (
    next_stage,
    previous_stage,
    stage_label,
)


def workspace_snapshot(workspace: CurriculumWorkspace) -> WorkspaceSnapshot:
    """Project a CurriculumWorkspace to WorkspaceSnapshot."""
    checklist = workspace.checklist
    return WorkspaceSnapshot(
        workspace_id=workspace.workspace_id,
        subject_code=workspace.subject_code,
        subject_title=workspace.subject_title,
        version_label=workspace.version_label,
        version_id=workspace.version_id,
        status=workspace.status.value,
        current_stage=workspace.current_stage.value,
        ready_to_publish=workspace.ready_to_publish,
        checklist_satisfied_count=checklist.satisfied_count,
        checklist_pending_count=checklist.pending_count,
        section_ids=workspace.section_ids,
        topic_ids=workspace.topic_ids,
        objective_ids=workspace.objective_ids,
        estimated_workload_hours=workspace.estimated_workload_hours,
        notes=workspace.notes,
    )


def workflow_snapshot(
    workflow: StudioWorkflow,
    *,
    can_advance: bool | None = None,
    can_retreat: bool | None = None,
) -> WorkflowSnapshot:
    """Project a StudioWorkflow to WorkflowSnapshot."""
    advance = (
        can_advance
        if can_advance is not None
        else next_stage(workflow.current_stage) is not None
    )
    retreat = (
        can_retreat
        if can_retreat is not None
        else previous_stage(workflow.current_stage) is not None
    )
    history = tuple(
        WorkflowTransitionSnapshot(
            from_stage=r.from_stage.value,
            to_stage=r.to_stage.value,
            event=r.event.value,
            occurred_at=r.occurred_at,
            actor_id=r.actor_id,
            reason=r.reason,
        )
        for r in workflow.history
    )
    return WorkflowSnapshot(
        workflow_id=workflow.workflow_id,
        workspace_id=workflow.workspace_id,
        current_stage=workflow.current_stage.value,
        highest_stage_reached=workflow.highest_stage_reached.value,
        stage_index=workflow.stage_index,
        transition_count=workflow.transition_count,
        history=history,
        stage_label=stage_label(workflow.current_stage),
        can_advance=advance,
        can_retreat=retreat,
    )


def validation_snapshot(summary: ValidationSummary) -> ValidationSnapshot:
    """Project a ValidationSummary to ValidationSnapshot."""

    def _finding(f) -> ValidationFindingSnapshot:  # noqa: ANN001
        return ValidationFindingSnapshot(
            code=f.code,
            message=f.message,
            severity=f.severity.value,
            section_id=f.section_id,
            topic_id=f.topic_id,
            is_blocking=f.is_blocking,
        )

    return ValidationSnapshot(
        summary_id=summary.summary_id,
        workspace_id=summary.workspace_id,
        readiness=summary.readiness.value,
        passed=summary.passed,
        section_count=summary.section_count,
        objective_count=summary.objective_count,
        prerequisite_count=summary.prerequisite_count,
        warning_count=summary.warning_count,
        error_count=summary.error_count,
        blocks_publication=summary.blocks_publication,
        detected_sections=summary.detected_sections,
        detected_objectives=summary.detected_objectives,
        warnings=tuple(_finding(w) for w in summary.warnings),
        errors=tuple(_finding(e) for e in summary.errors),
    )


def preview_snapshot(summary: PreviewSummary) -> PreviewSnapshot:
    """Project a PreviewSummary to PreviewSnapshot."""
    hierarchy = tuple(
        PreviewNodeSnapshot(
            node_id=n.node_id,
            title=n.title,
            kind=n.kind,
            parent_id=n.parent_id,
            order_index=n.order_index,
        )
        for n in summary.hierarchy
    )
    return PreviewSnapshot(
        preview_id=summary.preview_id,
        workspace_id=summary.workspace_id,
        readiness=summary.readiness.value,
        validation_passed=summary.validation_passed,
        publication_ready=summary.publication_ready,
        is_approved=summary.is_approved,
        node_count=summary.node_count,
        objective_count=summary.objective_count,
        prerequisite_count=summary.prerequisite_count,
        estimated_workload_hours=summary.estimated_workload_hours,
        subject_code=summary.subject_code,
        version_label=summary.version_label,
        hierarchy=hierarchy,
        objectives=summary.objectives,
        prerequisites=summary.prerequisites,
    )


def publication_snapshot(summary: PublicationSummary) -> PublicationSnapshot:
    """Project a PublicationSummary to PublicationSnapshot."""
    items: tuple[ChecklistItemSnapshot, ...] = ()
    if summary.checklist is not None:
        items = tuple(
            ChecklistItemSnapshot(
                code=i.code.value,
                label=i.label,
                status=i.status.value,
                satisfied=i.satisfied,
            )
            for i in summary.checklist.items
        )
    return PublicationSnapshot(
        summary_id=summary.summary_id,
        workspace_id=summary.workspace_id,
        subject_code=summary.subject_code,
        version_label=summary.version_label,
        workflow_stage=summary.workflow_stage.value,
        lifecycle_status=summary.lifecycle_status.value,
        ready_to_publish=summary.ready_to_publish,
        rollback_eligible=summary.rollback_eligible,
        version_id=summary.version_id,
        checklist_item_count=summary.checklist_item_count,
        blocking_codes=tuple(c.value for c in summary.blocking_codes),
        checklist_items=items,
    )


def version_record_snapshot(record: VersionRecord) -> VersionRecordSnapshot:
    """Project a VersionRecord to VersionRecordSnapshot."""
    return VersionRecordSnapshot(
        version_id=record.version_id,
        workspace_id=record.workspace_id,
        subject_code=record.subject_code,
        version_label=record.version_label,
        status=record.status.value,
        created_at=record.created_at,
        published_at=record.published_at,
        archived_at=record.archived_at,
        parent_version_id=record.parent_version_id,
        rollback_snapshot_id=record.rollback_snapshot_id,
        rollback_eligible=record.rollback_eligible,
        notes=record.notes,
    )


def version_snapshot(history: VersionHistory) -> VersionSnapshot:
    """Project a VersionHistory to VersionSnapshot."""
    current = history.current_published()
    return VersionSnapshot(
        subject_code=history.subject_code,
        version_count=history.version_count,
        published_count=len(history.published()),
        draft_count=len(history.drafts()),
        archived_count=len(history.archived()),
        current_published_id=current.version_id if current else None,
        records=tuple(version_record_snapshot(r) for r in history.records),
    )
