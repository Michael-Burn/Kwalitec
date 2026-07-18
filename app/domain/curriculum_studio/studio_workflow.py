"""Studio workflow — Founder stage machine for curriculum readiness.

Lifecycle only. Does not teach, ingest PDFs, or persist.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from app.domain.curriculum_studio.workflow_stage import (
    CANONICAL_WORKFLOW,
    WorkflowStage,
    next_stage,
    previous_stage,
    resolve_workflow_stage,
    stage_index,
)


class WorkflowTransitionEvent(StrEnum):
    """Named events for Studio workflow stage transitions."""

    ADVANCE = "advance"
    RETREAT = "retreat"
    JUMP_TO_SUBJECT = "jump_to_subject"
    JUMP_TO_CONTENT_SOURCES = "jump_to_content_sources"
    JUMP_TO_VALIDATION = "jump_to_validation"
    JUMP_TO_PREVIEW = "jump_to_preview"
    JUMP_TO_APPROVAL = "jump_to_approval"
    JUMP_TO_PUBLICATION = "jump_to_publication"
    RESET = "reset"


# (from_stage, event) → to_stage — authoritative lawful map.
LAWFUL_WORKFLOW_TRANSITIONS: dict[
    tuple[WorkflowStage, WorkflowTransitionEvent], WorkflowStage
] = {}

for _stage in CANONICAL_WORKFLOW:
    _nxt = next_stage(_stage)
    if _nxt is not None:
        LAWFUL_WORKFLOW_TRANSITIONS[(_stage, WorkflowTransitionEvent.ADVANCE)] = (
            _nxt
        )
    _prev = previous_stage(_stage)
    if _prev is not None:
        LAWFUL_WORKFLOW_TRANSITIONS[(_stage, WorkflowTransitionEvent.RETREAT)] = (
            _prev
        )
    LAWFUL_WORKFLOW_TRANSITIONS[(_stage, WorkflowTransitionEvent.RESET)] = (
        WorkflowStage.SUBJECT
    )

# Explicit jump events (allowed only to current or earlier stages, or
# forward when the workflow records the jump as lawful for Studio navigation).
_JUMP_TARGETS: dict[WorkflowTransitionEvent, WorkflowStage] = {
    WorkflowTransitionEvent.JUMP_TO_SUBJECT: WorkflowStage.SUBJECT,
    WorkflowTransitionEvent.JUMP_TO_CONTENT_SOURCES: (
        WorkflowStage.CONTENT_SOURCES
    ),
    WorkflowTransitionEvent.JUMP_TO_VALIDATION: WorkflowStage.VALIDATION,
    WorkflowTransitionEvent.JUMP_TO_PREVIEW: WorkflowStage.PREVIEW,
    WorkflowTransitionEvent.JUMP_TO_APPROVAL: WorkflowStage.APPROVAL,
    WorkflowTransitionEvent.JUMP_TO_PUBLICATION: WorkflowStage.PUBLICATION,
}

for _stage in CANONICAL_WORKFLOW:
    for _event, _target in _JUMP_TARGETS.items():
        # Jumps are lawful to any stage — application gates enforce readiness.
        LAWFUL_WORKFLOW_TRANSITIONS[(_stage, _event)] = _target


@dataclass(frozen=True)
class WorkflowTransitionRecord:
    """Immutable audit entry for a workflow transition."""

    from_stage: WorkflowStage
    to_stage: WorkflowStage
    event: WorkflowTransitionEvent
    occurred_at: str = ""
    actor_id: str | None = None
    reason: str = ""

    @classmethod
    def create(
        cls,
        from_stage: WorkflowStage | str,
        to_stage: WorkflowStage | str,
        event: WorkflowTransitionEvent | str,
        *,
        occurred_at: str = "",
        actor_id: str | None = None,
        reason: str = "",
    ) -> WorkflowTransitionRecord:
        """Construct a transition record after validating tokens."""
        return cls(
            from_stage=resolve_workflow_stage(from_stage),
            to_stage=resolve_workflow_stage(to_stage),
            event=_resolve_event(event),
            occurred_at=(occurred_at or "").strip(),
            actor_id=(
                None if actor_id is None else _require_non_empty(actor_id, "actor_id")
            ),
            reason=(reason or "").strip(),
        )


@dataclass(frozen=True)
class StudioWorkflow:
    """Founder workflow carrier for a curriculum workspace.

    Answers: where is this educational product in the readiness pipeline?
    """

    workflow_id: str
    workspace_id: str
    current_stage: WorkflowStage = WorkflowStage.SUBJECT
    history: tuple[WorkflowTransitionRecord, ...] = field(default_factory=tuple)
    highest_stage_reached: WorkflowStage = WorkflowStage.SUBJECT

    @classmethod
    def create(
        cls,
        workflow_id: str,
        workspace_id: str,
        *,
        current_stage: WorkflowStage | str = WorkflowStage.SUBJECT,
        history: (
            list[WorkflowTransitionRecord] | tuple[WorkflowTransitionRecord, ...] | None
        ) = None,
        highest_stage_reached: WorkflowStage | str | None = None,
    ) -> StudioWorkflow:
        """Construct a StudioWorkflow after validating invariants."""
        wid = _require_non_empty(workflow_id, "workflow_id")
        wsid = _require_non_empty(workspace_id, "workspace_id")
        stage = resolve_workflow_stage(current_stage)
        hist = tuple(history or ())
        highest = resolve_workflow_stage(
            highest_stage_reached if highest_stage_reached is not None else stage
        )
        if stage_index(highest) < stage_index(stage):
            highest = stage
        return cls(
            workflow_id=wid,
            workspace_id=wsid,
            current_stage=stage,
            history=hist,
            highest_stage_reached=highest,
        )

    @property
    def stage_index(self) -> int:
        """Zero-based index of the current stage."""
        return stage_index(self.current_stage)

    @property
    def transition_count(self) -> int:
        """Number of recorded transitions."""
        return len(self.history)

    def with_transition(
        self,
        event: WorkflowTransitionEvent | str,
        *,
        occurred_at: str = "",
        actor_id: str | None = None,
        reason: str = "",
    ) -> StudioWorkflow:
        """Return a new workflow after applying a lawful transition."""
        resolved_event = _resolve_event(event)
        target = next_workflow_state(self.current_stage, resolved_event)
        record = WorkflowTransitionRecord.create(
            self.current_stage,
            target,
            resolved_event,
            occurred_at=occurred_at,
            actor_id=actor_id,
            reason=reason,
        )
        highest = self.highest_stage_reached
        if stage_index(target) > stage_index(highest):
            highest = target
        return StudioWorkflow(
            workflow_id=self.workflow_id,
            workspace_id=self.workspace_id,
            current_stage=target,
            history=(*self.history, record),
            highest_stage_reached=highest,
        )


def resolve_workflow_event(
    value: WorkflowTransitionEvent | str,
) -> WorkflowTransitionEvent:
    """Resolve a WorkflowTransitionEvent from enum or string token."""
    return _resolve_event(value)


def next_workflow_state(
    current: WorkflowStage | str,
    event: WorkflowTransitionEvent | str,
) -> WorkflowStage:
    """Return the lawful next stage for ``(current, event)``.

    Raises:
        ValueError: When the transition is not lawful.
    """
    stage = resolve_workflow_stage(current)
    resolved_event = _resolve_event(event)
    key = (stage, resolved_event)
    if key not in LAWFUL_WORKFLOW_TRANSITIONS:
        raise ValueError(
            f"Illegal workflow transition: {stage.value} + {resolved_event.value}"
        )
    return LAWFUL_WORKFLOW_TRANSITIONS[key]


def is_lawful_transition(
    current: WorkflowStage | str,
    event: WorkflowTransitionEvent | str,
) -> bool:
    """True when ``(current, event)`` is in the lawful map."""
    try:
        next_workflow_state(current, event)
        return True
    except ValueError:
        return False


def _resolve_event(
    value: WorkflowTransitionEvent | str,
) -> WorkflowTransitionEvent:
    if isinstance(value, WorkflowTransitionEvent):
        return value
    token = (value or "").strip().lower().replace("-", "_").replace(" ", "_")
    try:
        return WorkflowTransitionEvent(token)
    except ValueError as exc:
        raise ValueError(f"Unknown workflow event: {value!r}") from exc


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
