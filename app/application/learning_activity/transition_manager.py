"""Valid state transitions for Learning Activities.

Allowed::

    NOT_STARTED → ACTIVE → PAUSED ⇄ ACTIVE → COMPLETED
    NOT_STARTED | ACTIVE | PAUSED → SKIPPED

No invalid transitions.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.learning_activity.dto.activity_sequence import ActivitySequence
from app.application.learning_activity.dto.activity_transition import (
    ActivityTransition,
)
from app.application.learning_activity.exceptions import (
    ActivityAlreadyCompleted,
    ActivityAlreadySkipped,
    ActivityNotFound,
    TransitionError,
)
from app.application.learning_activity.policies.transition_policy import (
    TransitionPolicy,
)
from app.domain.learning_activity.entities.learning_activity import LearningActivity
from app.domain.learning_activity.value_objects.activity_state import (
    ActivityState,
    ActivityTransitionEvent,
)


@dataclass(frozen=True)
class TransitionResult:
    """Outcome of a lawful activity transition."""

    activity: LearningActivity
    sequence: ActivitySequence
    transition: ActivityTransition


class TransitionManager:
    """Enforce lawful Learning Activity state transitions."""

    def start(
        self,
        sequence: ActivitySequence,
        activity_id: str,
        *,
        allow_multiple_active: bool = False,
    ) -> TransitionResult:
        """NOT_STARTED → ACTIVE."""
        activity = self._require(sequence, activity_id)
        if not allow_multiple_active:
            active = [
                a for a in sequence.activities if a.state == ActivityState.ACTIVE
            ]
            if active and active[0].activity_id != activity_id:
                raise TransitionError(
                    f"Cannot start {activity_id!r}; activity "
                    f"{active[0].activity_id!r} is already ACTIVE"
                )
        return self._apply(sequence, activity, ActivityTransitionEvent.START)

    def pause(
        self, sequence: ActivitySequence, activity_id: str
    ) -> TransitionResult:
        """ACTIVE → PAUSED."""
        activity = self._require(sequence, activity_id)
        return self._apply(sequence, activity, ActivityTransitionEvent.PAUSE)

    def resume(
        self,
        sequence: ActivitySequence,
        activity_id: str,
        *,
        allow_multiple_active: bool = False,
    ) -> TransitionResult:
        """PAUSED → ACTIVE."""
        activity = self._require(sequence, activity_id)
        if not allow_multiple_active:
            active = [
                a for a in sequence.activities if a.state == ActivityState.ACTIVE
            ]
            if active and active[0].activity_id != activity_id:
                raise TransitionError(
                    f"Cannot resume {activity_id!r}; activity "
                    f"{active[0].activity_id!r} is already ACTIVE"
                )
        return self._apply(sequence, activity, ActivityTransitionEvent.RESUME)

    def complete(
        self, sequence: ActivitySequence, activity_id: str
    ) -> TransitionResult:
        """ACTIVE | PAUSED → COMPLETED."""
        activity = self._require(sequence, activity_id)
        return self._apply(sequence, activity, ActivityTransitionEvent.COMPLETE)

    def skip(
        self, sequence: ActivitySequence, activity_id: str
    ) -> TransitionResult:
        """NOT_STARTED | ACTIVE | PAUSED → SKIPPED."""
        activity = self._require(sequence, activity_id)
        return self._apply(sequence, activity, ActivityTransitionEvent.SKIP)

    def _apply(
        self,
        sequence: ActivitySequence,
        activity: LearningActivity,
        event: ActivityTransitionEvent,
    ) -> TransitionResult:
        self._reject_terminal(activity)
        if not TransitionPolicy.is_lawful(activity.state, event):
            raise TransitionError(
                f"Cannot {event.value} activity {activity.activity_id!r} "
                f"in state {activity.state.value}"
            )
        try:
            updated = activity.apply_transition(event)
        except ValueError as exc:
            raise TransitionError(str(exc)) from exc
        transition = ActivityTransition(
            activity_id=activity.activity_id,
            session_id=activity.session_id,
            event=event,
            from_state=activity.state,
            to_state=updated.state,
        )
        return TransitionResult(
            activity=updated,
            sequence=sequence.with_activity(updated),
            transition=transition,
        )

    @staticmethod
    def _require(sequence: ActivitySequence, activity_id: str) -> LearningActivity:
        activity = sequence.activity_by_id(activity_id)
        if activity is None:
            raise ActivityNotFound(f"Activity {activity_id!r} not found in sequence")
        return activity

    @staticmethod
    def _reject_terminal(activity: LearningActivity) -> None:
        if activity.state == ActivityState.COMPLETED:
            raise ActivityAlreadyCompleted(
                f"Activity {activity.activity_id} is already completed"
            )
        if activity.state == ActivityState.SKIPPED:
            raise ActivityAlreadySkipped(
                f"Activity {activity.activity_id} is already skipped"
            )
