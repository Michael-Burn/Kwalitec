"""Immutable result of evaluating Learning Session completion."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CompletionResult:
    """Whether the Learning Session itself is educationally complete.

    Never asserts Journey / Topic Complete. Session completion is a local
    educational closure signal only.

    Attributes:
        is_complete: True when session work and required reflection are closed.
        session_finished: True when session state is COMPLETED.
        reflection_required: True when reflection is owed by policy.
        reflection_satisfied: True when required reflection is captured or
            explicitly not required / deferred under policy.
        evidence_recorded: True when at least one evidence item is attached.
        blockers: Deterministic blocker tags when not complete.
        reason: Human-readable educational explanation.
        journey_complete: Always False — session runtime never completes journeys.
    """

    is_complete: bool
    session_finished: bool
    reflection_required: bool
    reflection_satisfied: bool
    evidence_recorded: bool
    blockers: tuple[str, ...]
    reason: str
    journey_complete: bool = False
