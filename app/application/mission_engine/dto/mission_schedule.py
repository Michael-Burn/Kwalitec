"""Immutable MissionSchedule — ordered mission commitments for a learner."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.application.mission_engine.dto.daily_mission import DailyMission


@dataclass(frozen=True)
class MissionSchedule:
    """Deterministic schedule snapshot for a learner as of a calendar date.

    Attributes:
        learner_id: Owning learner.
        as_of_date: Calendar date the schedule was computed for.
        today: Today's primary mission, if any.
        tomorrow: Tomorrow's scheduled mission, if any.
        deferred: Deferred missions (ordered).
        missed: Missed missions awaiting reschedule (ordered).
        revision: Revision-slot missions (ordered).
        ordered: Full deterministic ordering across slots.
    """

    learner_id: str
    as_of_date: date
    today: DailyMission | None
    tomorrow: DailyMission | None
    deferred: tuple[DailyMission, ...]
    missed: tuple[DailyMission, ...]
    revision: tuple[DailyMission, ...]
    ordered: tuple[DailyMission, ...]
