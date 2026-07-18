"""Immutable Twin snapshot DTO for application consumers."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.application.student_twin.dto.evidence_summary import EvidenceSummary
from app.application.student_twin.dto.mastery_summary import MasterySummary
from app.application.student_twin.dto.readiness_summary import ReadinessSummary
from app.application.student_twin.dto.recommendation_snapshot import (
    RecommendationSnapshot,
)
from app.domain.student_twin.twin_snapshot import TwinSnapshot


@dataclass(frozen=True)
class TwinSnapshotDTO:
    """Read-only Twin snapshot for consumers outside the domain package."""

    twin_id: str
    learner_id: str
    version_label: str
    captured_at: datetime
    subject_code: str | None = None
    mastery: MasterySummary | None = None
    readiness: ReadinessSummary | None = None
    evidence: EvidenceSummary | None = None
    recommendations: RecommendationSnapshot | None = None
    overall_knowledge: float = 0.0
    overall_retention: float = 0.0
    overall_confidence: str = "very_low"
    history_event_ids: tuple[str, ...] = field(default_factory=tuple)
    weakness_topic_ids: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_domain(cls, snapshot: TwinSnapshot) -> TwinSnapshotDTO:
        """Project a domain TwinSnapshot to a DTO."""
        return cls(
            twin_id=snapshot.twin_id,
            learner_id=snapshot.learner_id,
            version_label=snapshot.version_label,
            captured_at=snapshot.captured_at,
            subject_code=snapshot.identity.subject_code,
            mastery=MasterySummary.from_domain(snapshot.mastery),
            readiness=ReadinessSummary.from_domain(snapshot.readiness),
            evidence=EvidenceSummary.from_domain(snapshot.evidence_profile),
            recommendations=RecommendationSnapshot.from_domain(
                snapshot.recommendations
            ),
            overall_knowledge=snapshot.knowledge.overall_score,
            overall_retention=snapshot.retention.overall_score,
            overall_confidence=snapshot.confidence.overall_band.value,
            history_event_ids=snapshot.history_event_ids,
            weakness_topic_ids=snapshot.weaknesses.topic_ids,
        )
