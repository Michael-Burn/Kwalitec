"""Coordinate Journey Engine → Runtime → Mission → Dashboard DTO.

Orchestration only. Does not invent educational decisions.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import date

from app.application.learning_journey.engine import LearningJourneyEngine
from app.application.learning_session.runtime import (
    LearningSessionRuntime,
    SessionHandle,
)
from app.application.mission_engine.dto.daily_mission import DailyMission
from app.application.mission_engine.dto.mission_delivery import MissionDelivery
from app.application.mission_engine.dto.mission_schedule import MissionSchedule
from app.application.mission_engine.dto.mission_summary import MissionSummary
from app.application.mission_engine.exceptions import WorkloadExceeded
from app.application.mission_engine.mission_archive import MissionArchive
from app.application.mission_engine.mission_builder import MissionBuilder
from app.application.mission_engine.mission_dispatcher import MissionDispatcher
from app.application.mission_engine.mission_scheduler import MissionScheduler
from app.application.mission_engine.mission_state import MissionSlot, MissionState
from app.application.mission_engine.mission_validator import MissionValidator
from app.application.mission_engine.policies.workload_policy import WorkloadPolicy
from app.domain.curriculum.services.curriculum_navigation_service import (
    CurriculumNavigationService,
)
from app.domain.learning_journey.entities.learning_journey import LearningJourney


class MissionCoordinator:
    """Orchestrate mission generation, scheduling, and delivery DTOs."""

    def __init__(
        self,
        *,
        builder: MissionBuilder | None = None,
        scheduler: MissionScheduler | None = None,
        validator: MissionValidator | None = None,
        dispatcher: MissionDispatcher | None = None,
        archive: MissionArchive | None = None,
        journey_engine: LearningJourneyEngine | None = None,
        session_runtime: LearningSessionRuntime | None = None,
        navigation: CurriculumNavigationService | None = None,
    ) -> None:
        self._journey_engine = journey_engine or LearningJourneyEngine()
        self._session_runtime = session_runtime
        self._navigation = navigation
        self._builder = builder or MissionBuilder(
            journey_engine=self._journey_engine,
            session_runtime=self._session_runtime,
            navigation=self._navigation,
        )
        self._scheduler = scheduler or MissionScheduler()
        self._validator = validator or MissionValidator()
        self._dispatcher = dispatcher or MissionDispatcher()
        self._archive = archive or MissionArchive()

    @property
    def archive(self) -> MissionArchive:
        return self._archive

    @property
    def builder(self) -> MissionBuilder:
        return self._builder

    @property
    def scheduler(self) -> MissionScheduler:
        return self._scheduler

    @property
    def validator(self) -> MissionValidator:
        return self._validator

    @property
    def dispatcher(self) -> MissionDispatcher:
        return self._dispatcher

    def generate_today_mission(
        self,
        journey: LearningJourney,
        *,
        as_of_date: date,
        existing: list[DailyMission] | tuple[DailyMission, ...] = (),
        session_handle: SessionHandle | None = None,
        is_revision: bool = False,
    ) -> DailyMission:
        """Build + validate + place today's mission for ``journey``."""
        self._validator.validate_journey_state(journey)
        mission = self._builder.build_daily_mission(
            journey,
            scheduled_date=as_of_date,
            as_of_date=as_of_date,
            slot=MissionSlot.REVISION if is_revision else MissionSlot.TODAY,
            is_revision=is_revision,
            session_handle=session_handle,
            initial_state=MissionState.SCHEDULED,
        )
        if is_revision:
            if not WorkloadPolicy.can_add_revision(existing):
                raise WorkloadExceeded("Revision mission capacity exceeded")
            # Revision stays SCHEDULED in REVISION slot — does not claim ACTIVE.
            mission = replace(
                mission,
                slot=MissionSlot.REVISION,
                state=MissionState.SCHEDULED,
                is_revision=True,
            )
        else:
            mission = self._scheduler.schedule_today(
                mission,
                as_of_date=as_of_date,
                existing=existing,
            )
        self._validator.validate_new_mission(existing, mission, journey)
        return mission

    def generate_tomorrow_mission(
        self,
        journey: LearningJourney,
        *,
        as_of_date: date,
        existing: list[DailyMission] | tuple[DailyMission, ...] = (),
    ) -> DailyMission:
        """Build + schedule tomorrow's mission."""
        self._validator.validate_journey_state(journey)
        mission = self._builder.build_daily_mission(
            journey,
            scheduled_date=as_of_date,
            as_of_date=as_of_date,
            initial_state=MissionState.SCHEDULED,
        )
        mission = self._scheduler.schedule_tomorrow(mission, as_of_date=as_of_date)
        self._validator.validate_new_mission(existing, mission, journey)
        return mission

    def orchestrate(
        self,
        journey: LearningJourney,
        missions: list[DailyMission] | tuple[DailyMission, ...],
        *,
        as_of_date: date,
        session_handle: SessionHandle | None = None,
        ensure_today: bool = True,
    ) -> tuple[tuple[DailyMission, ...], MissionSchedule, MissionSummary | None]:
        """Full pass: refresh missed → ensure today → schedule → summary.

        Returns updated mission ledger, schedule, and today's summary (if any).
        Does not mutate journey or runtime.
        """
        refreshed = self._scheduler.refresh_missed(missions, as_of_date=as_of_date)
        ledger = list(refreshed)
        today = self._scheduler.build_schedule(
            journey.learner_id,
            ledger,
            as_of_date=as_of_date,
        ).today
        if ensure_today and today is None:
            new_mission = self.generate_today_mission(
                journey,
                as_of_date=as_of_date,
                existing=ledger,
                session_handle=session_handle,
            )
            ledger.append(new_mission)
        schedule = self._scheduler.build_schedule(
            journey.learner_id,
            ledger,
            as_of_date=as_of_date,
        )
        summary = None
        if schedule.today is not None:
            phase = session_handle.phase.value if session_handle else None
            summary = self._builder.build_summary(
                schedule.today,
                runtime_phase=phase,
            )
        return tuple(ledger), schedule, summary

    def dashboard_summary(
        self,
        mission: DailyMission,
        *,
        runtime_phase: str | None = None,
    ) -> MissionSummary:
        """Produce a dashboard-ready summary for ``mission``."""
        return self._builder.build_summary(mission, runtime_phase=runtime_phase)

    def deliver(
        self,
        mission: DailyMission,
        *,
        runtime_phase: str | None = None,
    ) -> MissionDelivery:
        """Produce a delivery payload for ``mission``."""
        return self._dispatcher.dispatch(mission, runtime_phase=runtime_phase)
