"""Shared helpers for Learning Session Runtime application tests."""

from __future__ import annotations

from datetime import UTC, datetime

from app.application.learning_session.runtime import (
    LearningSessionRuntime,
    SessionHandle,
)
from app.application.learning_session.runtime_phase import RuntimePhase
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
from app.domain.learning_journey.value_objects.effort_estimate import EffortEstimate
from app.domain.learning_journey.value_objects.journey_state import JourneyState
from app.domain.learning_journey.value_objects.session_state import SessionState

NOW = datetime(2026, 7, 18, 14, 0, tzinfo=UTC)


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
    objective_id: str | None = "obj-1",
    effort: EffortEstimate = EffortEstimate.MEDIUM,
    reflection: JourneyReflection | None = None,
    evidence: list[JourneyEvidence] | None = None,
    actual_duration_minutes: int | None = None,
) -> LearningSession:
    return LearningSession.create(
        sid,
        journey_id,
        sequence_index=sequence_index,
        state=state,
        estimated_effort=effort,
        objective_id=objective_id,
        reflection=reflection,
        evidence=evidence,
        actual_duration_minutes=actual_duration_minutes,
    )


def make_evidence(
    jeid: str = "je-1",
    *,
    evidence_id: str = "ev-1",
    journey_id: str = "journey-1",
    session_id: str | None = "sess-1",
    objective_id: str | None = "obj-1",
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


def make_runtime() -> LearningSessionRuntime:
    return LearningSessionRuntime(
        clock=lambda: NOW,
        id_factory=lambda: "fixed",
    )


def active_handle(
    runtime: LearningSessionRuntime | None = None,
) -> SessionHandle:
    rt = runtime or make_runtime()
    handle = rt.create_session(make_journey(), objectives=[make_objective()])
    handle = rt.prepare_session(handle)
    return rt.start_session(handle)


def completed_handle(
    runtime: LearningSessionRuntime | None = None,
    *,
    with_evidence: bool = True,
    with_reflection: bool = False,
) -> SessionHandle:
    rt = runtime or make_runtime()
    handle = active_handle(rt)
    if with_evidence:
        handle, _, _ = rt.collect_evidence(handle)
    handle = rt.complete_session(handle, actual_duration_minutes=25)
    if with_reflection:
        handle, _ = rt.collect_reflection(
            handle,
            summary="Covered definitions",
            challenges="Edge cases unclear",
            questions_remaining=["How does X relate?"],
            confidence=ReflectionConfidence.MEDIUM,
            next_intention="Practice tomorrow",
        )
    return handle


def phase_handle(
    phase: RuntimePhase,
    *,
    runtime: LearningSessionRuntime | None = None,
) -> SessionHandle:
    """Build a handle advanced to the requested phase (happy path)."""
    rt = runtime or make_runtime()
    handle = rt.create_session(make_journey(), objectives=[make_objective()])
    if phase == RuntimePhase.PLANNED:
        return handle
    handle = rt.prepare_session(handle)
    if phase == RuntimePhase.READY:
        return handle
    handle = rt.start_session(handle)
    if phase == RuntimePhase.ACTIVE:
        return handle
    if phase == RuntimePhase.PAUSED:
        return rt.pause_session(handle)
    handle = rt.complete_session(handle, actual_duration_minutes=20)
    if phase == RuntimePhase.COMPLETED:
        return handle
    handle, _ = rt.collect_reflection(
        handle,
        summary="Done",
        challenges="None major",
        confidence=ReflectionConfidence.HIGH,
    )
    return rt.archive_session(handle)
