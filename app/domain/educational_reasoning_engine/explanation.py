"""Explainability layer for educational decisions (EI-007).

No decision may exist without an explanation that cites beliefs, curriculum
dependencies, rules, evidence references, priority calculation, and rationale.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RuleProposalRecord:
    """One rule's proposal contribution, for audit and explanation."""

    rule_id: str
    priority_delta: float
    detail: str = ""
    supporting_belief_ids: tuple[str, ...] = ()
    supporting_curriculum_refs: tuple[str, ...] = ()
    supporting_evidence_ids: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "priority_delta": self.priority_delta,
            "detail": self.detail,
            "supporting_belief_ids": list(self.supporting_belief_ids),
            "supporting_curriculum_refs": list(self.supporting_curriculum_refs),
            "supporting_evidence_ids": list(self.supporting_evidence_ids),
        }


@dataclass(frozen=True)
class PriorityCalculation:
    """Deterministic priority arithmetic exposed for explainability."""

    raw_sum: float
    clamped: float
    formula: str
    components: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "raw_sum": self.raw_sum,
            "clamped": self.clamped,
            "formula": self.formula,
            "components": list(self.components),
        }


@dataclass(frozen=True)
class DecisionExplanation:
    """Complete explanation bound to one educational decision."""

    decision_id: str
    contributing_beliefs: tuple[str, ...]
    curriculum_dependencies: tuple[str, ...]
    educational_rules_applied: tuple[str, ...]
    evidence_references: tuple[str, ...]
    priority_calculation: PriorityCalculation
    rule_proposals: tuple[RuleProposalRecord, ...]
    rationale_summary: str
    reasoning_version: str

    def __post_init__(self) -> None:
        if not (self.rationale_summary or "").strip():
            raise ValueError("rationale_summary is required")
        if not (self.reasoning_version or "").strip():
            raise ValueError("reasoning_version is required")
        if not self.educational_rules_applied:
            raise ValueError("educational_rules_applied must be non-empty")

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "contributing_beliefs": list(self.contributing_beliefs),
            "curriculum_dependencies": list(self.curriculum_dependencies),
            "educational_rules_applied": list(self.educational_rules_applied),
            "evidence_references": list(self.evidence_references),
            "priority_calculation": self.priority_calculation.to_dict(),
            "rule_proposals": [r.to_dict() for r in self.rule_proposals],
            "rationale_summary": self.rationale_summary,
            "reasoning_version": self.reasoning_version,
        }
