"""Shared display-formatting helpers for student-facing surfaces.

PX-002A T1-2: a single source of truth for study-duration wording so Home,
Mission, and Session Overview never disagree on how the same number of
minutes is described. Formatting only — never compute the underlying
estimate.
"""

from __future__ import annotations


def format_minutes(minutes: int | None) -> str:
    """Format study minutes as a duration phrase, e.g. "1 hour 30 min"."""
    if minutes is None:
        return ""
    if minutes <= 0:
        return "Less than a minute"
    if minutes == 1:
        return "1 minute"
    if minutes < 60:
        return f"{minutes} minutes"
    hours, rem = divmod(minutes, 60)
    if rem == 0:
        return "1 hour" if hours == 1 else f"{hours} hours"
    hour_part = "1 hour" if hours == 1 else f"{hours} hours"
    return f"{hour_part} {rem} min"


def format_duration_estimate(minutes: int | None) -> str:
    """Format a duration with an "About" qualifier, e.g. "About 45 minutes"."""
    label = format_minutes(minutes)
    if not label or label == "Less than a minute":
        return label
    return f"About {label}"


def format_remaining_minutes(minutes: int | None) -> str:
    """Format remaining study minutes (e.g. "About 45 minutes remaining")."""
    label = format_minutes(minutes)
    if not label:
        return ""
    if label == "Less than a minute":
        return f"{label} remaining"
    return f"About {label} remaining"
