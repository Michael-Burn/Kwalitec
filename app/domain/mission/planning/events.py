"""Factual Mission planning events (AP-002D5).

No Tutor notifications. No student notifications.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum


class PlanningEventKind(StrEnum):
    """Kinds of factual planning events."""

    STARTED = "mission_planning_started"
    GENERATED = "mission_generated"
    SKIPPED = "mission_planning_skipped"
    COMPLETED = "mission_planning_completed"


@dataclass(frozen=True, slots=True)
class MissionPlanningStarted:
    """Mission planning cycle began for a Twin decision set."""

    event_id: str
    twin_id: str
    decision_set_id: str
    mission_request_id: str
    occurred_at: datetime
    planning_version: str
    kind: PlanningEventKind = PlanningEventKind.STARTED

    def __post_init__(self) -> None:
        _require_nonblank(
            self,
            "event_id",
            "twin_id",
            "decision_set_id",
            "mission_request_id",
            "planning_version",
        )
        when = self.occurred_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "occurred_at", when.astimezone(UTC).replace(tzinfo=None)
            )


@dataclass(frozen=True, slots=True)
class MissionGenerated:
    """A study mission plan was generated from Twin decisions."""

    event_id: str
    plan_id: str
    mission_id: str
    twin_id: str
    decision_id: str
    concept_id: str
    occurred_at: datetime
    planning_version: str
    kind: PlanningEventKind = PlanningEventKind.GENERATED

    def __post_init__(self) -> None:
        _require_nonblank(
            self,
            "event_id",
            "plan_id",
            "mission_id",
            "twin_id",
            "decision_id",
            "concept_id",
            "planning_version",
        )
        when = self.occurred_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "occurred_at", when.astimezone(UTC).replace(tzinfo=None)
            )


@dataclass(frozen=True, slots=True)
class MissionPlanningSkipped:
    """A decision produced no mission candidate (idempotent / non-plannable)."""

    event_id: str
    twin_id: str
    decision_id: str
    reason_code: str
    occurred_at: datetime
    planning_version: str
    candidate_id: str = ""
    plan_id: str = ""
    kind: PlanningEventKind = PlanningEventKind.SKIPPED

    def __post_init__(self) -> None:
        _require_nonblank(
            self,
            "event_id",
            "twin_id",
            "decision_id",
            "reason_code",
            "planning_version",
        )
        when = self.occurred_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "occurred_at", when.astimezone(UTC).replace(tzinfo=None)
            )


@dataclass(frozen=True, slots=True)
class MissionPlanningCompleted:
    """Mission planning cycle finished (generated or empty after skips)."""

    event_id: str
    twin_id: str
    decision_set_id: str
    mission_request_id: str
    plan_id: str
    candidate_count: int
    skipped_count: int
    occurred_at: datetime
    planning_version: str
    kind: PlanningEventKind = PlanningEventKind.COMPLETED

    def __post_init__(self) -> None:
        _require_nonblank(
            self,
            "event_id",
            "twin_id",
            "decision_set_id",
            "mission_request_id",
            "plan_id",
            "planning_version",
        )
        when = self.occurred_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "occurred_at", when.astimezone(UTC).replace(tzinfo=None)
            )
        object.__setattr__(self, "candidate_count", int(self.candidate_count))
        object.__setattr__(self, "skipped_count", int(self.skipped_count))


def _require_nonblank(obj: object, *fields: str) -> None:
    for field_name in fields:
        if not (getattr(obj, field_name) or "").strip():
            raise ValueError(f"{field_name} is required")
