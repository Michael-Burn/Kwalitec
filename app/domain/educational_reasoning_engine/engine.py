"""Deterministic Educational Reasoning Engine core (EI-007).

Converts trusted educational assets into ordered, explainable educational
decisions. Pure domain — no Flask, SQLAlchemy, mission text, or UI content.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any

from app.domain.educational_reasoning_engine.context import ReasoningContext
from app.domain.educational_reasoning_engine.decision import (
    EducationalDecision,
    clamp01,
)
from app.domain.educational_reasoning_engine.decision_type import ExpectedOutcome
from app.domain.educational_reasoning_engine.explanation import (
    DecisionExplanation,
    PriorityCalculation,
    RuleProposalRecord,
)
from app.domain.educational_reasoning_engine.prioritisation import (
    merge_proposals,
    rank_candidates,
    resolve_effort,
)
from app.domain.educational_reasoning_engine.rules import default_rule_pack
from app.domain.educational_reasoning_engine.rules.base import ReasoningRule
from app.domain.educational_reasoning_engine.version import REASONING_VERSION


@dataclass(frozen=True)
class ReasoningResultItem:
    """Decision plus mandatory explanation produced together."""

    decision: EducationalDecision
    explanation: DecisionExplanation

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision.to_dict(),
            "explanation": self.explanation.to_dict(),
        }


@dataclass(frozen=True)
class ReasoningResult:
    """Ordered educational decisions for one SCI evaluation."""

    instance_id: str
    reasoning_version: str
    items: tuple[ReasoningResultItem, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "reasoning_version": self.reasoning_version,
            "decision_count": len(self.items),
            "items": [i.to_dict() for i in self.items],
        }


class EducationalReasoningEngine:
    """Rule-based deterministic reasoning from learner state → decisions."""

    def __init__(
        self,
        rules: tuple[ReasoningRule, ...] | None = None,
        *,
        reasoning_version: str = REASONING_VERSION,
    ) -> None:
        self._rules = rules if rules is not None else default_rule_pack()
        self._reasoning_version = reasoning_version

    @property
    def reasoning_version(self) -> str:
        return self._reasoning_version

    def evaluate(self, context: ReasoningContext) -> ReasoningResult:
        """Evaluate an SCI and return ordered explainable decisions.

        Identical context and rule pack always yield identical decisions,
        priorities, ranks, and explanations.
        """
        proposals = []
        for rule in self._rules:
            proposals.extend(rule.apply(context))

        merged = merge_proposals(proposals)
        ranked = rank_candidates(merged)

        items: list[ReasoningResultItem] = []
        for rank, cand in enumerate(ranked, start=1):
            decision_id = _stable_decision_id(
                instance_id=context.instance_id,
                decision_type=cand.decision_type,
                curriculum_target=cand.curriculum_target,
            )

            priority = clamp01(cand.priority_raw)
            effort = resolve_effort(cand)
            outcome = cand.expected_educational_outcome or (
                ExpectedOutcome.ADVANCE_MASTERY.value
            )
            rationale = _build_rationale(
                decision_type=cand.decision_type,
                target=cand.curriculum_target,
                priority=priority,
                rank=rank,
                rule_ids=sorted(cand.applied_rule_ids),
                rationales=cand.rationales,
            )
            decision = EducationalDecision(
                decision_id=decision_id,
                instance_id=context.instance_id,
                decision_type=cand.decision_type,
                curriculum_target=cand.curriculum_target,
                priority=priority,
                rank_position=rank,
                rationale_summary=rationale,
                prerequisite_chain=cand.prerequisite_chain,
                estimated_effort_minutes=effort,
                expected_educational_outcome=outcome,
                supporting_belief_ids=tuple(sorted(cand.supporting_belief_ids)),
                supporting_curriculum_refs=tuple(
                    sorted(cand.supporting_curriculum_refs)
                ),
                supporting_evidence_ids=tuple(
                    sorted(cand.supporting_evidence_ids)
                ),
                applied_rule_ids=tuple(sorted(cand.applied_rule_ids)),
                reasoned_at=context.as_of,
                reasoning_version=self._reasoning_version,
            )
            explanation = DecisionExplanation(
                decision_id=decision_id,
                contributing_beliefs=tuple(sorted(cand.supporting_belief_ids)),
                curriculum_dependencies=tuple(
                    sorted(cand.supporting_curriculum_refs)
                ),
                educational_rules_applied=tuple(sorted(cand.applied_rule_ids)),
                evidence_references=tuple(sorted(cand.supporting_evidence_ids)),
                priority_calculation=PriorityCalculation(
                    raw_sum=round(cand.priority_raw, 6),
                    clamped=priority,
                    formula="clamp(sum(rule priority_deltas), 0, 1)",
                    components=tuple(cand.priority_components),
                ),
                rule_proposals=tuple(
                    RuleProposalRecord(
                        rule_id=p.rule_id,
                        priority_delta=p.priority_delta,
                        detail=p.detail or p.rationale,
                        supporting_belief_ids=p.supporting_belief_ids,
                        supporting_curriculum_refs=p.supporting_curriculum_refs,
                        supporting_evidence_ids=p.supporting_evidence_ids,
                    )
                    for p in cand.proposals
                ),
                rationale_summary=rationale,
                reasoning_version=self._reasoning_version,
            )
            items.append(
                ReasoningResultItem(decision=decision, explanation=explanation)
            )

        return ReasoningResult(
            instance_id=context.instance_id,
            reasoning_version=self._reasoning_version,
            items=tuple(items),
        )


def _stable_decision_id(
    *,
    instance_id: str,
    decision_type: str,
    curriculum_target: str,
) -> str:
    """Deterministic decision id independent of PYTHONHASHSEED."""
    raw = f"{instance_id}|{decision_type}|{curriculum_target}"
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:20]
    return f"ere-{digest}"


def _build_rationale(
    *,
    decision_type: str,
    target: str,
    priority: float,
    rank: int,
    rule_ids: list[str],
    rationales: list[str],
) -> str:
    head = (
        f"Rank {rank} {decision_type} on {target} with priority {priority:.4f} "
        f"via rules [{', '.join(rule_ids)}] ({REASONING_VERSION})."
    )
    if rationales:
        # Keep deterministic: first unique rationale snippets.
        seen: set[str] = set()
        extras: list[str] = []
        for r in rationales:
            if r not in seen:
                seen.add(r)
                extras.append(r)
        return head + " " + " ".join(extras[:3])
    return head
