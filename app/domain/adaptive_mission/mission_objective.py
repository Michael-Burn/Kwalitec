"""Educational objective for a daily adaptive mission."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MissionObjective:
    """What the learner should achieve in today's study session."""

    objective_id: str
    statement: str
    primary_concept_id: str
    supporting_concept_ids: tuple[str, ...] = ()
    source_recommendation_id: str = ""
    source_gap_id: str = ""

    def __post_init__(self) -> None:
        if not (self.objective_id or "").strip():
            raise ValueError("objective_id is required")
        if not (self.statement or "").strip():
            raise ValueError("objective statement is required")
        if not (self.primary_concept_id or "").strip():
            raise ValueError("primary_concept_id is required")
        object.__setattr__(
            self,
            "supporting_concept_ids",
            tuple(self.supporting_concept_ids or ()),
        )
