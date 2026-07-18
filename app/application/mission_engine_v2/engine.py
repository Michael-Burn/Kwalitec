"""Mission Engine 2.0 — public application interface.

Pure orchestration layer that composes Daily Mission commitments from
Version 2 educational services. Owns mission creation, scheduling,
lifecycle, and dashboard-ready DTOs. Does NOT own educational reasoning.

Implements Mission Adapter ``MissionEnginePort`` for dual-run routing.
"""

from __future__ import annotations

from datetime import UTC, date, datetime
from types import MappingProxyType
from uuid import uuid4

from app.application.learning_journey.dto.journey_snapshot import JourneySnapshot
from app.application.mission_adapter.dto.adapter_request import AdapterRequest
from app.application.mission_adapter.dto.mission_snapshot import MissionSnapshot
from app.application.mission_engine_v2.coordinator import MissionCoordinator
from app.application.mission_engine_v2.dispatcher import MissionDispatcher
from app.application.mission_engine_v2.dto.daily_mission import DailyMission
from app.application.mission_engine_v2.dto.mission_card import MissionCard
from app.application.mission_engine_v2.dto.mission_dashboard import MissionDashboard
from app.application.mission_engine_v2.dto.mission_execution import MissionExecution
from app.application.mission_engine_v2.dto.mission_timeline import MissionTimeline
from app.application.mission_engine_v2.exceptions import (
    InvalidMissionState,
    MissionAlreadyArchived,
    MissionAlreadyCompleted,
    MissionFactoryError,
    MissionNotFound,
)
from app.application.mission_engine_v2.lifecycle import (
    MissionState,
    MissionTransitionEvent,
)
from app.application.mission_engine_v2.mission_factory import MissionFactory
from app.application.mission_engine_v2.policies.lifecycle_policy import LifecyclePolicy
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


