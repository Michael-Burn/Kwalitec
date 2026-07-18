"""Evaluates whether a Learning Session itself is educationally complete.

Must NOT determine Journey / Topic Complete. That authority belongs solely
to the Learning Journey Engine.
"""

from __future__ import annotations

from app.application.learning_session.dto.completion_result import CompletionResult
from app.application.learning_session.policies.completion_policy import (
    CompletionPolicy,
)
from app.domain.learning_journey.entities.learning_session import LearningSession


class CompletionEvaluator:
    """Session-local completion evaluation (never journey completion)."""

    def evaluate(self, session: LearningSession) -> CompletionResult:
        """Evaluate educational completeness of ``session`` only."""
        result = CompletionPolicy.evaluate(session)
        # Hard invariant: session runtime never claims journey completion.
        if result.journey_complete:
            return CompletionResult(
                is_complete=result.is_complete,
                session_finished=result.session_finished,
                reflection_required=result.reflection_required,
                reflection_satisfied=result.reflection_satisfied,
                evidence_recorded=result.evidence_recorded,
                blockers=result.blockers,
                reason=result.reason,
                journey_complete=False,
            )
        return result

    @staticmethod
    def asserts_session_not_journey() -> bool:
        """Documentation/test hook: session complete ≠ journey complete."""
        return CompletionPolicy.rejects_journey_completion()
