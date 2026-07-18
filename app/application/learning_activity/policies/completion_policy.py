"""Stateless completion rules for Learning Activities.

Determines activity / sequence completion and a ready-for-session signal.
Must NEVER complete a Learning Session.
"""

from __future__ import annotations

from app.application.learning_activity.dto.activity_result import ActivityResult
from app.application.learning_activity.dto.activity_sequence import ActivitySequence
from app.domain.learning_activity.entities.learning_activity import LearningActivity
from app.domain.learning_activity.value_objects.activity_state import (
    ActivityState,
    is_terminal_activity_state,
)


class CompletionPolicy:
    """Educational activity-completion rules (stateless, deterministic)."""

    # When True, sequence readiness requires at least one COMPLETED activity
    # (all-skipped sequences are not session-ready).
    REQUIRE_AT_LEAST_ONE_COMPLETED = True

    @staticmethod
    def is_activity_complete(activity: LearningActivity) -> bool:
        """True when the activity is in COMPLETED state."""
        return activity.state == ActivityState.COMPLETED

    @staticmethod
    def is_sequence_complete(sequence: ActivitySequence) -> bool:
        """True when every activity is terminal (COMPLETED or SKIPPED)."""
        if not sequence.activities:
            return False
        return all(is_terminal_activity_state(a.state) for a in sequence.activities)

    @staticmethod
    def ready_for_session_completion(sequence: ActivitySequence) -> bool:
        """True when the Session Runtime may consider completing the session.

        Never completes the session. All-skipped sequences are not ready when
        ``REQUIRE_AT_LEAST_ONE_COMPLETED`` is True.
        """
        if not CompletionPolicy.is_sequence_complete(sequence):
            return False
        if CompletionPolicy.REQUIRE_AT_LEAST_ONE_COMPLETED:
            return any(a.state == ActivityState.COMPLETED for a in sequence.activities)
        return True

    @staticmethod
    def evaluate(
        sequence: ActivitySequence,
        *,
        activity: LearningActivity | None = None,
    ) -> ActivityResult:
        """Evaluate activity and/or sequence completion posture."""
        completed = sum(
            1 for a in sequence.activities if a.state == ActivityState.COMPLETED
        )
        skipped = sum(
            1 for a in sequence.activities if a.state == ActivityState.SKIPPED
        )
        remaining = sum(
            1
            for a in sequence.activities
            if not is_terminal_activity_state(a.state)
        )
        activity_complete = (
            CompletionPolicy.is_activity_complete(activity)
            if activity is not None
            else False
        )
        sequence_complete = CompletionPolicy.is_sequence_complete(sequence)
        ready = CompletionPolicy.ready_for_session_completion(sequence)

        blockers: list[str] = []
        if activity is not None and not activity_complete:
            if activity.state == ActivityState.SKIPPED:
                blockers.append("activity_skipped")
            elif not is_terminal_activity_state(activity.state):
                blockers.append("activity_not_complete")
        if not sequence_complete:
            blockers.append("sequence_incomplete")
        elif not ready:
            blockers.append("no_completed_activity")

        if ready:
            reason = (
                "Activity sequence is ready for session completion "
                "(all activities terminal; at least one completed)"
            )
        elif sequence_complete:
            reason = (
                "Activity sequence is closed but not session-ready "
                "(no completed activity)"
            )
        else:
            reason = "Activity sequence is not yet complete"

        return ActivityResult(
            activity_id=activity.activity_id if activity else None,
            session_id=sequence.session_id,
            activity_complete=activity_complete,
            sequence_complete=sequence_complete,
            ready_for_session_completion=ready,
            blockers=tuple(blockers),
            reason=reason,
            completed_count=completed,
            skipped_count=skipped,
            remaining_count=remaining,
        )

    @staticmethod
    def rejects_session_completion() -> bool:
        """Activity completion never completes a Learning Session."""
        return True

    @staticmethod
    def rejects_journey_completion() -> bool:
        """Activity completion never authorises Journey / Topic Complete."""
        return True
