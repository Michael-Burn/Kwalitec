"""Spacing Scheduler application facade — sole query/write entry point.

Canonical source of truth for time-based review due status. Callers must
use this service (or ``get_spacing_scheduler``) rather than inventing due
dates from ``TopicProgress.next_review_date`` or MissionOptimizer slots.

Revision reads due status only through this facade (via
``revision_board``). Persistence defaults to an in-process store until a
durable adapter is wired.
"""

from __future__ import annotations

from datetime import date

from app.application.spacing_scheduler.board import (
    SpacingRevisionBoard,
    build_revision_board,
)
from app.application.spacing_scheduler.store import (
    InMemorySpacingStateStore,
    SpacingStateStore,
)
from app.domain.spacing_scheduler.policy import SpacingIntervalPolicy
from app.domain.spacing_scheduler.scheduler import SpacingScheduler
from app.domain.spacing_scheduler.types import (
    ReviewableUnitId,
    SchedulingDecision,
    SpacingState,
    reject_forbidden_kwargs,
)


class SpacingSchedulerService:
    """Application entry for recording exposures and querying due status.

    All reads and writes of spacing due-state for a given store instance
    go through this service so Revision and the daily loop can later share
    one authority without recalculating intervals independently.
    """

    def __init__(
        self,
        *,
        store: SpacingStateStore,
        policy: SpacingIntervalPolicy | None = None,
        scheduler: SpacingScheduler | None = None,
    ) -> None:
        self._store = store
        self._scheduler = scheduler or SpacingScheduler(policy)

    @property
    def policy(self) -> SpacingIntervalPolicy:
        return self._scheduler.policy

    def record_completed_exposure(
        self,
        *,
        learner_id: str,
        package_id: str,
        completed_on: date,
        **kwargs: object,
    ) -> SpacingState:
        """Hook for a genuine package completion.

        Completion signal (locked investigation): Runtime C
        ``MISSION_COMPLETED`` with a non-empty ``educational_package_id``.
        This method does not call Runtime C; callers supply the completed
        package id and calendar date.
        """
        reject_forbidden_kwargs(kwargs)
        unit = ReviewableUnitId(package_id=package_id)
        prior = self._store.get(learner_id, unit.package_id)
        state = self._scheduler.apply_completed_exposure(
            learner_id=learner_id,
            unit_id=unit.package_id,
            completed_on=completed_on,
            prior=prior,
        )
        self._store.put(state)
        return state

    def record_missed_review(
        self,
        *,
        learner_id: str,
        package_id: str,
        as_of: date,
        **kwargs: object,
    ) -> SpacingState:
        """Record that a due review passed without a completed exposure."""
        reject_forbidden_kwargs(kwargs)
        unit = ReviewableUnitId(package_id=package_id)
        prior = self._store.get(learner_id, unit.package_id)
        if prior is None:
            raise ValueError(
                "cannot record a missed review with no prior spacing state"
            )
        state = self._scheduler.apply_missed_review(
            learner_id=learner_id,
            unit_id=unit.package_id,
            as_of=as_of,
            prior=prior,
        )
        self._store.put(state)
        return state

    def get_state(
        self, *, learner_id: str, package_id: str
    ) -> SpacingState | None:
        """Return the canonical spacing state for the unit, if any."""
        unit = ReviewableUnitId(package_id=package_id)
        return self._store.get(learner_id, unit.package_id)

    def list_states_for_learner(self, *, learner_id: str) -> tuple[SpacingState, ...]:
        """Return every stored spacing state for the learner."""
        return self._store.list_for_learner(learner_id.strip())

    def evaluate(
        self,
        *,
        learner_id: str,
        package_id: str,
        as_of: date,
        **kwargs: object,
    ) -> SchedulingDecision:
        """Return due status and a plain-language explanation."""
        reject_forbidden_kwargs(kwargs)
        unit = ReviewableUnitId(package_id=package_id)
        state = self._store.get(learner_id, unit.package_id)
        return self._scheduler.evaluate(
            learner_id=learner_id,
            unit_id=unit.package_id,
            as_of=as_of,
            state=state,
        )

    def revision_board(
        self,
        *,
        learner_id: str,
        as_of: date,
        **kwargs: object,
    ) -> SpacingRevisionBoard:
        """Build Revision Due now / Upcoming / Recently reviewed sections.

        Due status comes only from ``evaluate`` over stored canonical state.
        """
        reject_forbidden_kwargs(kwargs)
        lid = learner_id.strip()
        return build_revision_board(
            learner_id=lid,
            as_of=as_of,
            states=self.list_states_for_learner(learner_id=lid),
            evaluate=self.evaluate,
        )

    def explain(
        self,
        *,
        learner_id: str,
        package_id: str,
        as_of: date,
        **kwargs: object,
    ) -> str:
        """Plain-language explanation for the scheduling decision."""
        return self.evaluate(
            learner_id=learner_id,
            package_id=package_id,
            as_of=as_of,
            **kwargs,
        ).explanation


# Process-wide default store: one canonical in-memory source until a
# durable adapter replaces it. Tests that need isolation should inject
# their own store rather than clearing the shared default casually.
_CANONICAL_STORE = InMemorySpacingStateStore()
_CANONICAL_SERVICE = SpacingSchedulerService(store=_CANONICAL_STORE)


def get_spacing_scheduler() -> SpacingSchedulerService:
    """Return the process-canonical Spacing Scheduler service.

    Every caller that wants the shared authority must go through this
    function (or an explicitly injected service wrapping the same store).
    """
    return _CANONICAL_SERVICE


def reset_canonical_spacing_scheduler_for_tests() -> None:
    """Clear the process-canonical store (tests only)."""
    _CANONICAL_STORE.clear()
