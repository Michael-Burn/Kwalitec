"""Mission Engine 2.0 — public application interface.

Coordinates Curriculum Graph → Learning Journey Engine → Learning Session
Runtime → Daily Mission → Student Dashboard DTOs.

Responsible only for mission generation, scheduling, lifecycle, and delivery.
Educational reasoning belongs in the Journey Engine / Session Runtime.
"""

from __future__ import annotations

from datetime import UTC, date, datetime
from uuid import uuid4

from app.application.learning_journey.engine import LearningJourneyEngine
from app.application.learning_session.runtime import (
    LearningSessionRuntime,
    SessionHandle,
)
from app.application.mission_engine.dto.daily_mission import DailyMission
from app.application.mission_engine.dto.mission_delivery import MissionDelivery
from app.application.mission_engine.dto.mission_schedule import MissionSchedule
from app.application.mission_engine.dto.mission_summary import MissionSummary
from app.application.mission_engine.exceptions import (
    InvalidMissionState,
    MissionAlreadyArchived,
    MissionAlreadyCompleted,
    MissionNotFound,
)
from app.application.mission_engine.mission_archive import MissionArchive
from app.application.mission_engine.mission_builder import MissionBuilder
from app.application.mission_engine.mission_coordinator import MissionCoordinator
from app.application.mission_engine.mission_dispatcher import MissionDispatcher
from app.application.mission_engine.mission_scheduler import MissionScheduler
from app.application.mission_engine.mission_state import MissionState
from app.application.mission_engine.mission_validator import MissionValidator
from app.domain.curriculum.services.curriculum_navigation_service import (
    CurriculumNavigationService,
)
from app.domain.learning_journey.entities.learning_journey import LearningJourney


