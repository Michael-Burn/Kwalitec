"""Stateless completion rules for Learning Sessions.

Determines whether the Learning Session itself is educationally complete.
Must NEVER determine Journey / Topic Complete.
"""

from __future__ import annotations

from app.application.learning_session.dto.completion_result import CompletionResult
from app.application.learning_session.policies.reflection_policy import (
    ReflectionPolicy,
)
from app.domain.learning_journey.entities.learning_session import LearningSession
from app.domain.learning_journey.value_objects.session_state import SessionState


class CompletionPolicy:
    """Educational session-completion rules (stateless, deterministic)."""

    REQUIRE_REFLECTION = True
    REQUIRE_EVIDENCE = False

    @staticmethod
    def evaluate(session: LearningSession) -> CompletionResult:
        """Evaluate whether the Learning Session is educationally complete.

        Journey completion is always False — that authority belongs to the
        Learning Journey Engine alone.
        """
        blockers: list[str] = []
        session_finished = session.state == SessionState.COMPLETED
        reflection_required = (
            CompletionPolicy.REQUIRE_REFLECTION and session_finished
        )
        reflection_satisfied = (
            ReflectionPolicy.is_satisfied(session)
            if session_finished
            else False
        )
        evidence_recorded = len(session.evidence) > 0

        if session.state in {SessionState.ABANDONED, SessionState.SKIPPED}:
            return CompletionResult(
                is_complete=False,
                session_finished=False,
                reflection_required=False,
                reflection_satisfied=False,
                evidence_recorded=evidence_recorded,
                blockers=(f"session_{session.state.value}",),
                reason=(
                    f"Session is {session.state.value}; educational completion "
                    "does not apply"
                ),
                journey_complete=False,
            )

        if not session_finished:
            blockers.append("session_not_finished")
            return CompletionResult(
                is_complete=False,
                session_finished=False,
                reflection_required=False,
                reflection_satisfied=False,
                evidence_recorded=evidence_recorded,
                blockers=tuple(blockers),
                reason="Session has not finished; completion is not yet evaluable",
                journey_complete=False,
            )

        if reflection_required and not reflection_satisfied:
            blockers.append("reflection_unsatisfied")

        if CompletionPolicy.REQUIRE_EVIDENCE and not evidence_recorded:
            blockers.append("evidence_absent")

        is_complete = not blockers
        reason = (
            "Learning Session is educationally complete "
            "(session finished; reflection closed)"
            if is_complete
            else "Learning Session is not yet educationally complete"
        )
        return CompletionResult(
            is_complete=is_complete,
            session_finished=True,
            reflection_required=reflection_required,
            reflection_satisfied=reflection_satisfied,
            evidence_recorded=evidence_recorded,
            blockers=tuple(blockers),
            reason=reason,
            journey_complete=False,
        )

    @staticmethod
    def rejects_journey_completion() -> bool:
        """Session completion never authorises Journey / Topic Complete."""
        return True

    @staticmethod
    def rejects_mastery_estimation() -> bool:
        """Completion evaluation never estimates mastery."""
        return True
