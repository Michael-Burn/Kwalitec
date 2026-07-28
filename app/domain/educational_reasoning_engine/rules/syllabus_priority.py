"""Syllabus priority rule (EI-007).

Boost earlier syllabus-index targets so curriculum order shapes ranking.
"""

from __future__ import annotations

from app.domain.educational_reasoning_engine.context import ReasoningContext
from app.domain.educational_reasoning_engine.rules.base import RuleProposal
from app.domain.educational_reasoning_engine.rules.thresholds import is_actionable


class SyllabusPriorityRule:
    """Priority boost inversely proportional to syllabus index."""

    @property
    def rule_id(self) -> str:
        return "syllabus_priority"

    def apply(self, context: ReasoningContext) -> tuple[RuleProposal, ...]:
        targets = context.study_targets()
        if not targets:
            return ()
        max_index = max(n.syllabus_index for n in targets)
        span = max(max_index, 1)
        out: list[RuleProposal] = []
        for node in targets:
            if not is_actionable(node):
                continue
            # Earlier nodes get larger boost: index 0 → ~0.12, last → ~0.0
            boost = round(0.12 * (1.0 - (node.syllabus_index / span)), 6)
            if boost <= 0.0:
                continue
            out.append(
                RuleProposal(
                    rule_id=self.rule_id,
                    curriculum_target=node.node_stable_id,
                    decision_type=None,
                    priority_delta=boost,
                    rationale=(
                        f"Syllabus order boost for index {node.syllabus_index}."
                    ),
                    supporting_curriculum_refs=(node.node_stable_id,),
                    detail=f"syllabus_index={node.syllabus_index};boost={boost}",
                )
            )
        return tuple(out)
