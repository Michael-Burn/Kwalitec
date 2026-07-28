"""Low-confidence topics rule (EI-007).

Propose confidence strengthening when mastery exists but belief confidence
is below threshold.
"""

from __future__ import annotations

from app.domain.educational_reasoning_engine.context import ReasoningContext
from app.domain.educational_reasoning_engine.decision_type import (
    DecisionType,
    ExpectedOutcome,
)
from app.domain.educational_reasoning_engine.rules.base import RuleProposal
from app.domain.educational_reasoning_engine.rules.thresholds import (
    LOW_CONFIDENCE_THRESHOLD,
    MIN_MASTERY_FOR_CONFIDENCE,
    belief_support,
)
from app.domain.student_curriculum_binding.node_state import CompletionStatus


class LowConfidenceRule:
    """Propose strengthen_confidence for under-confident developed nodes."""

    @property
    def rule_id(self) -> str:
        return "low_confidence_topics"

    def apply(self, context: ReasoningContext) -> tuple[RuleProposal, ...]:
        out: list[RuleProposal] = []
        for node in context.study_targets():
            if node.completion_status == CompletionStatus.NOT_STARTED.value:
                continue
            if node.mastery < MIN_MASTERY_FOR_CONFIDENCE:
                continue
            if node.confidence >= LOW_CONFIDENCE_THRESHOLD:
                continue
            deficit = LOW_CONFIDENCE_THRESHOLD - node.confidence
            priority = round(0.55 + min(0.25, deficit), 6)
            out.append(
                RuleProposal(
                    rule_id=self.rule_id,
                    curriculum_target=node.node_stable_id,
                    decision_type=DecisionType.STRENGTHEN_CONFIDENCE.value,
                    priority_delta=priority,
                    rationale=(
                        f"Node {node.node_stable_id} has mastery "
                        f"{node.mastery:.4f} but confidence "
                        f"{node.confidence:.4f} below "
                        f"{LOW_CONFIDENCE_THRESHOLD}."
                    ),
                    prerequisite_chain=node.prerequisite_ids,
                    expected_educational_outcome=ExpectedOutcome.RAISE_CONFIDENCE.value,
                    supporting_belief_ids=belief_support(node),
                    supporting_curriculum_refs=(node.node_stable_id,),
                    supporting_evidence_ids=node.supporting_evidence_ids,
                    detail=(
                        f"confidence={node.confidence:.4f};"
                        f"mastery={node.mastery:.4f}"
                    ),
                )
            )
        return tuple(out)
