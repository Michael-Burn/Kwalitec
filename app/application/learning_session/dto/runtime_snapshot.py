"""Immutable snapshot of Learning Session Runtime posture."""

from __future__ import annotations

from dataclasses import dataclass

from app.application.learning_session.dto.completion_result import CompletionResult
from app.application.learning_session.dto.evidence_summary import EvidenceSummary
from app.application.learning_session.dto.learning_session_plan import (
    LearningSessionPlan,
)
from app.application.learning_session.dto.reflection_summary import ReflectionSummary
from app.domain.learning_journey.value_objects.session_state import SessionState


@dataclass(frozen=True)
class RuntimeSnapshot:
    """Read-only educational snapshot of a Learning Session at runtime.

    Attributes:
        session_id: Session identity.
        journey_id: Parent journey identity.
        topic_id: Curriculum topic when known from the plan.
        phase: Runtime lifecycle phase (PLANNED…ARCHIVED vocabulary).
        session_state: Domain SessionState.
        objective_id: Primary objective in focus, if any.
        plan: Plan used to create / guide the session, if available.
        evidence_summary: Session-scoped evidence posture.
        reflection_summary: Session-scoped reflection posture.
        completion: Session completion evaluation.
        next_action: Deterministic next-action recommendation tag.
        actual_duration_minutes: Observed duration when known.
    """

    session_id: str
    journey_id: str
    topic_id: str | None
    phase: str
    session_state: SessionState
    objective_id: str | None
    plan: LearningSessionPlan | None
    evidence_summary: EvidenceSummary
    reflection_summary: ReflectionSummary
    completion: CompletionResult
    next_action: str
    actual_duration_minutes: int | None
