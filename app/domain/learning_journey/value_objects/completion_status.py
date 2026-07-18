"""Educational completion posture for a Learning Journey.

Avoids mastery, competence-score, and Exam Ready terminology. Completion here
means journey obligations / coverage posture — not understanding estimates
(Twin-owned).
"""

from __future__ import annotations

from enum import StrEnum


class CompletionStatus(StrEnum):
    """Educational completion posture for journey progress.

    Does not encode Estimated Mastery, Exam Ready, or certified competence.
    """

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PARTIALLY_ADDRESSED = "partially_addressed"
    READY_FOR_COMPLETION = "ready_for_completion"
    COMPLETED = "completed"
    INCOMPLETE = "incomplete"
