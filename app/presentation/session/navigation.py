"""Session flow navigation helpers — linear steps only."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.session_experience.session_navigation import (
    SESSION_FLOW,
    flow_position,
    step_label,
)
from app.domain.session_experience.session_workspace import (
    SURFACE_LABELS,
    SessionSurface,
)

SURFACE_ENDPOINTS: dict[SessionSurface, str] = {
    SessionSurface.OVERVIEW: "session.overview",
    SessionSurface.ACTIVITY: "session.activity",
    SessionSurface.REFLECTION: "session.reflection",
    SessionSurface.SUMMARY: "session.summary",
    SessionSurface.COMPLETE: "session.complete",
}


@dataclass(frozen=True)
class SessionNavStep:
    surface: str
    label: str
    endpoint: str
    is_active: bool
    is_complete: bool
    step_number: int


def build_session_steps(
    active: SessionSurface | str, *, session_id: str
) -> tuple[SessionNavStep, ...]:
    """Build minimal linear progress steps for the session chrome."""
    resolved = SessionSurface(str(active).strip().lower())
    active_idx = list(SESSION_FLOW).index(resolved)
    steps: list[SessionNavStep] = []
    for idx, surface in enumerate(SESSION_FLOW):
        # Complete is terminal — still listed for flow awareness.
        steps.append(
            SessionNavStep(
                surface=surface.value,
                label=SURFACE_LABELS[surface],
                endpoint=SURFACE_ENDPOINTS[surface],
                is_active=surface is resolved,
                is_complete=idx < active_idx,
                step_number=idx + 1,
            )
        )
    return tuple(steps)


def page_meta(surface: SessionSurface | str) -> tuple[str, str, str]:
    """Return ``(eyebrow, title, description)`` for ``surface``."""
    resolved = SessionSurface(str(surface).strip().lower())
    step, total = flow_position(resolved)
    eyebrow = f"Session · Step {step} of {total}"
    title = SURFACE_LABELS[resolved]
    description = step_label(resolved)
    return eyebrow, title, description
