"""Adaptive Study Planner contracts (EP-001.2).

Immutable DTOs for Canonical Learner State → planning projections.
Planner owns planning outputs; Twin owns learner state. These contracts
never invent mastery, streaks, readiness, or mock performance.
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

PLANNER_CONSUMER_VERSION = "ep001.2.0"

REASON_TWIN_FLAG_OFF = "twin_foundation_flag_off"
REASON_STATE_UNAVAILABLE = "canonical_learner_state_unavailable"
REASON_INVALID_STUDENT_ID = "invalid_student_id"
REASON_NO_ACTIVE_PLAN = "no_active_study_plan"

SOURCE_SERVICE_ADAPTIVE_STUDY_PLANNER = "adaptive_study_planner"


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
class TopicPlanRow:
    """One topic row projected from Canonical Learner State."""

    topic_id: str
    topic_name: str
    mastery_score: float | None
    average_accuracy: float | None
    current_stage: str
    completed: bool
    next_review_date: str | None
    revision_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "topic_id": self.topic_id,
            "topic_name": self.topic_name,
            "mastery_score": self.mastery_score,
            "average_accuracy": self.average_accuracy,
            "current_stage": self.current_stage,
            "completed": self.completed,
            "next_review_date": self.next_review_date,
            "revision_count": self.revision_count,
        }


@dataclass(frozen=True)
class AdaptivePlannerInputs:
    """Read-only planner inputs derived from CanonicalLearnerState.

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
    planned_weekly_hours: float | None
    preferred_session_minutes: int | None
    current_streak: int | None
    longest_streak: int | None
    consistency_label: str
    behaviour_labels: Mapping[str, str]
    topics: tuple[TopicPlanRow, ...]
    evidence_attempt_count: int
    practice_mean_accuracy_pct: float | None
    mission_completed_count: int
    mission_missed_count: int
    provenance_refs: tuple[str, ...]
    limitations_codes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        object.__setattr__(
            self, "behaviour_labels", _freeze_mapping(self.behaviour_labels)
        )
        object.__setattr__(self, "topics", tuple(self.topics))
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
            "behaviour_labels": dict(self.behaviour_labels),
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
            "planned_weekly_hours": self.planned_weekly_hours,
            "practice_mean_accuracy_pct": self.practice_mean_accuracy_pct,
            "preferred_session_minutes": self.preferred_session_minutes,
            "provenance_refs": list(self.provenance_refs),
            "student_id": self.student_id,
            "topics": [row.to_dict() for row in self.topics],
            "twin_id": self.twin_id,
            "unavailable_reason": self.unavailable_reason,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_dict())


@dataclass(frozen=True)
class MissionSlot:
    """One today's-mission priority slot (planning output, not ORM)."""

    slot: str
    topic_id: str | None
    topic_name: str
    reason: str
    priority: str
    expected_benefit: str
    allocated_minutes: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "slot": self.slot,
            "topic_id": self.topic_id,
            "topic_name": self.topic_name,
            "reason": self.reason,
            "priority": self.priority,
            "expected_benefit": self.expected_benefit,
            "allocated_minutes": self.allocated_minutes,
        }


@dataclass(frozen=True)
class RevisionPriority:
    """Revision priority derived from Canonical mastery / progress."""

    topic_id: str
    topic_name: str
    mastery_score: float | None
    reason: str
    rank: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "topic_id": self.topic_id,
            "topic_name": self.topic_name,
            "mastery_score": self.mastery_score,
            "reason": self.reason,
            "rank": self.rank,
        }


@dataclass(frozen=True)
class RecommendedWorkload:
    """Planner-owned workload recommendation (uses Twin signals, not Twin math)."""

    available_study_minutes: int
    recommended_minutes: int
    rationale: str
    authority: str = AUTHORITY_RUNTIME_A

    def to_dict(self) -> dict[str, Any]:
        return {
            "available_study_minutes": self.available_study_minutes,
            "recommended_minutes": self.recommended_minutes,
            "rationale": self.rationale,
            "authority": self.authority,
        }


@dataclass(frozen=True)
class DailyStudyPlanProjection:
    """Adaptive daily study plan projected from Canonical Learner State.

    Planning artefact — regenerable. Does not persist missions; callers may
    still use PlanningService.generate_today_mission for ORM persistence.
    """

    student_id: str
    as_of: str | None
    plan_date: str
    consumer_version: str
    foundation_version: str
    twin_id: str
    availability: str
    unavailable_reason: str
    lifecycle_stage: str
    today_missions: tuple[MissionSlot, ...]
    revision_priorities: tuple[RevisionPriority, ...]
    topic_ordering: tuple[Mapping[str, Any], ...]
    recommended_workload: RecommendedWorkload
    provenance_refs: tuple[str, ...] = ()
    limitations_codes: tuple[str, ...] = ()
    explainability: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        object.__setattr__(self, "today_missions", tuple(self.today_missions))
        object.__setattr__(
            self, "revision_priorities", tuple(self.revision_priorities)
        )
        object.__setattr__(
            self, "topic_ordering", _freeze_rows(self.topic_ordering)
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
            "consumer_version": self.consumer_version,
            "explainability": dict(self.explainability),
            "foundation_version": self.foundation_version,
            "lifecycle_stage": self.lifecycle_stage,
            "limitations_codes": list(self.limitations_codes),
            "plan_date": self.plan_date,
            "provenance_refs": list(self.provenance_refs),
            "recommended_workload": self.recommended_workload.to_dict(),
            "revision_priorities": [r.to_dict() for r in self.revision_priorities],
            "student_id": self.student_id,
            "today_missions": [m.to_dict() for m in self.today_missions],
            "topic_ordering": [dict(row) for row in self.topic_ordering],
            "twin_id": self.twin_id,
            "unavailable_reason": self.unavailable_reason,
            "authority": AUTHORITY_DIGITAL_TWIN,
            "source_service": SOURCE_SERVICE_ADAPTIVE_STUDY_PLANNER,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_dict())


__all__ = [
    "PLANNER_CONSUMER_VERSION",
    "REASON_INVALID_STUDENT_ID",
    "REASON_NO_ACTIVE_PLAN",
    "REASON_STATE_UNAVAILABLE",
    "REASON_TWIN_FLAG_OFF",
    "SOURCE_SERVICE_ADAPTIVE_STUDY_PLANNER",
    "AdaptivePlannerInputs",
    "DailyStudyPlanProjection",
    "MissionSlot",
    "RecommendedWorkload",
    "RevisionPriority",
    "TopicPlanRow",
    "AVAILABILITY_AVAILABLE",
    "AVAILABILITY_UNAVAILABLE",
    "AUTHORITY_DIGITAL_TWIN",
    "AUTHORITY_RUNTIME_A",
    "serialize_canonical",
]
