"""Completion evaluation for Learning Activities and sequences.

Never completes a Learning Session. Returns only ready_for_session_completion.
"""

from __future__ import annotations

from app.application.learning_activity.dto.activity_result import ActivityResult
from app.application.learning_activity.dto.activity_sequence import ActivitySequence
from app.application.learning_activity.policies.completion_policy import (
    CompletionPolicy,
)
from app.domain.learning_activity.entities.learning_activity import LearningActivity


class CompletionManager:
    """Determine activity / sequence completion and session-ready signal."""

    def evaluate_activity(
        self,
        sequence: ActivitySequence,
        activity: LearningActivity,
    ) -> ActivityResult:
        """Evaluate whether a specific activity is complete."""
        return CompletionPolicy.evaluate(sequence, activity=activity)

    def evaluate_sequence(self, sequence: ActivitySequence) -> ActivityResult:
        """Evaluate sequence completion and session readiness."""
        return CompletionPolicy.evaluate(sequence)

    def is_activity_complete(self, activity: LearningActivity) -> bool:
        """True when the activity is COMPLETED."""
        return CompletionPolicy.is_activity_complete(activity)

    def is_sequence_complete(self, sequence: ActivitySequence) -> bool:
        """True when all activities are terminal."""
        return CompletionPolicy.is_sequence_complete(sequence)

    def ready_for_session_completion(self, sequence: ActivitySequence) -> bool:
        """True when Session Runtime may consider completing the session.

        Never completes the session.
        """
        return CompletionPolicy.ready_for_session_completion(sequence)
