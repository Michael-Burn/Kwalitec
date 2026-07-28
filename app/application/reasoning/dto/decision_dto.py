"""Application DTOs for AP-002D3 educational decisions / Twin updates."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class DecisionReasonDTO:
    code: str
    summary: str
    detail: str = ""
    observation_ids: tuple[str, ...] = ()
    rule_code: str = ""


@dataclass(frozen=True, slots=True)
class EducationalDecisionDTO:
    decision_id: str
    category: str
    twin_id: str
    subject_ref: str
    value: Any
    reason: DecisionReasonDTO
    decision_version: str
    created_at: datetime
    evidence_bundle_id: str
    educational_observation_ids: tuple[str, ...]
    reasoning_request_id: str
    assessment_session_id: str
    correlation_id: str
    learning_objective_reference: str
    concept_reference: str = ""
    provenance: dict[str, Any] = field(default_factory=dict)
    traceability: dict[str, Any] = field(default_factory=dict)
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class DecisionResultDTO:
    """Application-facing decision outcome (before or after Twin apply)."""

    twin_id: str
    reasoning_request_id: str
    evidence_bundle_id: str
    session_id: str
    correlation_id: str
    decision_version: str
    set_id: str
    decided_at: datetime
    prior_twin_version: int
    decisions: tuple[EducationalDecisionDTO, ...]
    decision_ids: tuple[str, ...]
    observation_ids: tuple[str, ...]
