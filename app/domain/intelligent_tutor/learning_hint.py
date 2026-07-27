"""Learning hints — short, evidence-backed study prompts."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LearningHint:
    """A brief, actionable hint derived from assembled educational evidence."""

    hint_id: str
    text: str
    concept_id: str = ""
    evidence_ids: tuple[str, ...] = ()
    priority: int = 1

    def __post_init__(self) -> None:
        if not (self.hint_id or "").strip():
            raise ValueError("hint_id is required")
        if not (self.text or "").strip():
            raise ValueError("hint text is required")
        object.__setattr__(self, "evidence_ids", tuple(self.evidence_ids or ()))
        object.__setattr__(self, "priority", max(1, int(self.priority)))
