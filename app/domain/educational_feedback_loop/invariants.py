"""Educational Feedback Loop invariants (ILE-005).

Calibration speech must stay educational, never overclaim, and never
optimise for engagement theatre.
"""

from __future__ import annotations

from app.domain.decision_journal.invariants import (
    FORBIDDEN_STUDENT_TERMS,
    assert_student_safe_text,
)
from app.domain.educational_feedback_loop.enums import (
    FORBIDDEN_CALIBRATION_TERMS,
)

__all__ = [
    "FORBIDDEN_CALIBRATION_TERMS",
    "FORBIDDEN_STUDENT_TERMS",
    "assert_calibration_speech_safe",
    "assert_student_safe_text",
]


def assert_calibration_speech_safe(
    text: str,
    *,
    field: str = "calibration",
) -> None:
    """Raise ValueError if text leaks internals or engagement theatre."""
    assert_student_safe_text(text or "", field=field)
    lowered = (text or "").lower()
    for term in FORBIDDEN_CALIBRATION_TERMS:
        if term in lowered:
            raise ValueError(
                f"Educational Feedback Loop {field} must not optimise "
                f"for '{term}'"
            )
