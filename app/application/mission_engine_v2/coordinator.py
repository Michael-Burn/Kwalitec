"""Coordinate Journey Engine → Session Runtime → Mission Factory → DTOs.

Orchestration only. Does not invent educational decisions.
"""

from __future__ import annotations

from datetime import date

from app.application.learning_journey.dto.journey_snapshot import JourneySnapshot
from app.application.mission_engine_v2.dispatcher import MissionDispatcher
from app.application.mission_engine_v2.dto.daily_mission import DailyMission
from app.application.mission_engine_v2.dto.mission_card import MissionCard
from app.application.mission_engine_v2.dto.mission_dashboard import MissionDashboard
from app.application.mission_engine_v2.dto.mission_execution import MissionExecution
from app.application.mission_engine_v2.dto.mission_timeline import MissionTimeline
from app.application.mission_engine_v2.exceptions import (
    MissionFactoryError,
    WorkloadExceeded,
)
from app.application.mission_engine_v2.lifecycle import MissionState
from app.application.mission_engine_v2.mission_factory import MissionFactory
from app.application.mission_engine_v2.policies.workload_policy import WorkloadPolicy
from app.application.mission_engine_v2.ports.curriculum_navigation_port import (
    CurriculumNavigationPort,
)
from app.application.mission_engine_v2.ports.journey_engine_port import (
    JourneyEnginePort,
)
from app.application.mission_engine_v2.ports.session_runtime_port import (
    SessionRuntimePort,
)
from app.application.mission_engine_v2.scheduler import MissionScheduler
from app.application.mission_engine_v2.validator import MissionValidator
from app.application.mission_engine_v2.workload_balancer import WorkloadBalancer


