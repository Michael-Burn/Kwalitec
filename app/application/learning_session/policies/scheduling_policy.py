"""Stateless activity scheduling rules for Learning Sessions.

Produces deterministic recommendations for breaks, reflection, continuation,
revision, and next-session advice. Never generates study content or
estimates mastery.
"""

from __future__ import annotations

from enum import StrEnum

from app.application.learning_session.dto.completion_result import CompletionResult
from app.application.learning_session.policies.reflection_policy import (
    ReflectionPolicy,
)
from app.application.learning_session.runtime_phase import RuntimePhase
from app.domain.learning_journey.entities.learning_session import LearningSession
from app.domain.learning_journey.value_objects.effort_estimate import (
    EffortEstimate,
    effort_at_least,
)
from app.domain.learning_journey.value_objects.session_state import SessionState


class NextAction(StrEnum):
    """Deterministic next-action recommendation tags."""

    PREPARE = "prepare"
    START = "start"
    CONTINUE = "continue"
    BREAK = "break"
    REFLECT = "reflect"
    REVISE = "revise"
    NEXT_SESSION = "next_session"
    ARCHIVE = "archive"
    NONE = "none"


class SchedulingPolicy:
    """Educational activity scheduling rules (stateless, deterministic)."""

    BREAK_EFFORT_FLOOR = EffortEstimate.HIGH
    BREAK_DURATION_MINUTES = 45

    @staticmethod
    def decide(
        session: LearningSession,
        *,
        phase: RuntimePhase,
        completion: CompletionResult,
        actual_duration_minutes: int | None = None,
    ) -> NextAction:
        """Select the next educational action for the session.

        Priority (deterministic):
        1. ARCHIVED → NONE
        2. COMPLETED + reflection owed → REFLECT
        3. COMPLETED + educationally complete → ARCHIVE (or NEXT_SESSION)
        4. COMPLETED + reflection deferred → REFLECT
        5. ACTIVE + high effort / long duration → BREAK
        6. ACTIVE → CONTINUE
        7. PAUSED → CONTINUE (resume)
        8. READY → START
        9. PLANNED → PREPARE
        10. Thin evidence on completed work → REVISE hint when reflecting done
        """
        if phase == RuntimePhase.ARCHIVED:
            return NextAction.NONE

        if phase == RuntimePhase.COMPLETED or session.state == SessionState.COMPLETED:
            if ReflectionPolicy.is_required(session):
                return NextAction.REFLECT
            if completion.is_complete:
                return NextAction.NEXT_SESSION
            return NextAction.ARCHIVE

        if phase == RuntimePhase.ACTIVE:
            if SchedulingPolicy.should_recommend_break(
                session,
                actual_duration_minutes=actual_duration_minutes,
            ):
                return NextAction.BREAK
            return NextAction.CONTINUE

        if phase == RuntimePhase.PAUSED:
            return NextAction.CONTINUE

        if phase == RuntimePhase.READY:
            return NextAction.START

        if phase == RuntimePhase.PLANNED:
            return NextAction.PREPARE

        return NextAction.NONE

    @staticmethod
    def should_recommend_break(
        session: LearningSession,
        *,
        actual_duration_minutes: int | None = None,
    ) -> bool:
        """True when a short break is educationally warranted (deterministic)."""
        if session.state != SessionState.ACTIVE:
            return False
        if actual_duration_minutes is not None and (
            actual_duration_minutes >= SchedulingPolicy.BREAK_DURATION_MINUTES
        ):
            return True
        return effort_at_least(
            session.estimated_effort,
            SchedulingPolicy.BREAK_EFFORT_FLOOR,
        ) and (
            actual_duration_minutes is not None and actual_duration_minutes >= 30
        )

    @staticmethod
    def revise_after_thin_evidence(session: LearningSession) -> bool:
        """True when completed session has no evidence — suggest revise later."""
        return (
            session.state == SessionState.COMPLETED
            and len(session.evidence) == 0
            and not ReflectionPolicy.is_required(session)
        )
