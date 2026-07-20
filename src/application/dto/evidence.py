"""Evidence application DTOs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EvidenceRecordDTO:
    """Projection of a recorded EvidenceRecord aggregate."""

    evidence_id: str
    student_id: str
    status: str
    strength_level: str
    confidence_level: str
    item_count: int
    concept_ids: tuple[str, ...]
    learning_episode_ids: tuple[str, ...]
    occurred_at: str


@dataclass(frozen=True, slots=True)
class EvidenceHistoryDTO:
    """Ordered evidence history projection for a student."""

    student_id: str
    records: tuple[EvidenceRecordDTO, ...]

    @property
    def count(self) -> int:
        return len(self.records)
