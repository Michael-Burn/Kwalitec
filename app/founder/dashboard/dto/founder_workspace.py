"""Founder Publication Workspace DTO — FV-001A workflow alignment."""

from __future__ import annotations

from dataclasses import dataclass, field

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
class PreviewNodeRow:
    """One node in the Founder preview hierarchy tree."""

    node_id: str
    title: str
    kind: str = "topic"
    parent_id: str | None = None
    order_index: int = 0


@dataclass(frozen=True)
class FounderWorkspacePage:
    """FV-001A Publication Workspace projection."""

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
    show_processing: bool = False
    preview_nodes: tuple[PreviewNodeRow, ...] = field(default_factory=tuple)
    preview_nodes_json: str = "[]"
    topic_count: int = 0
    section_count: int = 0
    preview_built: bool = False
    preview_approved: bool = False
    can_retreat: bool = False
    can_reset: bool = False

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
