"""View-model projections for Curriculum Studio UI."""

from __future__ import annotations

from dataclasses import dataclass

from app.application.curriculum_studio.dto.dashboard_snapshot import DashboardSnapshot
from app.application.curriculum_studio.dto.workspace_snapshot import WorkspaceSnapshot
from app.domain.curriculum_studio.workflow_stage import WorkflowStage

# Founder-facing stage labels (aligned with domain STAGE_LABELS).
STAGE_LABELS: dict[str, str] = {
    WorkflowStage.SUBJECT.value: "Subject",
    WorkflowStage.CONTENT_SOURCES.value: "Content Sources",
    WorkflowStage.VALIDATION.value: "Validation",
    WorkflowStage.PREVIEW.value: "Preview",
    WorkflowStage.APPROVAL.value: "Approval",
    WorkflowStage.PUBLICATION.value: "Publish",
}

# Suggested primary CTA key → button/form identity for templates.
PRIMARY_ACTION_BY_STAGE: dict[str, str] = {
    WorkflowStage.SUBJECT.value: "advance",
    WorkflowStage.CONTENT_SOURCES.value: "validate",
    WorkflowStage.VALIDATION.value: "preview",
    WorkflowStage.PREVIEW.value: "approve",
    WorkflowStage.APPROVAL.value: "publish",
    WorkflowStage.PUBLICATION.value: "version",
}

NEXT_ACTION_BY_STAGE: dict[str, str] = {
    WorkflowStage.SUBJECT.value: (
        "Confirm the subject, then advance to Content Sources."
    ),
    WorkflowStage.CONTENT_SOURCES.value: (
        "When sources are in place, validate the curriculum."
    ),
    WorkflowStage.VALIDATION.value: (
        "Validation looks ready — build a student-facing preview."
    ),
    WorkflowStage.PREVIEW.value: (
        "Assign a version label if needed, review the preview, "
        "then approve when it looks right."
    ),
    WorkflowStage.APPROVAL.value: (
        "Curriculum is approved — publish when you are ready. "
        "Published curriculum becomes available to students."
    ),
    WorkflowStage.PUBLICATION.value: (
        "Confirm the version label and keep version history up to date."
    ),
}

EMPTY_WORKSPACES_GUIDANCE = (
    "No workspaces yet. Create a subject, then open a workspace to begin "
    "the validate → preview → approve → publish journey."
)

EMPTY_ACTIVITY_GUIDANCE = (
    "No recent Studio activity yet. Open a workspace to validate, preview, "
    "or publish a curriculum."
)

EMPTY_VERSION_HISTORY_GUIDANCE = (
    "No versions recorded yet. Assign a version label after approval "
    "to start version history."
)

EMPTY_VALIDATION_SUMMARY = "Not validated yet — run validation when sources are ready."
EMPTY_PREVIEW_SUMMARY = "No preview yet — build a preview after validation."
EMPTY_CHECKLIST_SUMMARY = (
    "Publication checklist unavailable until the workspace is fully prepared."
)

FLASH_SUCCESS = {
    "subject_created": "We've created your subject successfully.",
    "workspace_opened": "We've opened your workspace successfully.",
    "workflow_advanced": "We've advanced the workflow to the next stage.",
    "validation_ok": "We've completed validation successfully.",
    "preview_ok": "We've built the preview successfully.",
    "approved": "We've approved your curriculum successfully.",
    "published": "We've published your curriculum successfully.",
    "version_assigned": "We've assigned the version successfully.",
}

FLASH_WARNING = {
    "subject_create": (
        "We couldn't create this subject. "
        "Check the required fields and try again."
    ),
    "workspace_open": (
        "We couldn't open this workspace. "
        "Check the subject code and try again."
    ),
    "advance": (
        "We couldn't advance the workflow. "
        "Complete the current stage and try again."
    ),
    "validate": (
        "We couldn't complete validation. "
        "Review the curriculum and try again."
    ),
    "preview": (
        "We couldn't build this preview. "
        "Validate the curriculum first, then try again."
    ),
    "approve": (
        "We couldn't approve this curriculum. Assign a version label, "
        "complete preview, and try again."
    ),
    "publish": (
        "We couldn't publish this curriculum. Assign a version label, "
        "complete approval, and try again."
    ),
    "version": (
        "We couldn't assign this version. "
        "Enter a valid version label and try again."
    ),
    "workspace_missing": (
        "That workspace could not be found. "
        "Return to Curriculum Studio, select a valid workspace, and try again."
    ),
}


