"""Twin belief domain model (EI-006).

Beliefs are derived projections over immutable Learning Evidence. They
reference evidence ids rather than duplicating observation payloads.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.domain.twin_inference.learning_state import LearningState
from app.domain.twin_inference.version import INFERENCE_VERSION


@dataclass(frozen=True)
class TwinBelief:
    """Explainable educational belief for one curriculum node.

    Every belief must carry supporting evidence references, an inference
    version, and a human-readable rationale summary.
    """

    belief_id: str
    instance_id: str
    node_stable_id: str
    mastery_level: float
    confidence_score: float
    learning_state: str
    supporting_evidence_ids: tuple[str, ...]
    inference_timestamp: datetime
    inference_version: str = INFERENCE_VERSION
    rationale_summary: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "mastery_level", _clamp01(self.mastery_level)
        )
        object.__setattr__(
            self, "confidence_score", _clamp01(self.confidence_score)
        )
        state = (self.learning_state or "").strip().lower()
        if state not in {m.value for m in LearningState}:
            raise ValueError(f"Invalid learning_state: {self.learning_state!r}")
        object.__setattr__(self, "learning_state", state)
        ids = tuple(
            eid.strip()
            for eid in self.supporting_evidence_ids
            if isinstance(eid, str) and eid.strip()
        )
        object.__setattr__(self, "supporting_evidence_ids", ids)
        if not (self.inference_version or "").strip():
            raise ValueError("inference_version is required")
        if not (self.rationale_summary or "").strip():
            raise ValueError("rationale_summary is required — no unexplained belief")

    def to_dict(self) -> dict[str, Any]:
        return {
            "belief_id": self.belief_id,
            "instance_id": self.instance_id,
            "node_stable_id": self.node_stable_id,
            "mastery_level": self.mastery_level,
            "confidence_score": self.confidence_score,
            "learning_state": self.learning_state,
            "supporting_evidence_ids": list(self.supporting_evidence_ids),
            "inference_timestamp": self.inference_timestamp.isoformat(),
            "inference_version": self.inference_version,
            "rationale_summary": self.rationale_summary,
        }


@dataclass(frozen=True)
class EmptyBeliefFactory:
    """Factory helpers for nodes with no usable evidence."""

    @staticmethod
    def unknown(
        *,
        belief_id: str,
        instance_id: str,
        node_stable_id: str,
        inference_timestamp: datetime,
        inference_version: str = INFERENCE_VERSION,
    ) -> TwinBelief:
        return TwinBelief(
            belief_id=belief_id,
            instance_id=instance_id,
            node_stable_id=node_stable_id,
            mastery_level=0.0,
            confidence_score=0.0,
            learning_state=LearningState.UNKNOWN.value,
            supporting_evidence_ids=(),
            inference_timestamp=inference_timestamp,
            inference_version=inference_version,
            rationale_summary=(
                "No usable learning evidence for this node; "
                "belief defaults to unknown with zero mastery and confidence."
            ),
        )


def _clamp01(value: float) -> float:
    return round(max(0.0, min(1.0, float(value))), 6)


# Re-export helper used by aggregation modules.
clamp01 = _clamp01
