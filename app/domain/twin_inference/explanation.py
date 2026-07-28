"""Explainability layer for Twin beliefs (EI-006).

No belief may exist without an explanation that cites evidence, rules,
confidence calculation, rationale, and inference version.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RuleContributionRecord:
    """One rule's contribution to a belief, for audit and explanation."""

    rule_id: str
    mastery_delta: float
    confidence_delta: float
    weight: float
    evidence_ids: tuple[str, ...] = ()
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "mastery_delta": self.mastery_delta,
            "confidence_delta": self.confidence_delta,
            "weight": self.weight,
            "evidence_ids": list(self.evidence_ids),
            "detail": self.detail,
        }


@dataclass(frozen=True)
class ConfidenceCalculation:
    """Deterministic confidence arithmetic exposed for explainability."""

    raw_sum: float
    clamped: float
    formula: str
    components: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "raw_sum": self.raw_sum,
            "clamped": self.clamped,
            "formula": self.formula,
            "components": list(self.components),
        }


@dataclass(frozen=True)
class BeliefExplanation:
    """Complete explanation bound to one Twin belief.

    Supporting evidence is referenced by id only — payloads stay in EI-005.
    """

    belief_id: str
    supporting_evidence_ids: tuple[str, ...]
    contributing_rules: tuple[RuleContributionRecord, ...]
    confidence_calculation: ConfidenceCalculation
    inference_rationale: str
    inference_version: str
    mastery_calculation: ConfidenceCalculation | None = None
    learning_state_reason: str = ""

    def __post_init__(self) -> None:
        if not (self.inference_rationale or "").strip():
            raise ValueError("inference_rationale is required")
        if not (self.inference_version or "").strip():
            raise ValueError("inference_version is required")

    def to_dict(self) -> dict[str, Any]:
        return {
            "belief_id": self.belief_id,
            "supporting_evidence_ids": list(self.supporting_evidence_ids),
            "contributing_rules": [r.to_dict() for r in self.contributing_rules],
            "confidence_calculation": self.confidence_calculation.to_dict(),
            "mastery_calculation": (
                self.mastery_calculation.to_dict()
                if self.mastery_calculation is not None
                else None
            ),
            "inference_rationale": self.inference_rationale,
            "inference_version": self.inference_version,
            "learning_state_reason": self.learning_state_reason,
        }
