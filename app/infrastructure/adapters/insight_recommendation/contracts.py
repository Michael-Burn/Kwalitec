"""Insight & Recommendation Layer contracts (EP-001.4).

Immutable DTOs for Canonical Learner State + Planner + Readiness Intelligence
→ student-facing study guidance. Insight owns communication only; Twin owns
learner state; Planner owns planning; Readiness owns evaluation.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

from app.infrastructure.adapters.digital_twin.contracts import (
    AUTHORITY_DIGITAL_TWIN,
    AUTHORITY_RUNTIME_A,
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
)

INSIGHT_LAYER_VERSION = "ep001.4.0"

REASON_TWIN_FLAG_OFF = "twin_foundation_flag_off"
REASON_STATE_UNAVAILABLE = "canonical_learner_state_unavailable"
REASON_INVALID_STUDENT_ID = "invalid_student_id"
REASON_PLANNER_UNAVAILABLE = "planner_outputs_unavailable"
REASON_READINESS_UNAVAILABLE = "readiness_intelligence_unavailable"

SOURCE_SERVICE_INSIGHT_RECOMMENDATION = "insight_recommendation"


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if value is None:
        return MappingProxyType({})
    if isinstance(value, MappingProxyType):
        return value
    return MappingProxyType(dict(value))


def serialize_canonical(payload: Mapping[str, Any]) -> str:
    return json.dumps(dict(payload), sort_keys=True, separators=(",", ":"), default=str)


@dataclass(frozen=True)
class InsightField:
    """One student-facing guidance field with provenance."""

    field_id: str
    title: str
    message: str
    topic_id: str | None
    source: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "field_id": self.field_id,
            "title": self.title,
            "message": self.message,
            "topic_id": self.topic_id,
            "source": self.source,
        }


@dataclass(frozen=True)
class StudyInsightInputs:
    """Read-only insight inputs derived from Twin + Planner + Readiness.

    Contains no invented estimates. Unavailable upstream packages stay empty
    with explicit limitation codes.
    """

    student_id: str
    as_of: str | None
    foundation_version: str
    twin_id: str
    availability: str
    unavailable_reason: str
    lifecycle_stage: str
    examination_label: str
    exam_countdown_days: int | None
    current_streak: int | None
    longest_streak: int | None
    consistency_label: str
    mission_completed_count: int
    mission_missed_count: int
    evidence_attempt_count: int
    topics_started: int | None
    topics_mastered: int | None
    total_topics: int | None
    planner_available: bool
    readiness_available: bool
    planner_missions: tuple[Mapping[str, Any], ...]
    planner_revision_priorities: tuple[Mapping[str, Any], ...]
    recommended_workload: Mapping[str, Any]
    readiness_score: float | None
    confidence_level: str
    strongest_areas: tuple[Mapping[str, Any], ...]
    weakest_areas: tuple[Mapping[str, Any], ...]
    readiness_drivers: tuple[Mapping[str, Any], ...]
    recommended_next_actions: tuple[Mapping[str, Any], ...]
    provenance_refs: tuple[str, ...]
    limitations_codes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        object.__setattr__(
            self,
            "planner_missions",
            tuple(MappingProxyType(dict(row)) for row in self.planner_missions),
        )
        object.__setattr__(
            self,
            "planner_revision_priorities",
            tuple(
                MappingProxyType(dict(row))
                for row in self.planner_revision_priorities
            ),
        )
        object.__setattr__(
            self, "recommended_workload", _freeze_mapping(self.recommended_workload)
        )
        object.__setattr__(
            self,
            "strongest_areas",
            tuple(MappingProxyType(dict(row)) for row in self.strongest_areas),
        )
        object.__setattr__(
            self,
            "weakest_areas",
            tuple(MappingProxyType(dict(row)) for row in self.weakest_areas),
        )
        object.__setattr__(
            self,
            "readiness_drivers",
            tuple(MappingProxyType(dict(row)) for row in self.readiness_drivers),
        )
        object.__setattr__(
            self,
            "recommended_next_actions",
            tuple(
                MappingProxyType(dict(row)) for row in self.recommended_next_actions
            ),
        )
        object.__setattr__(
            self,
            "provenance_refs",
            tuple(str(item) for item in self.provenance_refs if item),
        )
        object.__setattr__(
            self,
            "limitations_codes",
            tuple(str(item) for item in self.limitations_codes if item),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "as_of": self.as_of,
            "availability": self.availability,
            "confidence_level": self.confidence_level,
            "consistency_label": self.consistency_label,
            "current_streak": self.current_streak,
            "evidence_attempt_count": self.evidence_attempt_count,
            "exam_countdown_days": self.exam_countdown_days,
            "examination_label": self.examination_label,
            "foundation_version": self.foundation_version,
            "lifecycle_stage": self.lifecycle_stage,
            "limitations_codes": list(self.limitations_codes),
            "longest_streak": self.longest_streak,
            "mission_completed_count": self.mission_completed_count,
            "mission_missed_count": self.mission_missed_count,
            "planner_available": self.planner_available,
            "planner_missions": [dict(row) for row in self.planner_missions],
            "planner_revision_priorities": [
                dict(row) for row in self.planner_revision_priorities
            ],
            "provenance_refs": list(self.provenance_refs),
            "readiness_available": self.readiness_available,
            "readiness_drivers": [dict(row) for row in self.readiness_drivers],
            "readiness_score": self.readiness_score,
            "recommended_next_actions": [
                dict(row) for row in self.recommended_next_actions
            ],
            "recommended_workload": dict(self.recommended_workload),
            "strongest_areas": [dict(row) for row in self.strongest_areas],
            "student_id": self.student_id,
            "topics_mastered": self.topics_mastered,
            "topics_started": self.topics_started,
            "total_topics": self.total_topics,
            "twin_id": self.twin_id,
            "unavailable_reason": self.unavailable_reason,
            "weakest_areas": [dict(row) for row in self.weakest_areas],
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_dict())


@dataclass(frozen=True)
class StudyInsightGuidance:
    """Student-facing insight package — regenerable.

    Does not write Twin, Planner, or Readiness state.
    """

    student_id: str
    as_of: str | None
    consumer_version: str
    foundation_version: str
    twin_id: str
    availability: str
    unavailable_reason: str
    todays_key_focus: InsightField | None
    strongest_area: InsightField | None
    greatest_risk: InsightField | None
    recommended_next_action: InsightField | None
    workload_explanation: InsightField | None
    readiness_explanation: InsightField | None
    motivational_progress_summary: InsightField | None
    provenance_refs: tuple[str, ...] = ()
    limitations_codes: tuple[str, ...] = ()
    explainability: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        object.__setattr__(
            self,
            "provenance_refs",
            tuple(str(item) for item in self.provenance_refs if item),
        )
        object.__setattr__(
            self,
            "limitations_codes",
            tuple(str(item) for item in self.limitations_codes if item),
        )
        object.__setattr__(
            self, "explainability", _freeze_mapping(self.explainability)
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "as_of": self.as_of,
            "availability": self.availability,
            "authority": AUTHORITY_DIGITAL_TWIN,
            "consumer_version": self.consumer_version,
            "explainability": dict(self.explainability),
            "foundation_version": self.foundation_version,
            "greatest_risk": (
                self.greatest_risk.to_dict() if self.greatest_risk else None
            ),
            "limitations_codes": list(self.limitations_codes),
            "motivational_progress_summary": (
                self.motivational_progress_summary.to_dict()
                if self.motivational_progress_summary
                else None
            ),
            "provenance_refs": list(self.provenance_refs),
            "readiness_explanation": (
                self.readiness_explanation.to_dict()
                if self.readiness_explanation
                else None
            ),
            "recommended_next_action": (
                self.recommended_next_action.to_dict()
                if self.recommended_next_action
                else None
            ),
            "source_service": SOURCE_SERVICE_INSIGHT_RECOMMENDATION,
            "strongest_area": (
                self.strongest_area.to_dict() if self.strongest_area else None
            ),
            "student_id": self.student_id,
            "todays_key_focus": (
                self.todays_key_focus.to_dict() if self.todays_key_focus else None
            ),
            "twin_id": self.twin_id,
            "unavailable_reason": self.unavailable_reason,
            "workload_explanation": (
                self.workload_explanation.to_dict()
                if self.workload_explanation
                else None
            ),
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_dict())


__all__ = [
    "AUTHORITY_DIGITAL_TWIN",
    "AUTHORITY_RUNTIME_A",
    "AVAILABILITY_AVAILABLE",
    "AVAILABILITY_UNAVAILABLE",
    "INSIGHT_LAYER_VERSION",
    "REASON_INVALID_STUDENT_ID",
    "REASON_PLANNER_UNAVAILABLE",
    "REASON_READINESS_UNAVAILABLE",
    "REASON_STATE_UNAVAILABLE",
    "REASON_TWIN_FLAG_OFF",
    "SOURCE_SERVICE_INSIGHT_RECOMMENDATION",
    "InsightField",
    "StudyInsightGuidance",
    "StudyInsightInputs",
    "serialize_canonical",
]
