"""Immutable WorkspaceSnapshot DTO."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class WorkspaceSnapshot:
    """Read-only Curriculum Studio workspace projection."""

    workspace_id: str
    subject_code: str
    subject_title: str = ""
    version_label: str = ""
    version_id: str | None = None
    status: str = "active"
    current_stage: str = "subject"
    ready_to_publish: bool = False
    checklist_satisfied_count: int = 0
    checklist_pending_count: int = 0
    section_ids: tuple[str, ...] = field(default_factory=tuple)
    topic_ids: tuple[str, ...] = field(default_factory=tuple)
    objective_ids: tuple[str, ...] = field(default_factory=tuple)
    estimated_workload_hours: float | None = None
    notes: str = ""
