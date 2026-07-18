"""Shared helpers for Mission Engine 2.0 (mission_engine_v2) tests."""

from __future__ import annotations

from datetime import UTC, date, datetime

from app.application.learning_journey.dto.journey_snapshot import (
    EvidenceSummary,
    JourneySnapshot,
    ReflectionSummary,
)
from app.application.learning_journey.dto.recommendation_result import (
    RecommendationResult,
)
from app.application.learning_journey.dto.session_plan import SessionPlan
from app.application.mission_adapter.dto.adapter_request import AdapterRequest
from app.application.mission_engine_v2.dto.daily_mission import DailyMission
from app.application.mission_engine_v2.engine import MissionEngineV2
from app.application.mission_engine_v2.lifecycle import MissionSlot, MissionState
from app.domain.learning_journey.entities.learning_objective import (
    LearningObjective,
    ObjectiveKind,
)
from app.domain.learning_journey.entities.learning_session import LearningSession
from app.domain.learning_journey.value_objects.completion_status import CompletionStatus
from app.domain.learning_journey.value_objects.effort_estimate import EffortEstimate
from app.domain.learning_journey.value_objects.journey_state import JourneyState
from app.domain.learning_journey.value_objects.session_state import SessionState

NOW = datetime(2026, 7, 18, 14, 0, tzinfo=UTC)
TODAY = date(2026, 7, 18)


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
) -> LearningSession:
    return LearningSession.create(
        sid,
        journey_id,
        sequence_index=sequence_index,
        state=state,
        estimated_effort=EffortEstimate.MEDIUM,
        objective_id=objective_id,
    )


def make_session_plan(
    *,
    session_id: str | None = "sess-1",
    sequence_index: int = 0,
    session_number: int = 1,
    effort: EffortEstimate = EffortEstimate.MEDIUM,
    objective: LearningObjective | None = None,
    is_existing: bool = True,
) -> SessionPlan:
    return SessionPlan(
        session_number=session_number,
        sequence_index=sequence_index,
        session_id=session_id,
        objective=objective if objective is not None else make_objective(),
        expected_effort=effort,
        recommended_activities=("study", "practice"),
        is_existing_session=is_existing,
    )


def make_snapshot(
    *,
    journey_id: str = "journey-1",
    learner_id: str = "learner-1",
    topic_id: str = "topic-a",
    curriculum_id: str = "curr-1",
    state: JourneyState = JourneyState.ACTIVE,
    sessions: tuple[LearningSession, ...] | None = None,
    reflections_pending: int = 0,
    recommendation=None,
) -> JourneySnapshot:
    sess = sessions if sessions is not None else (make_session(),)
    return JourneySnapshot(
        journey_id=journey_id,
        learner_id=learner_id,
        topic_id=topic_id,
        curriculum_id=curriculum_id,
        state=state,
        completion_status=CompletionStatus.IN_PROGRESS,
        meets_completion_criteria=False,
        current_objective=make_objective(),
        sessions=sess,
        evidence_summary=EvidenceSummary(
            evidence_count=0,
            evidence_confidence="none",
            sessions_with_evidence=0,
        ),
        reflection_summary=ReflectionSummary(
            reflections_captured=0,
            reflections_pending=reflections_pending,
            completed_sessions_owing_reflection=reflections_pending,
        ),
        recommendation=recommendation,
        objectives_total=1,
        objectives_addressed=0,
        sessions_completed=0,
    )


def make_recommendation(
    *,
    rationale_tags: tuple[str, ...] = ("continue", "session"),
) -> RecommendationResult:
    return RecommendationResult(
        recommendation=None,
        kind=None,
        reason="Continue current session",
        confidence_explanation="structural continuity",
        rationale_tags=rationale_tags,
    )