class MissionCoordinator:
    """Orchestrate mission generation, scheduling, and dashboard DTOs."""

    def __init__(
        self,
        *,
        factory: MissionFactory | None = None,
        scheduler: MissionScheduler | None = None,
        validator: MissionValidator | None = None,
        dispatcher: MissionDispatcher | None = None,
        balancer: WorkloadBalancer | None = None,
        journey_engine: JourneyEnginePort | None = None,
        session_runtime: SessionRuntimePort | None = None,
        navigation: CurriculumNavigationPort | None = None,
    ) -> None:
        self._journey_engine = journey_engine
        self._session_runtime = session_runtime
        self._navigation = navigation
        self._factory = factory or MissionFactory(
            journey_engine=self._journey_engine,
            session_runtime=self._session_runtime,
            navigation=self._navigation,
        )
        self._scheduler = scheduler or MissionScheduler()
        self._validator = validator or MissionValidator(navigation=self._navigation)
        self._dispatcher = dispatcher or MissionDispatcher()
        self._balancer = balancer or WorkloadBalancer()

    @property
    def factory(self) -> MissionFactory:
        return self._factory

    @property
    def scheduler(self) -> MissionScheduler:
        return self._scheduler

    @property
    def validator(self) -> MissionValidator:
        return self._validator

    @property
    def dispatcher(self) -> MissionDispatcher:
        return self._dispatcher

    @property
    def balancer(self) -> WorkloadBalancer:
        return self._balancer

    def _load_snapshot(self, journey_id: str) -> JourneySnapshot:
        if self._journey_engine is None:
            raise MissionFactoryError("Journey engine port is required")
        return self._journey_engine.snapshot(journey_id)

    def generate_today_mission(
        self,
        snapshot: JourneySnapshot,
        *,
        as_of_date: date,
        existing: list[DailyMission] | tuple[DailyMission, ...] = (),
        is_revision: bool = False,
    ) -> DailyMission:
        """Build + validate + place today's (or revision) mission."""
        self._validator.validate_journey_state(snapshot)
        if self._balancer.should_defer_new_work(existing) and not is_revision:
            assessment = self._balancer.assess(
                existing,
                journey_id=snapshot.journey_id,
            )
            if "open_capacity" in assessment.blocking_reasons:
                raise WorkloadExceeded("Cannot generate today: workload exceeded")
        mission = self._factory.create_from_snapshot(
            snapshot,
            scheduled_date=as_of_date,
            as_of_date=as_of_date,
            is_revision=is_revision,
            initial_state=MissionState.PLANNED,
        )
        if is_revision:
            mission = self._scheduler.schedule_revision(
                mission,
                as_of_date=as_of_date,
                existing=existing,
            )
        else:
            mission = self._scheduler.schedule_today(
                mission,
                as_of_date=as_of_date,
                existing=existing,
            )
        self._balancer.assert_can_add(existing, mission)
        self._validator.validate_new_mission(existing, mission, snapshot)
        return mission

    def generate_deferred_mission(
        self,
        snapshot: JourneySnapshot,
        *,
        as_of_date: date,
        existing: list[DailyMission] | tuple[DailyMission, ...] = (),
        target_date: date | None = None,
    ) -> DailyMission:
        """Build a deferred-slot mission."""
        self._validator.validate_journey_state(snapshot)
        mission = self._factory.create_from_snapshot(
            snapshot,
            scheduled_date=target_date or as_of_date,
            as_of_date=as_of_date,
            is_deferred=True,
            initial_state=MissionState.PLANNED,
        )
        mission = self._scheduler.schedule_deferred(
            mission,
            existing=existing,
            target_date=target_date,
        )
        self._balancer.assert_can_add(existing, mission)
        self._validator.validate_new_mission(existing, mission, snapshot)
        return mission

    def generate_future_mission(
        self,
        snapshot: JourneySnapshot,
        *,
        as_of_date: date,
        days_ahead: int = 1,
        existing: list[DailyMission] | tuple[DailyMission, ...] = (),
    ) -> DailyMission:
        """Build a future-queue mission."""
        self._validator.validate_journey_state(snapshot)
        mission = self._factory.create_from_snapshot(
            snapshot,
            scheduled_date=as_of_date,
            as_of_date=as_of_date,
            initial_state=MissionState.PLANNED,
        )
        mission = self._scheduler.schedule_future(
            mission,
            as_of_date=as_of_date,
            days_ahead=days_ahead,
            existing=existing,
        )
        self._balancer.assert_can_add(existing, mission)
        self._validator.validate_new_mission(existing, mission, snapshot)
        return mission

    def orchestrate(
        self,
        snapshot: JourneySnapshot,
        missions: list[DailyMission] | tuple[DailyMission, ...],
        *,
        as_of_date: date,
        ensure_today: bool = True,
    ) -> tuple[tuple[DailyMission, ...], MissionTimeline, MissionCard | None]:
        """Full pass: refresh missed → ensure today → timeline → card.

        Returns updated mission ledger, timeline, and today's card (if any).
        Does not mutate journey or runtime.
        """
        refreshed = self._scheduler.refresh_missed(missions, as_of_date=as_of_date)
        ledger = list(refreshed)
        timeline = self._scheduler.build_timeline(
            snapshot.learner_id,
            ledger,
            as_of_date=as_of_date,
        )
        if ensure_today and timeline.today is None:
            if not self._balancer.should_defer_new_work(ledger):
                new_mission = self.generate_today_mission(
                    snapshot,
                    as_of_date=as_of_date,
                    existing=ledger,
                )
                ledger.append(new_mission)
                timeline = self._scheduler.build_timeline(
                    snapshot.learner_id,
                    ledger,
                    as_of_date=as_of_date,
                )
        card = None
        if timeline.today is not None:
            phase = None
            if self._session_runtime is not None:
                phase = self._session_runtime.runtime_phase_for(
                    timeline.today.session_id
                )
            card = self._factory.build_card(timeline.today, runtime_phase=phase)
        return tuple(ledger), timeline, card

    def build_dashboard(
        self,
        learner_id: str,
        missions: list[DailyMission] | tuple[DailyMission, ...],
        *,
        as_of_date: date,
    ) -> MissionDashboard:
        """Assemble a MissionDashboard from the learner's mission ledger."""
        timeline = self._scheduler.build_timeline(
            learner_id,
            missions,
            as_of_date=as_of_date,
        )
        phase_lookup = self._session_runtime

        def to_card(mission: DailyMission) -> MissionCard:
            phase = None
            if phase_lookup is not None:
                phase = phase_lookup.runtime_phase_for(mission.session_id)
            return self._factory.build_card(mission, runtime_phase=phase)

        actives = WorkloadPolicy.active_missions(missions)
        assessment = self._balancer.assess(missions)
        return MissionDashboard(
            learner_id=learner_id,
            as_of_date=as_of_date,
            today=to_card(timeline.today) if timeline.today else None,
            deferred=tuple(to_card(m) for m in timeline.deferred),
            revision=tuple(to_card(m) for m in timeline.revision),
            missed=tuple(to_card(m) for m in timeline.missed),
            future=tuple(to_card(m) for m in timeline.future),
            timeline=timeline,
            active_mission_id=actives[0].mission_id if actives else None,
            open_mission_count=assessment.open_count,
            workload_ok=assessment.within_limits,
        )

    def deliver(
        self,
        mission: DailyMission,
        *,
        runtime_phase: str | None = None,
    ) -> MissionExecution:
        """Produce a delivery payload for ``mission``."""
        return self._dispatcher.dispatch(mission, runtime_phase=runtime_phase)
