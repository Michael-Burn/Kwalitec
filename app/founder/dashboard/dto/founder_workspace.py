"""Founder Publication Workspace DTO — DX-004C Execution First."""

from __future__ import annotations

from dataclasses import dataclass

from app.application.curriculum_studio.dto.workspace_snapshot import (
    WorkspaceSnapshot,
)


@dataclass(frozen=True)
class BlockingFindingRow:
    """One blocking finding for L0/L1 (reason · impact · required action)."""

    title: str
    impact: str = ""
    required_action: str = ""
    code: str = ""


@dataclass(frozen=True)
class FounderWorkspacePage:
    """DX-004C Publication Workspace projection."""

    workspace: WorkspaceSnapshot
    subject_code: str
    subject_name: str
    version_label: str
    stage_label: str
    status_label: str
    founder_stages: tuple[str, ...]
    stage_index: int
    primary_key: str
    primary_label: str
    next_step_sentence: str
    blocking_findings: tuple[BlockingFindingRow, ...]
    blocking_count: int
    show_upload: bool
    show_validate: bool
    show_review: bool
    show_approve: bool
    show_publish: bool
    supporting_lines: tuple[str, ...]
    review_summary: str
    version_history: tuple[str, ...]
    has_version_history: bool
    empty_version_message: str
    workspace_id: str
    subjects_href: str

    # Compatibility aliases for legacy presentation helpers / tests.
    @property
    def primary_action(self) -> str:
        return self.primary_key

    @property
    def next_action_label(self) -> str:
        return self.next_step_sentence

    @property
    def has_validation_findings(self) -> bool:
        return self.blocking_count > 0

    @property
    def validation_findings(self) -> tuple[BlockingFindingRow, ...]:
        return self.blocking_findings
