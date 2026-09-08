"""Pure Spacing Scheduler — state transitions and due evaluation."""

from __future__ import annotations

from datetime import date, timedelta

from app.domain.spacing_scheduler.policy import SpacingIntervalPolicy
from app.domain.spacing_scheduler.types import (
    ExposureKind,
    SchedulingDecision,
    SchedulingStatus,
    SpacingState,
    reject_forbidden_kwargs,
)


class SpacingScheduler:
    """Compute spacing state and due status from elapsed time alone.

    Does not persist. Does not rank. Does not accept performance inputs.
    """

    def __init__(self, policy: SpacingIntervalPolicy | None = None) -> None:
        self._policy = policy or SpacingIntervalPolicy()

    @property
    def policy(self) -> SpacingIntervalPolicy:
        return self._policy

    def apply_completed_exposure(
        self,
        *,
        learner_id: str,
        unit_id: str,
        completed_on: date,
        prior: SpacingState | None,
        **kwargs: object,
    ) -> SpacingState:
        """Record a completed exposure and produce the next spacing state."""
        reject_forbidden_kwargs(kwargs)
        if kwargs:
            raise TypeError(
                f"unexpected Spacing Scheduler kwargs: {sorted(kwargs)}"
            )
        if not isinstance(completed_on, date):
            raise TypeError("completed_on must be a date")

        if prior is None:
            kind = ExposureKind.INITIAL_COMPLETION
            interval = self._policy.interval_after(
                prior_interval_days=None,
                exposure_kind=kind,
            )
            cycle = 0
        else:
            if completed_on <= prior.next_due_on:
                kind = ExposureKind.ON_TIME_REVIEW
            else:
                kind = ExposureKind.LATE_REVIEW
            interval = self._policy.interval_after(
                prior_interval_days=prior.current_interval_days,
                exposure_kind=kind,
            )
            cycle = prior.review_cycle_count + 1

        return SpacingState(
            learner_id=learner_id.strip(),
            unit_id=unit_id.strip(),
            last_completed_on=completed_on,
            current_interval_days=interval,
            next_due_on=completed_on + timedelta(days=interval),
            review_cycle_count=cycle,
            last_exposure_kind=kind,
        )

    def apply_missed_review(
        self,
        *,
        learner_id: str,
        unit_id: str,
        as_of: date,
        prior: SpacingState,
        **kwargs: object,
    ) -> SpacingState:
        """Shorten the interval after a due date passes without completion.

        Anchors the shortened next due date from ``as_of`` (the day the miss
        is recorded). Does not invent a performance score.
        """
        reject_forbidden_kwargs(kwargs)
        if kwargs:
            raise TypeError(
                f"unexpected Spacing Scheduler kwargs: {sorted(kwargs)}"
            )
        if not isinstance(as_of, date):
            raise TypeError("as_of must be a date")
        if as_of < prior.next_due_on:
            raise ValueError(
                "cannot record a missed review before the unit is due"
            )

        kind = ExposureKind.MISSED_REVIEW
        interval = self._policy.interval_after(
            prior_interval_days=prior.current_interval_days,
            exposure_kind=kind,
        )
        return SpacingState(
            learner_id=learner_id.strip(),
            unit_id=unit_id.strip(),
            last_completed_on=prior.last_completed_on,
            current_interval_days=interval,
            next_due_on=as_of + timedelta(days=interval),
            review_cycle_count=prior.review_cycle_count + 1,
            last_exposure_kind=kind,
        )

    def evaluate(
        self,
        *,
        learner_id: str,
        unit_id: str,
        as_of: date,
        state: SpacingState | None,
        **kwargs: object,
    ) -> SchedulingDecision:
        """Answer whether the unit is due as of ``as_of``."""
        reject_forbidden_kwargs(kwargs)
        if kwargs:
            raise TypeError(
                f"unexpected Spacing Scheduler kwargs: {sorted(kwargs)}"
            )
        if not isinstance(as_of, date):
            raise TypeError("as_of must be a date")

        if state is None:
            return SchedulingDecision(
                status=SchedulingStatus.NEVER_SCHEDULED,
                as_of=as_of,
                learner_id=learner_id.strip(),
                unit_id=unit_id.strip(),
                last_completed_on=None,
                current_interval_days=None,
                next_due_on=None,
                days_since_completion=None,
                days_until_due=None,
                days_overdue=None,
                explanation=(
                    f"not scheduled: no completed exposure recorded for "
                    f"package {unit_id.strip()}"
                ),
            )

        days_since = (as_of - state.last_completed_on).days
        delta = (state.next_due_on - as_of).days
        if as_of < state.next_due_on:
            status = SchedulingStatus.NOT_DUE
            days_until = delta
            days_overdue = None
            explanation = (
                f"not yet due, next due in {days_until} day"
                f"{'' if days_until == 1 else 's'} "
                f"(last completed {days_since} day"
                f"{'' if days_since == 1 else 's'} ago, "
                f"current interval is {state.current_interval_days} day"
                f"{'' if state.current_interval_days == 1 else 's'})"
            )
        elif as_of == state.next_due_on:
            status = SchedulingStatus.DUE
            days_until = 0
            days_overdue = 0
            explanation = (
                f"due because last completed {days_since} day"
                f"{'' if days_since == 1 else 's'} ago, "
                f"current interval is {state.current_interval_days} day"
                f"{'' if state.current_interval_days == 1 else 's'}"
            )
        else:
            status = SchedulingStatus.OVERDUE
            days_until = None
            days_overdue = (as_of - state.next_due_on).days
            explanation = (
                f"overdue by {days_overdue} day"
                f"{'' if days_overdue == 1 else 's'} "
                f"(last completed {days_since} day"
                f"{'' if days_since == 1 else 's'} ago, "
                f"current interval is {state.current_interval_days} day"
                f"{'' if state.current_interval_days == 1 else 's'}, "
                f"was due on {state.next_due_on.isoformat()})"
            )

        return SchedulingDecision(
            status=status,
            as_of=as_of,
            learner_id=state.learner_id,
            unit_id=state.unit_id,
            last_completed_on=state.last_completed_on,
            current_interval_days=state.current_interval_days,
            next_due_on=state.next_due_on,
            days_since_completion=days_since,
            days_until_due=days_until,
            days_overdue=days_overdue,
            explanation=explanation,
        )
