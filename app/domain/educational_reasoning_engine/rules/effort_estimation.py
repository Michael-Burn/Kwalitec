"""Effort estimation rule (EI-007).

Annotates targets with deterministic effort estimates from difficulty.
Slightly prefers lower-effort actionable nodes via a small priority boost.
"""

from __future__ import annotations

from app.domain.educational_reasoning_engine.context import ReasoningContext
from app.domain.educational_reasoning_engine.rules.base import RuleProposal
from app.domain.educational_reasoning_engine.rules.thresholds import (
    DEFAULT_EFFORT_MINUTES,
    effort_for_difficulty,
    is_actionable,
)


class EffortEstimationRule:
    """Attach effort estimates and a small inverse-effort priority boost."""

    @property
    def rule_id(self) -> str:
        return "effort_estimation"

    def apply(self, context: ReasoningContext) -> tuple[RuleProposal, ...]:
        out: list[RuleProposal] = []
        for node in context.study_targets():
            if not is_actionable(node):
                continue
            effort = effort_for_difficulty(node.difficulty)
            # Lower effort → slightly higher boost (cap 0.05).
            boost = round(
                0.05 * (1.0 - (effort / max(DEFAULT_EFFORT_MINUTES * 3, effort))),
                6,
            )
            out.append(
                RuleProposal(
                    rule_id=self.rule_id,
                    curriculum_target=node.node_stable_id,
                    decision_type=None,
                    priority_delta=boost,
                    estimated_effort_minutes=effort,
                    rationale=(
                        f"Estimated effort {effort} minutes for difficulty "
                        f"{node.difficulty or 'default'}."
                    ),
                    supporting_curriculum_refs=(node.node_stable_id,),
                    detail=f"difficulty={node.difficulty};effort={effort}",
                )
            )
        return tuple(out)