class MissionEngine:
    """Public facade for Mission Engine 2.0 orchestration.

    Maintains an in-memory mission ledger. Never persists. Never touches
    Flask / SQLAlchemy / UI. Never mutates Journey Engine or Session Runtime
    aggregates — callers remain responsible for those systems.
    """

    def __init__(
        self,
        *,
        journey_engine: LearningJourneyEngine | None = None,
        session_runtime: LearningSessionRuntime | None = None,
        navigation: CurriculumNavigationService | None = None,
        coordinator: MissionCoordinator | None = None,
        builder: MissionBuilder | None = None,
        scheduler: MissionScheduler | None = None,
        validator: MissionValidator | None = None,
        dispatcher: MissionDispatcher | None = None,
        archive: MissionArchive | None = None,
        clock=None,
        id_factory=None,
    ) -> None:
        self._clock = clock or (lambda: datetime.now(tz=UTC))
        self._id_factory = id_factory or (lambda: uuid4().hex[:12])
        self._journey_engine = journey_engine or LearningJourneyEngine(
            clock=self._clock,
            id_factory=self._id_factory,
        )
        self._session_runtime = session_runtime
        self._navigation = navigation
        self._archive = archive or MissionArchive(clock=self._clock)
        self._builder = builder or MissionBuilder(
            journey_engine=self._journey_engine,
            session_runtime=self._session_runtime,
            navigation=self._navigation,
            clock=self._clock,
            id_factory=self._id_factory,
        )
        self._scheduler = scheduler or MissionScheduler()
        self._validator = validator or MissionValidator()
        self._dispatcher = dispatcher or MissionDispatcher()
        self._coordinator = coordinator or MissionCoordinator(
            builder=self._builder,
            scheduler=self._scheduler,
            validator=self._validator,
            dispatcher=self._dispatcher,
            archive=self._archive,
            journey_engine=self._journey_engine,
            session_runtime=self._session_runtime,
            navigation=self._navigation,
        )
        self._missions: dict[str, DailyMission] = {}

    # ------------------------------------------------------------------
    # Ledger helpers
    # ------------------------------------------------------------------

    def all_missions(self) -> tuple[DailyMission, ...]:
        """Return all known missions (unordered ledger snapshot)."""
        return tuple(self._missions.values())

    def missions_for_learner(self, learner_id: str) -> tuple[DailyMission, ...]:
        """Return missions for a learner."""
        return tuple(
            m for m in self._missions.values() if m.learner_id == learner_id
        )

    def get_mission(self, mission_id: str) -> DailyMission:
        """Load a mission by id.

        Raises:
            MissionNotFound: When the mission is unknown.
        """
        mission = self._missions.get(mission_id)
        if mission is None:
            archived = self._archive.find(mission_id)
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
            and self._archive.find(mission.mission_id) is None
        ):
            raise MissionNotFound(f"Mission {mission.mission_id} not found")
        if mission.state == MissionState.ARCHIVED:
            self._missions.pop(mission.mission_id, None)
        else:
            self._missions[mission.mission_id] = mission
        return mission

    # ------------------------------------------------------------------
    # Generation
    # ------------------------------------------------------------------

    def generate_today_mission(
        self,
        journey: LearningJourney,
        *,
        as_of_date: date | None = None,
        session_handle: SessionHandle | None = None,
        is_revision: bool = False,
    ) -> DailyMission:
        """Generate today's mission for ``journey`` and store it."""
        day = as_of_date or self._clock().date()
        existing = self.missions_for_learner(journey.learner_id)
        mission = self._coordinator.generate_today_mission(
            journey,
            as_of_date=day,
            existing=existing,
            session_handle=session_handle,
            is_revision=is_revision,
        )
        return self._store(mission)

    def generate_tomorrow_mission(
        self,
        journey: LearningJourney,
        *,
        as_of_date: date | None = None,
    ) -> DailyMission:
        """Generate tomorrow's mission for ``journey`` and store it."""
        day = as_of_date or self._clock().date()
        existing = self.missions_for_learner(journey.learner_id)
        mission = self._coordinator.generate_tomorrow_mission(
            journey,
            as_of_date=day,
            existing=existing,
        )
        return self._store(mission)

    def schedule_revision_mission(
        self,
        journey: LearningJourney,
        *,
        as_of_date: date | None = None,
        session_handle: SessionHandle | None = None,
    ) -> DailyMission:
        """Generate a revision-slot mission (still one session)."""
        return self.generate_today_mission(
            journey,
            as_of_date=as_of_date,
            session_handle=session_handle,
            is_revision=True,
        )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start_mission(self, mission_id: str) -> DailyMission:
        """Mark mission IN_PROGRESS (session execution begins elsewhere)."""
        mission = self.get_mission(mission_id)
        updated = self._scheduler.start(mission)
        return self._replace(updated)

    def defer_mission(
        self,
        mission_id: str,
        *,
        target_date: date | None = None,
    ) -> DailyMission:
        """Defer an incomplete mission."""
        mission = self.get_mission(mission_id)
        updated = self._scheduler.defer(
            mission,
            existing=self.missions_for_learner(mission.learner_id),
            target_date=target_date,
        )
        return self._replace(updated)

    def skip_mission(self, mission_id: str) -> DailyMission:
        """Skip a mission without completing its session."""
        mission = self.get_mission(mission_id)
        updated = self._scheduler.skip(mission)
        return self._replace(updated)

    def reschedule_mission(
        self,
        mission_id: str,
        *,
        new_date: date,
        as_of_date: date | None = None,
        is_revision: bool = False,
    ) -> DailyMission:
        """Reschedule an incomplete / missed / deferred mission."""
        mission = self.get_mission(mission_id)
        day = as_of_date or self._clock().date()
        updated = self._scheduler.reschedule(
            mission,
            new_date=new_date,
            as_of_date=day,
            existing=self.missions_for_learner(mission.learner_id),
            is_revision=is_revision,
        )
        return self._replace(updated)

    def complete_mission(self, mission_id: str) -> DailyMission:
        """Mark mission COMPLETED (does not complete the journey)."""
        mission = self.get_mission(mission_id)
        if mission.state == MissionState.ARCHIVED:
            raise MissionAlreadyArchived(
                f"Mission {mission_id} is already archived"
            )
        if mission.state == MissionState.COMPLETED:
            raise MissionAlreadyCompleted(
                f"Mission {mission_id} is already completed"
            )
        updated = self._archive.complete(mission, completed_at=self._clock())
        return self._replace(updated)

    def archive_mission(self, mission_id: str) -> DailyMission:
        """Archive a completed mission into mission history."""
        mission = self.get_mission(mission_id)
        if mission.state == MissionState.ARCHIVED:
            raise MissionAlreadyArchived(
                f"Mission {mission_id} is already archived"
            )
        if mission.state != MissionState.COMPLETED:
            # Allow complete-and-archive convenience for ACTIVE/IN_PROGRESS.
            if mission.state in {
                MissionState.ACTIVE,
                MissionState.IN_PROGRESS,
            }:
                mission = self._archive.complete(
                    mission,
                    completed_at=self._clock(),
                )
            else:
                raise InvalidMissionState(
                    f"Cannot archive mission in state {mission.state.value}"
                )
        archived = self._archive.archive(mission, archived_at=self._clock())
        return self._replace(archived)

    # ------------------------------------------------------------------
    # Queries / delivery
    # ------------------------------------------------------------------

    def get_schedule(
        self,
        learner_id: str,
        *,
        as_of_date: date | None = None,
        refresh_missed: bool = True,
    ) -> MissionSchedule:
        """Build a MissionSchedule for ``learner_id``."""
        day = as_of_date or self._clock().date()
        missions = self.missions_for_learner(learner_id)
        if refresh_missed:
            refreshed = self._scheduler.refresh_missed(missions, as_of_date=day)
            for mission in refreshed:
                self._missions[mission.mission_id] = mission
            missions = refreshed
        return self._scheduler.build_schedule(
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
        """Return today's primary mission, if any."""
        return self.get_schedule(learner_id, as_of_date=as_of_date).today

    def summarize(
        self,
        mission_id: str,
        *,
        runtime_phase: str | None = None,
    ) -> MissionSummary:
        """Dashboard-ready summary for a mission."""
        mission = self.get_mission(mission_id)
        return self._builder.build_summary(mission, runtime_phase=runtime_phase)

    def deliver(
        self,
        mission_id: str,
        *,
        runtime_phase: str | None = None,
    ) -> MissionDelivery:
        """Delivery payload for a mission (not UI)."""
        mission = self.get_mission(mission_id)
        return self._dispatcher.dispatch(mission, runtime_phase=runtime_phase)

    def orchestrate(
        self,
        journey: LearningJourney,
        *,
        as_of_date: date | None = None,
        session_handle: SessionHandle | None = None,
        ensure_today: bool = True,
    ) -> tuple[MissionSchedule, MissionSummary | None]:
        """Coordinate ledger refresh, today's mission, schedule, and summary."""
        day = as_of_date or self._clock().date()
        existing = self.missions_for_learner(journey.learner_id)
        ledger, schedule, summary = self._coordinator.orchestrate(
            journey,
            existing,
            as_of_date=day,
            session_handle=session_handle,
            ensure_today=ensure_today,
        )
        # Sync ledger: drop removed open missions for this learner, store new.
        keep_ids = {m.mission_id for m in ledger}
        for mid, mission in list(self._missions.items()):
            if (
                mission.learner_id == journey.learner_id
                and mid not in keep_ids
            ):
                # Should not normally happen; keep archive-safe.
                continue
        for mission in ledger:
            self._missions[mission.mission_id] = mission
        return schedule, summary

    def archived_missions(
        self,
        *,
        learner_id: str | None = None,
        journey_id: str | None = None,
    ) -> tuple[DailyMission, ...]:
        """Query completed mission history (not journey history)."""
        if learner_id is not None:
            return self._archive.for_learner(learner_id)
        if journey_id is not None:
            return self._archive.for_journey(journey_id)
        return self._archive.history
