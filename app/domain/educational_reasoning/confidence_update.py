"""Confidence Adjustment Rule — confidence from outcome ratio."""

from __future__ import annotations

from app.domain.educational_reasoning.decision import DecisionKind, EducationalDecision
from app.domain.educational_reasoning.explanation import Explanation
from app.domain.educational_reasoning.reasoning_context import ReasoningContext
from app.domain.educational_reasoning.reasoning_rule import ReasoningRule, RuleExecution
from app.domain.student_digital_twin.confidence import (
    ConfidenceState,
    confidence_band_from_score,
)

RULE_CODE = "confidence_adjustment"


class ConfidenceAdjustmentRule(ReasoningRule):
    """Adjust learner confidence from known observation outcomes."""

    code = RULE_CODE
    name = "Confidence Adjustment Rule"
    description = "Confidence derived from positive-outcome ratio across observations"

    def apply(self, context: ReasoningContext) -> RuleExecution:
        outcomes = [o.is_positive_outcome for o in context.observations]
        known = [o for o in outcomes if o is not None]
        score = (sum(1 for o in known if o) / len(known)) if known else 0.0
        score = round(score, 4)
        band = confidence_band_from_score(score)
        confidence = ConfidenceState(
            score=score,
            band=band,
            evidence_count=len(known),
            reason="deterministic_outcome_ratio_v1",
            updated_at=context.computed_at,
        )

        explanation = Explanation(
            summary=(
                f"Confidence adjusted to {score:.3f} ({band.value}) "
                f"from {len(known)} known outcomes"
            ),
            rule_code=self.code,
            observation_ids=context.observation_ids,
            detail=self.description,
            metadata={"score": score, "band": band.value, "known_outcomes": len(known)},
        )
        decision = EducationalDecision(
            decision_id=f"dec-conf-{context.twin_id[:16]}",
            kind=DecisionKind.CONFIDENCE_ADJUSTMENT,
            rule_code=self.code,
            twin_id=context.twin_id,
            subject_ref=context.twin_id,
            value=score,
            explanation=explanation,
            created_at=context.computed_at,
            observation_ids=context.observation_ids,
            payload={"band": band.value, "evidence_count": len(known)},
        )
        return RuleExecution(
            rule_code=self.code,
            rule_name=self.name,
            explanation=explanation,
            decisions=(decision,),
            confidence=confidence,
            inputs={"known_outcomes": len(known)},
            outputs={"score": score, "band": band.value},
        )
