"""Immutable DailyMission DTO — one executable learning session commitment."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from app.application.mission_engine_v2.lifecycle import MissionSlot, MissionState


@dataclass(frozen=True)
class DailyMission:
    """A Mission represents ONE executable learning session.

    Never an entire topic, chapter, or study day. Session Runtime owns
    execution; Mission Engine owns scheduling and lifecycle of the wrapper.

    Attributes:
        mission_id: Mission identity.
        learner_id: Owning learner.
        journey_id: Parent Learning Journey.
        session_id: Bound Learning Session identity.
        topic_id: Curriculum topic identity (structural label only).
        curriculum_id: Curriculum identity.
        scheduled_date: Calendar date for the commitment.
        slot: Deterministic schedule slot.
        state: Mission lifecycle posture.
        objective_id: Primary objective when known from journey plan.
        effort: Effort band string from journey / session plan.
        title: Structural title (objective/topic label — not generated content).
        sequence_index: Session sequence index within the journey.
        is_resume: True when built against a paused session runtime.
        is_revision: True when slotted as a revision commitment.
        explanation_keys: Traceable reason keys from recommendation (no body).
        outstanding_reflections: Structural count of owed reflections.
        revision_debt: Structural revision-debt signal (count, never mastery).
        created_at: Creation timestamp.
        completed_at: Completion timestamp when completed.
        archived_at: Archive timestamp when archived.
    """

    mission_id: str
    learner_id: str
    journey_id: str
    session_id: str
    topic_id: str
    curriculum_id: str
    scheduled_date: date
    slot: MissionSlot
    state: MissionState
    objective_id: str | None
    effort: str
    title: str
    sequence_index: int
    is_resume: bool
    is_revision: bool
    explanation_keys: tuple[str, ...]
    outstanding_reflections: int
    revision_debt: int
    created_at: datetime
    completed_at: datetime | None = None
    archived_at: datetime | None = None
