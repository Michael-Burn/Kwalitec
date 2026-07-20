"""Execution constraint — educational limit on decision commitment.

Architecture Source
    EDUCATIONAL_DECISION_POINTS.md
Concept
    Execution Constraint
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.decision.enums import (
    DecisionOutcome,
    ExecutionConstraintKind,
    ReadinessBand,
    ReadinessIndicatorKind,
)
from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class ExecutionConstraintId(EducationalValueObject):
    """Identity of an execution constraint within an EducationalDecision."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "ExecutionConstraintId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class ExecutionConstraint(EducationalEntity):
    """Educational constraint that execution decisions must not contradict.

    Constraints encode Decision Points discipline (prerequisites, evidence,
    remediation, capacity, lawful deferral). They do not diagnose or create
    strategies.
    """

    constraint_id: ExecutionConstraintId
    kind: ExecutionConstraintKind
    statement: str
    related_indicator_kind: ReadinessIndicatorKind | None = None
    min_readiness: ReadinessBand | None = None
    min_confidence: ConfidenceLevel | None = None
    forbidden_outcome: DecisionOutcome | None = None

    @property
    def entity_id(self) -> ExecutionConstraintId:
        return self.constraint_id

    def _validate(self) -> None:
        if not isinstance(self.constraint_id, ExecutionConstraintId):
            raise EducationalInvariantViolation(
                "constraint_id must be an ExecutionConstraintId",
                invariant="ExecutionConstraint.constraint_id.type",
            )
        if not isinstance(self.kind, ExecutionConstraintKind):
            raise EducationalInvariantViolation(
                "kind must be an ExecutionConstraintKind",
                invariant="ExecutionConstraint.kind.type",
            )
        object.__setattr__(
            self,
            "statement",
            require_non_empty_text(self.statement, "statement"),
        )
        if self.related_indicator_kind is not None and not isinstance(
            self.related_indicator_kind, ReadinessIndicatorKind
        ):
            raise EducationalInvariantViolation(
                "related_indicator_kind must be a ReadinessIndicatorKind "
                "when provided",
                invariant="ExecutionConstraint.related_indicator_kind.type",
            )
        if self.min_readiness is not None and not isinstance(
            self.min_readiness, ReadinessBand
        ):
            raise EducationalInvariantViolation(
                "min_readiness must be a ReadinessBand when provided",
                invariant="ExecutionConstraint.min_readiness.type",
            )
        if self.min_confidence is not None and not isinstance(
            self.min_confidence, ConfidenceLevel
        ):
            raise EducationalInvariantViolation(
                "min_confidence must be a ConfidenceLevel when provided",
                invariant="ExecutionConstraint.min_confidence.type",
            )
        if self.min_confidence is ConfidenceLevel.UNKNOWN:
            raise EducationalInvariantViolation(
                "min_confidence must not be UNKNOWN",
                invariant="ExecutionConstraint.min_confidence.known",
            )
        if self.forbidden_outcome is not None and not isinstance(
            self.forbidden_outcome, DecisionOutcome
        ):
            raise EducationalInvariantViolation(
                "forbidden_outcome must be a DecisionOutcome when provided",
                invariant="ExecutionConstraint.forbidden_outcome.type",
            )
        self._assert_kind_payload()

    def _assert_kind_payload(self) -> None:
        if (
            self.kind is ExecutionConstraintKind.REQUIRE_MINIMUM_READINESS
            and self.min_readiness is None
        ):
            raise EducationalInvariantViolation(
                "REQUIRE_MINIMUM_READINESS constraint requires min_readiness",
                invariant="ExecutionConstraint.min_readiness.payload",
            )
        if (
            self.kind is ExecutionConstraintKind.REQUIRE_MINIMUM_CONFIDENCE
            and self.min_confidence is None
        ):
            raise EducationalInvariantViolation(
                "REQUIRE_MINIMUM_CONFIDENCE constraint requires min_confidence",
                invariant="ExecutionConstraint.min_confidence.payload",
            )
        if self.kind in {
            ExecutionConstraintKind.REQUIRE_INDICATOR,
            ExecutionConstraintKind.FORBID_INDICATOR,
        } and self.related_indicator_kind is None:
            raise EducationalInvariantViolation(
                f"{self.kind.value} constraint requires related_indicator_kind",
                invariant="ExecutionConstraint.indicator_payload",
            )
        if (
            self.kind is ExecutionConstraintKind.FORBID_OUTCOME
            and self.forbidden_outcome is None
        ):
            raise EducationalInvariantViolation(
                "FORBID_OUTCOME constraint requires forbidden_outcome",
                invariant="ExecutionConstraint.forbid_outcome.payload",
            )

    def constraint_signature(
        self,
    ) -> tuple[str, str | None, str | None, str | None, str | None]:
        """Structural fingerprint used to reject duplicate constraints."""
        return (
            self.kind.value,
            self.related_indicator_kind.value
            if self.related_indicator_kind
            else None,
            self.min_readiness.value if self.min_readiness else None,
            self.min_confidence.value if self.min_confidence else None,
            self.forbidden_outcome.value if self.forbidden_outcome else None,
        )
