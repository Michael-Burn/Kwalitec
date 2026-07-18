"""Revision snapshot DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.domain.adaptive_learning.revision_candidate import RevisionCandidate
from app.domain.adaptive_learning.revision_plan import RevisionPlan
from app.domain.adaptive_learning.revision_window import RevisionWindow


@dataclass(frozen=True)
class RevisionCandidateSnapshot:
    """Immutable DTO for a revision candidate."""

    topic_id: str
    priority_score: float
    priority_band: str
    retention_score: float
    mastery_score: float
    knowledge_score: float
    confidence: str
    educational_benefit: float
    estimated_study_minutes: float
    return_on_study_time: float
    struggle_score: float = 0.0
    curriculum_importance: float = 0.5
    prerequisite_criticality: float = 0.0
    rationale: str = ""
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_candidate(cls, candidate: RevisionCandidate) -> RevisionCandidateSnapshot:
        """Project a RevisionCandidate."""
        return cls(
            topic_id=candidate.topic_id,
            priority_score=candidate.priority.score,
            priority_band=candidate.priority.band.value,
            retention_score=candidate.retention_score,
            mastery_score=candidate.mastery_score,
            knowledge_score=candidate.knowledge_score,
            confidence=candidate.confidence.value,
            educational_benefit=candidate.roi.educational_benefit,
            estimated_study_minutes=candidate.roi.estimated_study_minutes,
            return_on_study_time=candidate.roi.return_on_study_time,
            struggle_score=candidate.struggle_score,
            curriculum_importance=candidate.curriculum_importance,
            prerequisite_criticality=candidate.prerequisite_criticality,
            rationale=candidate.rationale,
            evidence_ids=candidate.evidence_ids,
        )


@dataclass(frozen=True)
class RevisionWindowSnapshot:
    """Immutable DTO for a revision window."""

    topic_id: str
    urgency: str
    suggested_start: datetime
    suggested_end: datetime
    allocated_minutes: float
    priority_score: float

    @classmethod
    def from_window(cls, window: RevisionWindow) -> RevisionWindowSnapshot:
        """Project a RevisionWindow."""
        return cls(
            topic_id=window.topic_id,
            urgency=window.urgency.value,
            suggested_start=window.suggested_start,
            suggested_end=window.suggested_end,
            allocated_minutes=window.allocated_minutes,
            priority_score=window.priority_score,
        )


@dataclass(frozen=True)
class RevisionSnapshot:
    """Immutable DTO for a full revision plan."""

    plan_id: str
    primary_topic_id: str | None
    intervention_count: int
    total_estimated_minutes: float
    topic_ids: tuple[str, ...]
    candidates: tuple[RevisionCandidateSnapshot, ...] = field(default_factory=tuple)
    windows: tuple[RevisionWindowSnapshot, ...] = field(default_factory=tuple)

    @classmethod
    def from_plan(cls, plan: RevisionPlan) -> RevisionSnapshot:
        """Project a RevisionPlan."""
        return cls(
            plan_id=plan.plan_id,
            primary_topic_id=plan.primary_topic_id,
            intervention_count=plan.intervention_count,
            total_estimated_minutes=plan.total_estimated_minutes,
            topic_ids=plan.topic_ids,
            candidates=tuple(
                RevisionCandidateSnapshot.from_candidate(c) for c in plan.candidates
            ),
            windows=tuple(RevisionWindowSnapshot.from_window(w) for w in plan.windows),
        )

    @property
    def is_empty(self) -> bool:
        """True when no interventions are planned."""
        return self.intervention_count == 0
