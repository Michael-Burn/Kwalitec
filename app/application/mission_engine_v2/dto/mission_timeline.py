"""Immutable MissionTimeline — ordered schedule view for a learner."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.application.mission_engine_v2.dto.daily_mission import DailyMission


@dataclass(frozen=True)
class MissionTimeline:
    """Ordered timeline of missions for a learner as of a calendar date.

    Attributes:
        learner_id: Owning learner.
        as_of_date: Calendar date the timeline was assembled for.
        today: Today's primary mission, if any.
        deferred: Learner-deferred incomplete missions.
        revision: Explicit revision commitments.
        missed: Past incomplete missions marked missed.
        future: Future queue (scheduled after as_of_date).
        ordered: Deterministic full ordering across slots.
    """

    learner_id: str
    as_of_date: date
    today: DailyMission | None
    deferred: tuple[DailyMission, ...]
    revision: tuple[DailyMission, ...]
    missed: tuple[DailyMission, ...]
    future: tuple[DailyMission, ...]
    ordered: tuple[DailyMission, ...]
