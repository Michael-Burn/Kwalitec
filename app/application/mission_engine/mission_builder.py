"""Build DailyMission artefacts from journey / runtime / navigation inputs.

No educational reasoning. Consumes Learning Journey Engine, Learning Session
Runtime, and Curriculum Navigation Service outputs — never manipulates them.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, date, datetime
from uuid import uuid4

from app.application.learning_journey.engine import LearningJourneyEngine
from app.application.learning_session.runtime import (
    LearningSessionRuntime,
    SessionHandle,
)
from app.application.mission_engine.dto.daily_mission import DailyMission
from app.application.mission_engine.dto.mission_summary import MissionSummary
from app.application.mission_engine.exceptions import MissionBuildError
from app.application.mission_engine.mission_state import (
    DeliveryAction,
    MissionSlot,
    MissionState,
)
from app.application.mission_engine.policies.delivery_policy import DeliveryPolicy
from app.application.mission_engine.policies.scheduling_policy import SchedulingPolicy
from app.domain.curriculum.services.curriculum_navigation_service import (
    CurriculumNavigationService,
)
from app.domain.learning_journey.entities.learning_journey import LearningJourney
from app.domain.learning_journey.value_objects.journey_state import JourneyState
from app.domain.learning_journey.value_objects.session_state import SessionState


class MissionBuilder:
    """Construct DailyMission / MissionSummary from upstream engines.

    Does not decide which topic or objective to study — that authority
    remains with the Learning Journey Engine.
    """

    def __init__(
        self,
        *,
        journey_engine: LearningJourneyEngine | None = None,
        session_runtime: LearningSessionRuntime | None = None,
        navigation: CurriculumNavigationService | None = None,
        clock=None,
        id_factory=None,
    ) -> None:
        self._journey_engine = journey_engine or LearningJourneyEngine()
        self._session_runtime = session_runtime
        self._navigation = navigation
        self._clock = clock or (lambda: datetime.now(tz=UTC))
        self._id_factory = id_factory or (lambda: uuid4().hex[:12])

    def build_daily_mission(
        self,
        journey: LearningJourney,
        *,
        scheduled_date: date,
        as_of_date: date | None = None,
        slot: MissionSlot | None = None,
        is_revision: bool = False,
        session_handle: SessionHandle | None = None,
        mission_id: str | None = None,
        initial_state: MissionState = MissionState.SCHEDULED,
    ) -> DailyMission:
        """Build one DailyMission wrapping a single learning session plan.

        Raises:
            MissionBuildError: When journey state or session plan is unavailable.
        """
        self._assert_journey_usable(journey)
        as_of = as_of_date or scheduled_date
        plan = self._journey_engine.session_plan(journey)
        if plan is None:
            raise MissionBuildError(
                f"No session plan available for journey {journey.journey_id}"
            )

        session = self._resolve_session(journey, plan.session_id, session_handle)
        session_id = session.session_id if session is not None else (
            plan.session_id or f"sess-{self._id_factory()}"
        )
        sequence_index = (
            session.sequence_index if session is not None else plan.sequence_index
        )
        objective_id = (
            session.objective_id
            if session is not None and session.objective_id
            else (plan.objective.objective_id if plan.objective else None)
        )
        effort = (
            session.estimated_effort.value
            if session is not None
            else plan.expected_effort.value
        )
        topic_id = self._resolve_topic_id(journey)
        title = self._structural_title(journey, plan, topic_id)
        is_resume = self._detect_resume(session, session_handle)
        resolved_slot = slot or SchedulingPolicy.slot_for_date(
            scheduled_date,
            as_of_date=as_of,
            is_revision=is_revision,
        )
        state = initial_state
        if (
            state == MissionState.SCHEDULED
            and resolved_slot == MissionSlot.TODAY
            and scheduled_date == as_of
        ):
            state = MissionState.ACTIVE

        return DailyMission(
            mission_id=mission_id or f"mission-{self._id_factory()}",
            learner_id=journey.learner_id,
            journey_id=journey.journey_id,
            session_id=session_id,
            topic_id=topic_id,
            curriculum_id=journey.curriculum_id,
            scheduled_date=scheduled_date,
            slot=resolved_slot,
            state=state,
            objective_id=objective_id,
            effort=effort,
            title=title,
            sequence_index=sequence_index,
            is_resume=is_resume,
            is_revision=is_revision or resolved_slot == MissionSlot.REVISION,
            created_at=self._clock(),
        )

    def build_summary(
        self,
        mission: DailyMission,
        *,
        runtime_phase: str | None = None,
        delivery_action: DeliveryAction | None = None,
    ) -> MissionSummary:
        """Build a dashboard-ready MissionSummary from a DailyMission."""
        action = delivery_action or DeliveryPolicy.decide(
            mission,
            runtime_phase=runtime_phase,
        )
        return MissionSummary(
            mission_id=mission.mission_id,
            learner_id=mission.learner_id,
            journey_id=mission.journey_id,
            session_id=mission.session_id,
            topic_id=mission.topic_id,
            scheduled_date=mission.scheduled_date,
            slot=mission.slot,
            state=mission.state,
            title=mission.title,
            delivery_action=action,
            is_active=mission.state
            in {MissionState.ACTIVE, MissionState.IN_PROGRESS},
            is_completed=mission.state
            in {MissionState.COMPLETED, MissionState.ARCHIVED},
            is_resume=mission.is_resume,
            is_revision=mission.is_revision,
            objective_id=mission.objective_id,
            effort=mission.effort,
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
    ) -> DailyMission:
        """Return a copy of ``mission`` with updated lifecycle fields."""
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
        )

    def _assert_journey_usable(self, journey: LearningJourney) -> None:
        if journey.state in {
            JourneyState.COMPLETED,
            JourneyState.ABANDONED,
            JourneyState.ARCHIVED,
        }:
            raise MissionBuildError(
                f"Cannot build mission for journey in state {journey.state.value}"
            )

    def _resolve_topic_id(self, journey: LearningJourney) -> str:
        topic_id = journey.topic_id
        if self._navigation is None:
            return topic_id
        # Structural confirmation only — never selects the next topic.
        ordered = {t.value for t in self._navigation.ordered_topics()}
        if topic_id not in ordered:
            raise MissionBuildError(
                f"Topic {topic_id} is not present in curriculum navigation"
            )
        return topic_id

    def _resolve_session(
        self,
        journey: LearningJourney,
        plan_session_id: str | None,
        handle: SessionHandle | None,
    ):
        if handle is not None:
            return handle.session
        if plan_session_id is not None:
            for session in journey.ordered_sessions():
                if session.session_id == plan_session_id:
                    return session
        current = self._journey_engine.current_learning_session(journey)
        if current is not None:
            return current
        return self._journey_engine.next_learning_session(journey)

    @staticmethod
    def _detect_resume(session, handle: SessionHandle | None) -> bool:
        if handle is not None and handle.phase.value == "paused":
            return True
        if session is None:
            return False
        return session.state == SessionState.PAUSED

    @staticmethod
    def _structural_title(journey: LearningJourney, plan, topic_id: str) -> str:
        if plan.objective is not None and plan.objective.title:
            return plan.objective.title
        if plan.is_existing_session and plan.session_id:
            return f"Session {plan.session_number}"
        return f"Topic {topic_id} session {plan.session_number}"
