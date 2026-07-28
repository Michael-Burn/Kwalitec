"""Deterministic Twin Inference Engine core (EI-006).

Converts Learning Evidence into explainable TwinBeliefs. Pure domain —
no Flask, SQLAlchemy, recommendations, or mission generation.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from typing import Any

from app.domain.learning_evidence.evidence_event import EvidenceEvent
from app.domain.twin_inference.belief import EmptyBeliefFactory, TwinBelief, clamp01
from app.domain.twin_inference.derive_state import derive_learning_state
from app.domain.twin_inference.evidence_prep import (
    evidence_ids,
    filter_usable_evidence,
)
from app.domain.twin_inference.explanation import (
    BeliefExplanation,
    ConfidenceCalculation,
    RuleContributionRecord,
)
from app.domain.twin_inference.rules import default_rule_pack
from app.domain.twin_inference.rules.base import (
    InferenceContext,
    InferenceRule,
    RuleContribution,
)
from app.domain.twin_inference.version import INFERENCE_VERSION

_PREREQ_RULE_ID = "prerequisite_awareness"
_ABSOLUTE_PREFIX = "absolute:"


@dataclass(frozen=True)
class InferenceResult:
    """Belief plus mandatory explanation produced together."""

    belief: TwinBelief
    explanation: BeliefExplanation

    def to_dict(self) -> dict[str, Any]:
        return {
            "belief": self.belief.to_dict(),
            "explanation": self.explanation.to_dict(),
        }


class TwinInferenceEngine:
    """Rule-based deterministic inference from evidence → beliefs."""

    def __init__(
        self,
        rules: tuple[InferenceRule, ...] | None = None,
        *,
        inference_version: str = INFERENCE_VERSION,
    ) -> None:
        self._rules = rules if rules is not None else default_rule_pack()
        self._inference_version = inference_version

    @property
    def inference_version(self) -> str:
        return self._inference_version

    def infer_node_belief(
        self,
        *,
        belief_id: str,
        instance_id: str,
        node_stable_id: str,
        evidence: tuple[EvidenceEvent, ...] | list[EvidenceEvent],
        as_of: datetime,
        prerequisite_mastery: dict[str, float] | None = None,
    ) -> InferenceResult:
        """Infer one node belief with a full explanation.

        Identical inputs always yield identical mastery, confidence, state,
        rationale, and explanation structure.
        """
        usable = filter_usable_evidence(evidence)
        if not usable:
            belief = EmptyBeliefFactory.unknown(
                belief_id=belief_id,
                instance_id=instance_id,
                node_stable_id=node_stable_id,
                inference_timestamp=as_of,
                inference_version=self._inference_version,
            )
            explanation = BeliefExplanation(
                belief_id=belief_id,
                supporting_evidence_ids=(),
                contributing_rules=(),
                confidence_calculation=ConfidenceCalculation(
                    raw_sum=0.0,
                    clamped=0.0,
                    formula="clamp(sum(weighted confidence deltas), 0, 1)",
                    components=("no usable evidence",),
                ),
                mastery_calculation=ConfidenceCalculation(
                    raw_sum=0.0,
                    clamped=0.0,
                    formula="clamp(sum(weighted mastery deltas), 0, 1)",
                    components=("no usable evidence",),
                ),
                inference_rationale=belief.rationale_summary,
                inference_version=self._inference_version,
                learning_state_reason="No usable evidence",
            )
            return InferenceResult(belief=belief, explanation=explanation)

        base_context = InferenceContext(
            instance_id=instance_id,
            node_stable_id=node_stable_id,
            evidence=usable,
            as_of=as_of,
            prerequisite_mastery=dict(prerequisite_mastery or {}),
            metadata={},
        )

        early_rules = [r for r in self._rules if r.rule_id != _PREREQ_RULE_ID]
        late_rules = [r for r in self._rules if r.rule_id == _PREREQ_RULE_ID]

        contributions: list[RuleContribution] = []
        for rule in early_rules:
            contributions.extend(rule.apply(base_context))

        mastery_raw, confidence_raw, absolute = _aggregate(contributions)
        # Absolute founder override replaces provisional mastery/confidence.
        if absolute is not None:
            mastery_raw, confidence_raw = absolute

        prereq_context = replace(
            base_context,
            metadata={"provisional_mastery": mastery_raw},
        )
        for rule in late_rules:
            contributions.extend(rule.apply(prereq_context))

        mastery_raw, confidence_raw, absolute = _aggregate(contributions)
        if absolute is not None:
            # Absolute still wins after prereq (founder authority), but record
            # prereq contributions for explainability.
            mastery_raw, confidence_raw = absolute

        mastery = clamp01(mastery_raw)
        confidence = clamp01(confidence_raw)
        state, state_reason = derive_learning_state(
            mastery=mastery,
            confidence=confidence,
            evidence=usable,
        )
        support = evidence_ids(usable)
        rationale = _build_rationale(
            mastery=mastery,
            confidence=confidence,
            state=state,
            contributions=contributions,
            evidence_count=len(usable),
        )

        belief = TwinBelief(
            belief_id=belief_id,
            instance_id=instance_id,
            node_stable_id=node_stable_id,
            mastery_level=mastery,
            confidence_score=confidence,
            learning_state=state,
            supporting_evidence_ids=support,
            inference_timestamp=as_of,
            inference_version=self._inference_version,
            rationale_summary=rationale,
        )
        explanation = BeliefExplanation(
            belief_id=belief_id,
            supporting_evidence_ids=support,
            contributing_rules=tuple(
                RuleContributionRecord(
                    rule_id=c.rule_id,
                    mastery_delta=c.mastery_delta,
                    confidence_delta=c.confidence_delta,
                    weight=c.weight,
                    evidence_ids=c.evidence_ids,
                    detail=c.detail,
                )
                for c in contributions
            ),
            confidence_calculation=ConfidenceCalculation(
                raw_sum=round(confidence_raw, 6),
                clamped=confidence,
                formula="clamp(sum(confidence_delta * weight), 0, 1); "
                "absolute founder override replaces sum when present",
                components=tuple(
                    f"{c.rule_id}:{c.weighted_confidence():+.4f}"
                    for c in contributions
                    if c.weighted_confidence() != 0.0
                    or c.detail.startswith(_ABSOLUTE_PREFIX)
                ),
            ),
            mastery_calculation=ConfidenceCalculation(
                raw_sum=round(mastery_raw, 6),
                clamped=mastery,
                formula="clamp(sum(mastery_delta * weight), 0, 1); "
                "absolute founder override replaces sum when present",
                components=tuple(
                    f"{c.rule_id}:{c.weighted_mastery():+.4f}"
                    for c in contributions
                    if c.weighted_mastery() != 0.0
                    or c.detail.startswith(_ABSOLUTE_PREFIX)
                ),
            ),
            inference_rationale=rationale,
            inference_version=self._inference_version,
            learning_state_reason=state_reason,
        )
        return InferenceResult(belief=belief, explanation=explanation)


def _aggregate(
    contributions: list[RuleContribution],
) -> tuple[float, float, tuple[float, float] | None]:
    mastery = 0.0
    confidence = 0.0
    absolute: tuple[float, float] | None = None
    for c in contributions:
        if c.detail.startswith(_ABSOLUTE_PREFIX):
            absolute = (c.mastery_delta, c.confidence_delta)
            continue
        mastery += c.weighted_mastery()
        confidence += c.weighted_confidence()
    return mastery, confidence, absolute


def _build_rationale(
    *,
    mastery: float,
    confidence: float,
    state: str,
    contributions: list[RuleContribution],
    evidence_count: int,
) -> str:
    rule_ids = sorted({c.rule_id for c in contributions})
    return (
        f"Inferred {state} with mastery {mastery:.4f} and confidence "
        f"{confidence:.4f} from {evidence_count} evidence event(s) via rules "
        f"[{', '.join(rule_ids)}] ({INFERENCE_VERSION})."
    )
