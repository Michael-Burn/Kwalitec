"""View-model projections for Curriculum Studio UI."""

from __future__ import annotations

from dataclasses import dataclass

from app.application.curriculum_studio.dto.dashboard_snapshot import DashboardSnapshot
from app.application.curriculum_studio.dto.workspace_snapshot import WorkspaceSnapshot
from app.domain.curriculum_studio.workflow_stage import WorkflowStage

# Founder-facing stage labels (DX-004C strip). Domain tokens unchanged.
STAGE_LABELS: dict[str, str] = {
    WorkflowStage.SUBJECT.value: "Upload",
    WorkflowStage.CONTENT_SOURCES.value: "Upload",
    WorkflowStage.VALIDATION.value: "Validate",
    WorkflowStage.PREVIEW.value: "Review",
    WorkflowStage.APPROVAL.value: "Approve",
    WorkflowStage.PUBLICATION.value: "Publish",
}

# Suggested primary CTA key → button/form identity for templates (DX-004C).
PRIMARY_ACTION_BY_STAGE: dict[str, str] = {
    WorkflowStage.SUBJECT.value: "advance",
    WorkflowStage.CONTENT_SOURCES.value: "upload",
    WorkflowStage.VALIDATION.value: "validate",
    WorkflowStage.PREVIEW.value: "preview",
    WorkflowStage.APPROVAL.value: "approve",
    WorkflowStage.PUBLICATION.value: "publish",
}

