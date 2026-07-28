"""Immutable reasoning inputs for the Educational Reasoning Engine (EI-007)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class NodeReasoningState:
    """Curriculum node snapshot consumed by reasoning rules.

    Combines SCI educational slots, Twin belief fields, and syllabus metadata.
    Does not mutate beliefs, evidence, or curriculum.
    """

    node_stable_id: str
    node_kind: str
    completion_status: str
    revision_status: str
    mastery: float
    confidence: float
    learning_state: str
    belief_id: str | None
    supporting_evidence_ids: tuple[str, ...]
    prerequisite_ids: tuple[str, ...]
    syllabus_index: int
    difficulty: str
    last_interaction_at: datetime | None
    attempts: int
    total_study_time_minutes: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_stable_id": self.node_stable_id,
            "node_kind": self.node_kind,
            "completion_status": self.completion_status,
            "revision_status": self.revision_status,
            "mastery": self.mastery,
            "confidence": self.confidence,
            "learning_state": self.learning_state,
            "belief_id": self.belief_id,
            "supporting_evidence_ids": list(self.supporting_evidence_ids),
            "prerequisite_ids": list(self.prerequisite_ids),
            "syllabus_index": self.syllabus_index,
            "difficulty": self.difficulty,
            "last_interaction_at": (
                self.last_interaction_at.isoformat()
                if self.last_interaction_at is not None
                else None
            ),
            "attempts": self.attempts,
            "total_study_time_minutes": self.total_study_time_minutes,
        }


@dataclass(frozen=True)
class ReasoningContext:
    """Immutable inputs for one SCI reasoning pass."""

    instance_id: str
    as_of: datetime
    nodes: tuple[NodeReasoningState, ...]
    metadata: dict[str, Any] = field(default_factory=dict)

    def node_map(self) -> dict[str, NodeReasoningState]:
        return {n.node_stable_id: n for n in self.nodes}

    def study_targets(self) -> tuple[NodeReasoningState, ...]:
        """Leaf learning objectives are primary study targets."""
        return tuple(
            n for n in self.nodes if n.node_kind == "learning_objective"
        )

    def last_studied_node_id(self) -> str | None:
        dated = [
            n
            for n in self.nodes
            if n.last_interaction_at is not None
        ]
        if not dated:
            return None
        dated.sort(
            key=lambda n: (
                n.last_interaction_at or datetime.min,
                n.node_stable_id,
            ),
            reverse=True,
        )
        return dated[0].node_stable_id
