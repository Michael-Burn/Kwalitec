"""Revision-session inference rule (EI-006)."""

from __future__ import annotations

from app.domain.learning_evidence.evidence_type import EvidenceType
from app.domain.twin_inference.rules.base import InferenceContext, RuleContribution


class RevisionEventRule:
    """Revision strengthens confidence and lightly refreshes mastery."""

    rule_id = "revision_events"

    def apply(self, context: InferenceContext) -> tuple[RuleContribution, ...]:
        out: list[RuleContribution] = []
        for event in context.evidence:
            if event.evidence_type != EvidenceType.REVISION_SESSION.value:
                continue
            duration = event.metadata.get("duration_minutes")
            duration_factor = 1.0
            detail = "Revision session"
            if isinstance(duration, int | float) and duration > 0:
                # Cap at 60 minutes → factor 1.25
                duration_factor = min(1.25, 0.75 + (float(duration) / 120.0))
                detail = (
                    f"Revision session ({duration} min, "
                    f"factor {duration_factor:.2f})"
                )
            out.append(
                RuleContribution(
                    rule_id=self.rule_id,
                    mastery_delta=0.06,
                    confidence_delta=0.12,
                    weight=duration_factor,
                    evidence_ids=(event.evidence_id,),
                    detail=detail,
                )
            )
        return tuple(out)
