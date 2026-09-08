"""Spacing Scheduler types — time and interval facts only.

Hard boundary (roadmap): these types must not be able to represent
performance, mastery, weakness, accuracy, or priority judgements.
Structural enforcement lives here and in the application facade tests.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from datetime import date
from enum import StrEnum

# Names that must never appear on Spacing Scheduler public types.
# Used by tests and by runtime guards on record/evaluate kwargs.
FORBIDDEN_SIGNAL_NAMES: frozenset[str] = frozenset(
    {
        "mastery",
        "mastery_score",
        "estimated_knowledge",
        "estimated_mastery",
        "weak",
        "weakness",
        "weak_score",
        "accuracy",
        "performance",
        "priority",
        "priority_score",
        "urgency",
        "confidence",
        "score",
        "roi",
    }
)


class ExposureKind(StrEnum):
    """How a completed exposure relates to the prior due schedule.

    These are calendar outcomes only. They are not grades or scores.
    """

    INITIAL_COMPLETION = "initial_completion"
    ON_TIME_REVIEW = "on_time_review"
    LATE_REVIEW = "late_review"
    MISSED_REVIEW = "missed_review"


class SchedulingStatus(StrEnum):
    """Due status derived only from elapsed time versus the current interval."""

    NEVER_SCHEDULED = "never_scheduled"
    NOT_DUE = "not_due"
    DUE = "due"
    OVERDUE = "overdue"


@dataclass(frozen=True, slots=True)
class ReviewableUnitId:
    """Identity of one reviewable learning block.

    V1 maps this to a certified educational package id (Mission+Session
    package), not a whole syllabus topic and not an individual item.
    """

    package_id: str

    def __post_init__(self) -> None:
        pid = (self.package_id or "").strip()
        if not pid:
            raise ValueError("package_id must be non-empty")
        object.__setattr__(self, "package_id", pid)


@dataclass(frozen=True, slots=True)
class SpacingState:
    """Canonical spacing state for one learner and one reviewable unit."""

    learner_id: str
    unit_id: str
    last_completed_on: date
    current_interval_days: int
    next_due_on: date
    review_cycle_count: int
    last_exposure_kind: ExposureKind

    def __post_init__(self) -> None:
        if not (self.learner_id or "").strip():
            raise ValueError("learner_id must be non-empty")
        if not (self.unit_id or "").strip():
            raise ValueError("unit_id must be non-empty")
        if self.current_interval_days < 1:
            raise ValueError("current_interval_days must be >= 1")
        if self.review_cycle_count < 0:
            raise ValueError("review_cycle_count must be >= 0")
        _assert_no_forbidden_fields(type(self))


@dataclass(frozen=True, slots=True)
class SchedulingDecision:
    """Result of asking whether a unit is due as of a calendar date.

    ``explanation`` is plain language and must remain queryable/testable
    even when no student surface consumes it yet.
    """

    status: SchedulingStatus
    as_of: date
    learner_id: str
    unit_id: str
    last_completed_on: date | None
    current_interval_days: int | None
    next_due_on: date | None
    days_since_completion: int | None
    days_until_due: int | None
    days_overdue: int | None
    explanation: str

    def __post_init__(self) -> None:
        _assert_no_forbidden_fields(type(self))
        if not (self.explanation or "").strip():
            raise ValueError("explanation must be non-empty")


def _assert_no_forbidden_fields(cls: type) -> None:
    """Reject type definitions that smuggle performance fields onto the API."""
    names = {f.name.lower() for f in fields(cls)}
    offenders = names & FORBIDDEN_SIGNAL_NAMES
    if offenders:
        raise TypeError(
            f"{cls.__name__} must not declare performance fields: "
            f"{sorted(offenders)}"
        )


def reject_forbidden_kwargs(kwargs: dict[str, object]) -> None:
    """Raise if a caller tries to pass a performance-flavoured keyword."""
    offenders = {k for k in kwargs if k.lower() in FORBIDDEN_SIGNAL_NAMES}
    if offenders:
        raise TypeError(
            "Spacing Scheduler refuses performance signals: "
            f"{sorted(offenders)}"
        )
