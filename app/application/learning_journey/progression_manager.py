"""Coordinate educational progression within a Learning Journey.

Session completed → evidence accumulated → reflection completed →
objective unlocked → recommendation updated.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from uuid import uuid4

from app.application.learning_journey.completion_manager import CompletionManager
from app.application.learning_journey.dto.progression_result import ProgressionResult
from app.application.learning_journey.exceptions import (
    InvalidJourneyState,
    InvalidProgression,
)
from app.application.learning_journey.policies.progression_policy import (
    ProgressionPolicy,
)
from app.application.learning_journey.recommendation_builder import (
    RecommendationBuilder,
)
from app.domain.learning_journey.entities.journey_history import (
    JourneyHistoryEntry,
    JourneyHistoryEventType,
)
from app.domain.learning_journey.entities.learning_journey import LearningJourney
from app.domain.learning_journey.entities.learning_session import LearningSession
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
from app.domain.learning_journey.value_objects.session_state import SessionState


class ProgressionManager:
    """Coordinate educational progression steps (domain objects only)."""

    def __init__(
        self,
        *,
        completion_manager: CompletionManager | None = None,
        recommendation_builder: RecommendationBuilder | None = None,
        clock: Callable[[], datetime] | None = None,
        history_id_factory: Callable[[], str] | None = None,
    ) -> None:
        self._completion = completion_manager or CompletionManager()
        self._recommendations = recommendation_builder or RecommendationBuilder()
        self._clock = clock or (lambda: datetime.now(tz=UTC))
        self._history_id_factory = history_id_factory or (
            lambda: f"hist-{uuid4().hex[:12]}"
        )

    def recalculate_progress(self, journey: LearningJourney) -> LearningJourney:
        """Refresh JourneyProgress from current artefacts."""
        progress = JourneyProgressService.calculate(journey)
        updated = journey.with_progress(progress)
        return self._append_history(
            updated,
            JourneyHistoryEventType.PROGRESS_RECALCULATED,
            detail_tags=(
                f"completion_status={progress.completion_status.value}",
                f"meets_criteria={progress.meets_completion_criteria}",
            ),
        )

    def validate_progression(self, journey: LearningJourney) -> None:
        """Validate aggregate consistency before progression.

        Raises:
            InvalidProgression: When consistency validation fails with errors.
        """
        result = JourneyValidationService.validate_consistency(journey)
        if not result.is_valid:
            messages = "; ".join(i.message for i in result.issues if i.is_error)
            raise InvalidProgression(messages or "Journey progression is invalid")

    def apply_session_completed(
        self,
        journey: LearningJourney,
        session: LearningSession,
        *,
        attach_recommendation: bool = True,
        auto_ready_for_completion: bool = True,
    ) -> ProgressionResult:
        """Coordinate progression after a session reaches COMPLETED.

        Expects ``session`` already in COMPLETED state and present (or to be
        merged) on the journey. Replaces the matching session on the journey,
        recalculates progress, optionally marks READY_FOR_COMPLETION, and
        refreshes the recommendation.
        """
        previous_state = journey.state
        previously_addressed = ProgressionPolicy.addressed_objective_ids(journey)

        if session.state != SessionState.COMPLETED:
            raise InvalidProgression(
                "apply_session_completed requires a COMPLETED session"
            )
        if journey.state in {
            JourneyState.PAUSED,
            JourneyState.DEFERRED,
            JourneyState.COMPLETED,
            JourneyState.ABANDONED,
            JourneyState.ARCHIVED,
        }:
            raise InvalidJourneyState(
                f"Cannot progress while journey is {journey.state.value}"
            )

        updated = self._replace_or_add_session(journey, session)
        if updated.state == JourneyState.NOT_STARTED:
            validation = JourneyValidationService.validate_journey_transition(
                updated.state,
                JourneyTransitionEvent.START_JOURNEY,
            )
            if validation.is_valid:
                updated = updated.apply_transition(
                    JourneyTransitionEvent.START_JOURNEY
                )

        updated = self.recalculate_progress(updated)
        unlocked = ProgressionPolicy.unlocked_objectives(
            updated,
            previously_addressed=previously_addressed,
        )

        if (
            auto_ready_for_completion
            and updated.progress.meets_completion_criteria
            and updated.state in {JourneyState.ACTIVE, JourneyState.RESUMED}
        ):
            evaluation = self._completion.evaluate(updated)
            if evaluation.eligible_for_ready:
                updated = updated.apply_transition(
                    JourneyTransitionEvent.COMPLETION_CRITERIA_MET
                )
                updated = self._append_history(
                    updated,
                    JourneyHistoryEventType.COMPLETION_CRITERIA_EVALUATED,
                    detail_tags=("eligible_for_ready=true",),
                )

        if attach_recommendation:
            updated, _ = self._recommendations.build_and_attach(updated)
            if updated.recommendations:
                latest = updated.recommendations[-1]
                updated = self._append_history(
                    updated,
                    JourneyHistoryEventType.RECOMMENDATION_PROPOSED,
                    detail_tags=(f"kind={latest.kind.value}",),
                    recommendation_id=latest.recommendation_id,
                )

        next_actions = ProgressionPolicy.next_actions_after_progression(
            updated,
            meets_completion_criteria=updated.progress.meets_completion_criteria,
        )
        return ProgressionResult(
            journey=updated,
            previous_state=previous_state,
            current_state=updated.state,
            unlocked_objectives=unlocked,
            next_actions=next_actions,
            state_changed=previous_state != updated.state,
            progress_recalculated=True,
            meets_completion_criteria=updated.progress.meets_completion_criteria,
        )

    def apply_reflection_captured(
        self,
        journey: LearningJourney,
        *,
        attach_recommendation: bool = True,
        auto_ready_for_completion: bool = True,
    ) -> ProgressionResult:
        """Recalculate progression after a reflection has been attached."""
        previous_state = journey.state
        previously_addressed = ProgressionPolicy.addressed_objective_ids(journey)
        self.validate_progression(journey)

        updated = self.recalculate_progress(journey)
        unlocked = ProgressionPolicy.unlocked_objectives(
            updated,
            previously_addressed=previously_addressed,
        )

        if (
            auto_ready_for_completion
            and updated.progress.meets_completion_criteria
            and updated.state in {JourneyState.ACTIVE, JourneyState.RESUMED}
        ):
            evaluation = self._completion.evaluate(updated)
            if evaluation.eligible_for_ready:
                updated = updated.apply_transition(
                    JourneyTransitionEvent.COMPLETION_CRITERIA_MET
                )

        if attach_recommendation:
            updated, _ = self._recommendations.build_and_attach(updated)

        next_actions = ProgressionPolicy.next_actions_after_progression(
            updated,
            meets_completion_criteria=updated.progress.meets_completion_criteria,
        )
        return ProgressionResult(
            journey=updated,
            previous_state=previous_state,
            current_state=updated.state,
            unlocked_objectives=unlocked,
            next_actions=next_actions,
            state_changed=previous_state != updated.state,
            progress_recalculated=True,
            meets_completion_criteria=updated.progress.meets_completion_criteria,
        )

    @staticmethod
    def _replace_or_add_session(
        journey: LearningJourney,
        session: LearningSession,
    ) -> LearningJourney:
        if session.journey_id != journey.journey_id:
            raise InvalidProgression("session journey_id must match journey")
        sessions = list(journey.sessions)
        replaced = False
        for idx, existing in enumerate(sessions):
            if existing.session_id == session.session_id:
                sessions[idx] = session
                replaced = True
                break
        if not replaced:
            existing_indexes = {s.sequence_index for s in sessions}
            if session.sequence_index in existing_indexes:
                raise InvalidProgression(
                    "session sequence_index must be unique within journey"
                )
            sessions.append(session)
        # Reconstruct via create to keep invariants.
        return LearningJourney.create(
            journey.journey_id,
            journey.learner_id,
            journey.topic_id,
            journey.curriculum_id,
            state=journey.state,
            objectives=list(journey.objectives),
            sessions=sessions,
            evidence=list(journey.evidence),
            reflections=list(journey.reflections),
            recommendations=list(journey.recommendations),
            progress=journey.progress,
            history=journey.history,
            study_plan_id=journey.study_plan_id,
        )

    def _append_history(
        self,
        journey: LearningJourney,
        event_type: JourneyHistoryEventType,
        *,
        detail_tags: tuple[str, ...] = (),
        session_id: str | None = None,
        recommendation_id: str | None = None,
    ) -> LearningJourney:
        entry = JourneyHistoryEntry.create(
            self._history_id_factory(),
            event_type,
            self._clock(),
            detail_tags=list(detail_tags),
            session_id=session_id,
            recommendation_id=recommendation_id,
        )
        return journey.with_history(journey.history.append(entry))
