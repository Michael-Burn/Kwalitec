"""Revision projection — Spacing Scheduler sections for the Revision surface.

Consumes only canonical Spacing Scheduler board entries. Never calculates
due dates, priority, or educational ROI.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RevisionItem:
    """One package entry for a Revision section."""

    package_id: str
    title: str
    explanation: str = ""
    status: str = ""
    next_due_on: str = ""
    last_completed_on: str = ""
    interval_days: int | None = None

    @classmethod
    def create(
        cls,
        package_id: str,
        title: str,
        *,
        explanation: str = "",
        status: str = "",
        next_due_on: str = "",
        last_completed_on: str = "",
        interval_days: int | None = None,
    ) -> RevisionItem:
        return cls(
            package_id=_require_non_empty(package_id, "package_id"),
            title=_require_non_empty(title, "title"),
            explanation=(explanation or "").strip(),
            status=(status or "").strip(),
            next_due_on=(next_due_on or "").strip(),
            last_completed_on=(last_completed_on or "").strip(),
            interval_days=interval_days,
        )


@dataclass(frozen=True)
class RevisionOption:
    """Compatibility option for Home consumers (oldest due package)."""

    option_id: str
    topic_title: str
    priority_label: str = ""
    estimated_study_minutes: int | None = None
    expected_benefit: str = ""
    explanation: object | None = None
    is_primary: bool = False
    package_id: str = ""

    @classmethod
    def create(
        cls,
        option_id: str,
        topic_title: str,
        *,
        priority_label: str = "",
        estimated_study_minutes: int | None = None,
        expected_benefit: str = "",
        explanation: object | None = None,
        is_primary: bool = False,
        package_id: str = "",
    ) -> RevisionOption:
        minutes = estimated_study_minutes
        if minutes is not None and minutes < 0:
            raise ValueError("estimated_study_minutes must be non-negative")
        return cls(
            option_id=_require_non_empty(option_id, "option_id"),
            topic_title=_require_non_empty(topic_title, "topic_title"),
            priority_label=(priority_label or "").strip(),
            estimated_study_minutes=minutes,
            expected_benefit=(expected_benefit or "").strip(),
            explanation=explanation,
            is_primary=bool(is_primary),
            package_id=(package_id or "").strip(),
        )


@dataclass(frozen=True)
class RevisionProjection:
    """Domain projection for the Revision experience."""

    student_id: str
    due_now: tuple[RevisionItem, ...] = field(default_factory=tuple)
    upcoming: tuple[RevisionItem, ...] = field(default_factory=tuple)
    recently_reviewed: tuple[RevisionItem, ...] = field(default_factory=tuple)
    empty_message: str = ""
    primary: RevisionOption | None = None
    alternatives: tuple[RevisionOption, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        student_id: str,
        *,
        due_now: list[RevisionItem] | tuple[RevisionItem, ...] | None = None,
        upcoming: list[RevisionItem] | tuple[RevisionItem, ...] | None = None,
        recently_reviewed: (
            list[RevisionItem] | tuple[RevisionItem, ...] | None
        ) = None,
        empty_message: str = "",
        primary: RevisionOption | None = None,
        alternatives: list[RevisionOption] | tuple[RevisionOption, ...] | None = None,
    ) -> RevisionProjection:
        due = tuple(due_now or ())
        up = tuple(upcoming or ())
        recent = tuple(recently_reviewed or ())
        alts = tuple(alternatives or ())
        if not due and not up and not recent:
            msg = (empty_message or "").strip() or (
                "Nothing is due for review yet. Packages return here after "
                "you complete them and enough time has passed."
            )
        else:
            msg = (empty_message or "").strip()
        return cls(
            student_id=_require_non_empty(student_id, "student_id"),
            due_now=due,
            upcoming=up,
            recently_reviewed=recent,
            empty_message=msg,
            primary=primary,
            alternatives=alts,
        )

    @property
    def has_revision(self) -> bool:
        return bool(self.due_now) or self.primary is not None

    @property
    def option_count(self) -> int:
        if self.due_now:
            return len(self.due_now)
        return (1 if self.primary else 0) + len(self.alternatives)


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
