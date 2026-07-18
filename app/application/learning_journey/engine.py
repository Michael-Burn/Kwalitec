"""Learning Journey Engine — public application interface.

Sole authority for educational progression within a Learning Journey.
Coordinates domain objects only; never persists, never touches Flask /
SQLAlchemy / UI.

Future Mission Engine 2.0, Twin 2.0, Recommendation, Revision, and Analytics
consumers must call this engine rather than inventing parallel progression.
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from app.application.learning_journey.completion_manager import CompletionManager
from app.application.learning_journey.coordinator import LearningJourneyCoordinator
from app.application.learning_journey.dto.journey_snapshot import JourneySnapshot
from app.application.learning_journey.dto.progression_result import ProgressionResult
from app.application.learning_journey.dto.recommendation_result import (
    RecommendationResult,
)
from app.application.learning_journey.dto.session_plan import SessionPlan
from app.application.learning_journey.exceptions import (
    InvalidJourneyState,
    JourneyAlreadyCompleted,
    JourneyNotFound,
)
from app.application.learning_journey.policies.completion_policy import (
    CompletionEvaluation,
)
from app.application.learning_journey.progression_manager import ProgressionManager
from app.application.learning_journey.recommendation_builder import (
    RecommendationBuilder,
)
from app.application.learning_journey.session_selector import SessionSelector
from app.domain.learning_journey.entities.journey_history import (
    JourneyHistory,
    JourneyHistoryEntry,
    JourneyHistoryEventType,
)
from app.domain.learning_journey.entities.learning_journey import LearningJourney
from app.domain.learning_journey.entities.learning_objective import LearningObjective
from app.domain.learning_journey.entities.learning_session import LearningSession
from app.domain.learning_journey.interfaces.learning_journey_repository import (
    LearningJourneyRepository,
)
from app.domain.learning_journey.value_objects.journey_state import (
    JourneyState,
    JourneyTransitionEvent,
)


class LearningJourneyEngine:
    """Public facade for Learning Journey educational orchestration.

    Persistence is never performed here. When a repository is supplied it is
    used only for read lookups (``load`` / identity resolution). Callers
    remain responsible for saving returned aggregates.
    """

    def __init__(
        self,
        *,
        repository: LearningJourneyRepository | None = None,
        coordinator: LearningJourneyCoordinator | None = None,
        session_selector: SessionSelector | None = None,
        recommendation_builder: RecommendationBuilder | None = None,
        progression_manager: ProgressionManager | None = None,
        completion_manager: CompletionManager | None = None,
        clock=None,
        id_factory=None,
    ) -> None:
        self._repository = repository
        self._clock = clock or (lambda: datetime.now(tz=UTC))
        self._id_factory = id_factory or (lambda: uuid4().hex[:12])
        self._sessions = session_selector or SessionSelector()
        self._recommendations = recommendation_builder or RecommendationBuilder(
            clock=self._clock,
        )
        self._completion = completion_manager or CompletionManager()
        self._progression = progression_manager or ProgressionManager(
            completion_manager=self._completion,
            recommendation_builder=self._recommendations,
            clock=self._clock,
        )
        self._coordinator = coordinator or LearningJourneyCoordinator(
            session_selector=self._sessions,
            recommendation_builder=self._recommendations,
            progression_manager=self._progression,
            completion_manager=self._completion,
        )

    # ------------------------------------------------------------------
    # Journey lifecycle
    # ------------------------------------------------------------------

    def create_journey(
        self,
        *,
        learner_id: str,
        topic_id: str,
        curriculum_id: str,
        journey_id: str | None = None,
        objectives: (
            list[LearningObjective] | tuple[LearningObjective, ...] | None
        ) = None,
        sessions: list[LearningSession] | tuple[LearningSession, ...] | None = None,
        study_plan_id: str | None = None,
    ) -> LearningJourney:
        """Create a new Learning Journey aggregate (NOT_STARTED).

        Does not persist. Records a JOURNEY_CREATED history entry.
        """
        jid = journey_id or f"journey-{self._id_factory()}"
        history = JourneyHistory.empty().append(
            JourneyHistoryEntry.create(
                f"hist-{self._id_factory()}",
                JourneyHistoryEventType.JOURNEY_CREATED,
                self._clock(),
                detail_tags=(
                    f"topic={topic_id}",
                    f"curriculum={curriculum_id}",
                ),
            )
        )
        return LearningJourney.create(
            jid,
            learner_id,
            topic_id,
            curriculum_id,
            state=JourneyState.NOT_STARTED,
            objectives=list(objectives or ()),
            sessions=list(sessions or ()),
            history=history,
            study_plan_id=study_plan_id,
        )

    def load_journey(self, journey_id: str) -> LearningJourney:
        """Load a journey via the injected repository (read-only).

        Raises:
            JourneyNotFound: When absent or no repository is configured.
        """
        if self._repository is None:
            raise JourneyNotFound(
                "No repository configured; pass a journey object instead"
            )
        journey = self._repository.get_by_id(journey_id)
        if journey is None:
            raise JourneyNotFound(f"Journey {journey_id!r} not found")
        return journey

    def resume_journey(self, journey: LearningJourney) -> LearningJourney:
        """Resume a PAUSED journey (PAUSED → RESUMED → ACTIVE).

        Raises:
            JourneyAlreadyCompleted: When completed.
            InvalidJourneyState: When resume is unlawful.
        """
        self._reject_if_completed(journey)
        if journey.state == JourneyState.RESUMED:
            return journey.apply_transition(JourneyTransitionEvent.SETTLE_ACTIVE)
        if journey.state != JourneyState.PAUSED:
            raise InvalidJourneyState(
                f"Cannot resume journey in state {journey.state.value}"
            )
        resumed = journey.apply_transition(JourneyTransitionEvent.RESUME_JOURNEY)
        return resumed.apply_transition(JourneyTransitionEvent.SETTLE_ACTIVE)

    def pause_journey(self, journey: LearningJourney) -> LearningJourney:
        """Pause an ACTIVE, RESUMED, or READY_FOR_COMPLETION journey."""
        self._reject_if_completed(journey)
        if journey.state == JourneyState.PAUSED:
            return journey
        if journey.state not in {
            JourneyState.ACTIVE,
            JourneyState.RESUMED,
            JourneyState.READY_FOR_COMPLETION,
        }:
            raise InvalidJourneyState(
                f"Cannot pause journey in state {journey.state.value}"
            )
        return journey.apply_transition(JourneyTransitionEvent.PAUSE_JOURNEY)

    def start_journey(self, journey: LearningJourney) -> LearningJourney:
        """Activate a NOT_STARTED journey."""
        self._reject_if_completed(journey)
        if journey.state == JourneyState.ACTIVE:
            return journey
        if journey.state != JourneyState.NOT_STARTED:
            raise InvalidJourneyState(
                f"Cannot start journey in state {journey.state.value}"
            )
        return journey.apply_transition(JourneyTransitionEvent.START_JOURNEY)

    def defer_journey(self, journey: LearningJourney) -> LearningJourney:
        """Defer a journey under explicit educational pause-of-plan rules."""
        self._reject_if_completed(journey)
        if journey.state not in {
            JourneyState.NOT_STARTED,
            JourneyState.ACTIVE,
            JourneyState.PAUSED,
        }:
            raise InvalidJourneyState(
                f"Cannot defer journey in state {journey.state.value}"
            )
        return journey.apply_transition(JourneyTransitionEvent.DEFER_JOURNEY)

    def abandon_journey(self, journey: LearningJourney) -> LearningJourney:
        """Abandon a non-terminal journey."""
        if journey.state in {
            JourneyState.COMPLETED,
            JourneyState.ABANDONED,
            JourneyState.ARCHIVED,
        }:
            if journey.state == JourneyState.COMPLETED:
                raise JourneyAlreadyCompleted(
                    f"Journey {journey.journey_id} is already completed"
                )
            return journey
        return journey.apply_transition(JourneyTransitionEvent.ABANDON_JOURNEY)

    def reactivate_journey(self, journey: LearningJourney) -> LearningJourney:
        """Reactivate a DEFERRED journey to ACTIVE."""
        if journey.state != JourneyState.DEFERRED:
            raise InvalidJourneyState(
                f"Cannot reactivate journey in state {journey.state.value}"
            )
        return journey.apply_transition(JourneyTransitionEvent.REACTIVATE_JOURNEY)

    # ------------------------------------------------------------------
    # Educational queries
    # ------------------------------------------------------------------

    def current_objective(
        self,
        journey: LearningJourney,
    ) -> LearningObjective | None:
        """Determine the current learning objective in focus."""
        return self._coordinator.current_objective(journey)

    def current_learning_session(
        self,
        journey: LearningJourney,
    ) -> LearningSession | None:
        """Determine the current learning session in focus."""
        return self._coordinator.current_session(journey)

    def next_learning_session(
        self,
        journey: LearningJourney,
    ) -> LearningSession | None:
        """Determine the next learning session that should occur."""
        return self._coordinator.next_session(journey)

    def session_plan(self, journey: LearningJourney) -> SessionPlan | None:
        """Build a deterministic plan for the next session block."""
        return self._coordinator.session_plan(journey)

    def generate_recommendation(
        self,
        journey: LearningJourney,
    ) -> RecommendationResult:
        """Generate an educational recommendation (does not mutate)."""
        return self._coordinator.generate_recommendation(journey)

    def validate_progression(self, journey: LearningJourney) -> None:
        """Validate educational progression consistency.

        Raises:
            InvalidProgression: When consistency errors are present.
        """
        self._coordinator.validate_progression(journey)

    def validate_completion(self, journey: LearningJourney) -> CompletionEvaluation:
        """Validate Topic Complete confirmation eligibility.

        Raises:
            JourneyAlreadyCompleted / InvalidJourneyState / InvalidProgression.
        """
        return self._coordinator.validate_completion(journey)

    def evaluate_completion(self, journey: LearningJourney) -> CompletionEvaluation:
        """Evaluate completion criteria without requiring READY state."""
        return self._coordinator.evaluate_completion(journey)

    def mark_ready_for_completion(
        self,
        journey: LearningJourney,
    ) -> LearningJourney:
        """Move to READY_FOR_COMPLETION when educationally eligible."""
        return self._completion.mark_ready_for_completion(journey)

    def confirm_topic_complete(
        self,
        journey: LearningJourney,
    ) -> LearningJourney:
        """Confirm Topic Complete when READY_FOR_COMPLETION and criteria hold."""
        return self._completion.confirm_topic_complete(journey)

    def apply_session_completed(
        self,
        journey: LearningJourney,
        session: LearningSession,
    ) -> ProgressionResult:
        """Coordinate progression after a session is completed."""
        return self._coordinator.apply_session_completed(journey, session)

    def apply_reflection_captured(
        self,
        journey: LearningJourney,
    ) -> ProgressionResult:
        """Coordinate progression after a reflection is captured."""
        return self._coordinator.apply_reflection_captured(journey)

    def orchestrate(self, journey: LearningJourney) -> LearningJourney:
        """Run the full coordinator pass (validate → progress → recommend)."""
        return self._coordinator.orchestrate(journey)

    def generate_journey_snapshot(
        self,
        journey: LearningJourney,
    ) -> JourneySnapshot:
        """Generate an immutable educational snapshot for consumers."""
        return self._coordinator.snapshot(journey)

    @staticmethod
    def _reject_if_completed(journey: LearningJourney) -> None:
        if journey.state == JourneyState.COMPLETED:
            raise JourneyAlreadyCompleted(
                f"Journey {journey.journey_id} is already completed"
            )
