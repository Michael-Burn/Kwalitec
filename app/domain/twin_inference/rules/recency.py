"""Recency handling rule (EI-006).

Older evidence contributes with a deterministic decay weight relative to
``as_of``. Emits multiplicative adjustments as separate contributions so the
explanation can show recency explicitly.
"""

from __future__ import annotations

from datetime import datetime

from app.domain.twin_inference.rules.base import InferenceContext, RuleContribution

# (max_age_days inclusive upper bound, factor) — ordered ascending.
_RECENCY_BANDS: tuple[tuple[int | None, float], ...] = (
    (7, 1.0),
    (30, 0.85),
    (90, 0.70),
    (None, 0.55),
)


def recency_factor(occurred_at: datetime, as_of: datetime) -> float:
    """Return deterministic recency multiplier for an evidence timestamp."""
    occurred = occurred_at.replace(tzinfo=None) if occurred_at.tzinfo else occurred_at
    reference = as_of.replace(tzinfo=None) if as_of.tzinfo else as_of
    age_days = max(0, (reference - occurred).days)
    for upper, factor in _RECENCY_BANDS:
        if upper is None or age_days <= upper:
            return factor
    return 0.55


class RecencyRule:
    """Emit a soft positive reinforcement scaled by recency of each event.

    Uses a small fixed delta × recency factor so older evidence still counts
    but recent activity dominates explainably.
    """

    rule_id = "recency_handling"

    _MASTERY_UNIT = 0.02
    _CONFIDENCE_UNIT = 0.03

    def apply(self, context: InferenceContext) -> tuple[RuleContribution, ...]:
        out: list[RuleContribution] = []
        for event in context.evidence:
            factor = recency_factor(event.occurred_at, context.as_of)
            out.append(
                RuleContribution(
                    rule_id=self.rule_id,
                    mastery_delta=self._MASTERY_UNIT,
                    confidence_delta=self._CONFIDENCE_UNIT,
                    weight=factor,
                    evidence_ids=(event.evidence_id,),
                    detail=f"Recency factor {factor:.2f} for age-banded evidence",
                )
            )
        return tuple(out)
