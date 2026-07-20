"""Recommendation — one deterministic educational decision projection.

Architecture Source
    EDUCATIONAL_LOGIC_REGISTRY.md (EL-008)
    EDUCATIONAL_PRIORITY_MODEL.md
Concept
    Recommendation
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.recommendation.enums import (
    RecommendationCategory,
    SupportingEvidenceCode,
)
from domain.recommendation.ids import RecommendationId
from domain.recommendation.recommendation_priority import RecommendationPriority
from domain.recommendation.recommendation_reason import RecommendationReason


@dataclass(frozen=True, slots=True)
class SupportingEvidence(EducationalValueObject):
    """Immutable citation of Educational OS state supporting a recommendation.

    Supporting evidence cites lawful educational state (diagnosis, progress,
    priority, strategy, mission, plan, twin). It is not Educational Evidence
    of understanding and must not be treated as mastery observation.
    """

    code: SupportingEvidenceCode
    statement: str
    source_id: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.code, SupportingEvidenceCode):
            raise EducationalInvariantViolation(
                "code must be a SupportingEvidenceCode",
                invariant="SupportingEvidence.code.type",
            )
        object.__setattr__(
            self,
            "statement",
            require_non_empty_text(self.statement, "statement"),
        )
        if self.source_id is not None:
            object.__setattr__(
                self,
                "source_id",
                require_non_empty_text(self.source_id, "source_id"),
            )


@dataclass(frozen=True, slots=True)
class RecommendationConfidence(EducationalValueObject):
    """Certainty that this educational recommendation fits the observed state.

    Confidence describes how well Educational OS signals agree on the move.
    It is not twin mastery confidence and not a UI trust badge.
    """

    level: ConfidenceLevel
    ratio: float | None = None
    millipoints: int | None = None

    def _validate(self) -> None:
        if not isinstance(self.level, ConfidenceLevel):
            raise EducationalInvariantViolation(
                "level must be a ConfidenceLevel",
                invariant="RecommendationConfidence.level.type",
            )
        if self.level is ConfidenceLevel.UNKNOWN:
            raise EducationalInvariantViolation(
                "recommendation confidence must not be UNKNOWN",
                invariant="RecommendationConfidence.level.known",
            )
        if self.ratio is not None:
            if isinstance(self.ratio, bool) or not isinstance(self.ratio, int | float):
                raise EducationalInvariantViolation(
                    "ratio must be a real number when provided",
                    invariant="RecommendationConfidence.ratio.type",
                )
            if self.ratio < 0.0 or self.ratio > 1.0:
                raise EducationalInvariantViolation(
                    "ratio must be between 0.0 and 1.0 inclusive",
                    invariant="RecommendationConfidence.ratio.range",
                )
            object.__setattr__(self, "ratio", float(self.ratio))
        if self.millipoints is not None:
            if isinstance(self.millipoints, bool) or not isinstance(
                self.millipoints, int
            ):
                raise EducationalInvariantViolation(
                    "millipoints must be an integer when provided",
                    invariant="RecommendationConfidence.millipoints.type",
                )
            if self.millipoints < 0 or self.millipoints > 1000:
                raise EducationalInvariantViolation(
                    "millipoints must be between 0 and 1000 inclusive",
                    invariant="RecommendationConfidence.millipoints.range",
                )

    @classmethod
    def of(
        cls,
        level: ConfidenceLevel,
        *,
        ratio: float | None = None,
        millipoints: int | None = None,
    ) -> RecommendationConfidence:
        return cls(level=level, ratio=ratio, millipoints=millipoints)

    def __str__(self) -> str:
        if self.ratio is None:
            return self.level.value
        return f"{self.level.value}({self.ratio:.2f})"


@dataclass(frozen=True, slots=True)
class Recommendation(EducationalValueObject):
    """One educational decision derived from Educational OS state.

    Contains category, educational reason, priority, expected outcome,
    supporting evidence, and confidence. Pure educational projection —
    not a UI hint, not persistence, and not Educational Evidence.
    """

    recommendation_id: RecommendationId
    category: RecommendationCategory
    reason: RecommendationReason
    priority: RecommendationPriority
    expected_outcome: str
    supporting_evidence: tuple[SupportingEvidence, ...]
    confidence: RecommendationConfidence

    def _validate(self) -> None:
        if not isinstance(self.recommendation_id, RecommendationId):
            raise EducationalInvariantViolation(
                "recommendation_id must be a RecommendationId",
                invariant="Recommendation.recommendation_id.type",
            )
        if not isinstance(self.category, RecommendationCategory):
            raise EducationalInvariantViolation(
                "category must be a RecommendationCategory",
                invariant="Recommendation.category.type",
            )
        if not isinstance(self.reason, RecommendationReason):
            raise EducationalInvariantViolation(
                "reason must be a RecommendationReason",
                invariant="Recommendation.reason.type",
            )
        if not isinstance(self.priority, RecommendationPriority):
            raise EducationalInvariantViolation(
                "priority must be a RecommendationPriority",
                invariant="Recommendation.priority.type",
            )
        object.__setattr__(
            self,
            "expected_outcome",
            require_non_empty_text(self.expected_outcome, "expected_outcome"),
        )
        if len(self.expected_outcome) < 12:
            raise EducationalInvariantViolation(
                "expected outcome must be educationally substantive",
                invariant="Recommendation.expected_outcome.substantive",
            )
        if (
            not isinstance(self.supporting_evidence, tuple)
            or not self.supporting_evidence
        ):
            raise EducationalInvariantViolation(
                "supporting_evidence must be a non-empty tuple",
                invariant="Recommendation.supporting_evidence.min_one",
            )
        for item in self.supporting_evidence:
            if not isinstance(item, SupportingEvidence):
                raise EducationalInvariantViolation(
                    "supporting_evidence must contain SupportingEvidence values",
                    invariant="Recommendation.supporting_evidence.item_type",
                )
        if not isinstance(self.confidence, RecommendationConfidence):
            raise EducationalInvariantViolation(
                "confidence must be a RecommendationConfidence",
                invariant="Recommendation.confidence.type",
            )
