"""Topic dependency ordering rule (EI-007).

Prefer nodes with fewer unsatisfied dependency hops (earlier in the
requires-graph) when ranking competing incomplete targets.
"""

from __future__ import annotations

from app.domain.educational_reasoning_engine.context import ReasoningContext
from app.domain.educational_reasoning_engine.rules.base import RuleProposal
from app.domain.educational_reasoning_engine.rules.thresholds import (
    PREREQ_MASTERY_THRESHOLD,
    is_actionable,
)


class TopicDependencyRule:
    """Boost nodes closer to the root of the prerequisite DAG."""

    @property
    def rule_id(self) -> str:
        return "topic_dependency_ordering"

    def apply(self, context: ReasoningContext) -> tuple[RuleProposal, ...]:
        node_map = context.node_map()
        depth_cache: dict[str, int] = {}

        def depth(nid: str, seen: frozenset[str]) -> int:
            if nid in depth_cache:
                return depth_cache[nid]
            node = node_map.get(nid)
            if node is None or not node.prerequisite_ids:
                depth_cache[nid] = 0
                return 0
            if nid in seen:
                depth_cache[nid] = 0
                return 0
            nxt = seen | {nid}
            d = 1 + max(
                (
                    depth(pid, nxt)
                    for pid in node.prerequisite_ids
                    if pid in node_map
                ),
                default=0,
            )
            depth_cache[nid] = d
            return d

        out: list[RuleProposal] = []
        for node in context.study_targets():
            if not is_actionable(node):
                continue
            d = depth(node.node_stable_id, frozenset())
            # Shallower dependency depth → higher boost.
            boost = round(max(0.0, 0.10 - (0.02 * d)), 6)
            unsatisfied = sum(
                1
                for pid in node.prerequisite_ids
                if (node_map[pid].mastery if pid in node_map else 0.0)
                < PREREQ_MASTERY_THRESHOLD
            )
            if unsatisfied:
                # Soft penalty already handled by prerequisite rule; small
                # negative keeps dependents below their prereqs when both appear.
                boost = round(boost - 0.05 * unsatisfied, 6)
            if boost == 0.0:
                continue
            out.append(
                RuleProposal(
                    rule_id=self.rule_id,
                    curriculum_target=node.node_stable_id,
                    decision_type=None,
                    priority_delta=boost,
                    rationale=(
                        f"Dependency depth {d} with {unsatisfied} weak "
                        f"prerequisite(s)."
                    ),
                    prerequisite_chain=node.prerequisite_ids,
                    supporting_curriculum_refs=(
                        node.node_stable_id,
                        *node.prerequisite_ids,
                    ),
                    detail=f"depth={d};unsatisfied={unsatisfied};boost={boost}",
                )
            )
        return tuple(out)
