"""Intervention snapshot DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.adaptive_learning.intervention import Intervention


@dataclass(frozen=True)
class InterventionSnapshot:
    """Immutable DTO for a recommended intervention."""

    intervention_id: str
    intervention_type: str
    topic_id: str | None
    priority_score: float
    priority_band: str
    estimated_study_minutes: float
    confidence: str
    rationale: str
    expected_benefit: str
    educational_benefit: float
    cost_benefit_ratio: float
    return_on_study_time: float
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_intervention(cls, intervention: Intervention) -> InterventionSnapshot:
        """Project an Intervention."""
        return cls(
            intervention_id=intervention.intervention_id,
            intervention_type=intervention.intervention_type.value,
            topic_id=intervention.topic_id,
            priority_score=intervention.priority.score,
            priority_band=intervention.priority.band.value,
            estimated_study_minutes=intervention.estimated_study_minutes,
            confidence=intervention.confidence.value,
            rationale=intervention.explanation.rationale,
            expected_benefit=intervention.explanation.expected_educational_benefit,
            educational_benefit=intervention.roi.educational_benefit,
            cost_benefit_ratio=intervention.roi.cost_benefit_ratio,
            return_on_study_time=intervention.roi.return_on_study_time,
            evidence_ids=intervention.explanation.evidence_considered,
        )

    @property
    def is_revision(self) -> bool:
        """True when intervention type is revision."""
        return self.intervention_type == "revision"
