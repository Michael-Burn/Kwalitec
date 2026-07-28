"""Application DTOs for AP-002D5 Mission planning."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class MissionCandidateDTO:
    candidate_id: str
    activity_type: str
    concept_id: str
    concept_title: str
    twin_id: str
    decision_id: str
    decision_version: str
    twin_version: int
    evidence_bundle_id: str
    educational_observation_ids: tuple[str, ...]
    reasoning_request_id: str
    assessment_session_id: str
    correlation_id: str
    planning_version: str
    created_at: datetime
    priority_score: float
    priority_band: str
    learning_objective_id: str = ""
    recommendation_id: str = ""
    gap_id: str = ""
    recovery_path_concept_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    priority_explanation: str = ""
    provenance: dict[str, Any] = field(default_factory=dict)
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class PlanningEventDTO:
    event_id: str
    kind: str
    twin_id: str
    occurred_at: datetime
    planning_version: str
    decision_id: str = ""
    decision_set_id: str = ""
    mission_request_id: str = ""
    plan_id: str = ""
    mission_id: str = ""
    concept_id: str = ""
    candidate_id: str = ""
    reason_code: str = ""
    candidate_count: int = 0
    skipped_count: int = 0


@dataclass(frozen=True, slots=True)
class PlanningResultDTO:
    """Application-facing planning outcome."""

    twin_id: str
    student_id: str
    reasoning_request_id: str
    evidence_bundle_id: str
    session_id: str
    correlation_id: str
    planning_version: str
    decision_version: str
    twin_version: int
    batch_id: str
    plan_id: str
    mission_id: str
    mission_request_id: str
    planned_at: datetime
    goal: str
    educational_explanation: str
    candidates: tuple[MissionCandidateDTO, ...]
    candidate_ids: tuple[str, ...]
    decision_ids: tuple[str, ...]
    skipped_decision_ids: tuple[str, ...]
    events: tuple[PlanningEventDTO, ...]
    generated_count: int
    skipped_count: int
    candidate_count: int
    validation_passed: bool
    validation_summary: str
