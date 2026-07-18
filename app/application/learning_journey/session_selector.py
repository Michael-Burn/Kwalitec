"""Deterministic selection of the next Learning Session.

No AI, no randomness, no database access. Pure educational ordering rules.
"""

from __future__ import annotations

from app.application.learning_journey.dto.session_plan import SessionPlan
from app.application.learning_journey.exceptions import (
    InvalidJourneyState,
    SessionOrderingViolation,
)
from app.application.learning_journey.policies.progression_policy import (
    ProgressionPolicy,
)
from app.domain.learning_journey.entities.learning_journey import LearningJourney
from app.domain.learning_journey.entities.learning_objective import LearningObjective
from app.domain.learning_journey.entities.learning_session import LearningSession
from app.domain.learning_journey.value_objects.effort_estimate import EffortEstimate
from app.domain.learning_journey.value_objects.journey_state import JourneyState
from app.domain.learning_journey.value_objects.session_state import SessionState

# Deterministic activity tags by objective kind (not generated study content).
_ACTIVITIES_BY_KIND: dict[str, tuple[str, ...]] = {
    "understand": ("read_core_notes", "check_definitions", "self_explain"),
    "apply": ("worked_example", "guided_practice", "independent_attempt"),
    "analyse": ("compare_approaches", "diagnose_errors", "structure_solution"),
    "review": ("spaced_review", "concept_check", "summary_recall"),
    "revise": ("targeted_revision", "evidence_review", "weak_spot_drill"),
}
_DEFAULT_ACTIVITIES: tuple[str, ...] = (
    "focused_study",
    "practice_check",
    "brief_reflection_prep",
)


class SessionSelector:
    """Decide which Learning Session should occur next (deterministic)."""

    def current_session(self, journey: LearningJourney) -> LearningSession | None:
        """Return the session currently in educational focus, if any.

        Preference: ACTIVE → PAUSED → None.
        """
        ordered = journey.ordered_sessions()
        for session in ordered:
            if session.state == SessionState.ACTIVE:
                return session
        for session in ordered:
            if session.state == SessionState.PAUSED:
                return session
        return None

    def next_session(self, journey: LearningJourney) -> LearningSession | None:
        """Return the next session that should run.

        Rules (deterministic):
        1. Reject terminal / deferred journeys.
        2. Prefer current ACTIVE or PAUSED session.
        3. Else first NOT_STARTED by sequence_index.
        4. Else None (caller may plan a new session).
        """
        self._assert_selectable(journey)
        current = self.current_session(journey)
        if current is not None:
            return current
        for session in journey.ordered_sessions():
            if session.state == SessionState.NOT_STARTED:
                return session
        return None

    def build_session_plan(
        self,
        journey: LearningJourney,
        *,
        session: LearningSession | None = None,
    ) -> SessionPlan | None:
        """Build a SessionPlan for ``session`` or the next selectable session.

        Returns None when no session can be planned under current state.
        """
        if journey.state in {
            JourneyState.COMPLETED,
            JourneyState.ABANDONED,
            JourneyState.ARCHIVED,
            JourneyState.DEFERRED,
        }:
            return None
        if journey.state == JourneyState.PAUSED and session is None:
            # Paused journeys may only describe an existing paused session.
            paused = self.current_session(journey)
            if paused is None or paused.state != SessionState.PAUSED:
                return None
            session = paused

        target = session if session is not None else self.next_session(journey)
        if target is None:
            return self._plan_for_new_session(journey)

        self._assert_ordering(journey)
        objective = self._resolve_objective(journey, target.objective_id)
        activities = self._activities_for(objective)
        return SessionPlan(
            session_number=target.sequence_index + 1,
            sequence_index=target.sequence_index,
            session_id=target.session_id,
            objective=objective,
            expected_effort=target.estimated_effort,
            recommended_activities=activities,
            is_existing_session=True,
        )

    def _plan_for_new_session(self, journey: LearningJourney) -> SessionPlan | None:
        """Plan a prospective next session when none are pending."""
        if not ProgressionPolicy.may_start_session(journey):
            return None
        next_index = 0
        if journey.sessions:
            next_index = max(s.sequence_index for s in journey.sessions) + 1
        objective = ProgressionPolicy.next_unaddressed_objective(journey)
        if objective is None and journey.objectives:
            # All addressed — still allow revision-oriented planning.
            ordered = journey.ordered_objectives()
            objective = ordered[-1] if ordered else None
        effort = EffortEstimate.MEDIUM
        if objective is not None and objective.kind.value == "revise":
            effort = EffortEstimate.HIGH
        return SessionPlan(
            session_number=next_index + 1,
            sequence_index=next_index,
            session_id=None,
            objective=objective,
            expected_effort=effort,
            recommended_activities=self._activities_for(objective),
            is_existing_session=False,
        )

    @staticmethod
    def _resolve_objective(
        journey: LearningJourney,
        objective_id: str | None,
    ) -> LearningObjective | None:
        if not objective_id:
            return ProgressionPolicy.current_focus_objective(journey)
        for objective in journey.objectives:
            if objective.objective_id == objective_id:
                return objective
        return None

    @staticmethod
    def _activities_for(objective: LearningObjective | None) -> tuple[str, ...]:
        if objective is None:
            return _DEFAULT_ACTIVITIES
        return _ACTIVITIES_BY_KIND.get(objective.kind.value, _DEFAULT_ACTIVITIES)

    @staticmethod
    def _assert_selectable(journey: LearningJourney) -> None:
        if journey.state in {
            JourneyState.COMPLETED,
            JourneyState.ABANDONED,
            JourneyState.ARCHIVED,
        }:
            raise InvalidJourneyState(
                f"Cannot select sessions for journey in state {journey.state.value}"
            )
        if journey.state == JourneyState.DEFERRED:
            raise InvalidJourneyState(
                "Cannot select sessions while journey is deferred"
            )

    @staticmethod
    def _assert_ordering(journey: LearningJourney) -> None:
        seen: set[int] = set()
        for session in journey.sessions:
            if session.sequence_index < 0:
                raise SessionOrderingViolation(
                    f"Session {session.session_id} has negative sequence_index"
                )
            if session.sequence_index in seen:
                raise SessionOrderingViolation(
                    f"Duplicate session sequence_index {session.sequence_index}"
                )
            seen.add(session.sequence_index)
            if session.journey_id != journey.journey_id:
                raise SessionOrderingViolation(
                    f"Session {session.session_id} journey_id mismatch"
                )
