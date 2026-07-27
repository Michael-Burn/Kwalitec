"""Consistency Rule — study-day consistency dimension."""

from __future__ import annotations

from app.domain.educational_reasoning.decision import DecisionKind, EducationalDecision
from app.domain.educational_reasoning.explanation import Explanation
from app.domain.educational_reasoning.reasoning_context import ReasoningContext
from app.domain.educational_reasoning.reasoning_rule import ReasoningRule, RuleExecution

RULE_CODE = "consistency"


class ConsistencyRule(ReasoningRule):
    """Compute consistency from unique study days relative to activity volume."""

    code = RULE_CODE
    name = "Consistency Rule"
    description = "Unique study days / expected window (capped at 1.0)"

    def apply(self, context: ReasoningContext) -> RuleExecution:
        n = len(context.observations)
        if n == 0:
            consistency = 0.0
            days_count = 0
        else:
            days = {o.recorded_at.date() for o in context.observations}
            days_count = len(days)
            consistency = round(min(1.0, days_count / max(5.0, n * 0.5)), 4)

        explanation = Explanation(
            summary=(
                f"Consistency is {consistency:.3f} across {days_count} study days"
            ),
            rule_code=self.code,
            observation_ids=context.observation_ids,
            detail=self.description,
            metadata={"unique_days": days_count, "observation_count": n},
        )
        decision = EducationalDecision(
            decision_id=f"dec-con-{context.twin_id[:16]}",
            kind=DecisionKind.CONSISTENCY,
            rule_code=self.code,
            twin_id=context.twin_id,
            subject_ref=context.twin_id,
            value=consistency,
            explanation=explanation,
            created_at=context.computed_at,
            observation_ids=context.observation_ids,
        )
        return RuleExecution(
            rule_code=self.code,
            rule_name=self.name,
            explanation=explanation,
            decisions=(decision,),
            consistency=consistency,
            inputs={"observation_count": n},
            outputs={"consistency": consistency, "unique_days": days_count},
        )
