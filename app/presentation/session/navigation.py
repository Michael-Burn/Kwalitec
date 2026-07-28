"""Session flow navigation helpers — linear steps only."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.session_experience.session_navigation import (
    SESSION_FLOW,
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
    """Build minimal linear progress steps for the session chrome.

    CQ-002 / CR1: the happy path finishes from Summary → Home. Keep Complete
    as a navigable surface, but omit it from the visible progress chrome so
    students are not shown a phantom fifth step (PX-003 N16).
    """
    resolved = SessionSurface(str(active).strip().lower())
    visible = tuple(
        s for s in SESSION_FLOW if s is not SessionSurface.COMPLETE
    )
    if resolved is SessionSurface.COMPLETE:
        # Terminal Complete: mark all visible steps complete.
        return tuple(
            SessionNavStep(
                surface=surface.value,
                label=SURFACE_LABELS[surface],
                endpoint=SURFACE_ENDPOINTS[surface],
                is_active=False,
                is_complete=True,
                step_number=idx + 1,
            )
            for idx, surface in enumerate(visible)
        )
    active_idx = list(visible).index(resolved)
    steps: list[SessionNavStep] = []
    for idx, surface in enumerate(visible):
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
    """Return ``(eyebrow, title, description)`` for ``surface``.

    CQ-002: student-facing step count matches the visible chrome (Complete
    omitted), while Complete itself is labelled as the return-home close.
    """
    resolved = SessionSurface(str(surface).strip().lower())
    visible = tuple(s for s in SESSION_FLOW if s is not SessionSurface.COMPLETE)
    if resolved is SessionSurface.COMPLETE:
        step, total = len(visible), len(visible)
    else:
        step = list(visible).index(resolved) + 1
        total = len(visible)
    eyebrow = f"Session · Step {step} of {total}"
    title = SURFACE_LABELS[resolved]
    description = step_label(resolved)
    return eyebrow, title, description
