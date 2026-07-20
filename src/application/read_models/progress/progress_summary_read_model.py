"""ProgressSummaryReadModel — non-selecting progress cues for the dashboard."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProgressSummaryReadModel:
    """Honest progress summary. Never selects the next action."""

    student_id: str
    activity_status: str
    twin_status: str
    concept_count: int
    evidence_count: int
    intervention_count: int
    progress_cues: tuple[str, ...]
    twin_id: str | None = None
