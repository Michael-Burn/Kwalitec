"""Application DTOs for Adaptive Decision Engine snapshots."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.adaptive_learning.adaptive_decision import AdaptiveDecision
from app.domain.adaptive_learning.decision_explanation import DecisionExplanation
from app.domain.adaptive_learning.decision_snapshot import DecisionSnapshot
from app.domain.adaptive_learning.intervention_type import InterventionType


@dataclass(frozen=True)
class DecisionSnapshotDTO:
    """Immutable DTO projection of an adaptive decision."""

    decision_id: str
    learner_id: str
    captured_at: datetime
    intervention_type: str
    topic_id: str | None
    priority_score: float
    educational_benefit: float
    estimated_study_minutes: float
    confidence: str
    rationale: str
    expected_benefit: str
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    twin_version_label: str = ""
    revision_plan_id: str = ""
    alternative_topic_ids: tuple[str, ...] = field(default_factory=tuple)
    cost_benefit_ratio: float = 0.0
    return_on_study_time: float = 0.0

    @classmethod
    def from_decision(cls, decision: AdaptiveDecision) -> DecisionSnapshotDTO:
        """Build DTO from an AdaptiveDecision."""
        snap = DecisionSnapshot.from_decision(decision)
        return cls.from_snapshot(snap)

    @classmethod
    def from_snapshot(cls, snapshot: DecisionSnapshot) -> DecisionSnapshotDTO:
        """Build DTO from a domain DecisionSnapshot."""
        return cls(
            decision_id=snapshot.decision_id,
            learner_id=snapshot.learner_id,
            captured_at=snapshot.captured_at,
            intervention_type=snapshot.intervention_type.value,
            topic_id=snapshot.topic_id,
            priority_score=snapshot.priority_score,
            educational_benefit=snapshot.educational_benefit,
            estimated_study_minutes=snapshot.estimated_study_minutes,
            confidence=snapshot.confidence.value,
            rationale=snapshot.rationale,
            expected_benefit=snapshot.expected_benefit,
            evidence_ids=snapshot.evidence_ids,
            twin_version_label=snapshot.twin_version_label,
            revision_plan_id=snapshot.revision_plan_id,
            alternative_topic_ids=snapshot.alternative_topic_ids,
            cost_benefit_ratio=snapshot.cost_benefit_ratio,
            return_on_study_time=snapshot.return_on_study_time,
        )


@dataclass(frozen=True)
class DecisionExplanationDTO:
    """Immutable explanation DTO for consumers / tests."""

    decision_id: str
    intervention_type: str
    topic_id: str | None
    evidence_considered: tuple[str, ...]
    rationale: str
    priority_score: float
    priority_band: str
    expected_educational_benefit: str
    confidence: str
    estimated_study_minutes: float = 0.0
    educational_benefit: float = 0.0
    detail_lines: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_explanation(
        cls,
        explanation: DecisionExplanation,
        *,
        decision_id: str,
        topic_id: str | None = None,
        intervention_type: str = InterventionType.REVISION.value,
        estimated_study_minutes: float = 0.0,
        educational_benefit: float = 0.0,
        confidence: str | None = None,
    ) -> DecisionExplanationDTO:
        """Build DTO from a domain DecisionExplanation."""
        return cls(
            decision_id=decision_id,
            intervention_type=intervention_type,
            topic_id=topic_id,
            evidence_considered=explanation.evidence_considered,
            rationale=explanation.rationale,
            priority_score=explanation.priority_score,
            priority_band=explanation.priority_band.value,
            expected_educational_benefit=explanation.expected_educational_benefit,
            confidence=confidence or explanation.confidence.value,
            estimated_study_minutes=estimated_study_minutes,
            educational_benefit=educational_benefit,
            detail_lines=explanation.detail_lines,
        )


def ensure_utc(value: datetime) -> datetime:
    """Normalise naive datetimes to UTC."""
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value
