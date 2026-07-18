"""Revision window — scheduled study-time slot for a revision intervention."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum


class RevisionUrgency(StrEnum):
    """Urgency class for scheduling revision windows."""

    IMMEDIATE = "immediate"
    TODAY = "today"
    THIS_WEEK = "this_week"
    DEFERRED = "deferred"


@dataclass(frozen=True)
class RevisionWindow:
    """A deterministic time window for completing a revision.

    Windows are derived from priority and exam proximity — never random.
    """

    topic_id: str
    urgency: RevisionUrgency
    suggested_start: datetime
    suggested_end: datetime
    allocated_minutes: float
    priority_score: float

    @classmethod
    def create(
        cls,
        topic_id: str,
        *,
        urgency: RevisionUrgency | str,
        suggested_start: datetime,
        suggested_end: datetime | None = None,
        allocated_minutes: float,
        priority_score: float,
    ) -> RevisionWindow:
        """Construct a RevisionWindow."""
        tid = _require_non_empty(topic_id, "topic_id")
        urg = (
            urgency
            if isinstance(urgency, RevisionUrgency)
            else RevisionUrgency(str(urgency).strip().lower())
        )
        if not isinstance(suggested_start, datetime):
            raise ValueError("suggested_start must be a datetime")
        start = (
            suggested_start
            if suggested_start.tzinfo
            else suggested_start.replace(tzinfo=UTC)
        )
        minutes = _non_negative(allocated_minutes, "allocated_minutes")
        if suggested_end is None:
            end = start + timedelta(minutes=max(minutes, 1.0))
        else:
            if not isinstance(suggested_end, datetime):
                raise ValueError("suggested_end must be a datetime")
            end = (
                suggested_end
                if suggested_end.tzinfo
                else suggested_end.replace(tzinfo=UTC)
            )
        if end < start:
            raise ValueError("suggested_end must not precede suggested_start")
        score = _unit_interval(priority_score, "priority_score")
        return cls(
            topic_id=tid,
            urgency=urg,
            suggested_start=start,
            suggested_end=end,
            allocated_minutes=minutes,
            priority_score=score,
        )

    @property
    def duration_minutes(self) -> float:
        """Wall-clock span of the window in minutes."""
        return (self.suggested_end - self.suggested_start).total_seconds() / 60.0

    @property
    def is_immediate(self) -> bool:
        """True when urgency is IMMEDIATE."""
        return self.urgency is RevisionUrgency.IMMEDIATE


def urgency_from_priority(
    priority_score: float,
    *,
    exam_proximity: float = 0.0,
) -> RevisionUrgency:
    """Map priority (+ exam proximity) to a deterministic urgency class."""
    score = _clamp01(priority_score)
    exam = _clamp01(exam_proximity)
    combined = min(1.0, score * 0.75 + exam * 0.25)
    if combined >= 0.85:
        return RevisionUrgency.IMMEDIATE
    if combined >= 0.65:
        return RevisionUrgency.TODAY
    if combined >= 0.40:
        return RevisionUrgency.THIS_WEEK
    return RevisionUrgency.DEFERRED


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _unit_interval(value: float, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(f"{field_name} must be a number in [0, 1]")
    numeric = float(value)
    if numeric < 0.0 or numeric > 1.0:
        raise ValueError(f"{field_name} must be in [0, 1]")
    return numeric


def _non_negative(value: float, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(f"{field_name} must be a non-negative number")
    numeric = float(value)
    if numeric < 0.0:
        raise ValueError(f"{field_name} must be a non-negative number")
    return numeric


def _clamp01(value: float) -> float:
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return float(value)
