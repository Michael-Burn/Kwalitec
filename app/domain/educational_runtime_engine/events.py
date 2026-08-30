"""Immutable educational event model for the curriculum-driven runtime.

Events are the durable student history. Progress and journey position are
derived from the event stream plus the published progress model — not stored
as a competing educational truth.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any


class EducationalEventType(StrEnum):
    """Canonical immutable educational event kinds."""

    STUDENT_ENROLLED = "student_enrolled"
    STUDY_PLAN_INSTANTIATED = "study_plan_instantiated"
    MISSION_GENERATED = "mission_generated"
    MISSION_ACCEPTED = "mission_accepted"  # SR-002a: session start
    MISSION_DEFERRED = "mission_deferred"  # SR-002a: ILE-004 deferral
    MISSION_COMPLETED = "mission_completed"
    TOPIC_COMPLETED = "topic_completed"
    JOURNEY_ADVANCED = "journey_advanced"
    SYLLABUS_COMPLETED = "syllabus_completed"
    # ADR-027 M0: Adaptive Decision Engine audit (additive; observational)
    DECISION_RECORDED = "decision_recorded"


@dataclass(frozen=True)
class EducationalEventRecord:
    """Pure event record used by derivation rules (no ORM coupling)."""

    event_id: str
    event_type: EducationalEventType
    user_id: int
    curriculum_identity: str
    enrolment_id: str | None = None
    plan_instance_id: str | None = None
    topic_id: str | None = None
    mission_instance_id: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    occurred_at: datetime | None = None
