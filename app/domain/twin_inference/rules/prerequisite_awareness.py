"""Prerequisite-awareness rule (EI-006).

Caps inferred mastery when hard prerequisites remain weak. Emits a negative
mastery contribution so the explanation cites the prerequisite constraint.
"""

from __future__ import annotations

from app.domain.twin_inference.rules.base import InferenceContext, RuleContribution

_WEAK_THRESHOLD = 0.40
_CAP_SLACK = 0.30


class PrerequisiteAwarenessRule:
    """Apply prerequisite caps after prior rules have scored the node.

    This rule reads ``context.metadata['provisional_mastery']`` (set by the
    engine after aggregating earlier rules) and ``prerequisite_mastery``.
    """

    rule_id = "prerequisite_awareness"

    def apply(self, context: InferenceContext) -> tuple[RuleContribution, ...]:
        prereqs = context.prerequisite_mastery
        if not prereqs:
            return ()

        provisional = float(context.metadata.get("provisional_mastery", 0.0))
        weak = sorted(
            (pid, float(m))
            for pid, m in prereqs.items()
            if float(m) < _WEAK_THRESHOLD
        )
        if not weak:
            return (
                RuleContribution(
                    rule_id=self.rule_id,
                    mastery_delta=0.0,
                    confidence_delta=0.0,
                    weight=1.0,
                    evidence_ids=(),
                    detail="All prerequisites meet the readiness threshold",
                ),
            )

        weakest_id, weakest_m = weak[0]
        allowed = weakest_m + _CAP_SLACK
        if provisional <= allowed:
            return (
                RuleContribution(
                    rule_id=self.rule_id,
                    mastery_delta=0.0,
                    confidence_delta=0.0,
                    weight=1.0,
                    evidence_ids=(),
                    detail=(
                        f"Weak prerequisite {weakest_id} "
                        f"(mastery {weakest_m:.4f}) noted; "
                        f"provisional mastery {provisional:.4f} "
                        f"within cap {allowed:.4f}"
                    ),
                ),
            )

        # Negative delta to bring provisional down to allowed.
        delta = allowed - provisional
        return (
            RuleContribution(
                rule_id=self.rule_id,
                mastery_delta=delta,
                confidence_delta=-0.05,
                weight=1.0,
                evidence_ids=(),
                detail=(
                    f"Capped mastery due to weak prerequisite {weakest_id} "
                    f"(mastery {weakest_m:.4f}); allowed {allowed:.4f}"
                ),
            ),
        )
