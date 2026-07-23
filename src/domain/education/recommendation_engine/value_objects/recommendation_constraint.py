"""Recommendation constraint — educational boundary on acting.

Architecture Source
    PROJECT_CONTEXT.md
Concept
    Recommendation Constraint
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.recommendation_engine.enums import RecommendationConstraintKind
from domain.education.recommendation_engine.ids import CompetencyId, SubjectId


@dataclass(frozen=True, slots=True)
class RecommendationConstraint(EducationalValueObject):
    """Immutable educational constraint attached to a recommendation or set.

    Constraints encode boundaries such as "do not advance until this
    prerequisite is addressed" — never UI locks or persistence rules.
    """

    kind: RecommendationConstraintKind
    subject_id: SubjectId | None = None
    competency_id: CompetencyId | None = None
    detail: float | None = None

    def _validate(self) -> None:
        if not isinstance(self.kind, RecommendationConstraintKind):
            raise EducationalInvariantViolation(
                "kind must be a RecommendationConstraintKind",
                invariant="RecommendationConstraint.kind.type",
            )
        if self.subject_id is not None and not isinstance(
            self.subject_id, SubjectId
        ):
            raise EducationalInvariantViolation(
                "subject_id must be a SubjectId when provided",
                invariant="RecommendationConstraint.subject_id.type",
            )
        if self.competency_id is not None and not isinstance(
            self.competency_id, CompetencyId
        ):
            raise EducationalInvariantViolation(
                "competency_id must be a CompetencyId when provided",
                invariant="RecommendationConstraint.competency_id.type",
            )
        if self.detail is not None:
            if isinstance(self.detail, bool) or not isinstance(
                self.detail, int | float
            ):
                raise EducationalInvariantViolation(
                    "detail must be a real number when provided",
                    invariant="RecommendationConstraint.detail.type",
                )
            object.__setattr__(self, "detail", round(float(self.detail), 4))

    def blocks_advancement(self) -> bool:
        return self.kind is RecommendationConstraintKind.BLOCK_ADVANCEMENT
