"""Study Progress DTOs — Progress Engine outputs (SR-003).

Coverage is Study Progress, not understanding. Twin estimates are optional
annotations for projections only; they never author coverage.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class TwinEstimateInput:
    """Optional Twin-owned educational estimates (read-only).

    Progress Engine never invents these. Absence is lawful and supported.
    """

    estimated_knowledge: dict[str, float] = field(default_factory=dict)
    estimated_mastery: dict[str, float] = field(default_factory=dict)
    overall_knowledge: float | None = None
    overall_mastery: float | None = None
    twin_status: str | None = None
    twin_id: str | None = None

    def is_present(self) -> bool:
        return bool(
            self.estimated_knowledge
            or self.estimated_mastery
            or self.overall_knowledge is not None
            or self.overall_mastery is not None
        )

    @classmethod
    def absent(cls) -> TwinEstimateInput:
        return cls()

    @classmethod
    def from_opaque(cls, raw: dict[str, Any] | None) -> TwinEstimateInput:
        if not raw:
            return cls.absent()
        knowledge = raw.get("estimated_knowledge") or {}
        mastery = raw.get("estimated_mastery") or {}
        return cls(
            estimated_knowledge={
                str(k): float(v) for k, v in dict(knowledge).items()
            },
            estimated_mastery={
                str(k): float(v) for k, v in dict(mastery).items()
            },
            overall_knowledge=(
                float(raw["overall_knowledge"])
                if raw.get("overall_knowledge") is not None
                else None
            ),
            overall_mastery=(
                float(raw["overall_mastery"])
                if raw.get("overall_mastery") is not None
                else None
            ),
            twin_status=(
                str(raw["twin_status"]) if raw.get("twin_status") else None
            ),
            twin_id=str(raw["twin_id"]) if raw.get("twin_id") else None,
        )


@dataclass(frozen=True)
class CurriculumPosition:
    """Singular syllabus position for one enrolment / curriculum identity."""

    curriculum_identity: str
    current_topic_id: str | None
    current_topic_index: int | None
    topic_count: int
    completed_count: int
    remaining_count: int
    coverage_ratio: float
    journey_stage: str
    syllabus_complete: bool

    def to_opaque(self) -> dict[str, Any]:
        return {
            "curriculum_identity": self.curriculum_identity,
            "current_topic_id": self.current_topic_id,
            "current_topic_index": self.current_topic_index,
            "topic_count": self.topic_count,
            "completed_count": self.completed_count,
            "remaining_count": self.remaining_count,
            "coverage_ratio": self.coverage_ratio,
            "journey_stage": self.journey_stage,
            "syllabus_complete": self.syllabus_complete,
            "authority": "progress_engine",
        }


@dataclass(frozen=True)
class ProgressProjection:
    """Forward-looking Study Progress projection for Mission / Dashboard.

    Twin annotations are optional. Coverage math never depends on Twin.
    """

    remaining_topic_ids: tuple[str, ...]
    next_topic_id: str | None
    estimated_topics_remaining: int
    twin_present: bool
    twin_annotated_remaining: tuple[dict[str, Any], ...] = ()
    weak_topic_ids: tuple[str, ...] = ()
    overall_estimated_mastery: float | None = None
    overall_estimated_knowledge: float | None = None
    projection_basis: str = "coverage_only"

    def to_opaque(self) -> dict[str, Any]:
        return {
            "remaining_topic_ids": list(self.remaining_topic_ids),
            "next_topic_id": self.next_topic_id,
            "estimated_topics_remaining": self.estimated_topics_remaining,
            "twin_present": self.twin_present,
            "twin_annotated_remaining": list(self.twin_annotated_remaining),
            "weak_topic_ids": list(self.weak_topic_ids),
            "overall_estimated_mastery": self.overall_estimated_mastery,
            "overall_estimated_knowledge": self.overall_estimated_knowledge,
            "projection_basis": self.projection_basis,
            "authority": "progress_engine",
        }


@dataclass(frozen=True)
class MissionCompositionInputs:
    """Progress inputs for tomorrow's mission composition.

    Mission selection remains Mission AUTHORITY. Progress supplies position
    truth only — never teaches or redesigns missions.
    """

    curriculum_identity: str
    current_topic_id: str | None
    completed_topic_ids: tuple[str, ...]
    remaining_topic_ids: tuple[str, ...]
    coverage_ratio: float
    journey_stage: str
    syllabus_complete: bool
    weak_topic_ids: tuple[str, ...] = ()
    twin_present: bool = False

    def to_opaque(self) -> dict[str, Any]:
        return {
            "curriculum_identity": self.curriculum_identity,
            "current_topic_id": self.current_topic_id,
            "completed_topic_ids": list(self.completed_topic_ids),
            "remaining_topic_ids": list(self.remaining_topic_ids),
            "coverage_ratio": self.coverage_ratio,
            "journey_stage": self.journey_stage,
            "syllabus_complete": self.syllabus_complete,
            "weak_topic_ids": list(self.weak_topic_ids),
            "twin_present": self.twin_present,
            "authority": "progress_engine",
        }


@dataclass(frozen=True)
class StudyProgress:
    """Singular Study Progress — One Educational State for curriculum coverage."""

    curriculum_identity: str
    topic_ids: tuple[str, ...]
    completed_topic_ids: tuple[str, ...]
    incomplete_topic_ids: tuple[str, ...]
    current_topic_id: str | None
    coverage_ratio: float
    journey_stage: str
    syllabus_complete: bool
    completed_objective_ids: tuple[str, ...]
    remaining_objective_ids: tuple[str, ...]
    position: CurriculumPosition
    projection: ProgressProjection
    twin_estimates_applied: bool = False
    authority: str = "progress_engine"

    def to_opaque(self) -> dict[str, Any]:
        return {
            "curriculum_identity": self.curriculum_identity,
            "topic_ids": list(self.topic_ids),
            "completed_topic_ids": list(self.completed_topic_ids),
            "incomplete_topic_ids": list(self.incomplete_topic_ids),
            "current_topic_id": self.current_topic_id,
            "coverage_ratio": self.coverage_ratio,
            "journey_stage": self.journey_stage,
            "syllabus_complete": self.syllabus_complete,
            "completed_objective_ids": list(self.completed_objective_ids),
            "remaining_objective_ids": list(self.remaining_objective_ids),
            "position": self.position.to_opaque(),
            "projection": self.projection.to_opaque(),
            "twin_estimates_applied": self.twin_estimates_applied,
            "authority": self.authority,
        }


@dataclass(frozen=True)
class CoverageAdvanceDecision:
    """Whether Progress Engine may advance coverage for one sitting.

    Trusts EducationalEvidenceAuthority columns. Never re-evaluates evidence.
    """

    may_advance: bool
    reason: str
    evidence_disposition: str | None = None
    topic_id: str | None = None
    package_id: str | None = None
    mission_instance_id: str | None = None

    def to_opaque(self) -> dict[str, Any]:
        return {
            "may_advance": self.may_advance,
            "reason": self.reason,
            "evidence_disposition": self.evidence_disposition,
            "topic_id": self.topic_id,
            "package_id": self.package_id,
            "mission_instance_id": self.mission_instance_id,
            "authority": "progress_engine",
            "evidence_authority": "educational_evidence_authority",
        }
