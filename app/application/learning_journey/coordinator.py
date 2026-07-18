"""Orchestrate Learning Journey educational flow.

Coordinates: Journey → Validation → Progress → Recommendation →
Session Selection → Completion Check.

Does not persist. Does not touch Flask or SQLAlchemy.
"""

from __future__ import annotations

from app.application.learning_journey.completion_manager import CompletionManager
from app.application.learning_journey.dto.journey_snapshot import (
    EvidenceSummary,
    JourneySnapshot,
    ReflectionSummary,
)
from app.application.learning_journey.dto.progression_result import ProgressionResult
from app.application.learning_journey.dto.recommendation_result import (
    RecommendationResult,
)
from app.application.learning_journey.dto.session_plan import SessionPlan
from app.application.learning_journey.exceptions import InvalidJourneyState
from app.application.learning_journey.policies.completion_policy import (
    CompletionEvaluation,
)
from app.application.learning_journey.policies.progression_policy import (
    ProgressionPolicy,
)
from app.application.learning_journey.progression_manager import ProgressionManager
from app.application.learning_journey.recommendation_builder import (
    RecommendationBuilder,
)
from app.application.learning_journey.session_selector import SessionSelector
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


class LearningJourneyCoordinator:
    """Application orchestrator for Learning Journey educational behaviour."""

    def __init__(
        self,
        *,
        session_selector: SessionSelector | None = None,
        recommendation_builder: RecommendationBuilder | None = None,
        progression_manager: ProgressionManager | None = None,
        completion_manager: CompletionManager | None = None,
    ) -> None:
        self._sessions = session_selector or SessionSelector()
        self._recommendations = recommendation_builder or RecommendationBuilder()
        self._progression = progression_manager or ProgressionManager(
            recommendation_builder=self._recommendations,
            completion_manager=completion_manager,
        )
        self._completion = completion_manager or CompletionManager()

    def orchestrate(self, journey: LearningJourney) -> LearningJourney:
        """Full orchestration pass: validate → progress → recommend.

        Returns an updated journey aggregate. Caller owns persistence.
        """
        consistency = JourneyValidationService.validate_consistency(journey)
        if not consistency.is_valid:
            raise InvalidJourneyState(
                "; ".join(i.message for i in consistency.issues if i.is_error)
            )

        updated = self._progression.recalculate_progress(journey)

        evaluation = self._completion.evaluate(updated)
        if (
            evaluation.eligible_for_ready
            and updated.state in {JourneyState.ACTIVE, JourneyState.RESUMED}
        ):
            updated = updated.apply_transition(
                JourneyTransitionEvent.COMPLETION_CRITERIA_MET
            )

        updated, _ = self._recommendations.build_and_attach(updated)
        return updated

    def current_objective(self, journey: LearningJourney):
        """Determine the current learning objective in focus."""
        return ProgressionPolicy.current_focus_objective(journey)

    def current_session(self, journey: LearningJourney) -> LearningSession | None:
        """Determine the current learning session in focus."""
        return self._sessions.current_session(journey)

    def next_session(self, journey: LearningJourney) -> LearningSession | None:
        """Determine the next learning session that should occur."""
        return self._sessions.next_session(journey)

    def session_plan(self, journey: LearningJourney) -> SessionPlan | None:
        """Build a deterministic session plan for the next work block."""
        return self._sessions.build_session_plan(journey)

    def generate_recommendation(
        self,
        journey: LearningJourney,
    ) -> RecommendationResult:
        """Generate an educational recommendation without mutating."""
        return self._recommendations.build(journey)

    def validate_progression(self, journey: LearningJourney) -> None:
        """Validate that progression is educationally consistent."""
        self._progression.validate_progression(journey)

    def validate_completion(self, journey: LearningJourney) -> CompletionEvaluation:
        """Validate Topic Complete confirmation eligibility."""
        return self._completion.validate_completion(journey)

    def evaluate_completion(self, journey: LearningJourney) -> CompletionEvaluation:
        """Evaluate completion criteria without requiring READY state."""
        return self._completion.evaluate(journey)

    def apply_session_completed(
        self,
        journey: LearningJourney,
        session: LearningSession,
    ) -> ProgressionResult:
        """Progression after session completion."""
        return self._progression.apply_session_completed(journey, session)

    def apply_reflection_captured(
        self,
        journey: LearningJourney,
    ) -> ProgressionResult:
        """Progression after reflection capture."""
        return self._progression.apply_reflection_captured(journey)

    def snapshot(self, journey: LearningJourney) -> JourneySnapshot:
        """Generate a read-only educational snapshot.

        Recalculates progress for honesty without mutating the caller's
        journey object (uses a local progress derivation).
        """
        progress = JourneyProgressService.calculate(journey)
        current_objective = ProgressionPolicy.current_focus_objective(journey)
        pending = ProgressionPolicy.pending_reflection_sessions(journey)
        sessions_with_evidence = len(
            {
                e.session_id
                for e in journey.evidence
                if e.session_id is not None
            }
        )
        recommendation = None
        if journey.recommendations:
            recommendation = journey.recommendations[-1]
        else:
            built = self._recommendations.build(journey)
            recommendation = built.recommendation

        return JourneySnapshot(
            journey_id=journey.journey_id,
            learner_id=journey.learner_id,
            topic_id=journey.topic_id,
            curriculum_id=journey.curriculum_id,
            state=journey.state,
            completion_status=progress.completion_status,
            meets_completion_criteria=progress.meets_completion_criteria,
            current_objective=current_objective,
            sessions=journey.ordered_sessions(),
            evidence_summary=EvidenceSummary(
                evidence_count=progress.evidence_count,
                evidence_confidence=progress.evidence_confidence.value,
                sessions_with_evidence=sessions_with_evidence,
            ),
            reflection_summary=ReflectionSummary(
                reflections_captured=progress.reflections_captured,
                reflections_pending=len(pending),
                completed_sessions_owing_reflection=len(pending),
            ),
            recommendation=recommendation,
            objectives_total=progress.objectives_total,
            objectives_addressed=progress.objectives_addressed,
            sessions_completed=progress.sessions_completed,
        )
