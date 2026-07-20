"""Intention constraint — educational limit on teaching intention.

Architecture Source
    TEACHING_INTENTION_MODEL.md
Concept
    Intention Constraint
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.enums import TeachingIntentionType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.teaching_intention.enums import (
    IntentionConstraintKind,
    IntentionStrengthLevel,
)


@dataclass(frozen=True, slots=True)
class IntentionConstraintId(EducationalValueObject):
    """Identity of a constraint within a TeachingIntention."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "IntentionConstraintId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class IntentionConstraint(EducationalEntity):
    """Educational constraint that intention construction must not contradict.

    Constraints encode Teaching Intention Model governing rules (priority
    required, no mastery claim, intention precedes strategy, atomicity,
    diagnosis alignment). They do not select strategies or assemble episodes.
    """

    constraint_id: IntentionConstraintId
    kind: IntentionConstraintKind
    statement: str
    forbidden_intention_type: TeachingIntentionType | None = None
    max_strength: IntentionStrengthLevel | None = None

    @property
    def entity_id(self) -> IntentionConstraintId:
        return self.constraint_id

    def _validate(self) -> None:
        if not isinstance(self.constraint_id, IntentionConstraintId):
            raise EducationalInvariantViolation(
                "constraint_id must be an IntentionConstraintId",
                invariant="IntentionConstraint.constraint_id.type",
            )
        if not isinstance(self.kind, IntentionConstraintKind):
            raise EducationalInvariantViolation(
                "kind must be an IntentionConstraintKind",
                invariant="IntentionConstraint.kind.type",
            )
        object.__setattr__(
            self,
            "statement",
            require_non_empty_text(self.statement, "statement"),
        )
        if self.forbidden_intention_type is not None and not isinstance(
            self.forbidden_intention_type, TeachingIntentionType
        ):
            raise EducationalInvariantViolation(
                "forbidden_intention_type must be a TeachingIntentionType "
                "when provided",
                invariant="IntentionConstraint.forbidden_intention_type.type",
            )
        if self.max_strength is not None and not isinstance(
            self.max_strength, IntentionStrengthLevel
        ):
            raise EducationalInvariantViolation(
                "max_strength must be an IntentionStrengthLevel when provided",
                invariant="IntentionConstraint.max_strength.type",
            )
        self._assert_kind_payload()

    def _assert_kind_payload(self) -> None:
        if (
            self.kind is IntentionConstraintKind.CAP_STRENGTH
            and self.max_strength is None
        ):
            raise EducationalInvariantViolation(
                "CAP_STRENGTH constraint requires max_strength",
                invariant="IntentionConstraint.cap_strength.payload",
            )
        if (
            self.kind is IntentionConstraintKind.FORBID_INTENTION_TYPE
            and self.forbidden_intention_type is None
        ):
            raise EducationalInvariantViolation(
                "FORBID_INTENTION_TYPE constraint requires "
                "forbidden_intention_type",
                invariant="IntentionConstraint.forbid_type.payload",
            )

    def constraint_signature(
        self,
    ) -> tuple[str, str | None, str | None]:
        """Structural fingerprint used to reject duplicate constraints."""
        return (
            self.kind.value,
            self.forbidden_intention_type.value
            if self.forbidden_intention_type
            else None,
            self.max_strength.value if self.max_strength else None,
        )
