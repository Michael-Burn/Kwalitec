"""Mission-completion continuity chrome — presentation copy only (PX-004).

Makes Reflection → Journey → Readiness → Coach → Home feel continuous.
Does not compute readiness, journey, or coaching content.
"""

from __future__ import annotations

from dataclasses import dataclass

COMPLETION_FLOW_STEPS: tuple[str, ...] = (
    "Reflection",
    "Journey",
    "Readiness",
    "Coach",
    "Home",
)

_SUCCESS_BY_ORIGIN: dict[str, str] = {
    "reflection": (
        "Reflection saved. Your journey, readiness, and coach context "
        "now reflect this session."
    ),
    "session": "Session complete. Continue with a short reflection while it is fresh.",
    "mission": "Mission ready. Begin when you have a focused block of time.",
}


@dataclass(frozen=True, slots=True)
class ContinuityBanner:
    """Calm continuity ribbon for post-action navigation."""

    origin: str
    steps: tuple[str, ...]
    active_step: str
    success_message: str
    readiness_hint: str


def success_reward_message(origin: str | None) -> str | None:
    """Return a subtle, professional success line for a completed action."""
    key = (origin or "").strip().lower()
    if not key:
        return None
    return _SUCCESS_BY_ORIGIN.get(key)


def continuity_from_query(
    *,
    from_surface: str | None = None,
    updated: str | None = None,
) -> ContinuityBanner | None:
    """Build continuity chrome from request query flags — no domain calls."""
    origin = (from_surface or "").strip().lower()
    if origin not in {"reflection", "session", "mission"}:
        return None
    if (updated or "").strip().lower() not in {"1", "true", "yes"}:
        # Still allow continuity ribbon after reflection redirects.
        if origin != "reflection":
            return None

    active = "Home" if origin == "reflection" else COMPLETION_FLOW_STEPS[0]
    success = success_reward_message(origin) or "Update saved."
    readiness_hint = (
        "Readiness and coach insight refresh from the evidence you just captured."
        if origin == "reflection"
        else ""
    )
    return ContinuityBanner(
        origin=origin,
        steps=COMPLETION_FLOW_STEPS,
        active_step=active,
        success_message=success,
        readiness_hint=readiness_hint,
    )
