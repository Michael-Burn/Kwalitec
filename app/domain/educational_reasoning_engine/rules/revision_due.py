"""Revision due nodes rule (EI-007).

Propose revise actions for nodes whose SCI revision_status is due or overdue.
"""

from __future__ import annotations

from app.domain.educational_reasoning_engine.context import ReasoningContext
from app.domain.educational_reasoning_engine.decision_type import (
    DecisionType,
    ExpectedOutcome,
)
from app.domain.educational_reasoning_engine.rules.base import RuleProposal
from app.domain.educational_reasoning_engine.rules.thresholds import belief_support
from app.domain.student_curriculum_binding.node_state import RevisionStatus

_REVISION_PRIORITY = {
    RevisionStatus.OVERDUE.value: 0.92,
    RevisionStatus.DUE.value: 0.80,
}


class RevisionDueRule:
    """Propose revise for due / overdue revision slots."""

    @property
    def rule_id(self) -> str:
        return "revision_due_nodes"

    def apply(self, context: ReasoningContext) -> tuple[RuleProposal, ...]:
        out: list[RuleProposal] = []
        for node in context.study_targets():
            priority = _REVISION_PRIORITY.get(node.revision_status)
            if priority is None:
                continue
            out.append(
                RuleProposal(
                    rule_id=self.rule_id,
                    curriculum_target=node.node_stable_id,
                    decision_type=DecisionType.REVISE.value,
                    priority_delta=priority,
                    rationale=(
                        f"Node {node.node_stable_id} revision_status="
                        f"{node.revision_status}."
                    ),
                    prerequisite_chain=node.prerequisite_ids,
                    expected_educational_outcome=ExpectedOutcome.RESTORE_RETENTION.value,
                    supporting_belief_ids=belief_support(node),
                    supporting_curriculum_refs=(node.node_stable_id,),
                    supporting_evidence_ids=node.supporting_evidence_ids,
                    detail=f"revision_status={node.revision_status}",
                )
            )
        return tuple(out)
