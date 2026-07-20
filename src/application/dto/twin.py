"""Digital Twin summary application DTOs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DigitalTwinSummaryDTO:
    """Lightweight Twin projection after an update command."""

    twin_id: str
    student_id: str
    status: str
    update_kind: str
    evidence_count: int
    concept_count: int
    trajectory_length: int
