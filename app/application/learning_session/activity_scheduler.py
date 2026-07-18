"""Deterministic activity scheduling for Learning Sessions.

Produces next-action recommendations for breaks, reflection, continuation,
revision, and next session. Never generates study content.
"""

from __future__ import annotations

from app.application.learning_session.dto.completion_result import CompletionResult
from app.application.learning_session.policies.scheduling_policy import (
    NextAction,
    SchedulingPolicy,
)
from app.application.learning_session.runtime_phase import RuntimePhase
from app.domain.learning_journey.entities.learning_session import LearningSession


class ActivityScheduler:
    """Recommend the next educational activity for a session."""

    def next_action(
        self,
        session: LearningSession,
        *,
        phase: RuntimePhase,
        completion: CompletionResult,
        actual_duration_minutes: int | None = None,
    ) -> NextAction:
        """Return a deterministic next-action recommendation."""
        action = SchedulingPolicy.decide(
            session,
            phase=phase,
            completion=completion,
            actual_duration_minutes=actual_duration_minutes,
        )
        if (
            action == NextAction.NEXT_SESSION
            and SchedulingPolicy.revise_after_thin_evidence(session)
        ):
            return NextAction.REVISE
        return action

    def recommend_break(
        self,
        session: LearningSession,
        *,
        actual_duration_minutes: int | None = None,
    ) -> bool:
        """True when a break is warranted under scheduling policy."""
        return SchedulingPolicy.should_recommend_break(
            session,
            actual_duration_minutes=actual_duration_minutes,
        )
