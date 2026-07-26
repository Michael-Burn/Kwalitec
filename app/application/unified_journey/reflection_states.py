"""Guided Reflection Experience states and controls (P2-MS005).

Experience Layer states only. Transitions never persist responses or
trigger Evidence / Runtime A / Strategy / Adaptive / Twin.
"""

from __future__ import annotations

from enum import StrEnum

REFLECTION_STATE_AVAILABLE = "available"
REFLECTION_STATE_IN_PROGRESS = "in_progress"
REFLECTION_STATE_COMPLETED = "completed"
REFLECTION_STATE_SKIPPED = "skipped"
REFLECTION_STATE_VALUES = frozenset(
    {
        REFLECTION_STATE_AVAILABLE,
        REFLECTION_STATE_IN_PROGRESS,
        REFLECTION_STATE_COMPLETED,
        REFLECTION_STATE_SKIPPED,
        "",
    }
)

REFLECTION_STATUS_LABELS: dict[str, str] = {
    REFLECTION_STATE_AVAILABLE: "Reflection available",
    REFLECTION_STATE_IN_PROGRESS: "Reflecting",
    REFLECTION_STATE_COMPLETED: "Reflection complete",
    REFLECTION_STATE_SKIPPED: "Reflection skipped",
}


class ReflectionState(StrEnum):
    """Guided Reflection Experience states — presentation only."""

    AVAILABLE = REFLECTION_STATE_AVAILABLE
    IN_PROGRESS = REFLECTION_STATE_IN_PROGRESS
    COMPLETED = REFLECTION_STATE_COMPLETED
    SKIPPED = REFLECTION_STATE_SKIPPED


class ReflectionControl(StrEnum):
    """UI actions that update reflection presentation state only."""

    START = "start"
    COMPLETE = "complete"
    SKIP = "skip"


REFLECTION_CONTROL_VALUES = frozenset(ReflectionControl)

# States where Home presents the reflection step before day completion.
ACTIVE_REFLECTION_STATES = frozenset(
    {
        ReflectionState.AVAILABLE,
        ReflectionState.IN_PROGRESS,
    }
)

# Terminal presentation states — day completion may follow.
TERMINAL_REFLECTION_STATES = frozenset(
    {
        ReflectionState.COMPLETED,
        ReflectionState.SKIPPED,
    }
)


def resolve_reflection_state(
    value: ReflectionState | str | None,
) -> ReflectionState | None:
    """Resolve a reflection state; ``None`` / blank means not yet available."""
    if value is None:
        return None
    if isinstance(value, ReflectionState):
        return value
    key = (value or "").strip().lower()
    if not key:
        return None
    try:
        return ReflectionState(key)
    except ValueError as exc:
        raise ValueError(f"unknown reflection state: {value!r}") from exc


def resolve_reflection_control(
    value: ReflectionControl | str,
) -> ReflectionControl:
    """Resolve a reflection control identifier."""
    if isinstance(value, ReflectionControl):
        return value
    key = (value or "").strip().lower()
    try:
        return ReflectionControl(key)
    except ValueError as exc:
        raise ValueError(f"unknown reflection control: {value!r}") from exc


def reflection_status_label(state: ReflectionState | str | None) -> str:
    """Student-facing status label for a reflection state."""
    resolved = resolve_reflection_state(state)
    if resolved is None:
        return ""
    return REFLECTION_STATUS_LABELS[resolved.value]


def reflection_is_active(state: ReflectionState | str | None) -> bool:
    """True when Home should present the reflection step."""
    resolved = resolve_reflection_state(state)
    return resolved in ACTIVE_REFLECTION_STATES


def reflection_is_terminal(state: ReflectionState | str | None) -> bool:
    """True when reflection has finished (completed or skipped)."""
    resolved = resolve_reflection_state(state)
    return resolved in TERMINAL_REFLECTION_STATES
