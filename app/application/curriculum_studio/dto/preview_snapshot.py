"""Immutable PreviewSnapshot DTO for Curriculum Studio."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PreviewNodeSnapshot:
    """Read-only hierarchy node."""

    node_id: str
    title: str
    kind: str = "topic"
    parent_id: str | None = None
    order_index: int = 0


@dataclass(frozen=True)
class PreviewSnapshot:
    """Read-only student-visible curriculum preview projection."""

    preview_id: str
    workspace_id: str
    readiness: str
    validation_passed: bool = False
    publication_ready: bool = False
    is_approved: bool = False
    node_count: int = 0
    objective_count: int = 0
    prerequisite_count: int = 0
    estimated_workload_hours: float | None = None
    subject_code: str = ""
    version_label: str = ""
    hierarchy: tuple[PreviewNodeSnapshot, ...] = field(default_factory=tuple)
    objectives: tuple[str, ...] = field(default_factory=tuple)
    prerequisites: tuple[tuple[str, str], ...] = field(default_factory=tuple)