class MissionEngineV2:
    """Public facade for Mission Engine 2.0 orchestration.

    Maintains an in-memory mission ledger. Never persists. Never touches
    Flask / SQLAlchemy / UI. Depends only on injected educational ports.
    """

    ENGINE_ID = "v2"
    ENGINE_VERSION = "2.0.0"

    def __init__(
        self,
        *,
        journey_engine: JourneyEnginePort | None = None,
        session_runtime: SessionRuntimePort | None = None,
        navigation: CurriculumNavigationPort | None = None,
        coordinator: MissionCoordinator | None = None,
        factory: MissionFactory | None = None,
        scheduler: MissionScheduler | None = None,
        validator: MissionValidator | None = None,
        dispatcher: MissionDispatcher | None = None,
        balancer: WorkloadBalancer | None = None,
        available: bool = True,
        clock=None,
        id_factory=None,
    ) -> None:
        self._clock = clock or (lambda: datetime.now(tz=UTC))
        self._id_factory = id_factory or (lambda: uuid4().hex[:12])
        self._journey_engine = journey_engine
        self._session_runtime = session_runtime
        self._navigation = navigation
        self._available = available
        self._factory = factory or MissionFactory(
            journey_engine=self._journey_engine,
            session_runtime=self._session_runtime,
            navigation=self._navigation,
            clock=self._clock,
            id_factory=self._id_factory,
        )
        self._scheduler = scheduler or MissionScheduler()
        self._validator = validator or MissionValidator(navigation=self._navigation)
        self._dispatcher = dispatcher or MissionDispatcher()
        self._balancer = balancer or WorkloadBalancer()
        self._coordinator = coordinator or MissionCoordinator(
            factory=self._factory,
            scheduler=self._scheduler,
            validator=self._validator,
            dispatcher=self._dispatcher,
            balancer=self._balancer,
            journey_engine=self._journey_engine,
            session_runtime=self._session_runtime,
            navigation=self._navigation,
        )
        self._missions: dict[str, DailyMission] = {}
        self._archive: dict[str, DailyMission] = {}

    # ------------------------------------------------------------------
    # MissionEnginePort (adapter contract)
    # ------------------------------------------------------------------

    @property
    def engine_id(self) -> str:
        return self.ENGINE_ID

    @property
    def engine_version(self) -> str:
        return self.ENGINE_VERSION

    def is_available(self) -> bool:
        return self._available

    def set_available(self, available: bool) -> None:
        self._available = available

    def generate_mission(self, request: AdapterRequest) -> MissionSnapshot:
        """Adapter port: generate a mission commitment from request context."""
        journey_id = request.journey_id
        if not journey_id:
            raise MissionFactoryError("AdapterRequest.journey_id is required")
        day = self._clock().date()
        context_date = request.context.get("as_of_date") if request.context else None
        if context_date:
            day = date.fromisoformat(str(context_date))
        is_revision = bool(
            request.context.get("is_revision") if request.context else False
        )
        mission = self.generate_today_mission(
            journey_id,
            as_of_date=day,
            is_revision=is_revision,
        )
        return self._to_adapter_snapshot(mission, request)

    def resume_mission(self, request: AdapterRequest) -> MissionSnapshot:
        mission = self.resume_mission_by_id(self._require_mission_id(request))
        return self._to_adapter_snapshot(mission, request)

    def pause_mission(self, request: AdapterRequest) -> MissionSnapshot:
        mission = self.pause_mission_by_id(self._require_mission_id(request))
        return self._to_adapter_snapshot(mission, request)

    def skip_mission(self, request: AdapterRequest) -> MissionSnapshot:
        """Skip maps to defer (mission wrapper remains open in deferred slot)."""
        mission = self.defer_mission(self._require_mission_id(request))
        return self._to_adapter_snapshot(mission, request)

    def archive_mission(self, request: AdapterRequest) -> MissionSnapshot:
        mission = self.archive_mission_by_id(self._require_mission_id(request))
        return self._to_adapter_snapshot(mission, request)

    # ------------------------------------------------------------------
    # Ledger helpers
    # ------------------------------------------------------------------

    def all_missions(self) -> tuple[DailyMission, ...]:
        return tuple(self._missions.values())

    def missions_for_learner(self, learner_id: str) -> tuple[DailyMission, ...]:
        return tuple(
            m for m in self._missions.values() if m.learner_id == learner_id
        )

    def get_mission(self, mission_id: str) -> DailyMission:
        mission = self._missions.get(mission_id)
        if mission is None:
            archived = self._archive.get(mission_id)
            if archived is not None:
                return archived
            raise MissionNotFound(f"Mission {mission_id} not found")
        return mission

    def _store(self, mission: DailyMission) -> DailyMission:
        self._missions[mission.mission_id] = mission
        return mission

    def _replace(self, mission: DailyMission) -> DailyMission:
        if (
            mission.mission_id not in self._missions
            and mission.mission_id not in self._archive
        ):
            raise MissionNotFound(f"Mission {mission.mission_id} not found")
        if mission.state == MissionState.ARCHIVED:
            self._missions.pop(mission.mission_id, None)
            self._archive[mission.mission_id] = mission
        else:
            self._missions[mission.mission_id] = mission
        return mission

    def _require_mission_id(self, request: AdapterRequest) -> str:
        if not request.mission_id:
            raise MissionNotFound("AdapterRequest.mission_id is required")
        return request.mission_id

    def _resolve_snapshot(self, journey_id: str) -> JourneySnapshot:
        if self._journey_engine is None:
            raise MissionFactoryError("Journey engine port is required")
        return self._journey_engine.snapshot(journey_id)

    def _to_adapter_snapshot(
        self,
        mission: DailyMission,
        request: AdapterRequest,
    ) -> MissionSnapshot:
        return MissionSnapshot(
            mission_id=mission.mission_id,
            learner_id=mission.learner_id or request.learner_id,
            journey_id=mission.journey_id,
            topic_id=mission.topic_id,
            session_id=mission.session_id,
            effort=mission.effort,
            mission_type=mission.slot.value,
            is_revision=mission.is_revision,
            sequence_index=mission.sequence_index,
            explanation_keys=mission.explanation_keys,
            engine_id=self.engine_id,
            engine_version=self.engine_version,
            metadata=MappingProxyType(
                {
                    "state": mission.state.value,
                    "slot": mission.slot.value,
                    "operation": request.operation,
                }
            ),
        )

    # ------------------------------------------------------------------
    # Generation
    # ------------------------------------------------------------------

    def generate_today_mission(
        self,
        journey_id: str,
        *,
        as_of_date: date | None = None,
        is_revision: bool = False,
        snapshot: JourneySnapshot | None = None,
    ) -> DailyMission:
        """Generate today's (or revision) mission and store it."""
        day = as_of_date or self._clock().date()
        snap = snapshot or self._resolve_snapshot(journey_id)
        existing = self.missions_for_learner(snap.learner_id)
        mission = self._coordinator.generate_today_mission(
            snap,
            as_of_date=day,
            existing=existing,
            is_revision=is_revision,
        )
        return self._store(mission)

    def generate_deferred_mission(
        self,
        journey_id: str,
        *,
        as_of_date: date | None = None,
        target_date: date | None = None,
        snapshot: JourneySnapshot | None = None,
    ) -> DailyMission:
        day = as_of_date or self._clock().date()
        snap = snapshot or self._resolve_snapshot(journey_id)
        existing = self.missions_for_learner(snap.learner_id)
        mission = self._coordinator.generate_deferred_mission(
            snap,
            as_of_date=day,
            existing=existing,
            target_date=target_date,
        )
        return self._store(mission)

    def generate_future_mission(
        self,
        journey_id: str,
        *,
        as_of_date: date | None = None,
        days_ahead: int = 1,
        snapshot: JourneySnapshot | None = None,
    ) -> DailyMission:
        day = as_of_date or self._clock().date()
        snap = snapshot or self._resolve_snapshot(journey_id)
        existing = self.missions_for_learner(snap.learner_id)
        mission = self._coordinator.generate_future_mission(
            snap,
            as_of_date=day,
            days_ahead=days_ahead,
            existing=existing,
        )
        return self._store(mission)

    def schedule_revision_mission(
        self,
        journey_id: str,
        *,
        as_of_date: date | None = None,
        snapshot: JourneySnapshot | None = None,
    ) -> DailyMission:
        return self.generate_today_mission(
            journey_id,
            as_of_date=as_of_date,
            is_revision=True,
            snapshot=snapshot,
        )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def prepare_mission(self, mission_id: str) -> DailyMission:
        """PLANNED → READY."""
        return self._transition(mission_id, MissionTransitionEvent.PREPARE)

    def activate_mission(self, mission_id: str) -> DailyMission:
        """PLANNED/READY → ACTIVE (exactly one active)."""
        mission = self.get_mission(mission_id)
        self._validator.validate_one_active(
            self.missions_for_learner(mission.learner_id),
            activating_mission_id=mission_id,
        )
        return self._transition(mission_id, MissionTransitionEvent.ACTIVATE)

    def pause_mission_by_id(self, mission_id: str) -> DailyMission:
        return self._transition(mission_id, MissionTransitionEvent.PAUSE)

    def resume_mission_by_id(self, mission_id: str) -> DailyMission:
        mission = self.get_mission(mission_id)
        self._validator.validate_one_active(
            self.missions_for_learner(mission.learner_id),
            activating_mission_id=mission_id,
        )
        updated = self._transition(mission_id, MissionTransitionEvent.RESUME)
        return self._replace(
            self._factory.with_state(updated, updated.state, is_resume=True)
        )

    def defer_mission(
        self,
        mission_id: str,
        *,
        target_date: date | None = None,
    ) -> DailyMission:
        mission = self.get_mission(mission_id)
        updated = self._scheduler.schedule_deferred(
            mission,
            existing=self.missions_for_learner(mission.learner_id),
            target_date=target_date,
        )
        return self._replace(updated)

    def reschedule_mission(
        self,
        mission_id: str,
        *,
        new_date: date,
        as_of_date: date | None = None,
        is_revision: bool = False,
        is_deferred: bool = False,
    ) -> DailyMission:
        mission = self.get_mission(mission_id)
        day = as_of_date or self._clock().date()
        updated = self._scheduler.reschedule(
            mission,
            new_date=new_date,
            as_of_date=day,
            existing=self.missions_for_learner(mission.learner_id),
            is_revision=is_revision,
            is_deferred=is_deferred,
        )
        return self._replace(updated)

    def complete_mission(self, mission_id: str) -> DailyMission:
        mission = self.get_mission(mission_id)
        if mission.state == MissionState.ARCHIVED:
            raise MissionAlreadyArchived(
                f"Mission {mission_id} is already archived"
            )
        if mission.state == MissionState.COMPLETED:
            raise MissionAlreadyCompleted(
                f"Mission {mission_id} is already completed"
            )
        LifecyclePolicy.assert_completable(mission.state)
        nxt = LifecyclePolicy.resolve(
            mission.state,
            MissionTransitionEvent.COMPLETE,
        )
        updated = self._factory.with_state(
            mission,
            nxt,
            completed_at=self._clock(),
        )
        return self._replace(updated)

    def archive_mission_by_id(self, mission_id: str) -> DailyMission:
        mission = self.get_mission(mission_id)
        if mission.state == MissionState.ARCHIVED:
            raise MissionAlreadyArchived(
                f"Mission {mission_id} is already archived"
            )
        if mission.state != MissionState.COMPLETED:
            if mission.state in {MissionState.ACTIVE, MissionState.PAUSED}:
                mission = self.complete_mission(mission_id)
            else:
                raise InvalidMissionState(
                    f"Cannot archive mission in state {mission.state.value}"
                )
        nxt = LifecyclePolicy.resolve(
            mission.state,
            MissionTransitionEvent.ARCHIVE,
        )
        archived = self._factory.with_state(
            mission,
            nxt,
            archived_at=self._clock(),
        )
        return self._replace(archived)

    def _transition(
        self,
        mission_id: str,
        event: MissionTransitionEvent,
    ) -> DailyMission:
        mission = self.get_mission(mission_id)
        nxt = LifecyclePolicy.resolve(mission.state, event)
        return self._replace(self._factory.with_state(mission, nxt))

    # ------------------------------------------------------------------
    # Queries / delivery
    # ------------------------------------------------------------------

    def get_timeline(
        self,
        learner_id: str,
        *,
        as_of_date: date | None = None,
        refresh_missed: bool = True,
    ) -> MissionTimeline:
        day = as_of_date or self._clock().date()
        missions = self.missions_for_learner(learner_id)
        if refresh_missed:
            refreshed = self._scheduler.refresh_missed(missions, as_of_date=day)
            for mission in refreshed:
                self._missions[mission.mission_id] = mission
            missions = refreshed
        return self._scheduler.build_timeline(
            learner_id,
            missions,
            as_of_date=day,
        )

    def get_today_mission(
        self,
        learner_id: str,
        *,
        as_of_date: date | None = None,
    ) -> DailyMission | None:
        return self.get_timeline(learner_id, as_of_date=as_of_date).today

    def get_dashboard(
        self,
        learner_id: str,
        *,
        as_of_date: date | None = None,
    ) -> MissionDashboard:
        day = as_of_date or self._clock().date()
        timeline = self.get_timeline(learner_id, as_of_date=day)
        return self._coordinator.build_dashboard(
            learner_id,
            timeline.ordered,
            as_of_date=day,
        )

    def summarize(
        self,
        mission_id: str,
        *,
        runtime_phase: str | None = None,
    ) -> MissionCard:
        mission = self.get_mission(mission_id)
        return self._factory.build_card(mission, runtime_phase=runtime_phase)

    def deliver(
        self,
        mission_id: str,
        *,
        runtime_phase: str | None = None,
    ) -> MissionExecution:
        mission = self.get_mission(mission_id)
        return self._dispatcher.dispatch(mission, runtime_phase=runtime_phase)

    def orchestrate(
        self,
        journey_id: str,
        *,
        as_of_date: date | None = None,
        ensure_today: bool = True,
        snapshot: JourneySnapshot | None = None,
    ) -> tuple[MissionTimeline, MissionCard | None]:
        day = as_of_date or self._clock().date()
        snap = snapshot or self._resolve_snapshot(journey_id)
        existing = self.missions_for_learner(snap.learner_id)
        ledger, timeline, card = self._coordinator.orchestrate(
            snap,
            existing,
            as_of_date=day,
            ensure_today=ensure_today,
        )
        for mission in ledger:
            self._missions[mission.mission_id] = mission
        return timeline, card

    def archived_missions(
        self,
        *,
        learner_id: str | None = None,
        journey_id: str | None = None,
    ) -> tuple[DailyMission, ...]:
        items = tuple(self._archive.values())
        if learner_id is not None:
            return tuple(m for m in items if m.learner_id == learner_id)
        if journey_id is not None:
            return tuple(m for m in items if m.journey_id == journey_id)
        return items
