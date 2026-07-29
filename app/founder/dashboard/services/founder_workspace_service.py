"""Founder Publication Workspace service — DX-004C Execution First.

Presentation projection only. Does not alter publication pipeline rules.
"""

from __future__ import annotations

from flask import url_for

from app.application.curriculum_studio.curriculum_studio_service import (
    CurriculumStudioService,
)
from app.application.curriculum_studio.dto.workspace_snapshot import (
    WorkspaceSnapshot,
)
from app.application.curriculum_studio.exceptions import WorkspaceNotFound
from app.domain.curriculum_studio.workflow_stage import (
    WorkflowStage,
    resolve_workflow_stage,
)
from app.founder.dashboard.dto.founder_workspace import (
    BlockingFindingRow,
    FounderWorkspacePage,
)
from app.presentation.curriculum_studio.factory import get_studio_service
from app.presentation.curriculum_studio.founder_stages import (
    FOUNDER_STAGES,
    founder_stage_index,
    founder_stage_label,
)
from app.presentation.curriculum_studio.view_models import (
    EMPTY_VERSION_HISTORY_GUIDANCE,
    ValidationFindingView,
)

# Primary keys map to forms / stage anchors in the workspace template.
PRIMARY_UPLOAD = "upload"
PRIMARY_VALIDATE = "validate"
PRIMARY_RESOLVE = "resolve"
PRIMARY_REVIEW = "preview"
PRIMARY_APPROVE = "approve"
PRIMARY_PUBLISH = "publish"
PRIMARY_ADVANCE = "advance"
PRIMARY_VERSION = "version"

_DEFAULT_PRIMARY_BY_FOUNDER: dict[str, tuple[str, str]] = {
    "Upload": (PRIMARY_UPLOAD, "Upload documents"),
    "Validate": (PRIMARY_VALIDATE, "Validate"),
    "Review": (PRIMARY_REVIEW, "Confirm structure"),
    "Approve": (PRIMARY_APPROVE, "Approve"),
    "Publish": (PRIMARY_PUBLISH, "Publish"),
}

_NEXT_STEP_BY_FOUNDER: dict[str, str] = {
    "Upload": "Upload the required CMP and syllabus, then continue.",
    "Validate": "Run validation so structure can pass readiness checks.",
    "Review": "Confirm the student-visible curriculum structure.",
    "Approve": "Approve this curriculum for release.",
    "Publish": "Publish this version so students can enrol.",
}


