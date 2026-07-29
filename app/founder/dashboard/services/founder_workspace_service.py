"""Founder Publication Workspace service — FV-001A workflow alignment.

Presentation projection only. Does not alter educational algorithms.
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
    PreviewNodeRow,
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
    "Preview": (PRIMARY_REVIEW, "Generate preview"),
    "Approve": (PRIMARY_APPROVE, "Approve"),
    "Publish": (PRIMARY_PUBLISH, "Publish"),
}

_NEXT_STEP_BY_FOUNDER: dict[str, str] = {
    "Upload": "Upload the required CMP and syllabus. Processing starts next.",
    "Preview": "Inspect the curriculum hierarchy, then approve the structure.",
    "Approve": "Confirm this curriculum may proceed to Publish.",
    "Publish": "Publish this version so students can enrol.",
}


class FounderWorkspaceService:
    """Build the FV-001A Publication Workspace page model."""

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
        entity = studio.registry.get_workspace(workspace_id)
        facts = entity.facts if entity is not None else None
        preview_built = bool(facts.preview_built) if facts is not None else False
        preview_approved = (
            bool(facts.preview_approved) if facts is not None else False
        )
        cmp_uploaded = bool(facts.cmp_uploaded) if facts is not None else False
        syllabus_uploaded = (
            bool(facts.official_syllabus_uploaded) if facts is not None else False
        )
        review_summary, supporting, preview_nodes, topic_count, section_count = (
            self._load_supporting(
                studio, workspace_id, workspace, founder_label=founder_label
            )
        )
        history = self._load_version_history(studio, workspace.subject_code)
        primary_key, primary_label = self._select_primary(
            workspace=workspace,
            blocking_count=len(findings),
            preview_built=preview_built,
            cmp_uploaded=cmp_uploaded,
            syllabus_uploaded=syllabus_uploaded,
        )
        stage_idx = founder_stage_index(workspace.current_stage)
        domain = resolve_workflow_stage(workspace.current_stage)
        processing = founder_label == "Upload" and (
            domain is WorkflowStage.VALIDATION or cmp_uploaded
        )
        preview_json = _preview_nodes_json(preview_nodes)

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
            show_validate=False,
            show_review=founder_label == "Preview",
            show_approve=founder_label == "Approve",
            show_publish=founder_label == "Publish",
            show_processing=processing,
            supporting_lines=supporting,
            review_summary=review_summary,
            preview_nodes=preview_nodes,
            preview_nodes_json=preview_json,
            topic_count=topic_count,
            section_count=section_count,
            preview_built=preview_built,
            preview_approved=preview_approved,
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
        preview_built: bool,
        cmp_uploaded: bool,
        syllabus_uploaded: bool,
    ) -> tuple[str, str]:
        founder = founder_stage_label(workspace.current_stage)
        if blocking_count > 0 and founder in {
            "Preview",
            "Approve",
            "Publish",
        }:
            return PRIMARY_RESOLVE, "Resolve findings"
        if founder == "Upload":
            domain = resolve_workflow_stage(workspace.current_stage)
            if domain is WorkflowStage.SUBJECT:
                return PRIMARY_ADVANCE, "Continue"
            if domain is WorkflowStage.VALIDATION:
                return PRIMARY_VALIDATE, "Continue processing"
            if cmp_uploaded and syllabus_uploaded:
                return PRIMARY_ADVANCE, "Continue to Preview"
            return PRIMARY_UPLOAD, "Upload documents"
        if founder == "Preview":
            if preview_built:
                return PRIMARY_APPROVE, "Approve structure"
            return PRIMARY_REVIEW, "Generate preview"
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
    ) -> tuple[str, tuple[str, ...], tuple[PreviewNodeRow, ...], int, int]:
        review_summary = ""
        lines: list[str] = []
        nodes: list[PreviewNodeRow] = []
        topic_count = 0
        section_count = 0
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
            topic_count = count
            topics = "topic" if count == 1 else "topics"
            review_summary = f"{count} student-visible {topics}"
            if count > 0 and founder_label in {"Preview", "Approve", "Publish"}:
                lines.append(f"Preview · {snap.readiness} · {count} {topics}")
            for node in snap.hierarchy:
                kind = (node.kind or "topic").strip().lower()
                if kind in {"section", "chapter", "unit", "module"}:
                    section_count += 1
                nodes.append(
                    PreviewNodeRow(
                        node_id=node.node_id,
                        title=node.title,
                        kind=node.kind,
                        parent_id=node.parent_id,
                        order_index=int(node.order_index),
                    )
                )
        except Exception:
            review_summary = "Preview not built yet"
        if (workspace.version_label or "").strip():
            lines.append(f"Version {workspace.version_label.strip()}")
        return (
            review_summary,
            tuple(lines),
            tuple(nodes),
            topic_count,
            section_count,
        )

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


def _preview_nodes_json(nodes: tuple[PreviewNodeRow, ...]) -> str:
    import json

    payload = [
        {
            "node_id": n.node_id,
            "title": n.title,
            "kind": n.kind,
            "parent_id": n.parent_id,
            "order_index": n.order_index,
        }
        for n in nodes
    ]
    return json.dumps(payload, separators=(",", ":"))


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
