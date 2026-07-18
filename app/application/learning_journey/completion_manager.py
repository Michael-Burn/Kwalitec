"""Determine whether a Learning Journey is eligible for completion.

Never allows completion solely from session finish, time spent, or
percentage reached. Educational domain criteria are authoritative.
"""

from __future__ import annotations

from app.application.learning_journey.exceptions import (
    InvalidJourneyState,
    InvalidProgression,
    JourneyAlreadyCompleted,
)
from app.application.learning_journey.policies.completion_policy import (
    CompletionEvaluation,
    CompletionPolicy,
)
from app.domain.learning_journey.entities.learning_journey import LearningJourney
from app.domain.learning_journey.services.journey_progress_service import (
    JourneyProgressService,
)
from app.domain.learning_journey.services.journey_validation_service import (
    JourneyValidationService,
)
from app.domain.learning_journey.value_objects.journey_state import (
    JourneyState,
    JourneyTransitionEvent,
)


class CompletionManager:
    """Educational completion eligibility and confirmation coordination."""

    def __init__(self, *, policy: CompletionPolicy | None = None) -> None:
        self._policy = policy or CompletionPolicy()

    def evaluate(self, journey: LearningJourney) -> CompletionEvaluation:
        """Evaluate completion eligibility without mutating the journey."""
        return self._policy.evaluate(journey)

    def validate_completion(self, journey: LearningJourney) -> CompletionEvaluation:
        """Validate whether Topic Complete may be confirmed.

        Raises:
            JourneyAlreadyCompleted: When already COMPLETED.
            InvalidProgression: When criteria are not met for confirmation.
        """
        if journey.state == JourneyState.COMPLETED:
            raise JourneyAlreadyCompleted(
                f"Journey {journey.journey_id} is already completed"
            )
        evaluation = self.evaluate(journey)
        if journey.state != JourneyState.READY_FOR_COMPLETION:
            raise InvalidJourneyState(
                "Journey must be READY_FOR_COMPLETION before Topic Complete"
            )
        if not evaluation.eligible_for_confirm:
            raise InvalidProgression(
                f"Cannot confirm Topic Complete: {evaluation.reason}"
            )
        return evaluation

    def mark_ready_for_completion(
        self,
        journey: LearningJourney,
    ) -> LearningJourney:
        """Transition ACTIVE/RESUMED → READY_FOR_COMPLETION when eligible.

        Raises:
            InvalidProgression: When educational criteria are not met.
            InvalidJourneyState: When the transition is unlawful.
        """
        evaluation = self.evaluate(journey)
        if not evaluation.eligible_for_ready:
            raise InvalidProgression(
                f"Cannot mark ready for completion: {evaluation.reason}"
                + (
                    f" blockers={list(evaluation.blockers)}"
                    if evaluation.blockers
                    else ""
                )
            )
        validation = JourneyValidationService.validate_journey_transition(
            journey.state,
            JourneyTransitionEvent.COMPLETION_CRITERIA_MET,
            meets_completion_criteria=True,
        )
        if not validation.is_valid:
            raise InvalidJourneyState(
                validation.issues[0].message if validation.issues else "invalid"
            )
        progress = JourneyProgressService.calculate(journey)
        updated = journey.with_progress(progress)
        return updated.apply_transition(JourneyTransitionEvent.COMPLETION_CRITERIA_MET)

    def confirm_topic_complete(
        self,
        journey: LearningJourney,
    ) -> LearningJourney:
        """Confirm Topic Complete (READY_FOR_COMPLETION → COMPLETED).

        Raises:
            JourneyAlreadyCompleted: When already completed.
            InvalidProgression / InvalidJourneyState: When unlawful.
        """
        self.validate_completion(journey)
        pending = JourneyValidationService.validate_journey_transition(
            journey.state,
            JourneyTransitionEvent.CONFIRM_TOPIC_COMPLETE,
            meets_completion_criteria=True,
            pending_reflection=False,
        )
        if not pending.is_valid:
            raise InvalidJourneyState(
                pending.issues[0].message if pending.issues else "invalid"
            )
        return journey.apply_transition(JourneyTransitionEvent.CONFIRM_TOPIC_COMPLETE)

    def rejects_shallow_completion(self, journey: LearningJourney) -> bool:
        """True when shallow signals alone would be insufficient."""
        return (
            self._policy.rejects_session_only_completion(journey)
            or self._policy.rejects_time_or_percentage_alone()
        )
