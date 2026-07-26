"""Readiness Intelligence contracts (EP-001.3).

Immutable DTOs for Canonical Learner State (+ optional planner outputs)
→ readiness evaluation. Readiness owns evaluation; Twin owns learner state;
Planner owns planning. Never invent mastery, streaks, or mock performance.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

from app.infrastructure.adapters.digital_twin.contracts import (
    AUTHORITY_DIGITAL_TWIN,
    AUTHORITY_RUNTIME_A,
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
)

READINESS_INTELLIGENCE_VERSION = "ep001.3.0"

REASON_TWIN_FLAG_OFF = "twin_foundation_flag_off"
REASON_STATE_UNAVAILABLE = "canonical_learner_state_unavailable"
REASON_INVALID_STUDENT_ID = "invalid_student_id"
REASON_PLANNER_UNAVAILABLE = "planner_outputs_unavailable"

SOURCE_SERVICE_READINESS_INTELLIGENCE = "readiness_intelligence"

CONFIDENCE_VERY_LOW = "very_low"
CONFIDENCE_LOW = "low"
CONFIDENCE_MEDIUM = "medium"
CONFIDENCE_HIGH = "high"

CONFIDENCE_LEVELS = (
    CONFIDENCE_VERY_LOW,
    CONFIDENCE_LOW,
    CONFIDENCE_MEDIUM,
    CONFIDENCE_HIGH,
)


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if value is None:
        return MappingProxyType({})
    if isinstance(value, MappingProxyType):
        return value
    return MappingProxyType(dict(value))


def _freeze_rows(
    value: Sequence[Mapping[str, Any]] | None,
) -> tuple[Mapping[str, Any], ...]:
    if not value:
        return ()
    return tuple(MappingProxyType(dict(row)) for row in value)


def serialize_canonical(payload: Mapping[str, Any]) -> str:
    return json.dumps(dict(payload), sort_keys=True, separators=(",", ":"), default=str)


@dataclass(frozen=True)
class TopicArea:
    """One strongest/weakest topic area from Canonical mastery."""

    topic_id: str
    topic_name: str
    mastery_score: float | None
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "topic_id": self.topic_id,
            "topic_name": self.topic_name,
            "mastery_score": self.mastery_score,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class ReadinessDriver:
    """Named readiness driver with provenance."""

    driver_id: str
    label: str
    influence: str
    value: float | str | None
    source: str
    rationale: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "driver_id": self.driver_id,
            "label": self.label,
            "influence": self.influence,
            "value": self.value,
            "source": self.source,
            "rationale": self.rationale,
        }


@dataclass(frozen=True)
class RecommendedNextAction:
    """Recommended next action grounded in Planner outputs (or empty)."""

    action_id: str
    title: str
    reason: str
    priority: str
    topic_id: str | None
    source: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "action_id": self.action_id,
            "title": self.title,
            "reason": self.reason,
            "priority": self.priority,
            "topic_id": self.topic_id,
            "source": self.source,
        }


@dataclass(frozen=True)
class ReadinessIntelligenceInputs:
    """Read-only readiness inputs derived from CanonicalLearnerState (+ planner).

    Contains no invented estimates. Unavailable Twin dimensions stay empty
    with an explicit unavailable reason.
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
    readiness_score: float | None
    coverage_pct: float | None
    avg_mastery: float | None
    review_discipline: float | None
    topics_started: int | None
    topics_mastered: int | None
    total_topics: int | None
    current_streak: int | None
    longest_streak: int | None
    consistency_label: str
    behaviour_labels: Mapping[str, str]
    evidence_attempt_count: int
    practice_mean_accuracy_pct: float | None
    mission_completed_count: int
    mission_missed_count: int
    topic_areas: tuple[TopicArea, ...]
    planner_missions: tuple[Mapping[str, Any], ...]
    planner_revision_priorities: tuple[Mapping[str, Any], ...]
    planner_available: bool
    provenance_refs: tuple[str, ...]
    limitations_codes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        object.__setattr__(
            self, "behaviour_labels", _freeze_mapping(self.behaviour_labels)
        )
        object.__setattr__(self, "topic_areas", tuple(self.topic_areas))
        object.__setattr__(
            self, "planner_missions", _freeze_rows(self.planner_missions)
        )
        object.__setattr__(
            self,
            "planner_revision_priorities",
            _freeze_rows(self.planner_revision_priorities),
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
            "avg_mastery": self.avg_mastery,
            "behaviour_labels": dict(self.behaviour_labels),
            "consistency_label": self.consistency_label,
            "coverage_pct": self.coverage_pct,
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
            "practice_mean_accuracy_pct": self.practice_mean_accuracy_pct,
            "provenance_refs": list(self.provenance_refs),
            "readiness_score": self.readiness_score,
            "review_discipline": self.review_discipline,
            "student_id": self.student_id,
            "topic_areas": [row.to_dict() for row in self.topic_areas],
            "topics_mastered": self.topics_mastered,
            "topics_started": self.topics_started,
            "total_topics": self.total_topics,
            "twin_id": self.twin_id,
            "unavailable_reason": self.unavailable_reason,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_dict())


