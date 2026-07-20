"""RecommendationReason — educational warrant for a recommendation decision.

Architecture Source
    EDUCATIONAL_LOGIC_REGISTRY.md (EL-008)
Concept
    Recommendation Reason
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.recommendation.enums import RecommendationReasonCode


@dataclass(frozen=True, slots=True)
class RecommendationReason(EducationalValueObject):
    """Single educational reason supporting a recommendation decision.

    Reasons cite *why this educational move fits*. They must not invent
    mastery claims, encode UI chrome, or invent evidence of understanding.
    """

    statement: str
    code: RecommendationReasonCode

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "statement",
            require_non_empty_text(self.statement, "statement"),
        )
        if not isinstance(self.code, RecommendationReasonCode):
            raise EducationalInvariantViolation(
                "code must be a RecommendationReasonCode",
                invariant="RecommendationReason.code.type",
            )
        if len(self.statement) < 12:
            raise EducationalInvariantViolation(
                "recommendation reason must be educationally substantive",
                invariant="RecommendationReason.statement.substantive",
            )
