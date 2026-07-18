"""Immutable MissionSummary — dashboard-ready mission posture."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.application.mission_engine.mission_state import (
    DeliveryAction,
    MissionSlot,
    MissionState,
)


@dataclass(frozen=True)
class MissionSummary:
    """Compact, dashboard-ready summary of a mission.

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
    delivery_action: DeliveryAction
    is_active: bool
    is_completed: bool
    is_resume: bool
    is_revision: bool
    objective_id: str | None
    effort: str
