"""Immutable WorkflowSnapshot DTO."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class WorkflowTransitionSnapshot:
    """Read-only workflow transition entry."""

    from_stage: str
    to_stage: str
    event: str
    occurred_at: str = ""
    actor_id: str | None = None
    reason: str = ""


@dataclass(frozen=True)
class WorkflowSnapshot:
    """Read-only Founder workflow projection."""

    workflow_id: str
    workspace_id: str
    current_stage: str
    highest_stage_reached: str
    stage_index: int = 0
    transition_count: int = 0
    history: tuple[WorkflowTransitionSnapshot, ...] = field(default_factory=tuple)
    stage_label: str = ""
    can_advance: bool = False
    can_retreat: bool = False
