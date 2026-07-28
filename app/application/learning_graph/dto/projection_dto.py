"""Application DTOs for AP-002D4 Learning Graph projections."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class RelationshipProjectionDTO:
    projection_id: str
    relationship_type: str
    from_ref: str
    to_ref: str
    twin_id: str
    graph_id: str
    decision_id: str
    decision_version: str
    twin_version: int
    evidence_bundle_id: str
    educational_observation_ids: tuple[str, ...]
    reasoning_request_id: str
    assessment_session_id: str
    correlation_id: str
    projection_version: str
    created_at: datetime
    provenance: dict[str, Any] = field(default_factory=dict)
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ProjectionEventDTO:
    event_id: str
    kind: str
    graph_id: str
    twin_id: str
    decision_id: str
    occurred_at: datetime
    projection_version: str
    projection_id: str = ""
    relationship_type: str = ""
    reason_code: str = ""


@dataclass(frozen=True, slots=True)
class ProjectionResultDTO:
    """Application-facing projection outcome."""

    twin_id: str
    student_id: str
    graph_id: str
    reasoning_request_id: str
    evidence_bundle_id: str
    session_id: str
    correlation_id: str
    projection_version: str
    decision_version: str
    twin_version: int
    batch_id: str
    graph_projection_id: str
    projected_at: datetime
    relationships: tuple[RelationshipProjectionDTO, ...]
    projection_ids: tuple[str, ...]
    decision_ids: tuple[str, ...]
    skipped_decision_ids: tuple[str, ...]
    events: tuple[ProjectionEventDTO, ...]
    created_count: int
    updated_count: int
    skipped_count: int
