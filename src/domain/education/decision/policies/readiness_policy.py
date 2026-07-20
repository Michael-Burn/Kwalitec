"""Policy assessing readiness from indicators for execution decisions.

Architecture Source
    EDUCATIONAL_DECISION_POINTS.md
Concept
    Readiness Policy
"""

from __future__ import annotations

from domain.education.decision.entities.readiness_indicator import ReadinessIndicator
from domain.education.decision.enums import ReadinessBand, ReadinessIndicatorKind
from domain.education.decision.value_objects.readiness_level import ReadinessLevel
from domain.education.foundation.errors import EducationalInvariantViolation

_HARD_BLOCKS = frozenset(
    {
        ReadinessIndicatorKind.PREREQUISITE_MISSING,
        ReadinessIndicatorKind.REMEDIATION_REQUIRED,
        ReadinessIndicatorKind.AFFECTIVE_BLOCK,
        ReadinessIndicatorKind.SESSION_CONSTRAINT,
    }
)

_SOFT_BLOCKS = frozenset(
    {
        ReadinessIndicatorKind.EVIDENCE_INSUFFICIENT,
        ReadinessIndicatorKind.CAPACITY_INSUFFICIENT,
        ReadinessIndicatorKind.CONFLICTING_SIGNAL,
    }
)

_SUPPORTING = frozenset(
    {
        ReadinessIndicatorKind.PREREQUISITE_SATISFIED,
        ReadinessIndicatorKind.EVIDENCE_SUFFICIENT,
        ReadinessIndicatorKind.CAPACITY_ADEQUATE,
        ReadinessIndicatorKind.INTENTION_ALIGNED,
        ReadinessIndicatorKind.STRATEGY_APPLICABLE,
    }
)


class ReadinessPolicy:
    """Derives and validates readiness posture from readiness indicators."""

    @classmethod
    def assess(
        cls,
        indicators: tuple[ReadinessIndicator, ...] | list[ReadinessIndicator],
        *,
        rationale: str | None = None,
    ) -> ReadinessLevel:
        """Compute readiness band from indicator polarity and weight."""
        collected = tuple(indicators)
        if not collected:
            raise EducationalInvariantViolation(
                "readiness assessment requires at least one readiness indicator",
                invariant="ReadinessPolicy.assess.indicators.min_one",
            )

        hard_block_weight = sum(
            indicator.weight
            for indicator in collected
            if indicator.kind in _HARD_BLOCKS
        )
        if hard_block_weight > 0.0:
            return ReadinessLevel.of(
                ReadinessBand.BLOCKED,
                ratio=min(1.0, hard_block_weight),
                rationale=rationale or "hard blocking readiness indicators present",
            )

        soft_block_weight = sum(
            indicator.weight
            for indicator in collected
            if indicator.kind in _SOFT_BLOCKS or indicator.is_blocking()
        )
        support_weight = sum(
            indicator.weight
            for indicator in collected
            if indicator.kind in _SUPPORTING and indicator.supports_readiness
        )
        total = support_weight + soft_block_weight
        ratio = support_weight / total if total > 0.0 else 0.0

        if soft_block_weight > 0.0 and support_weight <= soft_block_weight:
            return ReadinessLevel.of(
                ReadinessBand.NOT_READY,
                ratio=ratio,
                rationale=rationale or "blocking signals outweigh supporting readiness",
            )
        if soft_block_weight > 0.0 or support_weight < 1.5:
            return ReadinessLevel.of(
                ReadinessBand.PARTIALLY_READY,
                ratio=ratio,
                rationale=rationale or "partial readiness with residual blockers",
            )
        return ReadinessLevel.of(
            ReadinessBand.READY,
            ratio=min(1.0, ratio),
            rationale=rationale or "supporting readiness indicators dominate",
        )

    @classmethod
    def assert_permits_approval(cls, readiness: ReadinessLevel) -> None:
        if not isinstance(readiness, ReadinessLevel):
            raise EducationalInvariantViolation(
                "decision must possess readiness",
                invariant="ReadinessPolicy.approval.readiness.required",
            )
        if not readiness.permits_approval():
            raise EducationalInvariantViolation(
                "cannot approve intervention that is not READY",
                invariant="ReadinessPolicy.approval.readiness.ready",
            )

    @classmethod
    def assert_consistent_with_indicators(
        cls,
        readiness: ReadinessLevel,
        indicators: tuple[ReadinessIndicator, ...] | list[ReadinessIndicator],
    ) -> None:
        """Reject readiness that contradicts hard-blocking indicators."""
        if not isinstance(readiness, ReadinessLevel):
            raise EducationalInvariantViolation(
                "decision must possess readiness",
                invariant="ReadinessPolicy.consistency.readiness.required",
            )
        collected = tuple(indicators)
        has_hard_block = any(indicator.kind in _HARD_BLOCKS for indicator in collected)
        if has_hard_block and readiness.band is ReadinessBand.READY:
            raise EducationalInvariantViolation(
                "READY readiness contradicts hard-blocking indicators",
                invariant="ReadinessPolicy.consistency.ready_vs_block",
            )
        if (
            readiness.band is ReadinessBand.BLOCKED
            and not has_hard_block
            and not any(indicator.is_blocking() for indicator in collected)
        ):
            raise EducationalInvariantViolation(
                "BLOCKED readiness requires at least one blocking indicator",
                invariant="ReadinessPolicy.consistency.blocked_requires_indicator",
            )

    @classmethod
    def suggested_deferral_outcome(
        cls,
        indicators: tuple[ReadinessIndicator, ...] | list[ReadinessIndicator],
    ) -> str:
        """Suggest a non-teach outcome kind from dominant blocking indicators."""
        kinds = {indicator.kind for indicator in indicators}
        if ReadinessIndicatorKind.REMEDIATION_REQUIRED in kinds:
            return "require_remediation"
        if ReadinessIndicatorKind.PREREQUISITE_MISSING in kinds:
            return "require_prerequisite_work"
        if ReadinessIndicatorKind.EVIDENCE_INSUFFICIENT in kinds:
            return "require_additional_evidence"
        if ReadinessIndicatorKind.CONFLICTING_SIGNAL in kinds:
            return "require_additional_evidence"
        return "delay"
