"""Expected and observed learning outcomes for a mission."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MissionOutcome:
    """Expected learning outcome for today's mission."""

    outcome_id: str
    statement: str
    target_concept_id: str
    expected_mastery_delta: float = 0.0
    success_signals: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not (self.outcome_id or "").strip():
            raise ValueError("outcome_id is required")
        if not (self.statement or "").strip():
            raise ValueError("outcome statement is required")
        object.__setattr__(
            self, "expected_mastery_delta", float(self.expected_mastery_delta)
        )
        object.__setattr__(
            self, "success_signals", tuple(self.success_signals or ())
        )
