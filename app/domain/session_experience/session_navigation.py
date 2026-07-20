"""Session navigation — linear Learning Session workflow only.

No branching. No dashboard hopping. One objective. One flow.
"""

from __future__ import annotations

from app.domain.session_experience.session_workspace import (
    CANONICAL_SURFACES,
    SessionSurface,
    resolve_surface,
    surface_index,
)

# Student Home → Overview → Activity → Reflection → Summary → Complete → Home
SESSION_FLOW: tuple[SessionSurface, ...] = CANONICAL_SURFACES

FLOW_STEP_LABELS: dict[SessionSurface, str] = {
    SessionSurface.OVERVIEW: "Review today's objective",
    SessionSurface.ACTIVITY: "Complete learning activities",
    SessionSurface.REFLECTION: "Reflect on what you learned",
    SessionSurface.SUMMARY: "Review session summary",
    SessionSurface.COMPLETE: "Return home",
}


def next_surface(surface: SessionSurface | str) -> SessionSurface | None:
    """Return the next surface in the linear flow, or None at the end."""
    idx = surface_index(surface)
    if idx >= len(SESSION_FLOW) - 1:
        return None
    return SESSION_FLOW[idx + 1]


def previous_surface(surface: SessionSurface | str) -> SessionSurface | None:
    """Return the previous surface in the linear flow, or None at the start."""
    idx = surface_index(surface)
    if idx <= 0:
        return None
    return SESSION_FLOW[idx - 1]


def can_advance(surface: SessionSurface | str) -> bool:
    """True when the flow has a next surface after ``surface``."""
    return next_surface(surface) is not None


def can_retreat(surface: SessionSurface | str) -> bool:
    """True when the flow has a previous surface before ``surface``."""
    return previous_surface(surface) is not None


def is_terminal(surface: SessionSurface | str) -> bool:
    """True when ``surface`` is the terminal Complete step."""
    return resolve_surface(surface) is SessionSurface.COMPLETE


def is_entry(surface: SessionSurface | str) -> bool:
    """True when ``surface`` is the Session Overview entry."""
    return resolve_surface(surface) is SessionSurface.OVERVIEW


def flow_position(surface: SessionSurface | str) -> tuple[int, int]:
    """Return ``(1-based step, total steps)`` for ``surface``."""
    idx = surface_index(surface)
    return idx + 1, len(SESSION_FLOW)


def assert_linear_advance(
    current: SessionSurface | str, target: SessionSurface | str
) -> SessionSurface:
    """Validate a single-step forward advance; raise on branching.

    Session Experience forbids skipping surfaces or jumping sideways.
    """
    resolved_current = resolve_surface(current)
    resolved_target = resolve_surface(target)
    expected = next_surface(resolved_current)
    if expected is None:
        raise ValueError(
            f"cannot advance beyond terminal surface {resolved_current.value!r}"
        )
    if resolved_target is not expected:
        raise ValueError(
            f"illegal session navigation: {resolved_current.value!r} → "
            f"{resolved_target.value!r}; expected {expected.value!r}"
        )
    return resolved_target


def step_label(surface: SessionSurface | str) -> str:
    """Student-facing step description for ``surface``."""
    return FLOW_STEP_LABELS[resolve_surface(surface)]
