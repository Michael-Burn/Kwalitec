"""Study continuity rule (EI-007).

Prefer continuing the most recently studied incomplete path to preserve
learning momentum.
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


class StudyContinuityRule:
    """Propose continue_path for the latest in-progress / recent study target."""

    @property
    def rule_id(self) -> str:
        return "study_continuity"

    def apply(self, context: ReasoningContext) -> tuple[RuleProposal, ...]:
        last_id = context.last_studied_node_id()
        if last_id is None:
            return ()
        node_map = context.node_map()
        last = node_map.get(last_id)
        if last is None:
            return ()

        # Prefer continuing the last node if still incomplete.
        candidates = [last]
        # Also consider next incomplete LO with higher syllabus index.
        later = sorted(
            (
                n
                for n in context.study_targets()
                if n.syllabus_index > last.syllabus_index
                and n.completion_status != CompletionStatus.COMPLETED.value
                and prerequisites_satisfied(n, node_map)
            ),
            key=lambda n: (n.syllabus_index, n.node_stable_id),
        )
        if later:
            candidates.append(later[0])

        out: list[RuleProposal] = []
        seen: set[str] = set()
        for idx, node in enumerate(candidates):
            if node.node_stable_id in seen:
                continue
            if node.completion_status == CompletionStatus.COMPLETED.value:
                continue
            seen.add(node.node_stable_id)
            priority = 0.50 if idx == 0 else 0.35
            out.append(
                RuleProposal(
                    rule_id=self.rule_id,
                    curriculum_target=node.node_stable_id,
                    decision_type=DecisionType.CONTINUE_PATH.value,
                    priority_delta=priority,
                    rationale=(
                        f"Continue study path from last interaction on "
                        f"{last_id} toward {node.node_stable_id}."
                    ),
                    prerequisite_chain=node.prerequisite_ids,
                    expected_educational_outcome=ExpectedOutcome.MAINTAIN_MOMENTUM.value,
                    supporting_belief_ids=belief_support(node),
                    supporting_curriculum_refs=(node.node_stable_id, last_id),
                    supporting_evidence_ids=node.supporting_evidence_ids,
                    detail=f"last_studied={last_id};continuity_rank={idx}",
                )
            )
        return tuple(out)