class FounderWorkspaceService:
    """Build the DX-004C Publication Workspace page model."""

    def __init__(
        self,
        *,
        studio: CurriculumStudioService | None = None,
    ) -> None:
        self._studio = studio

    def build_page(self, workspace_id: str) -> FounderWorkspacePage:
        studio = self._studio or get_studio_service()
        try:
            workspace = studio.get_workspace(workspace_id)
        except WorkspaceNotFound as exc:
            raise LookupError(workspace_id) from exc

        findings = self._load_blocking_findings(studio, workspace_id)
        founder_label = founder_stage_label(workspace.current_stage)
        # Upload L1 owns source gaps — do not promote validation theatre to L0.
        if founder_label == "Upload":
            findings = ()
        review_summary, supporting = self._load_supporting(
            studio, workspace_id, workspace, founder_label=founder_label
        )
        history = self._load_version_history(studio, workspace.subject_code)
        primary_key, primary_label = self._select_primary(
            workspace=workspace,
            blocking_count=len(findings),
        )
        stage_idx = founder_stage_index(workspace.current_stage)

        return FounderWorkspacePage(
            workspace=workspace,
            subject_code=(workspace.subject_code or "").strip(),
            subject_name=_subject_name(workspace),
            version_label=(workspace.version_label or "").strip() or "Draft",
            stage_label=founder_label,
            status_label=_status_label(workspace),
            founder_stages=FOUNDER_STAGES,
            stage_index=stage_idx,
            primary_key=primary_key,
            primary_label=primary_label,
            next_step_sentence=_NEXT_STEP_BY_FOUNDER.get(
                founder_label,
                "Complete the next publication stage.",
            ),
            blocking_findings=findings,
            blocking_count=len(findings),
            show_upload=founder_label == "Upload",
            show_validate=founder_label == "Validate",
            show_review=founder_label == "Review",
            show_approve=founder_label == "Approve",
            show_publish=founder_label == "Publish",
            supporting_lines=supporting,
            review_summary=review_summary,
            version_history=history,
            has_version_history=bool(history),
            empty_version_message=EMPTY_VERSION_HISTORY_GUIDANCE,
            workspace_id=workspace.workspace_id,
            subjects_href=url_for("curriculum_studio.subjects_hub"),
        )

    def _select_primary(
        self,
        *,
        workspace: WorkspaceSnapshot,
        blocking_count: int,
    ) -> tuple[str, str]:
        founder = founder_stage_label(workspace.current_stage)
        if blocking_count > 0 and founder in {
            "Validate",
            "Review",
            "Approve",
            "Publish",
        }:
            return PRIMARY_RESOLVE, "Resolve findings"
        if founder == "Upload":
            domain = resolve_workflow_stage(workspace.current_stage)
            if domain is WorkflowStage.SUBJECT:
                return PRIMARY_ADVANCE, "Continue"
            return PRIMARY_UPLOAD, "Upload documents"
        if founder == "Publish" and workspace.ready_to_publish:
            return PRIMARY_PUBLISH, "Publish"
        if founder == "Publish" and not (workspace.version_label or "").strip():
            return PRIMARY_VERSION, "Assign version"
        return _DEFAULT_PRIMARY_BY_FOUNDER[founder]

    def _load_blocking_findings(
        self,
        studio: CurriculumStudioService,
        workspace_id: str,
    ) -> tuple[BlockingFindingRow, ...]:
        rows: list[BlockingFindingRow] = []
        try:
            snap = studio.validation.summarise(workspace_id)
        except Exception:
            return ()
        for item in (*snap.errors, *snap.warnings):
            if not bool(getattr(item, "is_blocking", False)):
                continue
            rows.append(
                BlockingFindingRow(
                    title=(item.message or item.code or "Blocking finding").strip(),
                    impact=(item.why_it_matters or "").strip(),
                    required_action=(item.recovery_action or "").strip(),
                    code=(item.code or "").strip(),
                )
            )
        return tuple(rows)

    def _load_supporting(
        self,
        studio: CurriculumStudioService,
        workspace_id: str,
        workspace: WorkspaceSnapshot,
        *,
        founder_label: str,
    ) -> tuple[str, tuple[str, ...]]:
        review_summary = ""
        lines: list[str] = []
        if founder_label != "Upload":
            try:
                snap = studio.validation.summarise(workspace_id)
                if snap.passed:
                    lines.append(f"Last validation passed · {snap.readiness}")
                else:
                    lines.append(f"Validation · {snap.readiness}")
            except Exception:
                pass
        try:
            snap = studio.preview.preview(workspace_id)
            count = int(snap.node_count)
            topics = "topic" if count == 1 else "topics"
            review_summary = f"{count} student-visible {topics}"
            if count > 0 and founder_label in {"Review", "Approve", "Publish"}:
                lines.append(f"Preview · {snap.readiness} · {count} {topics}")
        except Exception:
            review_summary = "Preview not built yet"
        if (workspace.version_label or "").strip():
            lines.append(f"Version {workspace.version_label.strip()}")
        return review_summary, tuple(lines)

    def _load_version_history(
        self,
        studio: CurriculumStudioService,
        subject_code: str,
    ) -> tuple[str, ...]:
        history: list[str] = []
        try:
            version_snap = studio.versions.history(subject_code)
            for record in version_snap.records:
                history.append(f"{record.version_label} ({record.status})")
        except Exception:
            pass
        return tuple(history)


def _subject_name(workspace: WorkspaceSnapshot) -> str:
    title = (workspace.subject_title or "").strip()
    if title:
        return title
    return (workspace.subject_code or workspace.workspace_id).strip()


def _status_label(workspace: WorkspaceSnapshot) -> str:
    if workspace.ready_to_publish:
        return "Ready to publish"
    status = (workspace.status or "").strip()
    if status:
        return status.replace("_", " ").title()
    return "In progress"


def findings_from_legacy(
    findings: tuple[ValidationFindingView, ...],
) -> tuple[BlockingFindingRow, ...]:
    """Adapt legacy ValidationFindingView rows to BlockingFindingRow."""
    return tuple(
        BlockingFindingRow(
            title=f.message,
            impact=f.why_it_matters,
            required_action=f.recovery_action,
            code=f.code,
        )
        for f in findings
        if f.is_blocking
    )
