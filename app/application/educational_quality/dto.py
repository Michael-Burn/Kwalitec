"""DTOs for EQ-001 educational quality certification."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class MissionQualityEnvelope:
    topic_id: str
    topic_code: str
    objective_ids: tuple[str, ...]
    estimated_duration_minutes: int
    completion_definition: str
    educational_rationale: str
    prerequisite_validation: dict[str, Any]
    explanation: dict[str, Any]


@dataclass(frozen=True)
class JourneyExplanationSnapshot:
    why_today: str
    why_previous_complete: str
    unlocks_next: str
    supporting_evidence: tuple[str, ...] = field(default_factory=tuple)
    explanation_schema_version: str = ""
    explanation_level: str = ""
    explanation_schema_complete: bool = False
    current_topic_id: str | None = None
    previous_topic_id: str | None = None
    next_topic_id: str | None = None


@dataclass(frozen=True)
class StudyPlanPacingSnapshot:
    exam_date_aware: bool
    first_pass_minutes: int
    revision_minutes: int
    total_required_minutes: int
    feasible: bool | None
    shortfall_minutes: int | None
    projection: dict[str, Any] = field(default_factory=dict)
