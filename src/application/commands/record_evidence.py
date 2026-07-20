"""RecordEvidence command."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class EvidenceItemSpec:
    """Application input describing one evidence observation item."""

    item_id: str
    kind: str
    summary: str
    concept_id: str | None = None
    learning_episode_id: str | None = None


@dataclass(frozen=True, slots=True)
class RecordEvidence:
    """Record educational evidence through the assessment application service.

    Strength, confidence, and item content are supplied; application does not
    calculate mastery or diagnose. Domain validates observational integrity.
    """

    evidence_id: str
    student_id: str
    source_id: str
    source_kind: str
    source_label: str
    context_id: str
    context_dimension: str
    context_summary: str
    confidence_level: str
    strength_level: str
    occurred_at: datetime
    items: tuple[EvidenceItemSpec, ...]
    concept_ids: tuple[str, ...] = ()
    learning_episode_ids: tuple[str, ...] = ()
    confidence_ratio: float | None = None
    twin_id: str | None = None
    evidence_type_for_twin: str | None = None
