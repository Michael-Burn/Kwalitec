"""Student-facing educational experience snapshots (PX-001).

Presentation-ready projections of Runtime C / EQ-001 outputs. No Twin,
Adaptive, or Runtime A authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True)
class CurriculumPositionSnapshot:
    """Where the student sits in the published syllabus."""

    subject_code: str
    subject_title: str
    version_label: str
    section_title: str
    topic_id: str
    topic_code: str
    topic_title: str
    position_index: int
    topic_count: int
    position_label: str
    coverage_ratio: float
    coverage_percent: int
    journey_stage: str


@dataclass(frozen=True)
class MissionEducationSnapshot:
    """EQ-001 mission fields surfaced for student display."""

    mission_instance_id: str
    title: str
    topic_code: str
    topic_title: str
    learning_objectives: tuple[str, ...]
    estimated_duration_minutes: int
    estimated_duration_label: str
    completion_definition: str
    educational_rationale: str
    prerequisite_status_label: str
    prerequisite_satisfied: bool
    task_descriptions: tuple[str, ...]
    status: str
    # Mapped EQ-001 explanation fields (P-001.2 schema)
    why_this_mission: str
    supporting_evidence: tuple[str, ...]
    confidence_label: str
    expected_benefit: str
    suggested_next_action: str
    review_point: str
    judgement: str
    educational_package_id: str = ""


@dataclass(frozen=True)
class JourneyEducationSnapshot:
    """EQ-001 journey explanation + topic lists for Journey surface."""

    why_today: str
    why_previous_complete: str
    unlocks_next: str
    supporting_evidence: tuple[str, ...]
    current_topic_title: str
    completed_topics: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    upcoming_topics: tuple[tuple[str, str], ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class PacingEducationSnapshot:
    """Exam-date-aware pacing projection (EQ-P*)."""

    exam_date: date | None
    exam_date_label: str
    exam_date_aware: bool
    first_pass_minutes: int
    revision_minutes: int
    total_required_minutes: int
    feasible: bool | None
    shortfall_minutes: int | None
    pacing_summary: str
    feasibility_label: str


@dataclass(frozen=True)
class CoverageGapSnapshot:
    """Honest withhold when certified guidance is unavailable (PB-002 F7)."""

    topic_code: str
    message: str


@dataclass(frozen=True)
class EducationalExperienceSnapshot:
    """Full Runtime C educational projection for one enrolled student."""

    student_id: str
    enrolment_id: str
    subject_code: str
    curriculum_identity: str
    runtime_authority: str
    is_runtime_c: bool
    greeting: str
    examination_label: str
    curriculum_position: CurriculumPositionSnapshot
    mission: MissionEducationSnapshot | None
    journey: JourneyEducationSnapshot
    pacing: PacingEducationSnapshot
    syllabus_complete: bool = False
    coverage_gap: CoverageGapSnapshot | None = None