@dataclass(frozen=True)
class BreadcrumbItem:
    label: str
    endpoint: str | None = None
    url_kwargs: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class StudioDashboardView:
    published_count: int
    draft_count: int
    pending_validation_count: int
    pending_approval_count: int
    workspaces: tuple[WorkspaceSnapshot, ...]
    recent_activity: tuple[str, ...]
    has_workspaces: bool
    has_activity: bool
    empty_workspaces_message: str
    empty_activity_message: str
    breadcrumbs: tuple[BreadcrumbItem, ...]
    next_step_hint: str


@dataclass(frozen=True)
class WorkspacePageView:
    workspace: WorkspaceSnapshot
    stage_label: str
    workflow_stages: tuple[tuple[str, str, bool], ...]
    validation_summary: str
    preview_summary: str
    checklist_summary: str
    version_history: tuple[str, ...]
    has_version_history: bool
    empty_version_message: str
    next_action_label: str
    primary_action: str
    breadcrumbs: tuple[BreadcrumbItem, ...]


def _dashboard_breadcrumbs() -> tuple[BreadcrumbItem, ...]:
    return (
        BreadcrumbItem("Overview", "founder_dashboard.index"),
        BreadcrumbItem("Curriculum Studio"),
    )


def _workspace_breadcrumbs(workspace: WorkspaceSnapshot) -> tuple[BreadcrumbItem, ...]:
    return (
        BreadcrumbItem("Overview", "founder_dashboard.index"),
        BreadcrumbItem("Curriculum Studio", "curriculum_studio.index"),
        BreadcrumbItem(workspace.subject_code or workspace.workspace_id),
    )


def dashboard_view(snap: DashboardSnapshot) -> StudioDashboardView:
    workspaces = tuple(
        dict.fromkeys(
            list(snap.draft_curricula)
            + list(snap.pending_validation)
            + list(snap.pending_approval)
            + list(snap.published_curricula)
        ).keys()
    )
    activity = tuple(f"{a.kind}: {a.message}" for a in snap.recent_activity[:12])
    has_workspaces = bool(workspaces)
    next_hint = (
        "Open a workspace below, or create a subject to start a new curriculum."
        if has_workspaces
        else EMPTY_WORKSPACES_GUIDANCE
    )
    return StudioDashboardView(
        published_count=snap.published_count,
        draft_count=snap.draft_count,
        pending_validation_count=snap.pending_validation_count,
        pending_approval_count=snap.pending_approval_count,
        workspaces=workspaces,
        recent_activity=activity,
        has_workspaces=has_workspaces,
        has_activity=bool(activity),
        empty_workspaces_message=EMPTY_WORKSPACES_GUIDANCE,
        empty_activity_message=EMPTY_ACTIVITY_GUIDANCE,
        breadcrumbs=_dashboard_breadcrumbs(),
        next_step_hint=next_hint,
    )


def workspace_page(
    workspace: WorkspaceSnapshot,
    *,
    validation_summary: str = "",
    preview_summary: str = "",
    checklist_summary: str = "",
    version_history: tuple[str, ...] = (),
) -> WorkspacePageView:
    stages = []
    current = (workspace.current_stage or "").strip().lower()
    for stage in WorkflowStage:
        stages.append(
            (stage.value, STAGE_LABELS[stage.value], stage.value == current)
        )
    history = tuple(version_history)
    return WorkspacePageView(
        workspace=workspace,
        stage_label=STAGE_LABELS.get(current, workspace.current_stage),
        workflow_stages=tuple(stages),
        validation_summary=validation_summary or EMPTY_VALIDATION_SUMMARY,
        preview_summary=preview_summary or EMPTY_PREVIEW_SUMMARY,
        checklist_summary=checklist_summary or EMPTY_CHECKLIST_SUMMARY,
        version_history=history,
        has_version_history=bool(history),
        empty_version_message=EMPTY_VERSION_HISTORY_GUIDANCE,
        next_action_label=NEXT_ACTION_BY_STAGE.get(
            current,
            "Continue the Studio workflow for this curriculum.",
        ),
        primary_action=PRIMARY_ACTION_BY_STAGE.get(current, "advance"),
        breadcrumbs=_workspace_breadcrumbs(workspace),
    )


def friendly_validation_summary(*, readiness: str, passed: bool) -> str:
    """Human-readable validation status for the workspace readiness card."""
    if passed:
        return f"Validation completed successfully · {readiness}"
    return f"Validation needs attention · {readiness}"


def friendly_preview_summary(*, readiness: str, node_count: int) -> str:
    """Human-readable preview status for the workspace readiness card."""
    nodes = "node" if node_count == 1 else "nodes"
    return f"Preview ready · {readiness} · {node_count} {nodes}"


def friendly_checklist_summary(*, ready: int, total: int) -> str:
    """Human-readable checklist status for the workspace readiness card."""
    if total <= 0:
        return EMPTY_CHECKLIST_SUMMARY
    if ready >= total:
        return f"All {total} checklist items are ready."
    return f"{ready} of {total} checklist items ready."
