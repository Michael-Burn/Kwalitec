"""Subject-level knowledge state derived from Twin beliefs (EI-006)."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.domain.twin_inference.belief import TwinBelief, clamp01
from app.domain.twin_inference.version import INFERENCE_VERSION


@dataclass(frozen=True)
class SubjectKnowledgeState:
    """Aggregated, explainable knowledge state for one SCI / subject."""

    instance_id: str
    subject_code: str
    node_belief_count: int
    mean_mastery: float
    mean_confidence: float
    learning_state_counts: tuple[tuple[str, int], ...]
    inferred_at: datetime
    inference_version: str
    rationale_summary: str
    node_stable_ids: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "subject_code": self.subject_code,
            "node_belief_count": self.node_belief_count,
            "mean_mastery": self.mean_mastery,
            "mean_confidence": self.mean_confidence,
            "learning_state_counts": dict(self.learning_state_counts),
            "inferred_at": self.inferred_at.isoformat(),
            "inference_version": self.inference_version,
            "rationale_summary": self.rationale_summary,
            "node_stable_ids": list(self.node_stable_ids),
        }


def aggregate_knowledge_state(
    *,
    instance_id: str,
    subject_code: str,
    beliefs: Iterable[TwinBelief],
    inferred_at: datetime,
    inference_version: str = INFERENCE_VERSION,
) -> SubjectKnowledgeState:
    """Deterministic subject roll-up from node beliefs (sorted by node id)."""
    ordered = sorted(beliefs, key=lambda b: b.node_stable_id)
    count = len(ordered)
    if count == 0:
        return SubjectKnowledgeState(
            instance_id=instance_id,
            subject_code=subject_code,
            node_belief_count=0,
            mean_mastery=0.0,
            mean_confidence=0.0,
            learning_state_counts=(),
            inferred_at=inferred_at,
            inference_version=inference_version,
            rationale_summary=(
                "No node beliefs available; subject knowledge state is empty."
            ),
            node_stable_ids=(),
        )

    mean_mastery = clamp01(sum(b.mastery_level for b in ordered) / count)
    mean_confidence = clamp01(sum(b.confidence_score for b in ordered) / count)
    counts = Counter(b.learning_state for b in ordered)
    state_counts = tuple(sorted(counts.items(), key=lambda kv: kv[0]))
    rationale = (
        f"Subject knowledge state over {count} node belief(s): "
        f"mean mastery {mean_mastery:.4f}, mean confidence {mean_confidence:.4f} "
        f"({inference_version})."
    )
    return SubjectKnowledgeState(
        instance_id=instance_id,
        subject_code=subject_code,
        node_belief_count=count,
        mean_mastery=mean_mastery,
        mean_confidence=mean_confidence,
        learning_state_counts=state_counts,
        inferred_at=inferred_at,
        inference_version=inference_version,
        rationale_summary=rationale,
        node_stable_ids=tuple(b.node_stable_id for b in ordered),
    )
