"""Recommendation target — curriculum / mission scope of a recommendation.

Architecture Source
    PROJECT_CONTEXT.md
Concept
    Recommendation Target
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.recommendation_engine.ids import CompetencyId, SubjectId


@dataclass(frozen=True, slots=True)
class RecommendationTarget(EducationalValueObject):
    """Immutable educational scope a recommendation addresses.

    At least one scoping identity must be present. Mission and checkpoint
    references are opaque string tokens correlated with student-state
    references — never owned as foreign Python types.
    """

    subject_id: SubjectId | None = None
    competency_id: CompetencyId | None = None
    mission_id: str | None = None
    checkpoint_id: str | None = None

    def _validate(self) -> None:
        if self.subject_id is not None and not isinstance(
            self.subject_id, SubjectId
        ):
            raise EducationalInvariantViolation(
                "subject_id must be a SubjectId when provided",
                invariant="RecommendationTarget.subject_id.type",
            )
        if self.competency_id is not None and not isinstance(
            self.competency_id, CompetencyId
        ):
            raise EducationalInvariantViolation(
                "competency_id must be a CompetencyId when provided",
                invariant="RecommendationTarget.competency_id.type",
            )
        if self.mission_id is not None:
            if not isinstance(self.mission_id, str) or not self.mission_id.strip():
                raise EducationalInvariantViolation(
                    "mission_id must be a non-empty string when provided",
                    invariant="RecommendationTarget.mission_id.required",
                )
            object.__setattr__(self, "mission_id", self.mission_id.strip())
        if self.checkpoint_id is not None:
            if (
                not isinstance(self.checkpoint_id, str)
                or not self.checkpoint_id.strip()
            ):
                raise EducationalInvariantViolation(
                    "checkpoint_id must be a non-empty string when provided",
                    invariant="RecommendationTarget.checkpoint_id.required",
                )
            object.__setattr__(self, "checkpoint_id", self.checkpoint_id.strip())
        if not self.has_scope():
            raise EducationalInvariantViolation(
                "recommendation target must scope at least one identity",
                invariant="RecommendationTarget.scope.required",
            )

    def has_scope(self) -> bool:
        return any(
            (
                self.subject_id is not None,
                self.competency_id is not None,
                self.mission_id is not None,
                self.checkpoint_id is not None,
            )
        )

    def correlation_key(self) -> str:
        """Stable, deterministic key used for ordering and identity derivation."""
        parts = [
            self.subject_id.value if self.subject_id is not None else "-",
            self.competency_id.value if self.competency_id is not None else "-",
            self.mission_id or "-",
            self.checkpoint_id or "-",
        ]
        return ":".join(parts)
