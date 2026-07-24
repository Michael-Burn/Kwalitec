"""Coordinates structured student reflection for a Learning Session.

Supports questions remaining, confidence, summary, challenges, and next
intention. Never invents student content. Never estimates mastery.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime

from app.application.learning_session.dto.reflection_summary import ReflectionSummary
from app.application.learning_session.exceptions import (
    InvalidSessionState,
    ReflectionRequired,
)
from app.application.learning_session.policies.reflection_policy import (
    ReflectionPolicy,
)
from app.domain.learning_journey.entities.journey_reflection import (
    JourneyReflection,
    ReflectionConfidence,
    ReflectionPosture,
)
from app.domain.learning_journey.entities.learning_session import LearningSession
from app.domain.learning_journey.value_objects.session_state import SessionState

logger = logging.getLogger(__name__)


class ReflectionManager:
    """Attach pending / captured / deferred reflection to a session."""

    def __init__(self, *, clock=None, id_factory=None) -> None:
        self._clock = clock or (lambda: datetime.now(tz=UTC))
        self._id_factory = id_factory or (lambda: "ref")

    def attach_pending(self, session: LearningSession) -> LearningSession:
        """Attach a PENDING reflection after session completion.

        Raises:
            InvalidSessionState: When session is not COMPLETED.
        """
        if session.state != SessionState.COMPLETED:
            raise InvalidSessionState(
                "Pending reflection requires a COMPLETED session"
            )
        if session.reflection is not None:
            if session.reflection.posture == ReflectionPosture.CAPTURED:
                return session
            if ReflectionPolicy.pending_artefact(session.reflection):
                return session
        pending = JourneyReflection.create_pending(
            f"ref-{self._id_factory()}",
            session.session_id,
            session.journey_id,
        )
        return session.with_reflection(pending)

    def capture(
        self,
        session: LearningSession,
        *,
        summary: str,
        challenges: str,
        questions_remaining: list[str] | tuple[str, ...] | None = None,
        confidence: ReflectionConfidence | str = ReflectionConfidence.UNSURE,
        next_intention: str | None = None,
        user_id: int | None = None,
    ) -> tuple[LearningSession, ReflectionSummary]:
        """Capture structured student reflection onto a completed session.

        Field mapping to domain ``JourneyReflection``:
        - summary → what_was_learned
        - challenges → uncertainty
        - questions_remaining / next_intention → questions_remaining

        When ``user_id`` is provided, analytics observes the successful capture
        **after** the reflection is attached (fail-open; never affects capture).

        Raises:
            InvalidSessionState / ReflectionRequired (content blockers).
        """
        if not ReflectionPolicy.may_capture(session):
            raise InvalidSessionState(
                "Cannot capture reflection in the current session posture"
            )
        blockers = ReflectionPolicy.validate_capture_content(
            summary=summary,
            challenges=challenges,
            confidence=(
                confidence.value
                if isinstance(confidence, ReflectionConfidence)
                else confidence
            ),
        )
        if blockers:
            raise ReflectionRequired(
                f"Reflection capture blocked: {', '.join(blockers)}"
            )

        questions = list(questions_remaining or ())
        intention = (next_intention or "").strip() or None
        if intention:
            questions.append(f"next_intention: {intention}")

        if session.reflection is not None and ReflectionPolicy.pending_artefact(
            session.reflection
        ):
            captured = session.reflection.with_captured_content(
                what_was_learned=summary,
                uncertainty=challenges,
                questions_remaining=questions,
                confidence=confidence,
                captured_at=self._clock(),
            )
        else:
            captured = JourneyReflection.create_captured(
                f"ref-{self._id_factory()}",
                session.session_id,
                session.journey_id,
                what_was_learned=summary,
                uncertainty=challenges,
                questions_remaining=questions,
                confidence=confidence,
                captured_at=self._clock(),
            )
        updated = session.with_reflection(captured)
        summary_dto = self.summarise(updated, next_intention=intention)
        # Analytics observes success only — never before capture completes.
        if user_id is not None and updated.reflection is not None:
            ReflectionManager._observe_reflection_captured(
                user_id=user_id,
                reflection_id=updated.reflection.reflection_id,
                session_id=updated.session_id,
            )
        return updated, summary_dto

    @staticmethod
    def _observe_reflection_captured(
        *,
        user_id: int,
        reflection_id: str,
        session_id: str,
    ) -> None:
        """Emit reflection.submitted + reflection.completed after capture.

        Fail-open: analytics errors never affect reflection processing.
        """
        try:
            from app.infrastructure.analytics.reflection_events import (
                emit_reflection_lifecycle,
            )

            emit_reflection_lifecycle(
                user_id=user_id,
                reflection_id=reflection_id,
                session_id=session_id,
            )
        except Exception:  # noqa: BLE001 — analytics must never break learning
            logger.exception(
                "analytics.emit_failed reflection capture reflection=%s user=%s",
                reflection_id,
                user_id,
            )

    def defer(self, session: LearningSession) -> LearningSession:
        """Move PENDING reflection to DEFERRED_CAPTURE under policy.

        Raises:
            InvalidSessionState: When deferral is unlawful.
        """
        if not ReflectionPolicy.may_defer(session):
            raise InvalidSessionState(
                "Cannot defer reflection in the current session posture"
            )
        assert session.reflection is not None
        deferred = JourneyReflection(
            reflection_id=session.reflection.reflection_id,
            session_id=session.reflection.session_id,
            journey_id=session.reflection.journey_id,
            posture=ReflectionPosture.DEFERRED_CAPTURE,
            what_was_learned=session.reflection.what_was_learned,
            uncertainty=session.reflection.uncertainty,
            questions_remaining=session.reflection.questions_remaining,
            confidence=session.reflection.confidence,
            captured_at=session.reflection.captured_at,
        )
        return session.with_reflection(deferred)

    def summarise(
        self,
        session: LearningSession,
        *,
        next_intention: str | None = None,
    ) -> ReflectionSummary:
        """Build an immutable reflection summary for ``session``."""
        reflection = session.reflection
        if reflection is None:
            posture = (
                ReflectionPosture.PENDING.value
                if session.state == SessionState.COMPLETED
                else ReflectionPosture.NOT_REQUIRED.value
            )
            return ReflectionSummary(
                session_id=session.session_id,
                posture=posture,
                is_captured=False,
                questions_remaining=(),
                confidence=None,
                summary=None,
                challenges=None,
                next_intention=None,
            )

        questions = reflection.questions_remaining
        intention = next_intention
        cleaned_questions: list[str] = []
        for question in questions:
            if question.startswith("next_intention:"):
                if intention is None:
                    intention = question.split(":", 1)[1].strip() or None
            else:
                cleaned_questions.append(question)

        return ReflectionSummary(
            session_id=session.session_id,
            posture=reflection.posture.value,
            is_captured=reflection.posture == ReflectionPosture.CAPTURED,
            questions_remaining=tuple(cleaned_questions),
            confidence=(
                reflection.confidence.value if reflection.confidence else None
            ),
            summary=reflection.what_was_learned,
            challenges=reflection.uncertainty,
            next_intention=intention,
        )
