"""Student-safe guidance scrubbing for Knowledge Architecture (KWP-014)."""

from __future__ import annotations

_FORBIDDEN: tuple[str, ...] = (
    "digital twin",
    "student twin",
    "evidence authority",
    "evidence package",
    "cognitive load",
    "mental load",
    "burnout",
    "overloaded",
    "pass probability",
    "guaranteed",
    "will definitely",
    "badge",
    "leaderboard",
)


def scrub(text: str) -> str:
    """Remove forbidden product/AI theatre phrasing from student copy."""
    out = (text or "").strip()
    lowered = out.lower()
    for phrase in _FORBIDDEN:
        if phrase in lowered:
            # Soft-remove by blanking the forbidden token region.
            idx = lowered.find(phrase)
            while idx >= 0:
                out = out[:idx] + out[idx + len(phrase) :]
                lowered = out.lower()
                idx = lowered.find(phrase)
    return " ".join(out.split()).strip()
