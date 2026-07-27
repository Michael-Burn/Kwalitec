"""Readiness Contribution Rule — exam readiness from state dimensions."""

from __future__ import annotations

import uuid

from app.domain.educational_reasoning.decision import DecisionKind, EducationalDecision
from app.domain.educational_reasoning.explanation import Explanation
from app.domain.educational_reasoning.reasoning_context import ReasoningContext
from app.domain.educational_reasoning.reasoning_rule import ReasoningRule, RuleExecution
from app.domain.student_digital_twin.observation import ObservationKind

RULE_CODE = "readiness_contribution"

W_KNOWLEDGE = 0.40
W_CONFIDENCE = 0.20
W_RETENTION = 0.15
W_CONSISTENCY = 0.10
W_MOMENTUM = 0.15


class ReadinessContributionRule(ReasoningRule):
    """Combine mastery-derived dimensions into exam readiness and retention.

    Retention is computed here from observation kinds; readiness blends
    knowledge, confidence, retention, consistency, and momentum.
    """

    code = RULE_CODE
    name = "Readiness Contribution Rule"
    description = "Weighted exam-readiness blend of learning-state dimensions"

    def apply(self, context: ReasoningContext) -> RuleExecution:
        n = len(context.observations)
        knowledge = context.knowledge if context.knowledge is not None else 0.0
        confidence_score = (
            context.confidence.score if context.confidence is not None else 0.0
        )
        consistency = context.consistency if context.consistency is not None else 0.0
        momentum = context.momentum if context.momentum is not None else 0.0

        retention_kinds = {
            ObservationKind.FORMULA_REVIEWED,
            ObservationKind.REVISION_COMPLETED,
            ObservationKind.CHAPTER_COMPLETED,
        }
        if n == 0:
            retention = 0.0
        else:
            retention_hits = sum(
                1 for o in context.observations if o.kind in retention_kinds
            )
            retention = round(min(1.0, retention_hits / max(3.0, n * 0.4)), 4)

        exam_readiness = round(
            W_KNOWLEDGE * knowledge
            + W_CONFIDENCE * confidence_score
            + W_RETENTION * retention
            + W_CONSISTENCY * consistency
            + W_MOMENTUM * momentum,
            4,
        )

        explanation = Explanation(
            summary=(
                f"Exam readiness contribution is {exam_readiness:.3f} "
                f"(knowledge={knowledge:.3f}, confidence={confidence_score:.3f}, "
                f"retention={retention:.3f}, consistency={consistency:.3f}, "
                f"momentum={momentum:.3f})"
            ),
            rule_code=self.code,
            observation_ids=context.observation_ids,
            detail=self.description,
            metadata={
                "weights": {
                    "knowledge": W_KNOWLEDGE,
                    "confidence": W_CONFIDENCE,
                    "retention": W_RETENTION,
                    "consistency": W_CONSISTENCY,
                    "momentum": W_MOMENTUM,
                },
                "snapshot_id": f"lss-{uuid.uuid4().hex[:12]}",
            },
        )
        decision = EducationalDecision(
            decision_id=f"dec-rdy-{context.twin_id[:16]}",
            kind=DecisionKind.READINESS,
            rule_code=self.code,
            twin_id=context.twin_id,
            subject_ref=context.twin_id,
            value=exam_readiness,
            explanation=explanation,
            created_at=context.computed_at,
            observation_ids=context.observation_ids,
            payload={
                "retention": retention,
                "knowledge": knowledge,
                "confidence": confidence_score,
                "consistency": consistency,
                "momentum": momentum,
            },
        )
        return RuleExecution(
            rule_code=self.code,
            rule_name=self.name,
            explanation=explanation,
            decisions=(decision,),
            retention=retention,
            exam_readiness=exam_readiness,
            inputs={
                "knowledge": knowledge,
                "confidence": confidence_score,
                "consistency": consistency,
                "momentum": momentum,
            },
            outputs={
                "retention": retention,
                "exam_readiness": exam_readiness,
                "snapshot_id": explanation.metadata["snapshot_id"],
            },
        )
