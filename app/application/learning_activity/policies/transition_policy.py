"""Stateless transition rules for Learning Activities."""

from __future__ import annotations

from app.domain.learning_activity.value_objects.activity_state import (
    LAWFUL_ACTIVITY_TRANSITIONS,
    ActivityState,
    ActivityTransitionEvent,
    is_terminal_activity_state,
    next_activity_state,
)


class TransitionPolicy:
    """Educational activity transition rules (stateless, deterministic)."""

    @staticmethod
    def is_lawful(
        current: ActivityState,
        event: ActivityTransitionEvent,
    ) -> bool:
        """True when ``current`` + ``event`` is a lawful transition."""
        return next_activity_state(current, event) is not None

    @staticmethod
    def next_state(
        current: ActivityState,
        event: ActivityTransitionEvent,
    ) -> ActivityState | None:
        """Return the next state, or None if unlawful."""
        return next_activity_state(current, event)

    @staticmethod
    def allowed_events(current: ActivityState) -> tuple[ActivityTransitionEvent, ...]:
        """Return events lawful from ``current``."""
        return tuple(
            event
            for (state, event), _ in LAWFUL_ACTIVITY_TRANSITIONS.items()
            if state == current
        )

    @staticmethod
    def is_terminal(state: ActivityState) -> bool:
        """True when the activity may not resume educational work."""
        return is_terminal_activity_state(state)

    @staticmethod
    def rejects_invalid_transitions() -> bool:
        """Transition policy never allows unlawful transitions."""
        return True
