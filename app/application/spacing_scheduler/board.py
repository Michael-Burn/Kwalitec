"""Revision board projection from canonical Spacing Scheduler state.

Groups stored states into Due now / Upcoming / Recently reviewed using only
``SpacingScheduler.evaluate`` decisions. Does not invent due dates, priority
scores, or performance judgements.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.domain.spacing_scheduler.types import (
    SchedulingDecision,
    SchedulingStatus,
    SpacingState,
)


@dataclass(frozen=True, slots=True)
class SpacingBoardEntry:
    """One package row for Revision, with the scheduler's own explanation."""

    state: SpacingState
    decision: SchedulingDecision

    @property
    def package_id(self) -> str:
        return self.state.unit_id

    @property
    def explanation(self) -> str:
        return self.decision.explanation


@dataclass(frozen=True, slots=True)
class SpacingRevisionBoard:
    """Honest Revision sections sourced only from canonical spacing state."""

    as_of: date
    learner_id: str
    due_now: tuple[SpacingBoardEntry, ...]
    upcoming: tuple[SpacingBoardEntry, ...]
    recently_reviewed: tuple[SpacingBoardEntry, ...]

    @property
    def has_due(self) -> bool:
        return bool(self.due_now)


def build_revision_board(
    *,
    learner_id: str,
    as_of: date,
    states: tuple[SpacingState, ...] | list[SpacingState],
    evaluate,
) -> SpacingRevisionBoard:
    """Partition learner states into the three Revision sections.

    Ordering (locked):
    - Due now: oldest ``next_due_on`` first (due and overdue).
    - Upcoming: soonest ``next_due_on`` first (not yet due).
    - Recently reviewed: most recent ``last_completed_on`` first.

    ``evaluate`` must be the scheduler's evaluate callable (or service method)
    so due status is never recalculated outside the canonical engine.
    """
    lid = learner_id.strip()
    due: list[SpacingBoardEntry] = []
    upcoming: list[SpacingBoardEntry] = []
    recent: list[SpacingBoardEntry] = []

    for state in states:
        decision = evaluate(
            learner_id=lid,
            package_id=state.unit_id,
            as_of=as_of,
        )
        entry = SpacingBoardEntry(state=state, decision=decision)
        recent.append(entry)
        if decision.status in {SchedulingStatus.DUE, SchedulingStatus.OVERDUE}:
            due.append(entry)
        elif decision.status is SchedulingStatus.NOT_DUE:
            upcoming.append(entry)

    due.sort(key=lambda e: e.state.next_due_on)
    upcoming.sort(key=lambda e: e.state.next_due_on)
    recent.sort(key=lambda e: e.state.last_completed_on, reverse=True)

    return SpacingRevisionBoard(
        as_of=as_of,
        learner_id=lid,
        due_now=tuple(due),
        upcoming=tuple(upcoming),
        recently_reviewed=tuple(recent),
    )
