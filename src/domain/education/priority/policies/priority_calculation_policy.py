"""Policy calculating instructional ordering from priority factors.

Architecture Source
    EDUCATIONAL_PRIORITY_MODEL.md
Concept
    Priority Calculation Policy
"""

from __future__ import annotations

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.priority.entities.priority_factor import PriorityFactor
from domain.education.priority.enums import (
    InstructionalImpactLevel,
    PriorityFactorKind,
    PriorityScoreBand,
    UrgencyLevel,
)
from domain.education.priority.value_objects.instructional_impact import (
    InstructionalImpact,
)
from domain.education.priority.value_objects.priority_score import PriorityScore
from domain.education.priority.value_objects.urgency import Urgency

# Gate affinity from Educational Priority Model §4 (lower gate → higher order).
_FACTOR_GATE: dict[PriorityFactorKind, int] = {
    PriorityFactorKind.PREREQUISITE_IMPORTANCE: 1,
    PriorityFactorKind.LEARNING_DEPENDENCY_DEPTH: 1,
    PriorityFactorKind.MISCONCEPTION_PERSISTENCE: 2,
    PriorityFactorKind.CONFIDENCE_IN_DIAGNOSIS: 3,
    PriorityFactorKind.CONCEPT_CENTRALITY: 4,
    PriorityFactorKind.EDUCATIONAL_LEVERAGE: 4,
    PriorityFactorKind.TRANSFER_BLOCKING: 7,
    PriorityFactorKind.EXAM_RELEVANCE: 8,
}

_SCORE_BANDS: tuple[PriorityScoreBand, ...] = (
    PriorityScoreBand.NEGLIGIBLE,
    PriorityScoreBand.LOW,
    PriorityScoreBand.MEDIUM,
    PriorityScoreBand.HIGH,
    PriorityScoreBand.CRITICAL,
)

_URGENCY_LEVELS: tuple[UrgencyLevel, ...] = (
    UrgencyLevel.DEFERRED,
    UrgencyLevel.ROUTINE,
    UrgencyLevel.ELEVATED,
    UrgencyLevel.IMMEDIATE,
    UrgencyLevel.CRITICAL,
)

_IMPACT_LEVELS: tuple[InstructionalImpactLevel, ...] = (
    InstructionalImpactLevel.MARGINAL,
    InstructionalImpactLevel.MATERIAL,
    InstructionalImpactLevel.SUBSTANTIAL,
    InstructionalImpactLevel.TRANSFORMATIONAL,
)


