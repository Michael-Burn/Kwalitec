"""Readiness indicator — supporting signal for execution readiness.

Architecture Source
    EDUCATIONAL_DECISION_POINTS.md
Concept
    Readiness Indicator
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.decision.enums import ReadinessIndicatorKind
from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class ReadinessIndicatorId(EducationalValueObject):
    """Identity of a readiness indicator within an EducationalDecision."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "ReadinessIndicatorId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class ReadinessIndicator(EducationalEntity):
    """Supporting educational signal that warrants a readiness posture.

    Indicators describe execution fitness. They never name diagnoses, create
    strategies, or orchestrate sessions.
    """

    indicator_id: ReadinessIndicatorId
    kind: ReadinessIndicatorKind
    description: str
    supports_readiness: bool = True
    weight: float = 1.0

    @property
    def entity_id(self) -> ReadinessIndicatorId:
        return self.indicator_id

    def _validate(self) -> None:
        if not isinstance(self.indicator_id, ReadinessIndicatorId):
            raise EducationalInvariantViolation(
                "indicator_id must be a ReadinessIndicatorId",
                invariant="ReadinessIndicator.indicator_id.type",
            )
        if not isinstance(self.kind, ReadinessIndicatorKind):
            raise EducationalInvariantViolation(
                "kind must be a ReadinessIndicatorKind",
                invariant="ReadinessIndicator.kind.type",
            )
        object.__setattr__(
            self,
            "description",
            require_non_empty_text(self.description, "description"),
        )
        if not isinstance(self.supports_readiness, bool):
            raise EducationalInvariantViolation(
                "supports_readiness must be a bool",
                invariant="ReadinessIndicator.supports_readiness.type",
            )
        if isinstance(self.weight, bool) or not isinstance(self.weight, int | float):
            raise EducationalInvariantViolation(
                "weight must be a real number",
                invariant="ReadinessIndicator.weight.type",
            )
        if self.weight <= 0.0 or self.weight > 1.0:
            raise EducationalInvariantViolation(
                "weight must be in (0.0, 1.0]",
                invariant="ReadinessIndicator.weight.range",
            )
        object.__setattr__(self, "weight", float(self.weight))
        self._assert_kind_polarity()

    def _assert_kind_polarity(self) -> None:
        blocking = {
            ReadinessIndicatorKind.PREREQUISITE_MISSING,
            ReadinessIndicatorKind.EVIDENCE_INSUFFICIENT,
            ReadinessIndicatorKind.CAPACITY_INSUFFICIENT,
            ReadinessIndicatorKind.REMEDIATION_REQUIRED,
            ReadinessIndicatorKind.AFFECTIVE_BLOCK,
            ReadinessIndicatorKind.SESSION_CONSTRAINT,
            ReadinessIndicatorKind.CONFLICTING_SIGNAL,
        }
        supporting = {
            ReadinessIndicatorKind.PREREQUISITE_SATISFIED,
            ReadinessIndicatorKind.EVIDENCE_SUFFICIENT,
            ReadinessIndicatorKind.CAPACITY_ADEQUATE,
            ReadinessIndicatorKind.INTENTION_ALIGNED,
            ReadinessIndicatorKind.STRATEGY_APPLICABLE,
        }
        if self.kind in blocking and self.supports_readiness:
            raise EducationalInvariantViolation(
                f"{self.kind.value} indicator cannot support readiness",
                invariant="ReadinessIndicator.kind.blocking_polarity",
            )
        if self.kind in supporting and not self.supports_readiness:
            raise EducationalInvariantViolation(
                f"{self.kind.value} indicator must support readiness",
                invariant="ReadinessIndicator.kind.supporting_polarity",
            )

    def is_blocking(self) -> bool:
        return not self.supports_readiness

    def indicator_signature(self) -> tuple[str, bool]:
        """Structural fingerprint used to reject duplicate indicators."""
        return (self.kind.value, self.supports_readiness)
