"""Revision candidate — a topic considered for revision intervention."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.adaptive_learning.educational_roi import EducationalROI
from app.domain.adaptive_learning.intervention_priority import InterventionPriority
from app.domain.student_twin.confidence_band import ConfidenceBand


@dataclass(frozen=True)
class RevisionCandidate:
    """A topic evaluated as a potential revision target.

    Candidates are ranked by priority and educational ROI before selection.
    """

    topic_id: str
    priority: InterventionPriority
    roi: EducationalROI
    retention_score: float
    mastery_score: float
    knowledge_score: float
    confidence: ConfidenceBand
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    struggle_score: float = 0.0
    curriculum_importance: float = 0.5
    prerequisite_criticality: float = 0.0
    rationale: str = ""

    @classmethod
    def create(
        cls,
        topic_id: str,
        *,
        priority: InterventionPriority | None = None,
        roi: EducationalROI | None = None,
        retention_score: float = 0.0,
        mastery_score: float = 0.0,
        knowledge_score: float = 0.0,
        confidence: ConfidenceBand | str = ConfidenceBand.VERY_LOW,
        evidence_ids: list[str] | tuple[str, ...] | None = None,
        struggle_score: float = 0.0,
        curriculum_importance: float = 0.5,
        prerequisite_criticality: float = 0.0,
        rationale: str = "",
    ) -> RevisionCandidate:
        """Construct a RevisionCandidate."""
        tid = _require_non_empty(topic_id, "topic_id")
        band = (
            confidence
            if isinstance(confidence, ConfidenceBand)
            else ConfidenceBand(str(confidence).strip().lower())
        )
        return cls(
            topic_id=tid,
            priority=(
                priority if priority is not None else InterventionPriority.negligible()
            ),
            roi=roi if roi is not None else EducationalROI.zero(),
            retention_score=_unit_interval(retention_score, "retention_score"),
            mastery_score=_unit_interval(mastery_score, "mastery_score"),
            knowledge_score=_unit_interval(knowledge_score, "knowledge_score"),
            confidence=band,
            evidence_ids=tuple(evidence_ids or ()),
            struggle_score=_unit_interval(struggle_score, "struggle_score"),
            curriculum_importance=_unit_interval(
                curriculum_importance, "curriculum_importance"
            ),
            prerequisite_criticality=_unit_interval(
                prerequisite_criticality, "prerequisite_criticality"
            ),
            rationale=(rationale or "").strip(),
        )

    @property
    def retention_risk(self) -> float:
        """Complement of retention score (higher = more at risk)."""
        return round(1.0 - self.retention_score, 6)

    @property
    def mastery_gap(self) -> float:
        """Complement of mastery score."""
        return round(1.0 - self.mastery_score, 6)

    @property
    def ranking_key(self) -> tuple[float, float, str]:
        """Stable sort key: higher priority, then higher ROI, then topic id."""
        return (-self.priority.score, -self.roi.return_on_study_time, self.topic_id)


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _unit_interval(value: float, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(f"{field_name} must be a number in [0, 1]")
    numeric = float(value)
    if numeric < 0.0 or numeric > 1.0:
        raise ValueError(f"{field_name} must be in [0, 1]")
    return numeric
