"""Immutable MissionCard — compact dashboard presentation of one mission."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.application.mission_engine_v2.lifecycle import (
    DispatchAction,
    MissionSlot,
    MissionState,
)


@dataclass(frozen=True)
class MissionCard:
    """Dashboard-ready card for a single mission.

    No UI rendering. Adapters / composers may map this to view models.
    """

    mission_id: str
    learner_id: str
    journey_id: str
    session_id: str
    topic_id: str
    scheduled_date: date
    slot: MissionSlot
    state: MissionState
    title: str
    effort: str
    dispatch_action: DispatchAction
    is_active: bool
    is_completed: bool
    is_resume: bool
    is_revision: bool
    objective_id: str | None
    sequence_index: int
    explanation_keys: tuple[str, ...] = ()
