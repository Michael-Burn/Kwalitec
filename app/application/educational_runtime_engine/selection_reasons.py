"""Locked daily-mission composer selection reasons (roadmap).

These are the only lawful values for ``composer_selection_reason`` on a
Runtime C daily sitting. They are distinct from certified LO selection
reasons and from session-origin labels.
"""

from __future__ import annotations

SELECTION_REASON_SEQUENTIAL = "sequential"
SELECTION_REASON_SPACED_REVIEW = "spaced_review"
SELECTION_REASON_ADAPTIVE_REVIEW = "adaptive_review"
SELECTION_REASON_STUDENT_SELECTED = "student_selected"

COMPOSER_SELECTION_REASONS = frozenset(
    {
        SELECTION_REASON_SEQUENTIAL,
        SELECTION_REASON_SPACED_REVIEW,
        SELECTION_REASON_ADAPTIVE_REVIEW,
        SELECTION_REASON_STUDENT_SELECTED,
    }
)
