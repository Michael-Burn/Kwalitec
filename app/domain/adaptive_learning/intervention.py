"""Intervention — recommended educational action with explainable priority."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.adaptive_learning.decision_explanation import DecisionExplanation
from app.domain.adaptive_learning.educational_roi import EducationalROI
from app.domain.adaptive_learning.intervention_priority import InterventionPriority
from app.domain.adaptive_learning.intervention_type import (
    InterventionType,
    resolve_intervention_type,
)
from app.domain.student_twin.confidence_band import ConfidenceBand


@dataclass(frozen=True)
class Intervention:
    """A single recommended educational intervention.

    Phase 1 produces REVISION interventions. Architecture supports future types.
    """

    intervention_id: str
    intervention_type: InterventionType
    topic_id: str | None
    priority: InterventionPriority
    roi: EducationalROI
    explanation: DecisionExplanation
    estimated_study_minutes: float
    confidence: ConfidenceBand
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        intervention_id: str,
        intervention_type: InterventionType | str,
        *,
        topic_id: str | None = None,
        priority: InterventionPriority | None = None,
        roi: EducationalROI | None = None,
        explanation: DecisionExplanation | None = None,
        estimated_study_minutes: float | None = None,
        confidence: ConfidenceBand | str | None = None,
        metadata: dict[str, str] | list[tuple[str, str]] | None = None,
    ) -> Intervention:
        """Construct an Intervention."""
        iid = _require_non_empty(intervention_id, "intervention_id")
        itype = resolve_intervention_type(intervention_type)
        if isinstance(topic_id, str) and topic_id.strip():
            tid = topic_id.strip()
        else:
            tid = None
        prio = priority if priority is not None else InterventionPriority.negligible()
        edu_roi = roi if roi is not None else EducationalROI.zero()
        minutes = (
            float(estimated_study_minutes)
            if estimated_study_minutes is not None
            else edu_roi.estimated_study_minutes
        )
        if minutes < 0.0:
            raise ValueError("estimated_study_minutes must be non-negative")
        if explanation is None:
            raise ValueError("explanation is required")
        band = (
            confidence
            if isinstance(confidence, ConfidenceBand)
            else (
                ConfidenceBand(str(confidence).strip().lower())
                if confidence is not None
                else explanation.confidence
            )
        )
        meta_pairs: tuple[tuple[str, str], ...]
        if metadata is None:
            meta_pairs = ()
        elif isinstance(metadata, dict):
            meta_pairs = tuple(sorted((str(k), str(v)) for k, v in metadata.items()))
        else:
            meta_pairs = tuple((str(k), str(v)) for k, v in metadata)
        return cls(
            intervention_id=iid,
            intervention_type=itype,
            topic_id=tid,
            priority=prio,
            roi=edu_roi,
            explanation=explanation,
            estimated_study_minutes=minutes,
            confidence=band,
            metadata=meta_pairs,
        )

    @property
    def is_revision(self) -> bool:
        """True when this intervention is a revision."""
        return self.intervention_type is InterventionType.REVISION

    @property
    def priority_score(self) -> float:
        """Numeric priority score."""
        return self.priority.score


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
