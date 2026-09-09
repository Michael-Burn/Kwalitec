"""Immutable RevisionSnapshot DTO for Student Experience."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RevisionItemSnapshot:
    """One package row from the Spacing Scheduler for Revision."""

    package_id: str
    title: str
    explanation: str = ""
    status: str = ""
    next_due_on: str = ""
    last_completed_on: str = ""
    interval_days: int | None = None


@dataclass(frozen=True)
class RevisionOptionSnapshot:
    """Compatibility projection of the oldest due package (Home consumers)."""

    option_id: str
    topic_title: str
    priority_label: str = ""
    estimated_study_minutes: int | None = None
    expected_benefit: str = ""
    explanation: object | None = None
    is_primary: bool = False
    package_id: str = ""


@dataclass(frozen=True)
class RevisionSnapshot:
    """Revision experience projection DTO (Spacing Scheduler sections)."""

    student_id: str
    due_now: tuple[RevisionItemSnapshot, ...] = field(default_factory=tuple)
    upcoming: tuple[RevisionItemSnapshot, ...] = field(default_factory=tuple)
    recently_reviewed: tuple[RevisionItemSnapshot, ...] = field(
        default_factory=tuple
    )
    empty_message: str = ""
    has_revision: bool = False
    option_count: int = 0
    primary: RevisionOptionSnapshot | None = None
    alternatives: tuple[RevisionOptionSnapshot, ...] = field(default_factory=tuple)
