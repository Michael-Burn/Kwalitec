"""Assessment outcome and founder-override rule (EI-006)."""

from __future__ import annotations

from app.domain.learning_evidence.evidence_type import EvidenceType
from app.domain.twin_inference.rules.base import InferenceContext, RuleContribution


class AssessmentOutcomeRule:
    """Interpret assessment_result and optional founder mastery overrides."""

    rule_id = "assessment_outcomes"

    def apply(self, context: InferenceContext) -> tuple[RuleContribution, ...]:
        out: list[RuleContribution] = []
        for event in context.evidence:
            if event.evidence_type == EvidenceType.ASSESSMENT_RESULT.value:
                out.extend(self._from_assessment(event.evidence_id, event.metadata))
            elif event.evidence_type == EvidenceType.MANUAL_FOUNDER_OVERRIDE.value:
                out.extend(self._from_override(event.evidence_id, event.metadata))
        return tuple(out)

    def _from_assessment(
        self, evidence_id: str, metadata: dict
    ) -> tuple[RuleContribution, ...]:
        contributions: list[RuleContribution] = []
        score = metadata.get("score")
        if isinstance(score, int | float):
            # Normalise 0–100 scores; leave 0–1 scores as-is.
            normalised = float(score)
            if normalised > 1.0:
                normalised = normalised / 100.0
            normalised = max(0.0, min(1.0, normalised))
            contributions.append(
                RuleContribution(
                    rule_id=self.rule_id,
                    mastery_delta=normalised * 0.35,
                    confidence_delta=0.20,
                    weight=1.0,
                    evidence_ids=(evidence_id,),
                    detail=(
                        f"Assessment score mapped to mastery "
                        f"factor {normalised:.4f}"
                    ),
                )
            )
        passed = metadata.get("passed")
        if passed is True:
            contributions.append(
                RuleContribution(
                    rule_id=self.rule_id,
                    mastery_delta=0.30,
                    confidence_delta=0.20,
                    weight=1.0,
                    evidence_ids=(evidence_id,),
                    detail="Assessment marked passed",
                )
            )
        elif passed is False:
            contributions.append(
                RuleContribution(
                    rule_id=self.rule_id,
                    mastery_delta=0.05,
                    confidence_delta=0.15,
                    weight=1.0,
                    evidence_ids=(evidence_id,),
                    detail="Assessment marked not passed",
                )
            )
        if not contributions:
            contributions.append(
                RuleContribution(
                    rule_id=self.rule_id,
                    mastery_delta=0.08,
                    confidence_delta=0.10,
                    weight=1.0,
                    evidence_ids=(evidence_id,),
                    detail="Assessment recorded without score/passed flags",
                )
            )
        return tuple(contributions)

    def _from_override(
        self, evidence_id: str, metadata: dict
    ) -> tuple[RuleContribution, ...]:
        """Optional absolute mastery/confidence in override metadata.

        When present, emit a contribution that the engine treats as a strong
        signal (high weight). Absolute replacement is applied by the engine
        via metadata flag on the contribution detail prefix ``absolute:``.
        """
        mastery = metadata.get("mastery")
        confidence = metadata.get("confidence")
        reason = str(metadata.get("reason") or "founder override").strip()
        if isinstance(mastery, int | float) or isinstance(confidence, int | float):
            m = float(mastery) if isinstance(mastery, int | float) else 0.0
            c = float(confidence) if isinstance(confidence, int | float) else 0.0
            return (
                RuleContribution(
                    rule_id=self.rule_id,
                    mastery_delta=max(0.0, min(1.0, m)),
                    confidence_delta=max(0.0, min(1.0, c)),
                    weight=1.0,
                    evidence_ids=(evidence_id,),
                    detail=f"absolute: Founder override — {reason}",
                ),
            )
        return (
            RuleContribution(
                rule_id=self.rule_id,
                mastery_delta=0.0,
                confidence_delta=0.05,
                weight=1.0,
                evidence_ids=(evidence_id,),
                detail=f"Founder override recorded — {reason}",
            ),
        )
