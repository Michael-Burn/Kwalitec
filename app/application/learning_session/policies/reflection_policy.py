"""Stateless reflection rules for Learning Sessions.

Coordinates when reflection is required, which fields are owed, and when
deferral is lawful. Never invents student reflection content.
"""

from __future__ import annotations

from app.domain.learning_journey.entities.journey_reflection import (
    JourneyReflection,
    ReflectionPosture,
)
from app.domain.learning_journey.entities.learning_session import LearningSession
from app.domain.learning_journey.value_objects.session_state import SessionState


class ReflectionPolicy:
    """Educational reflection rules (stateless, deterministic)."""

    REQUIRE_ON_COMPLETE = True
    ALLOW_DEFER = True

    @staticmethod
    def is_required(session: LearningSession) -> bool:
        """True when a completed session still owes reflection capture."""
        if not ReflectionPolicy.REQUIRE_ON_COMPLETE:
            return False
        if session.state != SessionState.COMPLETED:
            return False
        reflection = session.reflection
        if reflection is None:
            return True
        if reflection.posture == ReflectionPosture.CAPTURED:
            return False
        if reflection.posture == ReflectionPosture.NOT_REQUIRED:
            return False
        return reflection.posture in {
            ReflectionPosture.PENDING,
            ReflectionPosture.DEFERRED_CAPTURE,
        }

    @staticmethod
    def is_satisfied(session: LearningSession) -> bool:
        """True when reflection posture meets educational closure expectations."""
        if session.state != SessionState.COMPLETED:
            return False
        reflection = session.reflection
        if reflection is None:
            return not ReflectionPolicy.REQUIRE_ON_COMPLETE
        if reflection.posture == ReflectionPosture.CAPTURED:
            return True
        if reflection.posture == ReflectionPosture.NOT_REQUIRED:
            return True
        if (
            reflection.posture == ReflectionPosture.DEFERRED_CAPTURE
            and ReflectionPolicy.ALLOW_DEFER
        ):
            # Deferral is an explicit temporary posture — not final satisfaction
            # for session educational closure.
            return False
        return False

    @staticmethod
    def may_defer(session: LearningSession) -> bool:
        """True when PENDING reflection may move to DEFERRED_CAPTURE."""
        if not ReflectionPolicy.ALLOW_DEFER:
            return False
        if session.state != SessionState.COMPLETED:
            return False
        reflection = session.reflection
        return (
            reflection is not None
            and reflection.posture == ReflectionPosture.PENDING
        )

    @staticmethod
    def may_capture(session: LearningSession) -> bool:
        """True when reflection content may be captured onto the session."""
        if session.state != SessionState.COMPLETED:
            return False
        reflection = session.reflection
        if reflection is None:
            return True
        return reflection.posture in {
            ReflectionPosture.PENDING,
            ReflectionPosture.DEFERRED_CAPTURE,
        }

    @staticmethod
    def required_fields() -> tuple[str, ...]:
        """Structural reflection fields owed on capture (not generated content)."""
        return (
            "summary",
            "challenges",
            "questions_remaining",
            "confidence",
            "next_intention",
        )

    @staticmethod
    def validate_capture_content(
        *,
        summary: str,
        challenges: str,
        confidence: str | None = None,
    ) -> tuple[str, ...]:
        """Return blocker tags for missing required capture content."""
        blockers: list[str] = []
        if not summary or not summary.strip():
            blockers.append("missing_summary")
        if not challenges or not challenges.strip():
            blockers.append("missing_challenges")
        if confidence is not None and not str(confidence).strip():
            blockers.append("missing_confidence")
        return tuple(blockers)

    @staticmethod
    def pending_artefact(
        reflection: JourneyReflection | None,
    ) -> bool:
        """True when a PENDING or DEFERRED reflection artefact exists."""
        if reflection is None:
            return False
        return reflection.posture in {
            ReflectionPosture.PENDING,
            ReflectionPosture.DEFERRED_CAPTURE,
        }
