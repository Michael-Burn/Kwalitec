"""Question sequencing and session progress for one-item-at-a-time delivery."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SessionDeliveryState:
    """Mutable delivery cursor for a session (application concern, not domain)."""

    session_id: str
    current_index: int = 0
    visited_question_ids: list[str] = field(default_factory=list)
    question_started_at: dict[str, datetime] = field(default_factory=dict)
    hints_requested: dict[str, int] = field(default_factory=dict)
    started_at: datetime | None = None
    expires_at: datetime | None = None
    allow_previous: bool = True


@dataclass(frozen=True, slots=True)
class DeliveryProgress:
    """Student-facing progress snapshot."""

    current_index: int
    total_questions: int
    answered_count: int
    remaining_count: int
    percent_complete: int
    current_question_id: str | None
    can_go_previous: bool
    can_go_next: bool
    can_complete: bool
    is_complete: bool


def compute_progress(
    *,
    question_ids: tuple[str, ...],
    answered_question_ids: set[str],
    current_index: int,
    allow_previous: bool,
    session_submitted: bool,
) -> DeliveryProgress:
    """Derive progress from ordered questions and committed answers."""
    total = len(question_ids)
    answered = len(answered_question_ids & set(question_ids))
    remaining = max(0, total - answered)
    percent = int(round((answered / total) * 100)) if total else 100
    index = max(0, min(current_index, max(total - 1, 0)))
    current_id = question_ids[index] if total and not session_submitted else None
    can_previous = (
        allow_previous and not session_submitted and total > 0 and index > 0
    )
    can_next = not session_submitted and total > 0 and index < total - 1
    can_complete = not session_submitted and answered > 0 and remaining == 0
    return DeliveryProgress(
        current_index=index,
        total_questions=total,
        answered_count=answered,
        remaining_count=remaining,
        percent_complete=percent,
        current_question_id=current_id,
        can_go_previous=can_previous,
        can_go_next=can_next,
        can_complete=can_complete,
        is_complete=session_submitted,
    )