def make_mission(
    *,
    mission_id: str = "mission-1",
    learner_id: str = "learner-1",
    journey_id: str = "journey-1",
    session_id: str = "sess-1",
    topic_id: str = "topic-a",
    curriculum_id: str = "curr-1",
    scheduled_date: date = TODAY,
    slot: MissionSlot = MissionSlot.TODAY,
    state: MissionState = MissionState.READY,
    effort: str = "medium",
    title: str = "Objective obj-1",
    sequence_index: int = 0,
    is_resume: bool = False,
    is_revision: bool = False,
    explanation_keys: tuple[str, ...] = (),
    outstanding_reflections: int = 0,
    revision_debt: int = 0,
    objective_id: str | None = "obj-1",
) -> DailyMission:
    return DailyMission(
        mission_id=mission_id,
        learner_id=learner_id,
        journey_id=journey_id,
        session_id=session_id,
        topic_id=topic_id,
        curriculum_id=curriculum_id,
        scheduled_date=scheduled_date,
        slot=slot,
        state=state,
        objective_id=objective_id,
        effort=effort,
        title=title,
        sequence_index=sequence_index,
        is_resume=is_resume,
        is_revision=is_revision,
        explanation_keys=explanation_keys,
        outstanding_reflections=outstanding_reflections,
        revision_debt=revision_debt,
        created_at=NOW,
    )


class FakeJourneyEngine:
    """JourneyEnginePort double."""

    def __init__(
        self,
        snapshot: JourneySnapshot | None = None,
        plan: SessionPlan | None = None,
        recommendation: RecommendationResult | None = None,
    ) -> None:
        self._snapshot = snapshot or make_snapshot()
        self._plan = plan if plan is not None else make_session_plan()
        self._recommendation = (
            recommendation if recommendation is not None else make_recommendation()
        )
        self.calls: list[str] = []

    def snapshot(self, journey_id: str) -> JourneySnapshot:
        self.calls.append(f"snapshot:{journey_id}")
        if self._snapshot.journey_id != journey_id:
            # Allow lookup by requested id via shallow override
            from dataclasses import replace

            return replace(self._snapshot, journey_id=journey_id)
        return self._snapshot

    def session_plan_for(self, journey_id: str) -> SessionPlan | None:
        self.calls.append(f"session_plan:{journey_id}")
        return self._plan

    def recommendation_for(self, journey_id: str) -> RecommendationResult | None:
        self.calls.append(f"recommendation:{journey_id}")
        return self._recommendation


class FakeSessionRuntime:
    """SessionRuntimePort double."""

    def __init__(
        self,
        phases: dict[str, str] | None = None,
        reflections: dict[str, bool] | None = None,
    ) -> None:
        self._phases = phases or {}
        self._reflections = reflections or {}

    def runtime_phase_for(self, session_id: str) -> str | None:
        return self._phases.get(session_id)

    def has_outstanding_reflection(self, session_id: str) -> bool:
        return self._reflections.get(session_id, False)


class FakeNavigation:
    """CurriculumNavigationPort double."""

    def __init__(self, topics: tuple[str, ...] = ("topic-a", "topic-b")) -> None:
        self._topics = topics

    def topic_available(self, topic_id: str) -> bool:
        return topic_id in self._topics

    def ordered_topic_ids(self) -> tuple[str, ...]:
        return self._topics


def make_engine(
    *,
    journey: FakeJourneyEngine | None = None,
    runtime: FakeSessionRuntime | None = None,
    navigation: FakeNavigation | None = None,
    available: bool = True,
) -> MissionEngineV2:
    return MissionEngineV2(
        journey_engine=journey or FakeJourneyEngine(),
        session_runtime=runtime or FakeSessionRuntime(),
        navigation=navigation or FakeNavigation(),
        available=available,
        clock=lambda: NOW,
        id_factory=lambda: "fixed12abcd",
    )


def make_adapter_request(
    *,
    operation: str = "generate",
    learner_id: str = "learner-1",
    journey_id: str = "journey-1",
    mission_id: str | None = None,
    context: dict | None = None,
) -> AdapterRequest:
    from types import MappingProxyType

    return AdapterRequest(
        operation=operation,
        learner_id=learner_id,
        journey_id=journey_id,
        mission_id=mission_id,
        context=MappingProxyType(context or {"as_of_date": TODAY.isoformat()}),
    )
