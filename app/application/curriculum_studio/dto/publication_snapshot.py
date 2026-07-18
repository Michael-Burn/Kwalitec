"""Immutable PublicationSnapshot DTO for Curriculum Studio."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ChecklistItemSnapshot:
    """Read-only computed checklist item."""

    code: str
    label: str
    status: str
    satisfied: bool


@dataclass(frozen=True)
class PublicationSnapshot:
    """Read-only publication readiness projection."""

    summary_id: str
    workspace_id: str
    subject_code: str
    version_label: str = ""
    workflow_stage: str = "subject"
    lifecycle_status: str = "draft"
    ready_to_publish: bool = False
    rollback_eligible: bool = False
    version_id: str | None = None
    checklist_item_count: int = 0
    blocking_codes: tuple[str, ...] = field(default_factory=tuple)
    checklist_items: tuple[ChecklistItemSnapshot, ...] = field(
        default_factory=tuple
    )
