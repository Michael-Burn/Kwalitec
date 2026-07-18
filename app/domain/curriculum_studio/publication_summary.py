"""Publication summary — Founder-facing publication readiness projection."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from app.domain.curriculum_studio.publication_checklist import (
    ChecklistItemCode,
    PublicationChecklist,
)
from app.domain.curriculum_studio.workflow_stage import WorkflowStage


class PublicationLifecycleStatus(StrEnum):
    """High-level publication lifecycle for Studio (not CM state machine)."""

    DRAFT = "draft"
    READY = "ready"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class PublicationSummary:
    """Immutable publication readiness summary for a workspace.

    Answers: Is this curriculum ready to publish?
    """

    summary_id: str
    workspace_id: str
    subject_code: str
    version_label: str = ""
    workflow_stage: WorkflowStage = WorkflowStage.SUBJECT
    lifecycle_status: PublicationLifecycleStatus = PublicationLifecycleStatus.DRAFT
    checklist: PublicationChecklist | None = None
    ready_to_publish: bool = False
    blocking_codes: tuple[ChecklistItemCode, ...] = field(default_factory=tuple)
    version_id: str | None = None
    rollback_eligible: bool = False

    @classmethod
    def create(
        cls,
        summary_id: str,
        workspace_id: str,
        subject_code: str,
        *,
        version_label: str = "",
        workflow_stage: WorkflowStage | str = WorkflowStage.SUBJECT,
        lifecycle_status: (
            PublicationLifecycleStatus | str
        ) = PublicationLifecycleStatus.DRAFT,
        checklist: PublicationChecklist | None = None,
        version_id: str | None = None,
        rollback_eligible: bool = False,
    ) -> PublicationSummary:
        """Construct a PublicationSummary; readiness derived from checklist."""
        from app.domain.curriculum_studio.workflow_stage import (
            resolve_workflow_stage,
        )

        sid = _require_non_empty(summary_id, "summary_id")
        wid = _require_non_empty(workspace_id, "workspace_id")
        code = _require_non_empty(subject_code, "subject_code").upper()
        stage = resolve_workflow_stage(workflow_stage)
        status = (
            lifecycle_status
            if isinstance(lifecycle_status, PublicationLifecycleStatus)
            else PublicationLifecycleStatus(str(lifecycle_status).strip().lower())
        )
        ready = bool(checklist.ready_to_publish) if checklist else False
        blocking = checklist.blocking_codes if checklist else ()
        if ready and status is PublicationLifecycleStatus.DRAFT:
            status = PublicationLifecycleStatus.READY
        if not ready and status is PublicationLifecycleStatus.READY:
            status = PublicationLifecycleStatus.BLOCKED
        return cls(
            summary_id=sid,
            workspace_id=wid,
            subject_code=code,
            version_label=(version_label or "").strip(),
            workflow_stage=stage,
            lifecycle_status=status,
            checklist=checklist,
            ready_to_publish=ready,
            blocking_codes=blocking,
            version_id=(
                None
                if version_id is None
                else _require_non_empty(version_id, "version_id")
            ),
            rollback_eligible=bool(rollback_eligible),
        )

    @property
    def checklist_item_count(self) -> int:
        """Number of checklist items, or zero when unset."""
        return len(self.checklist.items) if self.checklist else 0

    @property
    def is_published(self) -> bool:
        """True when lifecycle status is PUBLISHED."""
        return self.lifecycle_status is PublicationLifecycleStatus.PUBLISHED

    @property
    def is_archived(self) -> bool:
        """True when lifecycle status is ARCHIVED."""
        return self.lifecycle_status is PublicationLifecycleStatus.ARCHIVED


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
