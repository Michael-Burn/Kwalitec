"""Application DTOs for AP-002D2 educational evidence interpretation."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from application.assessment.evidence.dto import EvidenceBundleDTO


@dataclass(frozen=True, slots=True)
class InterpretationRequestDTO:
    """Lawful request to interpret packaged assessment evidence."""

    bundle: EvidenceBundleDTO
    correlation_id: str
    reasoning_request_id: str | None = None


@dataclass(frozen=True, slots=True)
class InterpretedObservationDTO:
    """Serializable educational observation for Twin-facing consumers."""

    observation_id: str
    evidence_reference: str
    learning_objective_reference: str
    concept_reference: str
    category: str
    value: Any
    provenance: str
    interpretation_version: str
    recorded_at: datetime
    reasoning_request_id: str
    evidence_bundle_id: str
    session_id: str
    correlation_id: str
    source_observation_id: str = ""
    question_reference: str | None = None
    traceability: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class InterpretationResultDTO:
    """Application-facing interpretation outcome (no Twin mutation)."""

    reasoning_request_id: str
    evidence_bundle_id: str
    session_id: str
    packaging_version: str
    interpreter_version: str
    correlation_id: str
    set_id: str
    interpreted_at: datetime
    observations: tuple[InterpretedObservationDTO, ...]
    observation_ids: tuple[str, ...]
