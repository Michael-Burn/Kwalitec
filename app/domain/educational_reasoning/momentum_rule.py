"""Learning Momentum Rule — recent outcome momentum dimension."""

from __future__ import annotations

from app.domain.educational_reasoning.decision import DecisionKind, EducationalDecision
from app.domain.educational_reasoning.explanation import Explanation
from app.domain.educational_reasoning.reasoning_context import ReasoningContext
from app.domain.educational_reasoning.reasoning_rule import ReasoningRule, RuleExecution

RULE_CODE = "learning_momentum"
RECENT_WINDOW = 5


class LearningMomentumRule(ReasoningRule):
    """Compute learning momentum from the most recent observation outcomes."""

    code = RULE_CODE
    name = "Learning Momentum Rule"
    description = "Share of recent known outcomes that are positive"

    def apply(self, context: ReasoningContext) -> RuleExecution:
        recent = context.observations[-RECENT_WINDOW:]
        recent_known = [
            o.is_positive_outcome
            for o in recent
            if o.is_positive_outcome is not None
        ]
        momentum = (
            round(sum(1 for o in recent_known if o) / len(recent_known), 4)
            if recent_known
            else 0.0
        )
        recent_ids = tuple(o.observation_id for o in recent)

        explanation = Explanation(
            summary=(
                f"Learning momentum is {momentum:.3f} from "
                f"{len(recent_known)} recent known outcomes"
            ),
            rule_code=self.code,
            observation_ids=recent_ids,
            detail=self.description,
            metadata={"window": RECENT_WINDOW, "known": len(recent_known)},
        )
        decision = EducationalDecision(
            decision_id=f"dec-mom-{context.twin_id[:16]}",
            kind=DecisionKind.MOMENTUM,
            rule_code=self.code,
            twin_id=context.twin_id,
            subject_ref=context.twin_id,
            value=momentum,
            explanation=explanation,
            created_at=context.computed_at,
            observation_ids=recent_ids,
        )
        return RuleExecution(
            rule_code=self.code,
            rule_name=self.name,
            explanation=explanation,
            decisions=(decision,),
            momentum=momentum,
            inputs={"recent_count": len(recent)},
            outputs={"momentum": momentum},
        )