@dataclass(frozen=True)
class ReadinessIntelligenceAssessment:
    """Readiness evaluation artefact — regenerable; does not write Twin/Planner."""

    student_id: str
    as_of: str | None
    consumer_version: str
    foundation_version: str
    twin_id: str
    availability: str
    unavailable_reason: str
    readiness_score: float | None
    confidence_level: str
    strongest_areas: tuple[TopicArea, ...]
    weakest_areas: tuple[TopicArea, ...]
    readiness_drivers: tuple[ReadinessDriver, ...]
    recommended_next_actions: tuple[RecommendedNextAction, ...]
    provenance_refs: tuple[str, ...] = ()
    limitations_codes: tuple[str, ...] = ()
    explainability: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        object.__setattr__(self, "strongest_areas", tuple(self.strongest_areas))
        object.__setattr__(self, "weakest_areas", tuple(self.weakest_areas))
        object.__setattr__(
            self, "readiness_drivers", tuple(self.readiness_drivers)
        )
        object.__setattr__(
            self,
            "recommended_next_actions",
            tuple(self.recommended_next_actions),
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
        object.__setattr__(
            self, "explainability", _freeze_mapping(self.explainability)
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "as_of": self.as_of,
            "availability": self.availability,
            "authority": AUTHORITY_DIGITAL_TWIN,
            "confidence_level": self.confidence_level,
            "consumer_version": self.consumer_version,
            "explainability": dict(self.explainability),
            "foundation_version": self.foundation_version,
            "limitations_codes": list(self.limitations_codes),
            "provenance_refs": list(self.provenance_refs),
            "readiness_drivers": [d.to_dict() for d in self.readiness_drivers],
            "readiness_score": self.readiness_score,
            "recommended_next_actions": [
                a.to_dict() for a in self.recommended_next_actions
            ],
            "source_service": SOURCE_SERVICE_READINESS_INTELLIGENCE,
            "strongest_areas": [a.to_dict() for a in self.strongest_areas],
            "student_id": self.student_id,
            "twin_id": self.twin_id,
            "unavailable_reason": self.unavailable_reason,
            "weakest_areas": [a.to_dict() for a in self.weakest_areas],
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_dict())


__all__ = [
    "CONFIDENCE_HIGH",
    "CONFIDENCE_LEVELS",
    "CONFIDENCE_LOW",
    "CONFIDENCE_MEDIUM",
    "CONFIDENCE_VERY_LOW",
    "READINESS_INTELLIGENCE_VERSION",
    "REASON_INVALID_STUDENT_ID",
    "REASON_PLANNER_UNAVAILABLE",
    "REASON_STATE_UNAVAILABLE",
    "REASON_TWIN_FLAG_OFF",
    "SOURCE_SERVICE_READINESS_INTELLIGENCE",
    "AUTHORITY_DIGITAL_TWIN",
    "AUTHORITY_RUNTIME_A",
    "AVAILABILITY_AVAILABLE",
    "AVAILABILITY_UNAVAILABLE",
    "ReadinessDriver",
    "ReadinessIntelligenceAssessment",
    "ReadinessIntelligenceInputs",
    "RecommendedNextAction",
    "TopicArea",
    "serialize_canonical",
]
