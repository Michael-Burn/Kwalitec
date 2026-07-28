"""Prerequisite satisfaction rule (EI-007).

When a study target is incomplete but hard prerequisites are weak, propose
satisfying the weakest prerequisite before advancing.
"""

from __future__ import annotations

from app.domain.educational_reasoning_engine.context import ReasoningContext
from app.domain.educational_reasoning_engine.decision_type import (
    DecisionType,
    ExpectedOutcome,
)
from app.domain.educational_reasoning_engine.rules.base import RuleProposal
from app.domain.educational_reasoning_engine.rules.thresholds import (
    PREREQ_MASTERY_THRESHOLD,
    belief_support,
    weak_prerequisites,
)
from app.domain.student_curriculum_binding.node_state import CompletionStatus


class PrerequisiteSatisfactionRule:
    """Propose satisfy_prerequisite for blocked incomplete learning objectives."""

    @property
    def rule_id(self) -> str:
        return "prerequisite_satisfaction"

    def apply(self, context: ReasoningContext) -> tuple[RuleProposal, ...]:
        node_map = context.node_map()
        out: list[RuleProposal] = []
        for node in context.study_targets():
            if node.completion_status == CompletionStatus.COMPLETED.value:
                continue
            weak = weak_prerequisites(node, node_map)
            if not weak:
                continue
            # Target the weakest prerequisite (lowest mastery, then id).
            ranked = sorted(
                weak,
                key=lambda pid: (
                    node_map[pid].mastery if pid in node_map else 0.0,
                    pid,
                ),
            )
            target = ranked[0]
            target_node = node_map.get(target)
            out.append(
                RuleProposal(
                    rule_id=self.rule_id,
                    curriculum_target=target,
                    decision_type=DecisionType.SATISFY_PREREQUISITE.value,
                    priority_delta=0.72,
                    rationale=(
                        f"Node {node.node_stable_id} is blocked by weak "
                        f"prerequisite {target} "
                        f"(mastery < {PREREQ_MASTERY_THRESHOLD})."
                    ),
                    prerequisite_chain=node.prerequisite_ids,
                    expected_educational_outcome=ExpectedOutcome.UNLOCK_DEPENDENT.value,
                    supporting_belief_ids=belief_support(target_node)
                    if target_node
                    else (),
                    supporting_curriculum_refs=(
                        node.node_stable_id,
                        target,
                        *node.prerequisite_ids,
                    ),
                    supporting_evidence_ids=(
                        target_node.supporting_evidence_ids if target_node else ()
                    ),
                    detail=f"blocked_node={node.node_stable_id};weak={','.join(weak)}",
                )
            )
        return tuple(out)
