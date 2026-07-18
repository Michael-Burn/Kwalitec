"""Progress tracking across a Learning Activity sequence."""

from __future__ import annotations

from app.application.learning_activity.dto.activity_sequence import ActivitySequence
from app.application.learning_activity.policies.progression_policy import (
    ProgressionPolicy,
)
from app.domain.learning_activity.entities.activity_progress import ActivityProgress
from app.domain.learning_activity.entities.learning_activity import LearningActivity


class ProgressionManager:
    """Current / completed / remaining activities and progress percentage."""

    def current(self, sequence: ActivitySequence) -> LearningActivity | None:
        """Return the activity currently in focus."""
        return ProgressionPolicy.current_activity(sequence)

    def completed(
        self, sequence: ActivitySequence
    ) -> tuple[LearningActivity, ...]:
        """Return COMPLETED activities in sequence order."""
        return ProgressionPolicy.completed_activities(sequence)

    def remaining(
        self, sequence: ActivitySequence
    ) -> tuple[LearningActivity, ...]:
        """Return non-terminal activities in sequence order."""
        return ProgressionPolicy.remaining_activities(sequence)

    def skipped(self, sequence: ActivitySequence) -> tuple[LearningActivity, ...]:
        """Return SKIPPED activities in sequence order."""
        return ProgressionPolicy.skipped_activities(sequence)

    def next(
        self,
        sequence: ActivitySequence,
        *,
        after: LearningActivity | None = None,
    ) -> LearningActivity | None:
        """Return the next remaining activity."""
        return ProgressionPolicy.next_activity(sequence, after=after)

    def previous(
        self,
        sequence: ActivitySequence,
        *,
        before: LearningActivity | None = None,
    ) -> LearningActivity | None:
        """Return the previous activity."""
        return ProgressionPolicy.previous_activity(sequence, before=before)

    def percentage(self, sequence: ActivitySequence) -> float:
        """Return 0–100 progress percentage."""
        return ProgressionPolicy.progress_percentage(sequence)

    def summarise(self, sequence: ActivitySequence) -> ActivityProgress:
        """Build an ActivityProgress summary."""
        return ProgressionPolicy.build_progress(sequence)