NEXT_ACTION_BY_STAGE: dict[str, str] = {
    WorkflowStage.SUBJECT.value: (
        "Confirm the subject, then continue to Upload."
    ),
    WorkflowStage.CONTENT_SOURCES.value: (
        "Upload the Official CMP and Official Syllabus PDFs, then validate "
        "the curriculum."
    ),
    WorkflowStage.VALIDATION.value: (
        "Run validation after both official documents are uploaded and "
        "extraction has finished."
    ),
    WorkflowStage.PREVIEW.value: (
        "Confirm the student-visible curriculum structure, "
        "then approve when it looks right."
    ),
    WorkflowStage.APPROVAL.value: (
        "Approve this curriculum for release. "
        "Published curriculum becomes Ready for students."
    ),
    WorkflowStage.PUBLICATION.value: (
        "Publish this version so students can enrol. "
        "Assign a version label if one is still missing."
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
    "preview_ok": (
        "We've built the preview successfully — {count} curriculum "
        "topics ready to review."
    ),
    "approved": "We've approved your curriculum successfully.",
    "published": "We've published your verified curriculum successfully.",
    "version_assigned": "We've assigned the version successfully.",
    "sources_uploaded": "We've uploaded your curriculum documents successfully.",
}

FLASH_WARNING = {
    "subject_create": (
        "We couldn't create this subject. Incomplete or invalid details "
        "block a clean publishing history. Check the required fields, "
        "then try again."
    ),
    "workspace_open": (
        "We couldn't open this workspace. Workspaces must bind to a known "
        "subject code. Check the subject code, create the subject if needed, "
        "then try again."
    ),
    "advance": (
        "We couldn't advance the workflow. Skipping incomplete stages risks "
        "publishing unfinished curriculum. Complete the current stage, "
        "then try again."
    ),
    "validate": (
        "We couldn't complete validation. Blocking findings prevent a safe "
        "student curriculum. Review the Validation findings, fix CMP or "
        "syllabus issues, then try again."
    ),
    "preview": (
        "We couldn't build this preview. Preview requires a validated "
        "curriculum so students see accurate structure. Validate the "
        "curriculum first, then try again."
    ),
    "approve": (
        "We couldn't approve this curriculum. Approval without a version "
        "and preview risks publishing the wrong package. Assign a version "
        "label, complete preview, then try again."
    ),
    "publish": (
        "We couldn't publish this curriculum. Publication without approval "
        "and a version would expose incomplete material to students. "
        "Assign a version label, complete approval, then try again."
    ),
    "version": (
        "We couldn't assign this version. Clear version labels keep "
        "publication history immutable. Enter a valid version label "
        "(for example 1.0.0), then try again."
    ),
    "upload": (
        "We couldn't upload documents. Official CMP and Official Syllabus "
        "PDFs are required before validation. Choose valid PDF files, "
        "then try again."
    ),
    "workspace_missing": (
        "That workspace could not be found. Opening a missing workspace "
        "would lose your place in the publishing flow. Return to Curriculum "
        "Studio, select a valid workspace, then try again."
    ),
}


@dataclass(frozen=True)
class BreadcrumbItem:
    label: str
    endpoint: str | None = None
    url_kwargs: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class ValidationFindingView:
    """Founder-facing validation finding with recovery guidance."""

    code: str
    message: str
    severity: str
    is_blocking: bool
    why_it_matters: str
    recovery_action: str


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
    validation_findings: tuple[ValidationFindingView, ...] = ()
    has_validation_findings: bool = False


def _dashboard_breadcrumbs() -> tuple[BreadcrumbItem, ...]:
    return (
        BreadcrumbItem("Home", "founder_dashboard.index"),
        BreadcrumbItem("Curriculum Studio"),
    )


def _workspace_breadcrumbs(workspace: WorkspaceSnapshot) -> tuple[BreadcrumbItem, ...]:
    label = (
        workspace.subject_title
        or workspace.subject_code
        or workspace.workspace_id
    )
    return (
        BreadcrumbItem("Home", "founder_dashboard.index"),
        BreadcrumbItem("Subjects", "curriculum_studio.subjects_hub"),
        BreadcrumbItem(label),
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
    validation_findings: tuple[ValidationFindingView, ...] = (),
) -> WorkspacePageView:
    from app.presentation.curriculum_studio.founder_stages import (
        FOUNDER_STAGES,
        founder_stage_index,
        founder_stage_label,
    )

    current = (workspace.current_stage or "").strip().lower()
    founder_label = founder_stage_label(current)
    current_idx = founder_stage_index(current)
    stages = tuple(
        (label.lower(), label, idx == current_idx)
        for idx, label in enumerate(FOUNDER_STAGES)
    )
    history = tuple(version_history)
    findings = tuple(validation_findings)
    blocking = tuple(f for f in findings if f.is_blocking)
    primary = PRIMARY_ACTION_BY_STAGE.get(current, "advance")
    if blocking and founder_label in {
        "Validate",
        "Review",
        "Approve",
        "Publish",
    }:
        primary = "resolve"
    elif (
        founder_label == "Publish"
        and not (workspace.version_label or "").strip()
    ):
        primary = "version"
    return WorkspacePageView(
        workspace=workspace,
        stage_label=founder_label,
        workflow_stages=stages,
        validation_summary=validation_summary or EMPTY_VALIDATION_SUMMARY,
        preview_summary=preview_summary or EMPTY_PREVIEW_SUMMARY,
        checklist_summary=checklist_summary or EMPTY_CHECKLIST_SUMMARY,
        version_history=history,
        has_version_history=bool(history),
        empty_version_message=EMPTY_VERSION_HISTORY_GUIDANCE,
        next_action_label=NEXT_ACTION_BY_STAGE.get(
            current,
            "Complete the next publication stage.",
        ),
        primary_action=primary,
        breadcrumbs=_workspace_breadcrumbs(workspace),
        validation_findings=findings,
        has_validation_findings=bool(findings),
    )


def friendly_validation_summary(*, readiness: str, passed: bool) -> str:
    """Human-readable validation status for the workspace readiness card."""
    if passed:
        return f"Validation completed successfully · {readiness}"
    return f"Validation needs attention · {readiness}"


def friendly_preview_summary(*, readiness: str, node_count: int) -> str:
    """Human-readable preview status for the workspace readiness card."""
    topics = "topic" if node_count == 1 else "topics"
    token = (readiness or "").strip().lower()
    if node_count <= 0:
        return "Preview not ready — no extracted curriculum topics yet"
    if token in {"not_ready", "rejected"}:
        return f"Preview needs attention · {readiness} · {node_count} {topics}"
    if token in {"ready_for_review", "approved"}:
        return f"Preview ready · {readiness} · {node_count} {topics}"
    return f"Preview · {readiness} · {node_count} {topics}"


def friendly_checklist_summary(*, ready: int, total: int) -> str:
    """Human-readable checklist status for the workspace readiness card."""
    if total <= 0:
        return EMPTY_CHECKLIST_SUMMARY
    if ready >= total:
        return f"All {total} checklist items are ready."
    return f"{ready} of {total} checklist items ready."
