"""ConfidenceCard — confidence in the readiness assessment (not student confidence)."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.readiness.enums import (
    AssessmentConfidenceCategory,
    ConsistencyBand,
    EvidenceQualityBand,
    EvidenceQuantityBand,
)
from application.student_experience.readiness.errors import (
    ReadinessInvariantViolation,
)


@dataclass(frozen=True, slots=True)
class ConfidenceCard:
    """Immutable assessment-confidence card.

    Projects existing evidence quality, quantity, consistency, and
    assessment confidence. Never invents student confidence scores.
    """

    available: bool
    evidence_quality: EvidenceQualityBand
    evidence_quality_label: str
    evidence_quantity: EvidenceQuantityBand
    evidence_quantity_label: str
    evidence_count: int
    consistency: ConsistencyBand
    consistency_label: str
    assessment_confidence: AssessmentConfidenceCategory
    assessment_confidence_label: str
    message: str

    def __post_init__(self) -> None:
        if not isinstance(self.evidence_quality, EvidenceQualityBand):
            raise ReadinessInvariantViolation(
                "evidence_quality must be an EvidenceQualityBand",
                invariant="ConfidenceCard.evidence_quality.type",
            )
        if not isinstance(self.evidence_quantity, EvidenceQuantityBand):
            raise ReadinessInvariantViolation(
                "evidence_quantity must be an EvidenceQuantityBand",
                invariant="ConfidenceCard.evidence_quantity.type",
            )
        if not isinstance(self.consistency, ConsistencyBand):
            raise ReadinessInvariantViolation(
                "consistency must be a ConsistencyBand",
                invariant="ConfidenceCard.consistency.type",
            )
        if not isinstance(self.assessment_confidence, AssessmentConfidenceCategory):
            raise ReadinessInvariantViolation(
                "assessment_confidence must be an AssessmentConfidenceCategory",
                invariant="ConfidenceCard.assessment_confidence.type",
            )
        if isinstance(self.evidence_count, bool) or not isinstance(
            self.evidence_count, int
        ):
            raise ReadinessInvariantViolation(
                "evidence_count must be an integer",
                invariant="ConfidenceCard.evidence_count.type",
            )
        if self.evidence_count < 0:
            raise ReadinessInvariantViolation(
                "evidence_count must be >= 0",
                invariant="ConfidenceCard.evidence_count.range",
            )
        for name in (
            "evidence_quality_label",
            "evidence_quantity_label",
            "consistency_label",
            "assessment_confidence_label",
            "message",
        ):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise ReadinessInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"ConfidenceCard.{name}.required",
                )
            object.__setattr__(self, name, value)
