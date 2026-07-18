"""Compose DailyMission artefacts from educational service inputs.

Factory flow:
    Journey Snapshot → Current Topic → Session Plan → Recommendation → Mission DTO

No educational reasoning. Consumes injected ports only.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, date, datetime
from uuid import uuid4

from app.application.learning_journey.dto.journey_snapshot import JourneySnapshot
from app.application.learning_journey.dto.recommendation_result import (
    RecommendationResult,
)
from app.application.learning_journey.dto.session_plan import SessionPlan
from app.application.mission_engine_v2.dto.daily_mission import DailyMission
from app.application.mission_engine_v2.dto.mission_card import MissionCard
from app.application.mission_engine_v2.exceptions import (
    MissionFactoryError,
    TopicUnavailable,
)
from app.application.mission_engine_v2.lifecycle import (
    DispatchAction,
    MissionSlot,
    MissionState,
)
from app.application.mission_engine_v2.policies.dispatch_policy import DispatchPolicy
from app.application.mission_engine_v2.policies.scheduling_policy import (
    SchedulingPolicy,
)
from app.application.mission_engine_v2.ports.curriculum_navigation_port import (
    CurriculumNavigationPort,
)
from app.application.mission_engine_v2.ports.journey_engine_port import (
    JourneyEnginePort,
)
from app.application.mission_engine_v2.ports.session_runtime_port import (
    SessionRuntimePort,
)
from app.domain.learning_journey.value_objects.journey_state import JourneyState


class MissionFactory:
    """Construct DailyMission / MissionCard from upstream educational ports.

    Does not decide which topic or objective to study — that authority
    remains with the Learning Journey Engine.
    """

    TERMINAL_JOURNEY_STATES = frozenset(
        {
            JourneyState.COMPLETED,
            JourneyState.ABANDONED,
            JourneyState.ARCHIVED,
        }
    )

    def __init__(
        self,
        *,
        journey_engine: JourneyEnginePort | None = None,
        session_runtime: SessionRuntimePort | None = None,
        navigation: CurriculumNavigationPort | None = None,
        clock=None,
        id_factory=None,
    ) -> None:
        self._journey_engine = journey_engine
        self._session_runtime = session_runtime
        self._navigation = navigation
        self._clock = clock or (lambda: datetime.now(tz=UTC))
        self._id_factory = id_factory or (lambda: uuid4().hex[:12])

    def create_from_snapshot(
        self,
        snapshot: JourneySnapshot,
        *,
        scheduled_date: date,
        as_of_date: date | None = None,
        session_plan: SessionPlan | None = None,
        recommendation: RecommendationResult | None = None,
        slot: MissionSlot | None = None,
        is_revision: bool = False,
        is_deferred: bool = False,
        mission_id: str | None = None,
        initial_state: MissionState = MissionState.PLANNED,
    ) -> DailyMission:
        """Compose one DailyMission from a Journey Snapshot and plan inputs."""
        self._assert_journey_usable(snapshot)
        as_of = as_of_date or scheduled_date
        plan = session_plan or self._resolve_session_plan(snapshot.journey_id)
        if plan is None:
            raise MissionFactoryError(
                f"No session plan available for journey {snapshot.journey_id}"
            )
        topic_id = self._resolve_topic_id(snapshot.topic_id)
        rec = recommendation
        if rec is None and self._journey_engine is not None:
            rec = self._journey_engine.recommendation_for(snapshot.journey_id)

        session_id = plan.session_id or f"sess-{self._id_factory()}"
        objective_id = plan.objective.objective_id if plan.objective else None
        effort = plan.expected_effort.value
        title = self._structural_title(snapshot, plan, topic_id)
        is_resume = self._detect_resume(session_id)
        outstanding = snapshot.reflection_summary.reflections_pending
        revision_debt = 1 if is_revision else 0
        if snapshot.recommendation is not None and (
            getattr(snapshot.recommendation, "kind", None) is not None
        ):
            kind = snapshot.recommendation.kind
            kind_value = getattr(kind, "value", str(kind))
            if "revision" in kind_value.lower():
                revision_debt = max(revision_debt, 1)

        explanation_keys = ()
        if rec is not None:
            explanation_keys = tuple(rec.rationale_tags)

        resolved_slot = slot or SchedulingPolicy.slot_for_date(
            scheduled_date,
            as_of_date=as_of,
            is_revision=is_revision,
            is_deferred=is_deferred,
        )
        state = initial_state
        if (
            state == MissionState.PLANNED
            and resolved_slot == MissionSlot.TODAY
            and scheduled_date == as_of
            and not is_revision
        ):
            state = MissionState.READY

        return DailyMission(
            mission_id=mission_id or f"mission-{self._id_factory()}",
            learner_id=snapshot.learner_id,
            journey_id=snapshot.journey_id,
            session_id=session_id,
            topic_id=topic_id,
            curriculum_id=snapshot.curriculum_id,
            scheduled_date=scheduled_date,
            slot=resolved_slot,
            state=state,
            objective_id=objective_id,
            effort=effort,
            title=title,
            sequence_index=plan.sequence_index,
            is_resume=is_resume,
            is_revision=is_revision or resolved_slot == MissionSlot.REVISION,
            explanation_keys=explanation_keys,
            outstanding_reflections=outstanding,
            revision_debt=revision_debt,
            created_at=self._clock(),
        )

    def create_from_journey_id(
        self,
        journey_id: str,
        *,
        scheduled_date: date,
        as_of_date: date | None = None,
        is_revision: bool = False,
        is_deferred: bool = False,
        mission_id: str | None = None,
    ) -> DailyMission:
        """Load snapshot via injected journey port and compose a mission."""
        if self._journey_engine is None:
            raise MissionFactoryError("Journey engine port is required")
        snapshot = self._journey_engine.snapshot(journey_id)
        plan = self._journey_engine.session_plan_for(journey_id)
        recommendation = self._journey_engine.recommendation_for(journey_id)
        return self.create_from_snapshot(
            snapshot,
            scheduled_date=scheduled_date,
            as_of_date=as_of_date,
            session_plan=plan,
            recommendation=recommendation,
            is_revision=is_revision,
            is_deferred=is_deferred,
            mission_id=mission_id,
        )

    def build_card(
        self,
        mission: DailyMission,
        *,
        runtime_phase: str | None = None,
        dispatch_action: DispatchAction | None = None,
    ) -> MissionCard:
        """Build a dashboard-ready MissionCard from a DailyMission."""
        action = dispatch_action or DispatchPolicy.decide(
            mission,
            runtime_phase=runtime_phase,
        )
        return MissionCard(
            mission_id=mission.mission_id,
            learner_id=mission.learner_id,
            journey_id=mission.journey_id,
            session_id=mission.session_id,
            topic_id=mission.topic_id,
            scheduled_date=mission.scheduled_date,
            slot=mission.slot,
            state=mission.state,
            title=mission.title,
            effort=mission.effort,
            dispatch_action=action,
            is_active=mission.state
            in {MissionState.ACTIVE, MissionState.PAUSED},
            is_completed=mission.state
            in {MissionState.COMPLETED, MissionState.ARCHIVED},
            is_resume=mission.is_resume or mission.state == MissionState.PAUSED,
            is_revision=mission.is_revision,
            objective_id=mission.objective_id,
            sequence_index=mission.sequence_index,
            explanation_keys=mission.explanation_keys,
        )

    def with_state(
        self,
        mission: DailyMission,
        state: MissionState,
        *,
        completed_at: datetime | None = None,
        archived_at: datetime | None = None,
        scheduled_date: date | None = None,
        slot: MissionSlot | None = None,
        is_revision: bool | None = None,
        is_resume: bool | None = None,
    ) -> DailyMission:
        """Return a copy of ``mission`` with updated lifecycle / schedule fields."""
        return replace(
            mission,
            state=state,
            completed_at=(
                completed_at
                if completed_at is not None
                else mission.completed_at
            ),
            archived_at=(
                archived_at if archived_at is not None else mission.archived_at
            ),
            scheduled_date=(
                scheduled_date
                if scheduled_date is not None
                else mission.scheduled_date
            ),
            slot=slot if slot is not None else mission.slot,
            is_revision=(
                is_revision if is_revision is not None else mission.is_revision
            ),
            is_resume=is_resume if is_resume is not None else mission.is_resume,
        )

    def _resolve_session_plan(self, journey_id: str) -> SessionPlan | None:
        if self._journey_engine is None:
            return None
        return self._journey_engine.session_plan_for(journey_id)

    def _resolve_topic_id(self, topic_id: str) -> str:
        if self._navigation is None:
            return topic_id
        if not self._navigation.topic_available(topic_id):
            raise TopicUnavailable(
                f"Topic {topic_id} is not present in curriculum navigation"
            )
        return topic_id

    def _detect_resume(self, session_id: str) -> bool:
        if self._session_runtime is None:
            return False
        phase = self._session_runtime.runtime_phase_for(session_id)
        return phase == "paused"

    def _assert_journey_usable(self, snapshot: JourneySnapshot) -> None:
        if snapshot.state in self.TERMINAL_JOURNEY_STATES:
            raise MissionFactoryError(
                f"Cannot build mission for journey in state {snapshot.state.value}"
            )

    @staticmethod
    def _structural_title(
        snapshot: JourneySnapshot,
        plan: SessionPlan,
        topic_id: str,
    ) -> str:
        if plan.objective is not None and plan.objective.title:
            return plan.objective.title
        if snapshot.current_objective is not None and snapshot.current_objective.title:
            return snapshot.current_objective.title
        if plan.is_existing_session and plan.session_id:
            return f"Session {plan.session_number}"
        return f"Topic {topic_id} session {plan.session_number}"
