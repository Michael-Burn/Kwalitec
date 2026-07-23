"""Recommendation explanation — bundled structured reasoning.

Architecture Source
    PROJECT_CONTEXT.md
Concept
    Recommendation Explanation
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.recommendation_engine.enums import RecommendationReasonCode
from domain.education.recommendation_engine.value_objects.recommendation_reason import (
    RecommendationReason,
)


@dataclass(frozen=True, slots=True)
class RecommendationExplanation(EducationalValueObject):
    """Immutable bundle of structured reasons explaining a recommendation.

    Explanations never contain natural language prose — only machine-
    readable reason codes and optional primary code for quick narration.
    """

    reasons: tuple[RecommendationReason, ...]
    primary_reason_code: RecommendationReasonCode

    def _validate(self) -> None:
        object.__setattr__(self, "reasons", tuple(self.reasons))
        if not self.reasons:
            raise EducationalInvariantViolation(
                "explanation must contain at least one reason",
                invariant="RecommendationExplanation.reasons.required",
            )
        for reason in self.reasons:
            if not isinstance(reason, RecommendationReason):
                raise EducationalInvariantViolation(
                    "reasons must contain RecommendationReason value objects",
                    invariant="RecommendationExplanation.reasons.type",
                )
        if not isinstance(self.primary_reason_code, RecommendationReasonCode):
            raise EducationalInvariantViolation(
                "primary_reason_code must be a RecommendationReasonCode",
                invariant="RecommendationExplanation.primary_reason_code.type",
            )
        if self.primary_reason_code not in {
            reason.reason_code for reason in self.reasons
        }:
            raise EducationalInvariantViolation(
                "primary_reason_code must appear among reasons",
                invariant="RecommendationExplanation.primary_reason_code.member",
            )

    @classmethod
    def from_reasons(
        cls,
        reasons: list[RecommendationReason] | tuple[RecommendationReason, ...],
    ) -> RecommendationExplanation:
        items = tuple(reasons)
        if not items:
            raise EducationalInvariantViolation(
                "explanation must contain at least one reason",
                invariant="RecommendationExplanation.reasons.required",
            )
        return cls(reasons=items, primary_reason_code=items[0].reason_code)
