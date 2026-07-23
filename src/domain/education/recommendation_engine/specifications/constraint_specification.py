"""Specification: recommendation constraints are well-formed.

Architecture Source
    PROJECT_CONTEXT.md
Concept
    Constraint Specification
"""

from __future__ import annotations

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.recommendation_engine.enums import RecommendationConstraintKind
from domain.education.recommendation_engine.value_objects.recommendation_constraint import (  # noqa: E501
    RecommendationConstraint,
)


class ConstraintSpecification:
    """A constraint must carry enough scope for its kind."""

    @staticmethod
    def is_satisfied_by(constraint: RecommendationConstraint) -> bool:
        if not isinstance(constraint, RecommendationConstraint):
            return False
        if constraint.kind is RecommendationConstraintKind.REQUIRE_PREREQUISITE:
            return constraint.competency_id is not None
        if constraint.kind is RecommendationConstraintKind.BLOCK_ADVANCEMENT:
            return (
                constraint.competency_id is not None
                or constraint.subject_id is not None
            )
        if constraint.kind is RecommendationConstraintKind.DEFER_CHECKPOINT:
            return constraint.competency_id is not None
        return True

    @staticmethod
    def assert_satisfied_by(constraint: RecommendationConstraint) -> None:
        if not ConstraintSpecification.is_satisfied_by(constraint):
            raise EducationalInvariantViolation(
                "constraint must carry scope appropriate to its kind",
                invariant="ConstraintSpecification.well_formed",
            )
