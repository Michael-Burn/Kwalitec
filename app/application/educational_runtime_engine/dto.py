"""DTOs for the Educational Runtime Engine (PI-001C)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.application.educational_quality.dto import MissionQualityEnvelope


@dataclass(frozen=True)
class EnrolmentSnapshot:
    enrolment_id: str
    user_id: int
    subject_code: str
    curriculum_identity: str
    version_label: str
    published_package_id: int
    status: str
    exam_date: date | None = None
    created_at: datetime | None = None


@dataclass(frozen=True)
class StudyPlanInstanceSnapshot:
    plan_instance_id: str
    enrolment_id: str
    user_id: int
    subject_code: str
    curriculum_identity: str
    version_label: str
    status: str
    current_topic_id: str | None
    topic_template_ids: tuple[str, ...] = field(default_factory=tuple)
    created_at: datetime | None = None


@dataclass(frozen=True)
class MissionInstanceSnapshot:
    mission_instance_id: str
    plan_instance_id: str
    user_id: int
    curriculum_identity: str
    template_id: str
    topic_id: str
    topic_code: str
    title: str
    task_descriptions: tuple[str, ...]
    mission_date: date
    status: str
    created_at: datetime | None = None
    completed_at: datetime | None = None
    # EQ-001 quality envelope (derived at read time; not a UI contract change)
    quality: MissionQualityEnvelope | None = None
    # PB-002: publication_approved package selected for this sitting
    educational_package_id: str = ""


@dataclass(frozen=True)
class ProgressSnapshot:
    curriculum_identity: str
    topic_ids: tuple[str, ...]
    completed_topic_ids: tuple[str, ...]
    incomplete_topic_ids: tuple[str, ...]
    current_topic_id: str | None
    coverage_ratio: float
    journey_stage: str
    syllabus_complete: bool


@dataclass(frozen=True)
class ReadinessRuntimeInputs:
    """Inputs required by Readiness without duplicating educational state."""

    curriculum_identity: str
    subject_code: str
    topic_ids: tuple[str, ...]
    completed_topic_ids: tuple[str, ...]
    coverage_ratio: float
    current_topic_id: str | None
    syllabus_complete: bool
    journey_stage: str
    denominator_source: str = "published_progress_model"


@dataclass(frozen=True)
class EstimatedKnowledgeRuntimeInputs:
    """EK inputs: mission completion alone does not mint evidence."""

    curriculum_identity: str
    subject_code: str
    topic_ids: tuple[str, ...]
    completed_topic_ids: tuple[str, ...]
    topics: tuple[dict, ...] = field(default_factory=tuple)
    evidence_policy: str = (
        "mission_completion_is_study_progress_only; "
        "estimated_knowledge_requires_structured_question_evidence"
    )


@dataclass(frozen=True)
class EducationalEventSnapshot:
    event_id: str
    event_type: str
    user_id: int
    curriculum_identity: str
    enrolment_id: str | None = None
    plan_instance_id: str | None = None
    topic_id: str | None = None
    mission_instance_id: str | None = None
    payload: dict = field(default_factory=dict)
    occurred_at: datetime | None = None


@dataclass(frozen=True)
class RuntimeJourneySnapshot:
    """End-to-end runtime view for one student's published-subject journey."""

    enrolment: EnrolmentSnapshot
    study_plan: StudyPlanInstanceSnapshot
    progress: ProgressSnapshot
    readiness_inputs: ReadinessRuntimeInputs
    estimated_knowledge_inputs: EstimatedKnowledgeRuntimeInputs
    open_mission: MissionInstanceSnapshot | None = None
    runtime_authority: str = "published_curriculum"


@dataclass(frozen=True)
class SittingExecutionSpec:
    """Executable daily-sitting identity for Runtime C materialisation.

    Produced by selection (legacy path or ADR-027 Decision Engine). Contains
    pre-chunk objective_ids; session-budget chunking stays in materialisation.
    Runtime C must not import Adaptive Decision Engine types for control flow.
    """

    user_id: int
    subject_code: str
    mission_date: date
    curriculum_identity: str
    enrolment_id: str
    plan_instance_id: str
    topic_id: str
    topic_code: str
    template_id: str
    objective_ids: tuple[str, ...]
    educational_package_id: str | None = None
    educational_package_mode: str | None = None
    educational_campaign_day: str | int | None = None
    certified_mission_id: str | None = None
    selection_reasons: tuple[str, ...] = ()
    curriculum_provenance: dict | None = None
    calibration_notes: tuple[str, ...] = ()
    selection_trace: dict = field(default_factory=dict)
