"""Stateless progression rules for Learning Activity sequences."""

from __future__ import annotations

from app.application.learning_activity.dto.activity_sequence import ActivitySequence
from app.domain.learning_activity.entities.activity_progress import ActivityProgress
from app.domain.learning_activity.entities.learning_activity import LearningActivity
from app.domain.learning_activity.value_objects.activity_state import (
    ActivityState,
    is_terminal_activity_state,
)


class ProgressionPolicy:
    """Educational activity progression rules (stateless, deterministic)."""

    @staticmethod
    def current_activity(
        sequence: ActivitySequence,
    ) -> LearningActivity | None:
        """Return the activity currently in focus.

        Preference order: ACTIVE, then PAUSED, then first NOT_STARTED.
        """
        active = [
            a for a in sequence.activities if a.state == ActivityState.ACTIVE
        ]
        if active:
            return min(active, key=lambda a: a.sequence_index)
        paused = [
            a for a in sequence.activities if a.state == ActivityState.PAUSED
        ]
        if paused:
            return min(paused, key=lambda a: a.sequence_index)
        pending = [
            a for a in sequence.activities if a.state == ActivityState.NOT_STARTED
        ]
        if pending:
            return min(pending, key=lambda a: a.sequence_index)
        return None

    @staticmethod
    def completed_activities(
        sequence: ActivitySequence,
    ) -> tuple[LearningActivity, ...]:
        """Return COMPLETED activities in sequence order."""
        return tuple(
            a for a in sequence.activities if a.state == ActivityState.COMPLETED
        )

    @staticmethod
    def skipped_activities(
        sequence: ActivitySequence,
    ) -> tuple[LearningActivity, ...]:
        """Return SKIPPED activities in sequence order."""
        return tuple(
            a for a in sequence.activities if a.state == ActivityState.SKIPPED
        )

    @staticmethod
    def remaining_activities(
        sequence: ActivitySequence,
    ) -> tuple[LearningActivity, ...]:
        """Return non-terminal activities in sequence order."""
        return tuple(
            a
            for a in sequence.activities
            if not is_terminal_activity_state(a.state)
        )

    @staticmethod
    def next_activity(
        sequence: ActivitySequence,
        *,
        after: LearningActivity | None = None,
    ) -> LearningActivity | None:
        """Return the next remaining activity after ``after`` (or current)."""
        reference = after or ProgressionPolicy.current_activity(sequence)
        remaining = ProgressionPolicy.remaining_activities(sequence)
        if not remaining:
            return None
        if reference is None:
            return remaining[0]
        for activity in remaining:
            if activity.sequence_index > reference.sequence_index:
                return activity
        return None

    @staticmethod
    def previous_activity(
        sequence: ActivitySequence,
        *,
        before: LearningActivity | None = None,
    ) -> LearningActivity | None:
        """Return the previous activity before ``before`` (or current)."""
        reference = before or ProgressionPolicy.current_activity(sequence)
        if reference is None:
            return None
        prior = [
            a
            for a in sequence.activities
            if a.sequence_index < reference.sequence_index
        ]
        if not prior:
            return None
        return max(prior, key=lambda a: a.sequence_index)

    @staticmethod
    def progress_percentage(sequence: ActivitySequence) -> float:
        """Return 0–100 progress from terminal activities / total."""
        total = len(sequence.activities)
        if total == 0:
            return 0.0
        terminal = sum(
            1 for a in sequence.activities if is_terminal_activity_state(a.state)
        )
        return round(100.0 * terminal / total, 2)

    @staticmethod
    def build_progress(sequence: ActivitySequence) -> ActivityProgress:
        """Build an ActivityProgress summary from the sequence."""
        if not sequence.activities:
            return ActivityProgress.empty(sequence.session_id)
        current = ProgressionPolicy.current_activity(sequence)
        completed = ProgressionPolicy.completed_activities(sequence)
        skipped = ProgressionPolicy.skipped_activities(sequence)
        remaining = ProgressionPolicy.remaining_activities(sequence)
        return ActivityProgress(
            session_id=sequence.session_id,
            total_count=len(sequence.activities),
            completed_count=len(completed),
            skipped_count=len(skipped),
            remaining_count=len(remaining),
            current_activity_id=current.activity_id if current else None,
            current_index=current.sequence_index if current else -1,
            progress_percentage=ProgressionPolicy.progress_percentage(sequence),
        )
