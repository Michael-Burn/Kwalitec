"""Repeated practice-attempt rule (EI-006)."""

from __future__ import annotations

from app.domain.learning_evidence.evidence_type import EvidenceType
from app.domain.twin_inference.rules.base import InferenceContext, RuleContribution

_DIMINISH_AFTER = 3
_DIMINISH_FACTOR = 0.7


class RepeatedAttemptsRule:
    """Score practice attempts with success/failure and diminishing returns."""

    rule_id = "repeated_attempts"

    def apply(self, context: InferenceContext) -> tuple[RuleContribution, ...]:
        attempts = [
            e
            for e in context.evidence
            if e.evidence_type == EvidenceType.PRACTICE_ATTEMPT.value
        ]
        if not attempts:
            return ()

        out: list[RuleContribution] = []
        for index, event in enumerate(attempts, start=1):
            correct = event.metadata.get("correct")
            if correct is True:
                mastery, confidence, label = 0.12, 0.10, "correct practice"
            elif correct is False:
                mastery, confidence, label = 0.02, 0.05, "incorrect practice"
            else:
                mastery, confidence, label = 0.05, 0.06, "practice (outcome unknown)"

            weight = 1.0 if index <= _DIMINISH_AFTER else _DIMINISH_FACTOR
            detail = f"Attempt #{index}: {label}"
            if index > _DIMINISH_AFTER:
                detail += f"; diminishing weight {_DIMINISH_FACTOR}"

            out.append(
                RuleContribution(
                    rule_id=self.rule_id,
                    mastery_delta=mastery,
                    confidence_delta=confidence,
                    weight=weight,
                    evidence_ids=(event.evidence_id,),
                    detail=detail,
                )
            )
        return tuple(out)
