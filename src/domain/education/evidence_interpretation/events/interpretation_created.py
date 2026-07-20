"""Domain event: educational interpretation was created.

Architecture Source
    CAPABILITY_4_8_2_EDUCATIONAL_EVIDENCE_ANALYSIS.md /
    EDUCATIONAL_EVIDENCE_MODEL.md
Concept
    InterpretationCreated
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.evidence_interpretation.policies.interpretation_validation_policy import (  # noqa: E501
    InterpretationId,
)
from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class InterpretationCreated(EducationalValueObject):
    """Immutable record that an Interpretation was created from evidence."""

    interpretation_id: InterpretationId
    student_id: str
    pattern_count: int
    cluster_count: int
    confidence_level: ConfidenceLevel

    def _validate(self) -> None:
        if not isinstance(self.interpretation_id, InterpretationId):
            raise EducationalInvariantViolation(
                "interpretation_id must be an InterpretationId",
                invariant="InterpretationCreated.interpretation_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_identity_value(self.student_id, "student_id"),
        )
        if not isinstance(self.pattern_count, int) or self.pattern_count < 1:
            raise EducationalInvariantViolation(
                "pattern_count must be a positive integer",
                invariant="InterpretationCreated.pattern_count.positive",
            )
        if not isinstance(self.cluster_count, int) or self.cluster_count < 1:
            raise EducationalInvariantViolation(
                "cluster_count must be a positive integer",
                invariant="InterpretationCreated.cluster_count.positive",
            )
        if not isinstance(self.confidence_level, ConfidenceLevel):
            raise EducationalInvariantViolation(
                "confidence_level must be a ConfidenceLevel",
                invariant="InterpretationCreated.confidence_level.type",
            )
        if self.confidence_level is ConfidenceLevel.UNKNOWN:
            raise EducationalInvariantViolation(
                "confidence_level must not be UNKNOWN",
                invariant="InterpretationCreated.confidence_level.known",
            )
