"""Student-safe guidance scrubbing for Educational Authoring (KWP-015 / V1S-008).

Removes gamification and internal product theatre from authored copy without
mutating ordinary educational English. Short tokens such as ``xp`` must match
whole words only — never substrings inside Explain, exploratory, experience.
"""

from __future__ import annotations

import re

# Multi-word / distinctive phrases — safe as substring matches.
_FORBIDDEN_PHRASES: tuple[str, ...] = (
    "digital twin",
    "student twin",
    "evidence authority",
    "evidence package",
    "cognitive load",
    "mental load",
    "pass probability",
    "will definitely",
)

# Whole-token only. ``xp`` must never strip Explain / exploratory / experience.
# ``gamif…`` covers gamification / gamify without bare substring risk.
_FORBIDDEN_TOKEN_RE = re.compile(
    r"\b(?:"
    r"xp"
    r"|streak"
    r"|badge"
    r"|leaderboard"
    r"|gamif\w*"
    r"|guaranteed"
    r"|overloaded"
    r"|burnout"
    r")\b",
    re.IGNORECASE,
)


def scrub(text: str) -> str:
    """Remove forbidden product/AI theatre phrasing from authored copy."""
    out = (text or "").strip()
    if not out:
        return ""
    lowered = out.lower()
    for phrase in _FORBIDDEN_PHRASES:
        if phrase in lowered:
            idx = lowered.find(phrase)
            while idx >= 0:
                out = out[:idx] + out[idx + len(phrase) :]
                lowered = out.lower()
                idx = lowered.find(phrase)
    out = _FORBIDDEN_TOKEN_RE.sub("", out)
    return " ".join(out.split()).strip()
