"""Immutable DashboardSnapshot DTO for Curriculum Studio.

Projection only — no persistence.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.application.curriculum_studio.dto.publication_snapshot import (
    PublicationSnapshot,
)
from app.application.curriculum_studio.dto.workspace_snapshot import (
    WorkspaceSnapshot,
)


@dataclass(frozen=True)
class ActivityEntrySnapshot:
    """Read-only recent activity entry."""

    activity_id: str
    kind: str
    message: str
    occurred_at: str = ""
    workspace_id: str | None = None
    subject_code: str | None = None
    version_id: str | None = None


@dataclass(frozen=True)
class DashboardSnapshot:
    """Founder dashboard projection for Curriculum Studio.

    Aggregates published / draft / pending validation / pending approval
    curricula, recent publications, recent activity, and publication readiness.
    """

    published_curricula: tuple[WorkspaceSnapshot, ...] = field(
        default_factory=tuple
    )
    draft_curricula: tuple[WorkspaceSnapshot, ...] = field(
        default_factory=tuple
    )
    pending_validation: tuple[WorkspaceSnapshot, ...] = field(
        default_factory=tuple
    )
    pending_approval: tuple[WorkspaceSnapshot, ...] = field(
        default_factory=tuple
    )
    recent_publications: tuple[PublicationSnapshot, ...] = field(
        default_factory=tuple
    )
    recent_activity: tuple[ActivityEntrySnapshot, ...] = field(
        default_factory=tuple
    )
    publication_readiness: tuple[PublicationSnapshot, ...] = field(
        default_factory=tuple
    )
    published_count: int = 0
    draft_count: int = 0
    pending_validation_count: int = 0
    pending_approval_count: int = 0
    ready_to_publish_count: int = 0
