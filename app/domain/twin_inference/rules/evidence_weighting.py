"""Evidence-type weighting rule (EI-006).

Assigns base mastery/confidence deltas from catalogue evidence types.
"""

from __future__ import annotations

from app.domain.learning_evidence.evidence_type import EvidenceType
from app.domain.twin_inference.rules.base import InferenceContext, RuleContribution

# Base (unweighted) deltas per evidence type. Deterministic catalogue.
_BASE_WEIGHTS: dict[str, tuple[float, float]] = {
    EvidenceType.READING_COMPLETED.value: (0.05, 0.08),
    EvidenceType.WORKED_EXAMPLE_COMPLETED.value: (0.08, 0.10),
    EvidenceType.PRACTICE_ATTEMPT.value: (0.05, 0.06),
    EvidenceType.ASSESSMENT_RESULT.value: (0.10, 0.12),
    EvidenceType.STUDY_SESSION.value: (0.04, 0.05),
    EvidenceType.REVISION_SESSION.value: (0.03, 0.04),
    EvidenceType.MANUAL_FOUNDER_OVERRIDE.value: (0.0, 0.0),
}


class EvidenceWeightingRule:
    """Contribute base type weights for each usable evidence event."""

    rule_id = "evidence_weighting"

    def apply(self, context: InferenceContext) -> tuple[RuleContribution, ...]:
        out: list[RuleContribution] = []
        for event in context.evidence:
            mastery, confidence = _BASE_WEIGHTS.get(
                event.evidence_type, (0.02, 0.03)
            )
            if event.evidence_type == EvidenceType.MANUAL_FOUNDER_OVERRIDE.value:
                # Founder overrides are handled by assessment/override path;
                # still record presence with zero base delta for audit.
                out.append(
                    RuleContribution(
                        rule_id=self.rule_id,
                        mastery_delta=0.0,
                        confidence_delta=0.0,
                        weight=1.0,
                        evidence_ids=(event.evidence_id,),
                        detail="Founder override noted; no base type weight applied",
                    )
                )
                continue
            out.append(
                RuleContribution(
                    rule_id=self.rule_id,
                    mastery_delta=mastery,
                    confidence_delta=confidence,
                    weight=1.0,
                    evidence_ids=(event.evidence_id,),
                    detail=f"Base weight for {event.evidence_type}",
                )
            )
        return tuple(out)
