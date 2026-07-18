"""Twin snapshot — immutable point-in-time projection of Twin state."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.student_twin.confidence_state import ConfidenceState
from app.domain.student_twin.evidence_profile import EvidenceProfile
from app.domain.student_twin.knowledge_state import KnowledgeState
from app.domain.student_twin.learning_velocity import LearningVelocity
from app.domain.student_twin.mastery_state import MasteryState
from app.domain.student_twin.readiness_state import ReadinessState
from app.domain.student_twin.recommendation_state import RecommendationState
from app.domain.student_twin.retention_state import RetentionState
from app.domain.student_twin.twin_identity import TwinIdentity
from app.domain.student_twin.twin_version import TwinVersion
from app.domain.student_twin.weakness_profile import WeaknessProfile


@dataclass(frozen=True)
class TwinSnapshot:
    """Immutable educational state snapshot.

    Snapshots are never mutated. New evidence produces a new snapshot.
    """

    identity: TwinIdentity
    version: TwinVersion
    captured_at: datetime
    knowledge: KnowledgeState = field(default_factory=KnowledgeState.empty)
    mastery: MasteryState = field(default_factory=MasteryState.empty)
    confidence: ConfidenceState = field(default_factory=ConfidenceState.empty)
    retention: RetentionState = field(default_factory=RetentionState.empty)
    readiness: ReadinessState = field(default_factory=ReadinessState.empty)
    velocity: LearningVelocity = field(default_factory=LearningVelocity.empty)
    weaknesses: WeaknessProfile = field(default_factory=WeaknessProfile.empty)
    recommendations: RecommendationState = field(
        default_factory=RecommendationState.empty
    )
    evidence_profile: EvidenceProfile = field(default_factory=EvidenceProfile.empty)
    history_event_ids: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        identity: TwinIdentity,
        version: TwinVersion,
        captured_at: datetime,
        *,
        knowledge: KnowledgeState | None = None,
        mastery: MasteryState | None = None,
        confidence: ConfidenceState | None = None,
        retention: RetentionState | None = None,
        readiness: ReadinessState | None = None,
        velocity: LearningVelocity | None = None,
        weaknesses: WeaknessProfile | None = None,
        recommendations: RecommendationState | None = None,
        evidence_profile: EvidenceProfile | None = None,
        history_event_ids: list[str] | tuple[str, ...] | None = None,
    ) -> TwinSnapshot:
        """Construct a TwinSnapshot."""
        if not isinstance(captured_at, datetime):
            raise ValueError("captured_at must be a datetime")
        when = (
            captured_at
            if captured_at.tzinfo
            else captured_at.replace(tzinfo=UTC)
        )
        return cls(
            identity=identity,
            version=version,
            captured_at=when,
            knowledge=knowledge if knowledge is not None else KnowledgeState.empty(),
            mastery=mastery if mastery is not None else MasteryState.empty(),
            confidence=(
                confidence if confidence is not None else ConfidenceState.empty()
            ),
            retention=retention if retention is not None else RetentionState.empty(),
            readiness=readiness if readiness is not None else ReadinessState.empty(),
            velocity=velocity if velocity is not None else LearningVelocity.empty(),
            weaknesses=(
                weaknesses if weaknesses is not None else WeaknessProfile.empty()
            ),
            recommendations=(
                recommendations
                if recommendations is not None
                else RecommendationState.empty()
            ),
            evidence_profile=(
                evidence_profile
                if evidence_profile is not None
                else EvidenceProfile.empty()
            ),
            history_event_ids=tuple(history_event_ids or ()),
        )

    @property
    def twin_id(self) -> str:
        """Twin identity string."""
        return self.identity.twin_id

    @property
    def learner_id(self) -> str:
        """Learner identity string."""
        return self.identity.learner_id

    @property
    def version_label(self) -> str:
        """Dotted Twin version label."""
        return self.version.label
