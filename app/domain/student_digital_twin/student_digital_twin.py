"""StudentDigitalTwin aggregate root — sole source of truth for learner state.

Nothing outside this bounded context should directly manipulate learner state.
Curriculum evidence is consumed only via CurriculumRetrievalService at the
application layer — never by mutating this aggregate with raw vectors/graphs.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import UTC, datetime

from app.domain.student_digital_twin.confidence import ConfidenceState
from app.domain.student_digital_twin.goal import Goal
from app.domain.student_digital_twin.knowledge_gap import KnowledgeGap
from app.domain.student_digital_twin.learning_state import LearningState
from app.domain.student_digital_twin.mastery import MasteryMap
from app.domain.student_digital_twin.observation import Observation
from app.domain.student_digital_twin.prediction import Prediction
from app.domain.student_digital_twin.reasoning import ReasoningRecord
from app.domain.student_digital_twin.recommendation import Recommendation
from app.domain.student_digital_twin.student import Student
from app.domain.student_digital_twin.timeline import (
    Timeline,
    TimelineEvent,
    TimelineEventKind,
)


@dataclass(frozen=True)
class StudentDigitalTwin:
    """Canonical learner aggregate.

    Owns Student, Observations, Learning State, Mastery, Knowledge Gaps,
    Confidence, Recommendations, Predictions, and Timeline.
    """

    twin_id: str
    student: Student
    observations: tuple[Observation, ...] = ()
    learning_state: LearningState = field(default_factory=LearningState.empty)
    mastery: MasteryMap = field(default_factory=MasteryMap.empty)
    knowledge_gaps: tuple[KnowledgeGap, ...] = ()
    confidence: ConfidenceState = field(default_factory=ConfidenceState.empty)
    goals: tuple[Goal, ...] = ()
    recommendations: tuple[Recommendation, ...] = ()
    predictions: tuple[Prediction, ...] = ()
    timeline: Timeline = field(default_factory=Timeline)
    reasoning_history: tuple[ReasoningRecord, ...] = ()
    created_at: datetime | None = None
    updated_at: datetime | None = None
    version: int = 1

    def __post_init__(self) -> None:
        if not (self.twin_id or "").strip():
            raise ValueError("twin_id is required")
        for when_attr in ("created_at", "updated_at"):
            when = getattr(self, when_attr)
            if when is not None and when.tzinfo is not None:
                object.__setattr__(
                    self, when_attr, when.astimezone(UTC).replace(tzinfo=None)
                )

    @classmethod
    def create(
        cls,
        *,
        twin_id: str,
        student: Student,
        created_at: datetime | None = None,
    ) -> StudentDigitalTwin:
        """Construct an empty Twin for a learner."""
        when = created_at or datetime.now(UTC).replace(tzinfo=None)
        return cls(
            twin_id=twin_id,
            student=student,
            learning_state=LearningState.empty(computed_at=when),
            created_at=when,
            updated_at=when,
            version=1,
        )

    def append_observation(self, observation: Observation) -> StudentDigitalTwin:
        """Return a new Twin with an appended observation (never mutates history)."""
        if observation.twin_id != self.twin_id:
            raise ValueError("observation twin_id mismatch")
        if any(
            o.observation_id == observation.observation_id for o in self.observations
        ):
            raise ValueError(
                f"observation {observation.observation_id!r} already "
                "recorded (immutable)"
            )
        event = TimelineEvent(
            event_id=f"tl-obs-{observation.observation_id}",
            twin_id=self.twin_id,
            kind=TimelineEventKind.OBSERVATION,
            occurred_at=observation.recorded_at,
            summary=f"Observation {observation.kind.value}",
            reference_id=observation.observation_id,
        )
        return replace(
            self,
            observations=(*self.observations, observation),
            timeline=self.timeline.append(event),
            updated_at=observation.recorded_at,
            version=self.version + 1,
        )

    def with_inferences(
        self,
        *,
        learning_state: LearningState | None = None,
        mastery: MasteryMap | None = None,
        knowledge_gaps: tuple[KnowledgeGap, ...] | None = None,
        confidence: ConfidenceState | None = None,
        recommendations: tuple[Recommendation, ...] | None = None,
        predictions: tuple[Prediction, ...] | None = None,
        reasoning: ReasoningRecord | None = None,
        timeline_events: tuple[TimelineEvent, ...] = (),
        updated_at: datetime | None = None,
    ) -> StudentDigitalTwin:
        """Return a new Twin with updated inferences (observations untouched)."""
        timeline = self.timeline
        for event in timeline_events:
            timeline = timeline.append(event)
        history = self.reasoning_history
        if reasoning is not None:
            history = (*history, reasoning)
        when = updated_at or datetime.now(UTC).replace(tzinfo=None)
        return replace(
            self,
            learning_state=(
                learning_state if learning_state is not None else self.learning_state
            ),
            mastery=mastery if mastery is not None else self.mastery,
            knowledge_gaps=(
                knowledge_gaps if knowledge_gaps is not None else self.knowledge_gaps
            ),
            confidence=confidence if confidence is not None else self.confidence,
            recommendations=(
                recommendations
                if recommendations is not None
                else self.recommendations
            ),
            predictions=predictions if predictions is not None else self.predictions,
            timeline=timeline,
            reasoning_history=history,
            updated_at=when,
            version=self.version + 1,
        )

    @property
    def observation_count(self) -> int:
        return len(self.observations)
