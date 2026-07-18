"""Structured reflection after a Learning Session.

Captures student voice: what was learned, remaining uncertainty, open
questions, and qualitative confidence. System must not invent reflection
content. Reflection is not Educational Evidence of understanding by itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class ReflectionPosture(StrEnum):
    """Whether reflection is owed, captured, or deferred."""

    NOT_REQUIRED = "not_required"
    PENDING = "pending"
    CAPTURED = "captured"
    DEFERRED_CAPTURE = "deferred_capture"


class ReflectionConfidence(StrEnum):
    """Student-reported qualitative confidence — not a mastery score."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    UNSURE = "unsure"


@dataclass(frozen=True)
class JourneyReflection:
    """Structured reflection closing a Learning Session educationally.

    Attributes:
        reflection_id: Stable identity.
        session_id: Session this reflection closes.
        journey_id: Parent journey identity.
        posture: Capture lifecycle posture.
        what_was_learned: Student summary of learning attempted / gained.
        uncertainty: What still feels unclear.
        questions_remaining: Open questions for the next session.
        confidence: Qualitative self-reported confidence.
        captured_at: When CAPTURED (None while PENDING).
    """

    reflection_id: str
    session_id: str
    journey_id: str
    posture: ReflectionPosture
    what_was_learned: str | None = None
    uncertainty: str | None = None
    questions_remaining: tuple[str, ...] = ()
    confidence: ReflectionConfidence | None = None
    captured_at: datetime | None = None

    @classmethod
    def create_pending(
        cls,
        reflection_id: str,
        session_id: str,
        journey_id: str,
    ) -> JourneyReflection:
        """Create a PENDING reflection owed after session completion."""
        return cls(
            reflection_id=_require_non_empty(reflection_id, "reflection_id"),
            session_id=_require_non_empty(session_id, "session_id"),
            journey_id=_require_non_empty(journey_id, "journey_id"),
            posture=ReflectionPosture.PENDING,
        )

    @classmethod
    def create_captured(
        cls,
        reflection_id: str,
        session_id: str,
        journey_id: str,
        *,
        what_was_learned: str,
        uncertainty: str,
        questions_remaining: list[str] | tuple[str, ...] | None = None,
        confidence: ReflectionConfidence | str = ReflectionConfidence.UNSURE,
        captured_at: datetime,
    ) -> JourneyReflection:
        """Create a CAPTURED reflection with student content.

        Raises:
            ValueError: When required identities or content fields are empty.
        """
        learned = _require_non_empty(what_was_learned, "what_was_learned")
        unclear = _require_non_empty(uncertainty, "uncertainty")
        conf = (
            confidence
            if isinstance(confidence, ReflectionConfidence)
            else ReflectionConfidence(confidence)
        )
        questions = tuple(
            q.strip() for q in (questions_remaining or ()) if q and q.strip()
        )
        return cls(
            reflection_id=_require_non_empty(reflection_id, "reflection_id"),
            session_id=_require_non_empty(session_id, "session_id"),
            journey_id=_require_non_empty(journey_id, "journey_id"),
            posture=ReflectionPosture.CAPTURED,
            what_was_learned=learned,
            uncertainty=unclear,
            questions_remaining=questions,
            confidence=conf,
            captured_at=captured_at,
        )

    def with_captured_content(
        self,
        *,
        what_was_learned: str,
        uncertainty: str,
        questions_remaining: list[str] | tuple[str, ...] | None = None,
        confidence: ReflectionConfidence | str = ReflectionConfidence.UNSURE,
        captured_at: datetime,
    ) -> JourneyReflection:
        """Transition PENDING / DEFERRED_CAPTURE → CAPTURED with content.

        Raises:
            ValueError: When posture cannot accept capture, or content empty.
        """
        if self.posture not in {
            ReflectionPosture.PENDING,
            ReflectionPosture.DEFERRED_CAPTURE,
        }:
            raise ValueError(
                f"cannot capture reflection from posture {self.posture.value}"
            )
        return JourneyReflection.create_captured(
            self.reflection_id,
            self.session_id,
            self.journey_id,
            what_was_learned=what_was_learned,
            uncertainty=uncertainty,
            questions_remaining=questions_remaining,
            confidence=confidence,
            captured_at=captured_at,
        )


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
