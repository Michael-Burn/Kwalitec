"""Archive completed missions.

Responsible only for completed mission history.
Journey history remains inside the Journey Domain.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

from app.application.mission_engine.dto.daily_mission import DailyMission
from app.application.mission_engine.exceptions import (
    InvalidMissionState,
    MissionAlreadyArchived,
)
from app.application.mission_engine.mission_state import (
    MissionState,
    MissionTransitionEvent,
    next_mission_state,
)


class MissionArchive:
    """Completed-mission archival (in-memory history spine)."""

    def __init__(self, *, clock=None) -> None:
        self._clock = clock or (lambda: datetime.now(tz=UTC))
        self._history: list[DailyMission] = []

    @property
    def history(self) -> tuple[DailyMission, ...]:
        """Immutable view of archived missions (oldest first)."""
        return tuple(self._history)

    def complete(
        self,
        mission: DailyMission,
        *,
        completed_at: datetime | None = None,
    ) -> DailyMission:
        """Mark a mission COMPLETED (not yet archived)."""
        if mission.state == MissionState.ARCHIVED:
            raise MissionAlreadyArchived(
                f"Mission {mission.mission_id} is already archived"
            )
        if mission.state == MissionState.COMPLETED:
            return mission
        nxt = next_mission_state(mission.state, MissionTransitionEvent.COMPLETE)
        if nxt is None:
            raise InvalidMissionState(
                f"Cannot complete mission in state {mission.state.value}"
            )
        return replace(
            mission,
            state=MissionState.COMPLETED,
            completed_at=completed_at or self._clock(),
        )

    def archive(
        self,
        mission: DailyMission,
        *,
        archived_at: datetime | None = None,
    ) -> DailyMission:
        """Archive a COMPLETED mission into local history."""
        if mission.state == MissionState.ARCHIVED:
            raise MissionAlreadyArchived(
                f"Mission {mission.mission_id} is already archived"
            )
        if mission.state != MissionState.COMPLETED:
            raise InvalidMissionState(
                f"Cannot archive mission in state {mission.state.value}; "
                "complete it first"
            )
        stamped = replace(
            mission,
            state=MissionState.ARCHIVED,
            archived_at=archived_at or self._clock(),
            completed_at=mission.completed_at or self._clock(),
        )
        self._history.append(stamped)
        return stamped

    def complete_and_archive(
        self,
        mission: DailyMission,
        *,
        at: datetime | None = None,
    ) -> DailyMission:
        """Complete then archive in one step."""
        moment = at or self._clock()
        completed = self.complete(mission, completed_at=moment)
        return self.archive(completed, archived_at=moment)

    def find(self, mission_id: str) -> DailyMission | None:
        """Lookup an archived mission by id."""
        for mission in self._history:
            if mission.mission_id == mission_id:
                return mission
        return None

    def for_learner(self, learner_id: str) -> tuple[DailyMission, ...]:
        """Archived missions for a learner (oldest first)."""
        return tuple(m for m in self._history if m.learner_id == learner_id)

    def for_journey(self, journey_id: str) -> tuple[DailyMission, ...]:
        """Archived missions for a journey (oldest first)."""
        return tuple(m for m in self._history if m.journey_id == journey_id)

    def clear(self) -> None:
        """Reset archive history (test helper)."""
        self._history.clear()
