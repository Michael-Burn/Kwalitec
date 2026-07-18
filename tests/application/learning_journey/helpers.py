"""Shared helpers for Learning Journey Engine application tests."""

from __future__ import annotations

from datetime import UTC, datetime

from app.domain.evidence.evidence_category import EvidenceConfidenceLevel
from app.domain.evidence.evidence_type import EvidenceType
from app.domain.learning_journey.entities.journey_evidence import JourneyEvidence
from app.domain.learning_journey.entities.journey_reflection import (
    JourneyReflection,
    ReflectionConfidence,
)
from app.domain.learning_journey.entities.learning_journey import LearningJourney
from app.domain.learning_journey.entities.learning_objective import (
    LearningObjective,
    ObjectiveKind,
)
from app.domain.learning_journey.entities.learning_session import LearningSession
from app.domain.learning_journey.interfaces.learning_journey_repository import (
    LearningJourneyRepository,
)
from app.domain.learning_journey.value_objects.effort_estimate import EffortEstimate
from app.domain.learning_journey.value_objects.journey_state import JourneyState
from app.domain.learning_journey.value_objects.session_state import SessionState

NOW = datetime(2026, 7, 18, 12, 0, tzinfo=UTC)


def make_objective(
    oid: str = "obj-1",
    *,
    topic_id: str = "topic-a",
    kind: ObjectiveKind = ObjectiveKind.UNDERSTAND,
    sequence_index: int = 0,
) -> LearningObjective:
    return LearningObjective.create(
        oid,
        f"curr-{oid}",
        topic_id,
        kind,
        title=f"Objective {oid}",
        sequence_index=sequence_index,
    )


def make_session(
    sid: str = "sess-1",
    *,
    journey_id: str = "journey-1",
    sequence_index: int = 0,
    state: SessionState = SessionState.NOT_STARTED,
    objective_id: str | None = None,
    effort: EffortEstimate = EffortEstimate.MEDIUM,
    reflection: JourneyReflection | None = None,
) -> LearningSession:
    return LearningSession.create(
        sid,
        journey_id,
        sequence_index=sequence_index,
        state=state,
        estimated_effort=effort,
        objective_id=objective_id,
        reflection=reflection,
    )


def make_evidence(
    jeid: str = "je-1",
    *,
    evidence_id: str = "ev-1",
    journey_id: str = "journey-1",
    session_id: str | None = "sess-1",
    objective_id: str | None = None,
    confidence: EvidenceConfidenceLevel = EvidenceConfidenceLevel.MEDIUM,
) -> JourneyEvidence:
    return JourneyEvidence.create(
        jeid,
        evidence_id,
        journey_id,
        EvidenceType.STUDY_SESSION,
        NOW,
        confidence_level=confidence,
        session_id=session_id,
        objective_id=objective_id,
        topic_id="topic-a",
    )


def make_captured_reflection(
    rid: str,
    session_id: str,
    journey_id: str = "journey-1",
) -> JourneyReflection:
    return JourneyReflection.create_captured(
        rid,
        session_id,
        journey_id,
        what_was_learned="Covered core definitions",
        uncertainty="Edge cases remain unclear",
        questions_remaining=["How does X interact with Y?"],
        confidence=ReflectionConfidence.MEDIUM,
        captured_at=NOW,
    )


def make_journey(
    *,
    journey_id: str = "journey-1",
    learner_id: str = "learner-1",
    topic_id: str = "topic-a",
    curriculum_id: str = "curr-1",
    state: JourneyState = JourneyState.NOT_STARTED,
    objectives: list[LearningObjective] | None = None,
    sessions: list[LearningSession] | None = None,
    evidence: list[JourneyEvidence] | None = None,
    reflections: list[JourneyReflection] | None = None,
) -> LearningJourney:
    return LearningJourney.create(
        journey_id,
        learner_id,
        topic_id,
        curriculum_id,
        state=state,
        objectives=objectives or [],
        sessions=sessions or [],
        evidence=evidence or [],
        reflections=reflections or [],
    )


class InMemoryJourneyRepository(LearningJourneyRepository):
    """Minimal in-memory repository for engine load tests."""

    def __init__(self) -> None:
        self._store: dict[str, LearningJourney] = {}

    def get_by_id(self, journey_id: str) -> LearningJourney | None:
        return self._store.get(journey_id)

    def get_by_learner_and_topic(
        self,
        learner_id: str,
        topic_id: str,
        *,
        curriculum_id: str | None = None,
    ) -> LearningJourney | None:
        for journey in self._store.values():
            if journey.learner_id != learner_id or journey.topic_id != topic_id:
                continue
            if curriculum_id is not None and journey.curriculum_id != curriculum_id:
                continue
            return journey
        return None

    def list_for_learner(
        self,
        learner_id: str,
        *,
        curriculum_id: str | None = None,
    ) -> list[LearningJourney]:
        result = []
        for journey in self._store.values():
            if journey.learner_id != learner_id:
                continue
            if curriculum_id is not None and journey.curriculum_id != curriculum_id:
                continue
            result.append(journey)
        return result

    def save(self, journey: LearningJourney) -> None:
        self._store[journey.journey_id] = journey

    def delete(self, journey_id: str) -> bool:
        return self._store.pop(journey_id, None) is not None


def ready_journey() -> LearningJourney:
    """Journey meeting default completion criteria (2 sessions + reflections)."""
    objectives = [
        make_objective("obj-1", sequence_index=0),
        make_objective("obj-2", kind=ObjectiveKind.APPLY, sequence_index=1),
    ]
    r1 = make_captured_reflection("ref-1", "sess-1")
    r2 = make_captured_reflection("ref-2", "sess-2")
    sessions = [
        make_session(
            "sess-1",
            sequence_index=0,
            state=SessionState.COMPLETED,
            objective_id="obj-1",
            reflection=r1,
        ),
        make_session(
            "sess-2",
            sequence_index=1,
            state=SessionState.COMPLETED,
            objective_id="obj-2",
            reflection=r2,
        ),
    ]
    evidence = [
        make_evidence("je-1", session_id="sess-1", objective_id="obj-1"),
        make_evidence(
            "je-2",
            evidence_id="ev-2",
            session_id="sess-2",
            objective_id="obj-2",
            confidence=EvidenceConfidenceLevel.HIGH,
        ),
    ]
    return make_journey(
        state=JourneyState.ACTIVE,
        objectives=objectives,
        sessions=sessions,
        evidence=evidence,
        reflections=[r1, r2],
    )
