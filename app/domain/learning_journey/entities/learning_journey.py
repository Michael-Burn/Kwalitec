"""Learning Journey aggregate — educational path through one syllabus topic.

Pure domain object. No persistence, SQLAlchemy, or Flask. Session completion
never implies journey completion.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.learning_journey.entities.journey_evidence import JourneyEvidence
from app.domain.learning_journey.entities.journey_history import JourneyHistory
from app.domain.learning_journey.entities.journey_progress import JourneyProgress
from app.domain.learning_journey.entities.journey_recommendation import (
    JourneyRecommendation,
)
from app.domain.learning_journey.entities.journey_reflection import JourneyReflection
from app.domain.learning_journey.entities.learning_objective import LearningObjective
from app.domain.learning_journey.entities.learning_session import LearningSession
from app.domain.learning_journey.value_objects.journey_state import (
    JourneyState,
    JourneyTransitionEvent,
    is_terminal_journey_state,
    next_journey_state,
)


@dataclass(frozen=True)
class LearningJourney:
    """Multi-session educational journey for one curriculum topic.

    Attributes:
        journey_id: Stable aggregate identity.
        learner_id: Owning learner identity.
        topic_id: Canonical curriculum topic identity.
        curriculum_id: Canonical curriculum identity.
        state: Journey lifecycle posture.
        objectives: Ordered learning objectives for the topic journey.
        sessions: Ordered learning sessions.
        evidence: Journey-scoped evidence attributions (may include session ones).
        reflections: Reflections captured across sessions.
        recommendations: Journey-scoped advisory artefacts.
        progress: Derived educational progress posture.
        history: Append-only event log.
        study_plan_id: Optional V1 planning context (not educational owner).
    """

    journey_id: str
    learner_id: str
    topic_id: str
    curriculum_id: str
    state: JourneyState
    objectives: tuple[LearningObjective, ...] = field(default_factory=tuple)
    sessions: tuple[LearningSession, ...] = field(default_factory=tuple)
    evidence: tuple[JourneyEvidence, ...] = field(default_factory=tuple)
    reflections: tuple[JourneyReflection, ...] = field(default_factory=tuple)
    recommendations: tuple[JourneyRecommendation, ...] = field(default_factory=tuple)
    progress: JourneyProgress = field(default_factory=JourneyProgress.empty)
    history: JourneyHistory = field(default_factory=JourneyHistory.empty)
    study_plan_id: str | None = None

    @classmethod
    def create(
        cls,
        journey_id: str,
        learner_id: str,
        topic_id: str,
        curriculum_id: str,
        *,
        state: JourneyState | str = JourneyState.NOT_STARTED,
        objectives: list[LearningObjective]
        | tuple[LearningObjective, ...]
        | None = None,
        sessions: list[LearningSession] | tuple[LearningSession, ...] | None = None,
        evidence: list[JourneyEvidence] | tuple[JourneyEvidence, ...] | None = None,
        reflections: list[JourneyReflection]
        | tuple[JourneyReflection, ...]
        | None = None,
        recommendations: list[JourneyRecommendation]
        | tuple[JourneyRecommendation, ...]
        | None = None,
        progress: JourneyProgress | None = None,
        history: JourneyHistory | None = None,
        study_plan_id: str | None = None,
    ) -> LearningJourney:
        """Construct a LearningJourney after validating aggregate invariants.

        Raises:
            ValueError: On empty identities, topic/objective mismatch, or
                child entity journey_id mismatches.
        """
        jid = _require_non_empty(journey_id, "journey_id")
        lid = _require_non_empty(learner_id, "learner_id")
        tid = _require_non_empty(topic_id, "topic_id")
        cid = _require_non_empty(curriculum_id, "curriculum_id")
        state_value = (
            state if isinstance(state, JourneyState) else JourneyState(state)
        )
        objectives_t = tuple(objectives or ())
        for obj in objectives_t:
            if obj.topic_id != tid:
                raise ValueError("objective topic_id must match journey topic_id")
        sessions_t = tuple(sessions or ())
        for session in sessions_t:
            if session.journey_id != jid:
                raise ValueError("session journey_id must match journey")
        evidence_t = tuple(evidence or ())
        for item in evidence_t:
            if item.journey_id != jid:
                raise ValueError("evidence journey_id must match journey")
            if item.topic_id is not None and item.topic_id != tid:
                raise ValueError("evidence topic_id must match journey topic_id")
        reflections_t = tuple(reflections or ())
        for reflection in reflections_t:
            if reflection.journey_id != jid:
                raise ValueError("reflection journey_id must match journey")
        recommendations_t = tuple(recommendations or ())
        for recommendation in recommendations_t:
            if recommendation.journey_id != jid:
                raise ValueError("recommendation journey_id must match journey")
        return cls(
            journey_id=jid,
            learner_id=lid,
            topic_id=tid,
            curriculum_id=cid,
            state=state_value,
            objectives=objectives_t,
            sessions=sessions_t,
            evidence=evidence_t,
            reflections=reflections_t,
            recommendations=recommendations_t,
            progress=progress if progress is not None else JourneyProgress.empty(),
            history=history if history is not None else JourneyHistory.empty(),
            study_plan_id=_optional_id(study_plan_id),
        )

    def apply_transition(self, event: JourneyTransitionEvent) -> LearningJourney:
        """Return a new journey after a lawful state transition.

        Raises:
            ValueError: When the transition is not lawful.
        """
        nxt = next_journey_state(self.state, event)
        if nxt is None:
            raise ValueError(
                f"invalid journey transition: {self.state.value} + {event.value}"
            )
        return self._copy(state=nxt)

    def with_session(self, session: LearningSession) -> LearningJourney:
        """Append an ordered session (must match journey and sequence)."""
        if session.journey_id != self.journey_id:
            raise ValueError("session journey_id must match journey")
        existing_indexes = {s.sequence_index for s in self.sessions}
        if session.sequence_index in existing_indexes:
            raise ValueError("session sequence_index must be unique within journey")
        return self._copy(sessions=(*self.sessions, session))

    def with_evidence(self, evidence: JourneyEvidence) -> LearningJourney:
        """Append journey-scoped evidence (append-only)."""
        if evidence.journey_id != self.journey_id:
            raise ValueError("evidence journey_id must match journey")
        if evidence.topic_id is not None and evidence.topic_id != self.topic_id:
            raise ValueError("evidence topic_id must match journey topic_id")
        return self._copy(evidence=(*self.evidence, evidence))

    def with_reflection(self, reflection: JourneyReflection) -> LearningJourney:
        """Append a reflection artefact."""
        if reflection.journey_id != self.journey_id:
            raise ValueError("reflection journey_id must match journey")
        return self._copy(reflections=(*self.reflections, reflection))

    def with_recommendation(
        self, recommendation: JourneyRecommendation
    ) -> LearningJourney:
        """Append a recommendation artefact."""
        if recommendation.journey_id != self.journey_id:
            raise ValueError("recommendation journey_id must match journey")
        return self._copy(recommendations=(*self.recommendations, recommendation))

    def with_progress(self, progress: JourneyProgress) -> LearningJourney:
        """Replace derived progress posture."""
        return self._copy(progress=progress)

    def with_history(self, history: JourneyHistory) -> LearningJourney:
        """Replace history spine (typically via append on the history object)."""
        return self._copy(history=history)

    def ordered_sessions(self) -> tuple[LearningSession, ...]:
        """Sessions sorted by sequence_index ascending."""
        return tuple(sorted(self.sessions, key=lambda s: s.sequence_index))

    def ordered_objectives(self) -> tuple[LearningObjective, ...]:
        """Objectives sorted by sequence_index ascending."""
        return tuple(sorted(self.objectives, key=lambda o: o.sequence_index))

    @property
    def is_terminal(self) -> bool:
        """True when the journey cannot continue educational work."""
        return is_terminal_journey_state(self.state)

    def _copy(self, **overrides: object) -> LearningJourney:
        data = {
            "journey_id": self.journey_id,
            "learner_id": self.learner_id,
            "topic_id": self.topic_id,
            "curriculum_id": self.curriculum_id,
            "state": self.state,
            "objectives": self.objectives,
            "sessions": self.sessions,
            "evidence": self.evidence,
            "reflections": self.reflections,
            "recommendations": self.recommendations,
            "progress": self.progress,
            "history": self.history,
            "study_plan_id": self.study_plan_id,
        }
        data.update(overrides)
        return LearningJourney(**data)  # type: ignore[arg-type]


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _optional_id(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None
