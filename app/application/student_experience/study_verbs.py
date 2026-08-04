"""Canonical student study-start verb family (PX-003 / PX-B-034).

Presentation / microcopy only. Does not change routing or selection.
"""

from __future__ import annotations

# Authoritative student-facing labels for the primary study CTA.
START_TODAY = "Start Today's Session"
CONTINUE = "Continue"
RESUME = "Continue"  # paused / in-progress uses the same continue family
DAY_COMPLETE = "Today's Session complete"
SYLLABUS_COMPLETE = "Syllabus complete"
GUIDANCE_UNAVAILABLE = "Guidance not yet published"
REVIEW_MISSION = "Review today's mission"


def canonical_start_label(raw: str | None, *, in_progress: bool = False) -> str:
    """Normalize any start/continue/resume variant to the canonical family."""
    if in_progress:
        return CONTINUE
    text = (raw or "").strip()
    if not text:
        return START_TODAY
    lowered = text.lower()
    if any(token in lowered for token in ("resume", "continue")):
        return CONTINUE
    if any(
        token in lowered
        for token in (
            "start today's session",
            "start study session",
            "start session",
            "begin session",
            "begin",
            "start",
        )
    ):
        return START_TODAY
    if text in {START_TODAY, "Start Session", "Begin Session", "Start"}:
        return START_TODAY
    return text