class PriorityCalculationPolicy:
    """Deterministic calculation of score, urgency, and instructional impact.

    Calculation is educational governance, not a black-box ranking engine.
    Gate affinity from the Priority Model modulates factor contributions so
    prerequisites and misconceptions outrank exam technique and extension.
    """

    @staticmethod
    def gate_for(kind: PriorityFactorKind) -> int:
        if kind not in _FACTOR_GATE:
            raise EducationalInvariantViolation(
                f"unknown priority factor kind {kind!r}",
                invariant="PriorityCalculationPolicy.gate.known",
            )
        return _FACTOR_GATE[kind]

    @staticmethod
    def factor_ordering_weight(factor: PriorityFactor) -> float:
        """Map a factor to an ordering weight in (0, 1].

        Lower gates yield higher base weight; contribution scales intensity.
        """
        if not isinstance(factor, PriorityFactor):
            raise EducationalInvariantViolation(
                "factor must be a PriorityFactor",
                invariant="PriorityCalculationPolicy.factor.type",
            )
        gate = PriorityCalculationPolicy.gate_for(factor.kind)
        # Gates 1..10 → base in [1.0 .. ~0.1]
        gate_base = max(0.1, 1.0 - ((gate - 1) * 0.1))
        return round(gate_base * factor.contribution, 6)

    @staticmethod
    def aggregate_ratio(
        factors: tuple[PriorityFactor, ...] | list[PriorityFactor],
    ) -> float:
        if not factors:
            raise EducationalInvariantViolation(
                "cannot calculate priority without factors",
                invariant="PriorityCalculationPolicy.factors.min_one",
            )
        weights = [
            PriorityCalculationPolicy.factor_ordering_weight(factor)
            for factor in factors
        ]
        # Emphasise the strongest (lowest-gate / highest-weight) factor.
        peak = max(weights)
        mean = sum(weights) / len(weights)
        return round(min(1.0, (0.65 * peak) + (0.35 * mean)), 6)

    @staticmethod
    def band_for_ratio(ratio: float) -> PriorityScoreBand:
        if ratio < 0.0 or ratio > 1.0:
            raise EducationalInvariantViolation(
                "ratio must be between 0.0 and 1.0 inclusive",
                invariant="PriorityCalculationPolicy.ratio.range",
            )
        if ratio < 0.15:
            return PriorityScoreBand.NEGLIGIBLE
        if ratio < 0.35:
            return PriorityScoreBand.LOW
        if ratio < 0.55:
            return PriorityScoreBand.MEDIUM
        if ratio < 0.75:
            return PriorityScoreBand.HIGH
        return PriorityScoreBand.CRITICAL

    @staticmethod
    def urgency_for_ratio(
        ratio: float,
        factors: tuple[PriorityFactor, ...] | list[PriorityFactor],
    ) -> UrgencyLevel:
        has_exam = any(
            factor.kind is PriorityFactorKind.EXAM_RELEVANCE for factor in factors
        )
        has_blocking = any(
            factor.kind
            in {
                PriorityFactorKind.PREREQUISITE_IMPORTANCE,
                PriorityFactorKind.MISCONCEPTION_PERSISTENCE,
                PriorityFactorKind.LEARNING_DEPENDENCY_DEPTH,
            }
            for factor in factors
        )
        if ratio >= 0.75 and (has_blocking or has_exam):
            return UrgencyLevel.CRITICAL
        if ratio >= 0.75:
            return UrgencyLevel.IMMEDIATE
        if ratio >= 0.55:
            return UrgencyLevel.IMMEDIATE if has_blocking else UrgencyLevel.ELEVATED
        if ratio >= 0.35:
            return UrgencyLevel.ELEVATED if has_exam else UrgencyLevel.ROUTINE
        if ratio >= 0.15:
            return UrgencyLevel.ROUTINE
        return UrgencyLevel.DEFERRED

    @staticmethod
    def impact_for_ratio(
        ratio: float,
        factors: tuple[PriorityFactor, ...] | list[PriorityFactor],
    ) -> InstructionalImpactLevel:
        kinds = {factor.kind for factor in factors}
        if ratio >= 0.75 or PriorityFactorKind.PREREQUISITE_IMPORTANCE in kinds:
            if PriorityFactorKind.MISCONCEPTION_PERSISTENCE in kinds:
                return InstructionalImpactLevel.TRANSFORMATIONAL
            return InstructionalImpactLevel.SUBSTANTIAL
        if ratio >= 0.55:
            return InstructionalImpactLevel.SUBSTANTIAL
        if ratio >= 0.35:
            return InstructionalImpactLevel.MATERIAL
        return InstructionalImpactLevel.MARGINAL

    @staticmethod
    def impact_statement(
        factors: tuple[PriorityFactor, ...] | list[PriorityFactor],
        level: InstructionalImpactLevel,
    ) -> str:
        kinds = sorted(factor.kind.value for factor in factors)
        lead = kinds[0] if kinds else "educational_need"
        return (
            f"Addressing this priority first yields {level.value} instructional "
            f"consequence driven by {lead}"
        )

    @classmethod
    def calculate(
        cls,
        factors: tuple[PriorityFactor, ...] | list[PriorityFactor],
        *,
        rationale: str | None = None,
    ) -> tuple[PriorityScore, Urgency, InstructionalImpact]:
        """Compute score, urgency, and impact from priority factors."""
        collected = tuple(factors)
        if not collected:
            raise EducationalInvariantViolation(
                "cannot calculate priority without factors",
                invariant="PriorityCalculationPolicy.calculate.factors",
            )
        for factor in collected:
            if not isinstance(factor, PriorityFactor):
                raise EducationalInvariantViolation(
                    "factors must be PriorityFactor entities",
                    invariant="PriorityCalculationPolicy.calculate.type",
                )

        ratio = cls.aggregate_ratio(collected)
        band = cls.band_for_ratio(ratio)
        score = PriorityScore.of(
            band,
            ratio=ratio,
            rationale=rationale
            or "calculated from educational priority factors and gate affinity",
        )
        urgency = Urgency.of(
            cls.urgency_for_ratio(ratio, collected),
            rationale="derived from factor intensity and gate pressure",
        )
        impact_level = cls.impact_for_ratio(ratio, collected)
        impact = InstructionalImpact.of(
            impact_level,
            cls.impact_statement(collected, impact_level),
        )
        return score, urgency, impact

    @staticmethod
    def promote(
        score: PriorityScore,
        urgency: Urgency,
    ) -> tuple[PriorityScore, Urgency]:
        """Raise instructional ordering by one score band and urgency step."""
        if not isinstance(score, PriorityScore):
            raise EducationalInvariantViolation(
                "score must be a PriorityScore",
                invariant="PriorityCalculationPolicy.promote.score",
            )
        if not isinstance(urgency, Urgency):
            raise EducationalInvariantViolation(
                "urgency must be an Urgency",
                invariant="PriorityCalculationPolicy.promote.urgency",
            )
        next_score = score.promoted()
        try:
            next_urgency = urgency.elevated()
        except EducationalInvariantViolation:
            next_urgency = urgency
        return next_score, next_urgency

    @staticmethod
    def demote(
        score: PriorityScore,
        urgency: Urgency,
    ) -> tuple[PriorityScore, Urgency]:
        """Lower instructional ordering by one score band and urgency step."""
        if not isinstance(score, PriorityScore):
            raise EducationalInvariantViolation(
                "score must be a PriorityScore",
                invariant="PriorityCalculationPolicy.demote.score",
            )
        if not isinstance(urgency, Urgency):
            raise EducationalInvariantViolation(
                "urgency must be an Urgency",
                invariant="PriorityCalculationPolicy.demote.urgency",
            )
        next_score = score.demoted()
        try:
            next_urgency = urgency.deferred()
        except EducationalInvariantViolation:
            next_urgency = urgency
        return next_score, next_urgency

    @staticmethod
    def score_order() -> tuple[PriorityScoreBand, ...]:
        return _SCORE_BANDS

    @staticmethod
    def urgency_order() -> tuple[UrgencyLevel, ...]:
        return _URGENCY_LEVELS

    @staticmethod
    def impact_order() -> tuple[InstructionalImpactLevel, ...]:
        return _IMPACT_LEVELS
