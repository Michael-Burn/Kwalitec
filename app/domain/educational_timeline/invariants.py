"""Educational Timeline invariants (ILE-003).

Narrative speech must stay student-safe and never overclaim certainty.
"""

from __future__ import annotations

import re

from app.domain.decision_journal.invariants import (
    FORBIDDEN_STUDENT_TERMS,
    assert_student_safe_text,
)
from app.domain.educational_timeline.enums import NarrativeCertainty

# Re-export for callers that import timeline invariants only.
__all__ = [
    "FORBIDDEN_STUDENT_TERMS",
    "assert_student_safe_text",
    "assert_narrative_humble",
]


# Phrases that imply more certainty than journal evidence can support.
OVERCLAIM_PHRASES: tuple[str, ...] = (
    "proves that",
    "guarantees",
    "you have mastered",
    "you failed",
    "you are behind",
    "definitively",
    "without doubt",
)

_ABSOLUTE_WORD = re.compile(
    r"\b(always|never|certainly|proves)\b",
    re.IGNORECASE,
)


def assert_narrative_humble(
    text: str,
    *,
    certainty: NarrativeCertainty | str,
    field: str = "narrative",
) -> None:
    """Raise ValueError if narrative text overclaims or leaks internals."""
    assert_student_safe_text(text or "", field=field)
    lowered = (text or "").lower()
    for phrase in OVERCLAIM_PHRASES:
        if phrase in lowered:
            raise ValueError(
                f"Educational Timeline {field} must not overclaim "
                f"('{phrase}')"
            )
    band = NarrativeCertainty(str(certainty))
    if band == NarrativeCertainty.INSUFFICIENT:
        match = _ABSOLUTE_WORD.search(text or "")
        if match:
            raise ValueError(
                f"Educational Timeline {field} must stay tentative "
                f"when certainty is insufficient (found '{match.group(1)}')"
            )
