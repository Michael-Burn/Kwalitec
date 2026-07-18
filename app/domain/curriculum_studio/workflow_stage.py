"""Founder workflow stages for Curriculum Studio.

Deterministic stage vocabulary only — no Flask, no UI, no persistence.
"""

from __future__ import annotations

from enum import StrEnum


class WorkflowStage(StrEnum):
    """Canonical Founder workflow stages (product readiness order)."""

    SUBJECT = "subject"
    CONTENT_SOURCES = "content_sources"
    VALIDATION = "validation"
    PREVIEW = "preview"
    APPROVAL = "approval"
    PUBLICATION = "publication"


class StageOutcome(StrEnum):
    """Outcome reported for a workflow stage evaluation."""

    READY = "ready"
    BLOCKED = "blocked"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    SKIPPED = "skipped"


# Authoritative Founder workflow order.
CANONICAL_WORKFLOW: tuple[WorkflowStage, ...] = (
    WorkflowStage.SUBJECT,
    WorkflowStage.CONTENT_SOURCES,
    WorkflowStage.VALIDATION,
    WorkflowStage.PREVIEW,
    WorkflowStage.APPROVAL,
    WorkflowStage.PUBLICATION,
)

STAGE_LABELS: dict[WorkflowStage, str] = {
    WorkflowStage.SUBJECT: "Subject",
    WorkflowStage.CONTENT_SOURCES: "Content Sources",
    WorkflowStage.VALIDATION: "Validation",
    WorkflowStage.PREVIEW: "Preview",
    WorkflowStage.APPROVAL: "Approval",
    WorkflowStage.PUBLICATION: "Publication",
}

STAGE_QUESTIONS: dict[WorkflowStage, str] = {
    WorkflowStage.SUBJECT: "Which educational product is being prepared?",
    WorkflowStage.CONTENT_SOURCES: "Are CMP and official syllabus sources present?",
    WorkflowStage.VALIDATION: "Does the normalised structure pass readiness checks?",
    WorkflowStage.PREVIEW: "Is the student-visible curriculum acceptable?",
    WorkflowStage.APPROVAL: "Has a Founder approved publication?",
    WorkflowStage.PUBLICATION: "Is this curriculum ready to publish?",
}


def resolve_workflow_stage(value: WorkflowStage | str) -> WorkflowStage:
    """Resolve a WorkflowStage from enum or string token."""
    if isinstance(value, WorkflowStage):
        return value
    token = (value or "").strip().lower().replace("-", "_").replace(" ", "_")
    try:
        return WorkflowStage(token)
    except ValueError as exc:
        raise ValueError(f"Unknown workflow stage: {value!r}") from exc


def stage_index(stage: WorkflowStage | str) -> int:
    """Zero-based index of ``stage`` in the canonical workflow."""
    resolved = resolve_workflow_stage(stage)
    return CANONICAL_WORKFLOW.index(resolved)


def has_reached(
    current: WorkflowStage | str,
    milestone: WorkflowStage | str,
) -> bool:
    """True when ``current`` is at or beyond ``milestone``."""
    return stage_index(current) >= stage_index(milestone)


def next_stage(current: WorkflowStage | str) -> WorkflowStage | None:
    """Return the next forward stage, or None at PUBLICATION."""
    idx = stage_index(current)
    if idx >= len(CANONICAL_WORKFLOW) - 1:
        return None
    return CANONICAL_WORKFLOW[idx + 1]


def previous_stage(current: WorkflowStage | str) -> WorkflowStage | None:
    """Return the previous stage, or None at SUBJECT."""
    idx = stage_index(current)
    if idx <= 0:
        return None
    return CANONICAL_WORKFLOW[idx - 1]


def is_terminal_workflow_stage(stage: WorkflowStage | str) -> bool:
    """True when the Founder is on the publication stage."""
    return resolve_workflow_stage(stage) is WorkflowStage.PUBLICATION


def stage_label(stage: WorkflowStage | str) -> str:
    """Human-readable stage label for Studio surfaces."""
    return STAGE_LABELS[resolve_workflow_stage(stage)]
