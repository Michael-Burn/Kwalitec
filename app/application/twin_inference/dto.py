"""DTOs for Twin Inference Engine services (EI-006)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.domain.twin_inference.belief import TwinBelief
from app.domain.twin_inference.engine import InferenceResult
from app.domain.twin_inference.explanation import BeliefExplanation
from app.domain.twin_inference.knowledge_state import SubjectKnowledgeState


@dataclass(frozen=True)
class BeliefView:
    """Belief plus explanation for API/service consumers."""

    belief: TwinBelief
    explanation: BeliefExplanation

    def to_dict(self) -> dict[str, Any]:
        return {
            "belief": self.belief.to_dict(),
            "explanation": self.explanation.to_dict(),
        }

    @classmethod
    def from_result(cls, result: InferenceResult) -> BeliefView:
        return cls(belief=result.belief, explanation=result.explanation)


@dataclass(frozen=True)
class RebuildBeliefsResult:
    """Outcome of a full belief rebuild for one SCI."""

    instance_id: str
    belief_count: int
    inference_version: str
    beliefs: tuple[BeliefView, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "belief_count": self.belief_count,
            "inference_version": self.inference_version,
            "beliefs": [b.to_dict() for b in self.beliefs],
        }


@dataclass(frozen=True)
class KnowledgeStateView:
    """Subject-level knowledge state with optional node belief summaries."""

    state: SubjectKnowledgeState
    node_summaries: tuple[BeliefView, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "state": self.state.to_dict(),
            "node_summaries": [n.to_dict() for n in self.node_summaries],
        }
