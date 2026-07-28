"""Educational Decision domain model (EI-007).

Decisions are derived educational actions over trusted assets (published
curriculum, SCI, evidence references, Twin beliefs). They never encode UI
copy or mission text.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.domain.educational_reasoning_engine.decision_type import (
    DecisionType,
    ExpectedOutcome,
)
from app.domain.educational_reasoning_engine.version import REASONING_VERSION


def clamp01(value: float) -> float:
    return round(max(0.0, min(1.0, float(value))), 6)


@dataclass(frozen=True)
class EducationalDecision:
    """Explainable educational decision for one curriculum target.

    Every decision must carry a rationale, supporting beliefs/curriculum
    references, applied rules, and a reasoning version.
    """

    decision_id: str
    instance_id: str
    decision_type: str
    curriculum_target: str
    priority: float
    rank_position: int
    rationale_summary: str
    prerequisite_chain: tuple[str, ...]
    estimated_effort_minutes: int
    expected_educational_outcome: str
    supporting_belief_ids: tuple[str, ...]
    supporting_curriculum_refs: tuple[str, ...]
    supporting_evidence_ids: tuple[str, ...]
    applied_rule_ids: tuple[str, ...]
    reasoned_at: datetime
    reasoning_version: str = REASONING_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "priority", clamp01(self.priority))
        dtype = (self.decision_type or "").strip().lower()
        if dtype not in {m.value for m in DecisionType}:
            raise ValueError(f"Invalid decision_type: {self.decision_type!r}")
        object.__setattr__(self, "decision_type", dtype)

        outcome = (self.expected_educational_outcome or "").strip().lower()
        if outcome not in {m.value for m in ExpectedOutcome}:
            raise ValueError(
                f"Invalid expected_educational_outcome: "
                f"{self.expected_educational_outcome!r}"
            )
        object.__setattr__(self, "expected_educational_outcome", outcome)

        if not (self.curriculum_target or "").strip():
            raise ValueError("curriculum_target is required")
        if not (self.reasoning_version or "").strip():
            raise ValueError("reasoning_version is required")
        if not (self.rationale_summary or "").strip():
            raise ValueError(
                "rationale_summary is required — no opaque educational decision"
            )
        if self.rank_position < 1:
            raise ValueError("rank_position must be >= 1")
        if self.estimated_effort_minutes < 0:
            raise ValueError("estimated_effort_minutes must be >= 0")

        object.__setattr__(
            self,
            "prerequisite_chain",
            _clean_ids(self.prerequisite_chain),
        )
        object.__setattr__(
            self,
            "supporting_belief_ids",
            _clean_ids(self.supporting_belief_ids),
        )
        object.__setattr__(
            self,
            "supporting_curriculum_refs",
            _clean_ids(self.supporting_curriculum_refs),
        )
        object.__setattr__(
            self,
            "supporting_evidence_ids",
            _clean_ids(self.supporting_evidence_ids),
        )
        object.__setattr__(
            self,
            "applied_rule_ids",
            tuple(sorted(set(_clean_ids(self.applied_rule_ids)))),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "instance_id": self.instance_id,
            "decision_type": self.decision_type,
            "curriculum_target": self.curriculum_target,
            "priority": self.priority,
            "rank_position": self.rank_position,
            "rationale_summary": self.rationale_summary,
            "prerequisite_chain": list(self.prerequisite_chain),
            "estimated_effort_minutes": self.estimated_effort_minutes,
            "expected_educational_outcome": self.expected_educational_outcome,
            "supporting_belief_ids": list(self.supporting_belief_ids),
            "supporting_curriculum_refs": list(self.supporting_curriculum_refs),
            "supporting_evidence_ids": list(self.supporting_evidence_ids),
            "applied_rule_ids": list(self.applied_rule_ids),
            "reasoned_at": self.reasoned_at.isoformat(),
            "reasoning_version": self.reasoning_version,
        }


def _clean_ids(values: tuple[str, ...] | list[str]) -> tuple[str, ...]:
    return tuple(
        v.strip() for v in values if isinstance(v, str) and v.strip()
    )
