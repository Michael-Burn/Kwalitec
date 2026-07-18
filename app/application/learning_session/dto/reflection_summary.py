"""Immutable summary of structured student reflection for a session."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReflectionSummary:
    """Compact reflection posture for a Learning Session.

    Maps student voice fields to a consumer-facing summary. Does not invent
    reflection content.

    Attributes:
        session_id: Session this reflection closes.
        posture: Reflection posture value (pending / captured / deferred / …).
        is_captured: True when posture is CAPTURED.
        questions_remaining: Open questions for the next session.
        confidence: Qualitative self-reported confidence, if captured.
        summary: Student summary of learning (what was learned).
        challenges: Student-reported challenges / uncertainty.
        next_intention: Stated next educational intention, if provided.
    """

    session_id: str
    posture: str
    is_captured: bool
    questions_remaining: tuple[str, ...]
    confidence: str | None
    summary: str | None
    challenges: str | None
    next_intention: str | None
