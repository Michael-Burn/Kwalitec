"""Shared thresholds and helpers for EI-007 reasoning rules."""

from __future__ import annotations

from app.domain.educational_reasoning_engine.context import NodeReasoningState
from app.domain.student_curriculum_binding.node_state import (
    CompletionStatus,
    RevisionStatus,
)

# Prerequisite mastery required before studying a dependent node.
PREREQ_MASTERY_THRESHOLD = 0.50

# Confidence below this with some mastery → strengthen_confidence.
LOW_CONFIDENCE_THRESHOLD = 0.45
MIN_MASTERY_FOR_CONFIDENCE = 0.20

# Effort catalogue (minutes) by CKG difficulty label.
EFFORT_BY_DIFFICULTY: dict[str, int] = {
    "foundational": 25,
    "intermediate": 40,
    "advanced": 60,
}
DEFAULT_EFFORT_MINUTES = 30


def prerequisites_satisfied(
    node: NodeReasoningState,
    node_map: dict[str, NodeReasoningState],
    *,
    threshold: float = PREREQ_MASTERY_THRESHOLD,
) -> bool:
    if not node.prerequisite_ids:
        return True
    for pid in node.prerequisite_ids:
        prereq = node_map.get(pid)
        mastery = prereq.mastery if prereq is not None else 0.0
        if mastery < threshold:
            return False
    return True


def weak_prerequisites(
    node: NodeReasoningState,
    node_map: dict[str, NodeReasoningState],
    *,
    threshold: float = PREREQ_MASTERY_THRESHOLD,
) -> tuple[str, ...]:
    weak: list[str] = []
    for pid in node.prerequisite_ids:
        prereq = node_map.get(pid)
        mastery = prereq.mastery if prereq is not None else 0.0
        if mastery < threshold:
            weak.append(pid)
    return tuple(weak)


def effort_for_difficulty(difficulty: str) -> int:
    key = (difficulty or "").strip().lower()
    return EFFORT_BY_DIFFICULTY.get(key, DEFAULT_EFFORT_MINUTES)


def belief_support(node: NodeReasoningState) -> tuple[str, ...]:
    return (node.belief_id,) if node.belief_id else ()


def is_actionable(node: NodeReasoningState) -> bool:
    """True when a node may receive study, revise, or continuity actions."""
    if node.revision_status in {
        RevisionStatus.DUE.value,
        RevisionStatus.OVERDUE.value,
    }:
        return True
    return node.completion_status != CompletionStatus.COMPLETED.value
