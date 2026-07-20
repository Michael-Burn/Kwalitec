"""Priority constraint — educational limit on instructional ordering.

Architecture Source
    EDUCATIONAL_PRIORITY_MODEL.md
Concept
    Priority Constraint
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.priority.enums import (
    PriorityConstraintKind,
    PriorityFactorKind,
    PriorityScoreBand,
    UrgencyLevel,
)


@dataclass(frozen=True, slots=True)
class PriorityConstraintId(EducationalValueObject):
    """Identity of a priority constraint within an EducationalPriority."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "PriorityConstraintId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class PriorityConstraint(EducationalEntity):
    """Educational constraint that priority ordering must not contradict.

    Constraints encode Priority Model principles (prerequisites before
    extension, misconceptions before practice, durable learning over theatre,
    exam readiness without conceptual abandonment). They do not diagnose or
    select teaching strategies.
    """

    constraint_id: PriorityConstraintId
    kind: PriorityConstraintKind
    statement: str
    related_factor_kind: PriorityFactorKind | None = None
    max_urgency: UrgencyLevel | None = None
    max_score_band: PriorityScoreBand | None = None

    @property
    def entity_id(self) -> PriorityConstraintId:
        return self.constraint_id

    def _validate(self) -> None:
        if not isinstance(self.constraint_id, PriorityConstraintId):
            raise EducationalInvariantViolation(
                "constraint_id must be a PriorityConstraintId",
                invariant="PriorityConstraint.constraint_id.type",
            )
        if not isinstance(self.kind, PriorityConstraintKind):
            raise EducationalInvariantViolation(
                "kind must be a PriorityConstraintKind",
                invariant="PriorityConstraint.kind.type",
            )
        object.__setattr__(
            self,
            "statement",
            require_non_empty_text(self.statement, "statement"),
        )
        if self.related_factor_kind is not None and not isinstance(
            self.related_factor_kind, PriorityFactorKind
        ):
            raise EducationalInvariantViolation(
                "related_factor_kind must be a PriorityFactorKind when provided",
                invariant="PriorityConstraint.related_factor_kind.type",
            )
        if self.max_urgency is not None and not isinstance(
            self.max_urgency, UrgencyLevel
        ):
            raise EducationalInvariantViolation(
                "max_urgency must be an UrgencyLevel when provided",
                invariant="PriorityConstraint.max_urgency.type",
            )
        if self.max_score_band is not None and not isinstance(
            self.max_score_band, PriorityScoreBand
        ):
            raise EducationalInvariantViolation(
                "max_score_band must be a PriorityScoreBand when provided",
                invariant="PriorityConstraint.max_score_band.type",
            )
        self._assert_kind_payload()

    def _assert_kind_payload(self) -> None:
        if self.kind is PriorityConstraintKind.CAP_URGENCY and self.max_urgency is None:
            raise EducationalInvariantViolation(
                "CAP_URGENCY constraint requires max_urgency",
                invariant="PriorityConstraint.cap_urgency.payload",
            )
        if (
            self.kind is PriorityConstraintKind.CAP_SCORE
            and self.max_score_band is None
        ):
            raise EducationalInvariantViolation(
                "CAP_SCORE constraint requires max_score_band",
                invariant="PriorityConstraint.cap_score.payload",
            )
        if self.kind in {
            PriorityConstraintKind.REQUIRE_FACTOR,
            PriorityConstraintKind.FORBID_FACTOR,
        } and self.related_factor_kind is None:
            raise EducationalInvariantViolation(
                f"{self.kind.value} constraint requires related_factor_kind",
                invariant="PriorityConstraint.factor_payload",
            )

    def constraint_signature(self) -> tuple[str, str | None, str | None, str | None]:
        """Structural fingerprint used to reject duplicate constraints."""
        return (
            self.kind.value,
            self.related_factor_kind.value if self.related_factor_kind else None,
            self.max_urgency.value if self.max_urgency else None,
            self.max_score_band.value if self.max_score_band else None,
        )
