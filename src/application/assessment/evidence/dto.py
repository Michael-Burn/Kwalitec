"""Application DTOs for packaged assessment evidence (AP-001 export surface)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class EvidenceReferenceDTO:
    observation_id: str
    question_id: str | None = None
    kind: str | None = None


@dataclass(frozen=True, slots=True)
class EvidenceItemDTO:
    item_id: str
    observation_id: str
    kind: str
    evidence_source: str
    question_id: str | None = None
    correctness: str | None = None
    confidence: int | None = None
    response_time_ms: int | None = None
    hints_used: int = 0
    retries: int = 0
    misconception_tags: tuple[str, ...] = ()
    provenance: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class EvidenceSummaryDTO:
    observation_count: int
    question_observation_count: int
    distinct_question_count: int
    correctness_counts: dict[str, int] = field(default_factory=dict)
    hint_total: int = 0
    retry_total: int = 0
    confidence_supplied_count: int = 0
    timing_available_count: int = 0
    misconception_tag_count: int = 0


@dataclass(frozen=True, slots=True)
class EvidenceMetadataDTO:
    evidence_source: str
    packaging_version: str
    collected_at: str | None = None
    question_ids: tuple[str, ...] = ()
    learning_objective_ids: tuple[str, ...] = ()
    concept_ids: tuple[str, ...] = ()
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class EvidenceContextDTO:
    session_id: str
    instrument_id: str | None = None
    assessment_id: str | None = None
    purpose: str | None = None
    assessment_type: str | None = None
    student_id: str | None = None


@dataclass(frozen=True, slots=True)
class EvidenceBundleDTO:
    """Clean application boundary for packaged evidence (no Twin / Reasoning)."""

    bundle_id: str
    session_id: str
    evidence_strength: str
    context: EvidenceContextDTO
    metadata: EvidenceMetadataDTO
    summary: EvidenceSummaryDTO
    items: tuple[EvidenceItemDTO, ...] = ()
    observation_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class EvidencePackagingResultDTO:
    bundle: EvidenceBundleDTO
    result_id: str | None = None
    validated: bool = True
    evidence_strength: str | None = None
