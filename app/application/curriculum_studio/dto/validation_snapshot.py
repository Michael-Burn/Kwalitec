"""Immutable ValidationSnapshot DTO for Curriculum Studio."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ValidationFindingSnapshot:
    """Read-only validation finding."""

    code: str
    message: str
    severity: str
    section_id: str | None = None
    topic_id: str | None = None
    is_blocking: bool = False


@dataclass(frozen=True)
class ValidationSnapshot:
    """Read-only validation summary projection."""

    summary_id: str
    workspace_id: str
    readiness: str
    passed: bool
    section_count: int = 0
    objective_count: int = 0
    prerequisite_count: int = 0
    warning_count: int = 0
    error_count: int = 0
    blocks_publication: bool = False
    detected_sections: tuple[str, ...] = field(default_factory=tuple)
    detected_objectives: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[ValidationFindingSnapshot, ...] = field(default_factory=tuple)
    errors: tuple[ValidationFindingSnapshot, ...] = field(default_factory=tuple)
