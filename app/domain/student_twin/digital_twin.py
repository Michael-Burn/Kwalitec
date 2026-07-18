"""Digital Twin aggregate — living educational state of a learner.

Consumes evidence. Never consumes curriculum content, PDFs, or AI responses.
Evolves by producing new immutable snapshots — never by mutating history.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import UTC, datetime

from app.domain.student_twin.confidence_state import ConfidenceState
from app.domain.student_twin.evidence_event import EvidenceEvent
from app.domain.student_twin.evidence_profile import EvidenceProfile
from app.domain.student_twin.knowledge_state import KnowledgeState
from app.domain.student_twin.learner import Learner
from app.domain.student_twin.learning_history import LearningHistory
from app.domain.student_twin.learning_velocity import LearningVelocity
from app.domain.student_twin.mastery_state import MasteryState
from app.domain.student_twin.readiness_state import ReadinessState
from app.domain.student_twin.recommendation_state import RecommendationState
from app.domain.student_twin.retention_state import RetentionState
from app.domain.student_twin.twin_identity import TwinIdentity
from app.domain.student_twin.twin_snapshot import TwinSnapshot
from app.domain.student_twin.twin_version import TwinVersion
from app.domain.student_twin.weakness_profile import WeaknessProfile


@dataclass(frozen=True)
class DigitalTwin:
    """Immutable Student Digital Twin aggregate root.

    Application services derive updated states and return a new DigitalTwin.
    """

    identity: TwinIdentity
    learner: Learner
    version: TwinVersion
    history: LearningHistory = field(default_factory=LearningHistory.empty)
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
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @classmethod
    def create(
        cls,
        twin_id: str,
        learner: Learner | str,
        *,
        subject_code: str | None = None,
        created_at: datetime | None = None,
    ) -> DigitalTwin:
        """Construct an empty Digital Twin for a learner."""
        learner_obj = (
            learner
            if isinstance(learner, Learner)
            else Learner.create(learner)
        )
        identity = TwinIdentity.create(
            twin_id,
            learner_obj.learner_id,
            subject_code=subject_code,
        )
        when = created_at
        if when is not None and when.tzinfo is None:
            when = when.replace(tzinfo=UTC)
        return cls(
            identity=identity,
            learner=learner_obj,
            version=TwinVersion.initial(),
            created_at=when,
            updated_at=when,
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
    def event_count(self) -> int:
        """Number of evidence events in history."""
        return self.history.event_count

    def with_evidence(self, event: EvidenceEvent) -> DigitalTwin:
        """Return a Twin with ``event`` appended to history (states unchanged).

        Application calculators recompute derived states after append.
        """
        new_history = self.history.append(event)
        profile = EvidenceProfile.from_events(new_history.events)
        return replace(
            self,
            history=new_history,
            evidence_profile=profile,
            version=self.version.bump_patch(),
            updated_at=event.occurred_at,
        )

    def with_states(
        self,
        *,
        knowledge: KnowledgeState | None = None,
        mastery: MasteryState | None = None,
        confidence: ConfidenceState | None = None,
        retention: RetentionState | None = None,
        readiness: ReadinessState | None = None,
        velocity: LearningVelocity | None = None,
        weaknesses: WeaknessProfile | None = None,
        recommendations: RecommendationState | None = None,
        updated_at: datetime | None = None,
    ) -> DigitalTwin:
        """Return a Twin with replacement derived states (history preserved)."""
        when = updated_at if updated_at is not None else self.updated_at
        if when is not None and when.tzinfo is None:
            when = when.replace(tzinfo=UTC)
        return replace(
            self,
            knowledge=knowledge if knowledge is not None else self.knowledge,
            mastery=mastery if mastery is not None else self.mastery,
            confidence=confidence if confidence is not None else self.confidence,
            retention=retention if retention is not None else self.retention,
            readiness=readiness if readiness is not None else self.readiness,
            velocity=velocity if velocity is not None else self.velocity,
            weaknesses=weaknesses if weaknesses is not None else self.weaknesses,
            recommendations=(
                recommendations
                if recommendations is not None
                else self.recommendations
            ),
            updated_at=when,
        )

    def to_snapshot(self, captured_at: datetime | None = None) -> TwinSnapshot:
        """Project an immutable TwinSnapshot from current aggregate state."""
        when = captured_at if captured_at is not None else self.updated_at
        if when is None:
            when = datetime.now(tz=UTC)
        elif when.tzinfo is None:
            when = when.replace(tzinfo=UTC)
        return TwinSnapshot.create(
            self.identity,
            self.version,
            when,
            knowledge=self.knowledge,
            mastery=self.mastery,
            confidence=self.confidence,
            retention=self.retention,
            readiness=self.readiness,
            velocity=self.velocity,
            weaknesses=self.weaknesses,
            recommendations=self.recommendations,
            evidence_profile=self.evidence_profile,
            history_event_ids=self.history.event_ids,
        )
