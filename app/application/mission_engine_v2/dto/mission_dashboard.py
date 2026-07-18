"""Immutable MissionDashboard — assembled dashboard mission posture."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.application.mission_engine_v2.dto.mission_card import MissionCard
from app.application.mission_engine_v2.dto.mission_timeline import MissionTimeline


@dataclass(frozen=True)
class MissionDashboard:
    """Dashboard-ready assembly of today's mission and related queues.

    No UI rendering. Contains structural mission artefacts only.
    """

    learner_id: str
    as_of_date: date
    today: MissionCard | None
    deferred: tuple[MissionCard, ...]
    revision: tuple[MissionCard, ...]
    missed: tuple[MissionCard, ...]
    future: tuple[MissionCard, ...]
    timeline: MissionTimeline
    active_mission_id: str | None
    open_mission_count: int
    workload_ok: bool
