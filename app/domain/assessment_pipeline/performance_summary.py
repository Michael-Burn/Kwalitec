"""Performance summary — aggregate evidence metrics for diagnostics.

Does not store Twin mastery inferences; summarises assessment evidence only.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True)
class PerformanceSummary:
    """Deterministic summary of assessment evidence for a Twin window."""

    summary_id: str
    twin_id: str
    student_id: str
    event_count: int
    attempt_count: int
    correct_count: int
    incorrect_count: int
    mean_score: float | None
    concepts_touched: tuple[str, ...]
    generated_at: datetime
    window_start: datetime | None = None
    window_end: datetime | None = None

    def __post_init__(self) -> None:
        if not (self.summary_id or "").strip():
            raise ValueError("summary_id is required")
        if not (self.twin_id or "").strip():
            raise ValueError("twin_id is required")
        when = self.generated_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "generated_at", when.astimezone(UTC).replace(tzinfo=None)
            )
        object.__setattr__(self, "concepts_touched", tuple(self.concepts_touched or ()))
        object.__setattr__(self, "event_count", max(0, int(self.event_count)))
        object.__setattr__(self, "attempt_count", max(0, int(self.attempt_count)))
        object.__setattr__(self, "correct_count", max(0, int(self.correct_count)))
        object.__setattr__(self, "incorrect_count", max(0, int(self.incorrect_count)))

    @property
    def accuracy(self) -> float | None:
        scored = self.correct_count + self.incorrect_count
        if scored <= 0:
            return None
        return self.correct_count / scored
