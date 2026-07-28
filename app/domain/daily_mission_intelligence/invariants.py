"""Daily Mission Intelligence invariants (ILE-004).

Mission brief speech must stay student-safe, never overclaim, and never
optimise for engagement theatre.
"""

from __future__ import annotations

from app.domain.daily_mission_intelligence.enums import (
    FORBIDDEN_OPTIMISATION_TERMS,
)
from app.domain.decision_journal.invariants import (
    FORBIDDEN_STUDENT_TERMS,
    assert_student_safe_text,
)

__all__ = [
    "FORBIDDEN_OPTIMISATION_TERMS",
    "FORBIDDEN_STUDENT_TERMS",
    "assert_mission_speech_safe",
    "assert_student_safe_text",
]


def assert_mission_speech_safe(text: str, *, field: str = "mission") -> None:
    """Raise ValueError if mission text leaks internals or engagement theatre."""
    assert_student_safe_text(text or "", field=field)
    lowered = (text or "").lower()
    for term in FORBIDDEN_OPTIMISATION_TERMS:
        if term in lowered:
            raise ValueError(
                f"Daily Mission Intelligence {field} must not optimise "
                f"for '{term}'"
            )
