"""Application DTOs for AP-002D6 Tutor explainability."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class ExplanationSectionDTO:
    section_id: str
    kind: str
    title: str
    body: str
    decision_id: str
    decision_version: str
    twin_version: int
    evidence_bundle_id: str
    educational_observation_ids: tuple[str, ...]
    reasoning_request_id: str
    assessment_session_id: str
    correlation_id: str
    explanation_version: str
    concept_ids: tuple[str, ...] = ()
    learning_objective_ids: tuple[str, ...] = ()
    decision_ids: tuple[str, ...] = ()
    uncertainty_notes: tuple[str, ...] = ()
    learning_objective: str = ""
    concept: str = ""
    mission_plan_id: str = ""
    mission_id: str = ""
    provenance: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ExplanationEventDTO:
    event_id: str
    kind: str
    twin_id: str
    occurred_at: datetime
    explanation_version: str
    decision_set_id: str = ""
    explanation_request_id: str = ""
    explanation_id: str = ""
    mission_plan_id: str = ""
    reason_code: str = ""
    section_count: int = 0


@dataclass(frozen=True, slots=True)
class ExplanationResultDTO:
    """Application-facing Tutor explanation outcome."""

    twin_id: str
    student_id: str
    reasoning_request_id: str
    evidence_bundle_id: str
    session_id: str
    correlation_id: str
    explanation_version: str
    decision_version: str
    twin_version: int
    explanation_id: str
    explanation_request_id: str
    explained_at: datetime
    summary: str
    available: bool
    sections: tuple[ExplanationSectionDTO, ...]
    section_ids: tuple[str, ...]
    decision_ids: tuple[str, ...]
    concept_ids: tuple[str, ...]
    learning_objective_ids: tuple[str, ...]
    uncertainty_notes: tuple[str, ...]
    events: tuple[ExplanationEventDTO, ...]
    generated_count: int
    unavailable_count: int
    section_count: int
    mission_plan_id: str
    mission_id: str
    planning_version: str
    validation_passed: bool
    validation_summary: str
    provenance: dict[str, Any] = field(default_factory=dict)
