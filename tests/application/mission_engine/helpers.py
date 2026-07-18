"""Shared helpers for Mission Engine 2.0 application tests."""

from __future__ import annotations

from datetime import UTC, date, datetime

from app.application.learning_journey.engine import LearningJourneyEngine
from app.application.learning_session.runtime import LearningSessionRuntime
from app.application.mission_engine.engine import MissionEngine
from app.application.mission_engine.mission_builder import MissionBuilder
from app.domain.learning_journey.entities.journey_evidence import JourneyEvidence
from app.domain.learning_journey.entities.learning_journey import LearningJourney
from app.domain.learning_journey.entities.learning_objective import (
    LearningObjective,
    ObjectiveKind,
)
from app.domain.learning_journey.entities.learning_session import LearningSession
from app.domain.learning_journey.value_objects.effort_estimate import EffortEstimate
from app.domain.learning_journey.value_objects.journey_state import JourneyState
from app.domain.learning_journey.value_objects.session_state import SessionState

NOW = datetime(2026, 7, 18, 14, 0, tzinfo=UTC)
TODAY = date(2026, 7, 18)
TOMORROW = date(2026, 7, 19)
YESTERDAY = date(2026, 7, 17)


def make_objective(
    oid: str = "obj-1",
    *,
    topic_id: str = "topic-a",
    kind: ObjectiveKind = ObjectiveKind.UNDERSTAND,
    sequence_index: int = 0,
    title: str | None = None,
) -> LearningObjective:
    return LearningObjective.create(
        oid,
        f"curr-{oid}",
        topic_id,
        kind,
        title=title or f"Objective {oid}",
        sequence_index=sequence_index,
    )


def make_session(
    sid: str = "sess-1",
    *,
    journey_id: str = "journey-1",
    sequence_index: int = 0,
    state: SessionState = SessionState.NOT_STARTED,
    objective_id: str | None = "obj-1",
    effort: EffortEstimate = EffortEstimate.MEDIUM,
) -> LearningSession:
    return LearningSession.create(
        sid,
        journey_id,
        sequence_index=sequence_index,
        state=state,
        estimated_effort=effort,
        objective_id=objective_id,
    )


def make_journey(
    *,
    journey_id: str = "journey-1",
    learner_id: str = "learner-1",
    topic_id: str = "topic-a",
    curriculum_id: str = "curr-1",
    state: JourneyState = JourneyState.ACTIVE,
    objectives: list[LearningObjective] | None = None,
    sessions: list[LearningSession] | None = None,
    evidence: list[JourneyEvidence] | None = None,
) -> LearningJourney:
    return LearningJourney.create(
        journey_id,
        learner_id,
        topic_id,
        curriculum_id,
        state=state,
        objectives=objectives or [make_objective()],
        sessions=sessions or [],
        evidence=evidence or [],
    )


def make_journey_engine() -> LearningJourneyEngine:
    return LearningJourneyEngine(
        clock=lambda: NOW,
        id_factory=lambda: "fixed",
    )


def active_journey(
    *,
    with_session: bool = False,
    session_state: SessionState = SessionState.NOT_STARTED,
) -> LearningJourney:
    engine = make_journey_engine()
    objectives = [make_objective()]
    sessions = None
    if with_session:
        sessions = [
            make_session(state=session_state, objective_id=objectives[0].objective_id)
        ]
    journey = engine.create_journey(
        learner_id="learner-1",
        topic_id="topic-a",
        curriculum_id="curr-1",
        journey_id="journey-1",
        objectives=objectives,
        sessions=sessions,
    )
    return engine.start_journey(journey)


def make_mission_engine(
    *,
    journey_engine: LearningJourneyEngine | None = None,
    session_runtime: LearningSessionRuntime | None = None,
    id_token: str = "m",
) -> MissionEngine:
    return MissionEngine(
        journey_engine=journey_engine or make_journey_engine(),
        session_runtime=session_runtime,
        clock=lambda: NOW,
        id_factory=lambda: id_token,
    )


def make_builder(
    *,
    journey_engine: LearningJourneyEngine | None = None,
) -> MissionBuilder:
    return MissionBuilder(
        journey_engine=journey_engine or make_journey_engine(),
        clock=lambda: NOW,
        id_factory=lambda: "b",
    )
