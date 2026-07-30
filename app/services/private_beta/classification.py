"""Automatic severity classification for private-beta feedback (PB-001)."""

from __future__ import annotations

import re

from app.models.private_beta import FEEDBACK_CATEGORIES, FEEDBACK_SEVERITIES

_CRITICAL_PATTERNS = (
    r"\bdata\s*loss\b",
    r"\blost\s+(my\s+)?(progress|data|plan|session)\b",
    r"\bcan'?t\s+log\s*in\b",
    r"\bcannot\s+log\s*in\b",
    r"\bcrash(ed|es|ing)?\b",
    r"\b500\b",
    r"\bcorrupt(ed|ion)?\b",
    r"\bcertification\s+error\b",
    r"\bwipe[sd]?\b",
)

_MAJOR_PATTERNS = (
    r"\bbroken\b",
    r"\berror\b",
    r"\bfail(ed|ure|ing)?\b",
    r"\bstuck\b",
    r"\bblocked\b",
    r"\bwrong\s+recommend",
    r"\bincorrect\b",
    r"\bdoesn'?t\s+work\b",
    r"\bnot\s+working\b",
)

_CATEGORY_DEFAULT: dict[str, str] = {
    "bug": "major",
    "suggestion": "enhancement",
    "confusing_screen": "question",
    "missing_feature": "enhancement",
    "incorrect_recommendation": "major",
    "general": "minor",
}


def classify_feedback_severity(
    *,
    category: str,
    message: str,
) -> str:
    """Return a PB-001 severity for a feedback submission.

    Classification is deterministic keyword + category mapping — not ML.
    """
    cat = (category or "").strip().lower()
    if cat not in FEEDBACK_CATEGORIES:
        cat = "general"

    text = (message or "").strip().lower()
    for pattern in _CRITICAL_PATTERNS:
        if re.search(pattern, text):
            return "critical"
    if cat == "bug":
        for pattern in _MAJOR_PATTERNS:
            if re.search(pattern, text):
                return "major"
    if cat == "incorrect_recommendation":
        return "major"
    if cat == "confusing_screen":
        return "question"

    severity = _CATEGORY_DEFAULT.get(cat, "minor")
    if severity not in FEEDBACK_SEVERITIES:
        return "minor"
    return severity


def parse_user_agent(user_agent: str | None) -> tuple[str, str]:
    """Best-effort browser + device labels from a User-Agent string."""
    ua = (user_agent or "").strip()
    if not ua:
        return ("unknown", "unknown")

    lower = ua.lower()
    device = "mobile" if any(
        token in lower for token in ("iphone", "android", "mobile", "ipad")
    ) else "desktop"
    if "ipad" in lower or "tablet" in lower:
        device = "tablet"

    browser = "unknown"
    if "edg/" in lower or "edge/" in lower:
        browser = "Edge"
    elif "chrome/" in lower and "chromium" not in lower:
        browser = "Chrome"
    elif "firefox/" in lower:
        browser = "Firefox"
    elif "safari/" in lower and "chrome/" not in lower:
        browser = "Safari"
    elif "opr/" in lower or "opera" in lower:
        browser = "Opera"

    return (browser, device)
