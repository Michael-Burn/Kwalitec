"""Incomplete curriculum paths rule (EI-007).

Propose study_new for incomplete learning objectives whose prerequisites
are satisfied.
"""

from __future__ import annotations

from app.domain.educational_reasoning_engine.context import ReasoningContext
from app.domain.educational_reasoning_engine.decision_type import (
    DecisionType,
    ExpectedOutcome,
)
from app.domain.educational_reasoning_engine.rules.base import RuleProposal
from app.domain.educational_reasoning_engine.rules.thresholds import (
    belief_support,
    prerequisites_satisfied,
)
from app.domain.student_curriculum_binding.node_state import CompletionStatus


class IncompletePathsRule:
    """Propose study_new along incomplete, unblocked curriculum paths."""

    @property
    def rule_id(self) -> str:
        return "incomplete_curriculum_paths"

    def apply(self, context: ReasoningContext) -> tuple[RuleProposal, ...]:
        node_map = context.node_map()
        out: list[RuleProposal] = []
        for node in context.study_targets():
            if node.completion_status == CompletionStatus.COMPLETED.value:
                continue
            if not prerequisites_satisfied(node, node_map):
                continue
            if node.completion_status == CompletionStatus.NOT_STARTED.value:
                priority = 0.55
                outcome = ExpectedOutcome.INTRODUCE_NODE.value
            else:
                priority = 0.52
                outcome = ExpectedOutcome.ADVANCE_MASTERY.value
            out.append(
                RuleProposal(
                    rule_id=self.rule_id,
                    curriculum_target=node.node_stable_id,
                    decision_type=DecisionType.STUDY_NEW.value,
                    priority_delta=priority,
                    rationale=(
                        f"Node {node.node_stable_id} is "
                        f"{node.completion_status} with prerequisites satisfied."
                    ),
                    prerequisite_chain=node.prerequisite_ids,
                    expected_educational_outcome=outcome,
                    supporting_belief_ids=belief_support(node),
                    supporting_curriculum_refs=(
                        node.node_stable_id,
                        *node.prerequisite_ids,
                    ),
                    supporting_evidence_ids=node.supporting_evidence_ids,
                    detail=f"completion={node.completion_status}",
                )
            )
        return tuple(out)
