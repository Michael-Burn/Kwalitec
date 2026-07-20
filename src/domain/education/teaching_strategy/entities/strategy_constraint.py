"""Strategy constraint — educational limit on teaching strategy.

Architecture Source
    STRATEGY_INVARIANTS.md
Concept
    Strategy Constraint
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.enums import TeachingStrategyType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.teaching_strategy.enums import (
    ComplexityLevel,
    StrategyConstraintKind,
)


@dataclass(frozen=True, slots=True)
class StrategyConstraintId(EducationalValueObject):
    """Identity of a constraint within a TeachingStrategy."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "StrategyConstraintId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class StrategyConstraint(EducationalEntity):
    """Educational constraint that strategy construction must not contradict.

    Constraints encode Strategy Invariants (intention required, one primary,
    no mastery claim, misconception duty, composition integrity). They do
    not execute episodes or select prompts.
    """

    constraint_id: StrategyConstraintId
    kind: StrategyConstraintKind
    statement: str
    forbidden_strategy_type: TeachingStrategyType | None = None
    max_complexity: ComplexityLevel | None = None

    @property
    def entity_id(self) -> StrategyConstraintId:
        return self.constraint_id

    def _validate(self) -> None:
        if not isinstance(self.constraint_id, StrategyConstraintId):
            raise EducationalInvariantViolation(
                "constraint_id must be a StrategyConstraintId",
                invariant="StrategyConstraint.constraint_id.type",
            )
        if not isinstance(self.kind, StrategyConstraintKind):
            raise EducationalInvariantViolation(
                "kind must be a StrategyConstraintKind",
                invariant="StrategyConstraint.kind.type",
            )
        object.__setattr__(
            self,
            "statement",
            require_non_empty_text(self.statement, "statement"),
        )
        if self.forbidden_strategy_type is not None and not isinstance(
            self.forbidden_strategy_type, TeachingStrategyType
        ):
            raise EducationalInvariantViolation(
                "forbidden_strategy_type must be a TeachingStrategyType "
                "when provided",
                invariant="StrategyConstraint.forbidden_strategy_type.type",
            )
        if self.max_complexity is not None and not isinstance(
            self.max_complexity, ComplexityLevel
        ):
            raise EducationalInvariantViolation(
                "max_complexity must be a ComplexityLevel when provided",
                invariant="StrategyConstraint.max_complexity.type",
            )
        self._assert_kind_payload()

    def _assert_kind_payload(self) -> None:
        if (
            self.kind is StrategyConstraintKind.CAP_COMPLEXITY
            and self.max_complexity is None
        ):
            raise EducationalInvariantViolation(
                "CAP_COMPLEXITY constraint requires max_complexity",
                invariant="StrategyConstraint.cap_complexity.payload",
            )
        if (
            self.kind is StrategyConstraintKind.FORBID_STRATEGY_TYPE
            and self.forbidden_strategy_type is None
        ):
            raise EducationalInvariantViolation(
                "FORBID_STRATEGY_TYPE constraint requires "
                "forbidden_strategy_type",
                invariant="StrategyConstraint.forbid_type.payload",
            )

    def constraint_signature(
        self,
    ) -> tuple[str, str | None, str | None]:
        """Structural fingerprint used to reject duplicate constraints."""
        return (
            self.kind.value,
            self.forbidden_strategy_type.value
            if self.forbidden_strategy_type
            else None,
            self.max_complexity.value if self.max_complexity else None,
        )
