"""Stateless progression rules for Learning Journey educational advancement.

Encapsulates when sessions, evidence, and reflections unlock further work.
Does not estimate mastery or invent competence scores.
"""

from __future__ import annotations

from app.domain.learning_journey.entities.journey_reflection import ReflectionPosture
from app.domain.learning_journey.entities.learning_journey import LearningJourney
from app.domain.learning_journey.entities.learning_objective import LearningObjective
from app.domain.learning_journey.entities.learning_session import LearningSession
from app.domain.learning_journey.value_objects.journey_state import JourneyState
from app.domain.learning_journey.value_objects.session_state import SessionState


class ProgressionPolicy:
    """Educational progression rules (stateless)."""

    @staticmethod
    def may_start_session(journey: LearningJourney) -> bool:
        """True when a new or existing session may become ACTIVE."""
        return journey.state in {
            JourneyState.NOT_STARTED,
            JourneyState.ACTIVE,
            JourneyState.RESUMED,
        }

    @staticmethod
    def may_advance_after_session(
        journey: LearningJourney,
        session: LearningSession,
    ) -> bool:
        """True when a completed session may contribute to progression."""
        if journey.state in {
            JourneyState.COMPLETED,
            JourneyState.ABANDONED,
            JourneyState.ARCHIVED,
            JourneyState.PAUSED,
            JourneyState.DEFERRED,
        }:
            return False
        return session.state == SessionState.COMPLETED

    @staticmethod
    def session_reflection_satisfied(
        journey: LearningJourney,
        session: LearningSession,
    ) -> bool:
        """True when a completed session has a CAPTURED reflection."""
        if session.reflection is not None:
            if session.reflection.posture == ReflectionPosture.CAPTURED:
                return True
            if session.reflection.posture == ReflectionPosture.PENDING:
                return False
        for reflection in journey.reflections:
            if reflection.session_id != session.session_id:
                continue
            if reflection.posture == ReflectionPosture.CAPTURED:
                return True
            if reflection.posture == ReflectionPosture.PENDING:
                return False
        return False

    @staticmethod
    def pending_reflection_sessions(
        journey: LearningJourney,
    ) -> tuple[LearningSession, ...]:
        """Completed sessions that still owe a CAPTURED reflection."""
        pending: list[LearningSession] = []
        for session in journey.ordered_sessions():
            if session.state != SessionState.COMPLETED:
                continue
            if not ProgressionPolicy.session_reflection_satisfied(journey, session):
                pending.append(session)
        return tuple(pending)

    @staticmethod
    def addressed_objective_ids(journey: LearningJourney) -> frozenset[str]:
        """Objective ids contacted by active/completed sessions or evidence."""
        addressed: set[str] = set()
        objective_ids = {o.objective_id for o in journey.objectives}
        for session in journey.sessions:
            if (
                session.objective_id
                and session.objective_id in objective_ids
                and session.state
                in {
                    SessionState.COMPLETED,
                    SessionState.ACTIVE,
                    SessionState.PAUSED,
                }
            ):
                addressed.add(session.objective_id)
        for item in journey.evidence:
            if item.objective_id and item.objective_id in objective_ids:
                addressed.add(item.objective_id)
        return frozenset(addressed)

    @staticmethod
    def unlocked_objectives(
        journey: LearningJourney,
        *,
        previously_addressed: frozenset[str],
    ) -> tuple[LearningObjective, ...]:
        """Objectives newly addressed relative to ``previously_addressed``."""
        now = ProgressionPolicy.addressed_objective_ids(journey)
        newly = now - previously_addressed
        return tuple(
            o for o in journey.ordered_objectives() if o.objective_id in newly
        )

    @staticmethod
    def next_unaddressed_objective(
        journey: LearningJourney,
    ) -> LearningObjective | None:
        """First ordered objective not yet addressed, or None."""
        addressed = ProgressionPolicy.addressed_objective_ids(journey)
        for objective in journey.ordered_objectives():
            if objective.objective_id not in addressed:
                return objective
        return None

    @staticmethod
    def current_focus_objective(
        journey: LearningJourney,
    ) -> LearningObjective | None:
        """Objective currently in educational focus.

        Prefers the objective of an ACTIVE/PAUSED session, else the next
        unaddressed objective, else the last completed session's objective.
        """
        for session in journey.ordered_sessions():
            if session.state in {SessionState.ACTIVE, SessionState.PAUSED}:
                if session.objective_id:
                    for objective in journey.objectives:
                        if objective.objective_id == session.objective_id:
                            return objective
                return None
        next_obj = ProgressionPolicy.next_unaddressed_objective(journey)
        if next_obj is not None:
            return next_obj
        for session in reversed(journey.ordered_sessions()):
            if session.state == SessionState.COMPLETED and session.objective_id:
                for objective in journey.objectives:
                    if objective.objective_id == session.objective_id:
                        return objective
        return None

    @staticmethod
    def next_actions_after_progression(
        journey: LearningJourney,
        *,
        meets_completion_criteria: bool,
    ) -> tuple[str, ...]:
        """Deterministic structural next-action tags."""
        actions: list[str] = []
        pending = ProgressionPolicy.pending_reflection_sessions(journey)
        if pending:
            actions.append("capture_reflection")
        if journey.state == JourneyState.READY_FOR_COMPLETION:
            actions.append("confirm_topic_complete")
            return tuple(actions)
        if meets_completion_criteria and journey.state in {
            JourneyState.ACTIVE,
            JourneyState.RESUMED,
        }:
            actions.append("evaluate_completion_criteria")
        for session in journey.ordered_sessions():
            if session.state in {SessionState.ACTIVE, SessionState.PAUSED}:
                actions.append("continue_current_session")
                return tuple(actions)
        if ProgressionPolicy.next_unaddressed_objective(journey) is not None:
            actions.append("begin_next_objective")
        elif any(s.state == SessionState.NOT_STARTED for s in journey.sessions):
            actions.append("start_next_session")
        else:
            actions.append("plan_next_session")
        return tuple(actions)
