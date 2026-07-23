"""Shared factories for Student Educational State domain tests."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.ids import LearningEpisodeId
from domain.education.student_state import (
    CheckpointId,
    CheckpointReference,
    CompetencyId,
    CompetencyState,
    ConfidenceSummary,
    EducationalHealth,
    EducationalHealthBand,
    EducationalTimelineId,
    EducationalTimelineReference,
    MasteryBand,
    MasterySummary,
    MissionId,
    MissionReference,
    StudentEducationalState,
    StudentEducationalStateId,
    SubjectId,
    SubjectState,
    SubjectStatus,
)

STATE_001 = StudentEducationalStateId("state-001")
SUBJECT_MATH = SubjectId("subject-math")
SUBJECT_PHYSICS = SubjectId("subject-physics")
COMPETENCY_ALGEBRA = CompetencyId("competency-algebra")
COMPETENCY_CALCULUS = CompetencyId("competency-calculus")


@pytest.fixture
def state_id() -> StudentEducationalStateId:
    return StudentEducationalStateId("state-001")


@pytest.fixture
def student_id() -> str:
    return "student-ada"


@pytest.fixture
def as_of() -> datetime:
    return datetime(2026, 7, 21, 12, 0, 0, tzinfo=UTC)


def make_subject_state(
    *,
    subject_id: SubjectId | str = SUBJECT_MATH,
    status: SubjectStatus = SubjectStatus.ACTIVE,
    coverage_ratio: float | None = 0.4,
    label: str | None = None,
) -> SubjectState:
    if isinstance(subject_id, str):
        subject_id = SubjectId(subject_id)
    return SubjectState(
        subject_id=subject_id,
        status=status,
        coverage_ratio=coverage_ratio,
        label=label,
    )


def make_competency_state(
    *,
    competency_id: CompetencyId | str = COMPETENCY_ALGEBRA,
    subject_id: SubjectId | str = SUBJECT_MATH,
    band: MasteryBand = MasteryBand.DEVELOPING,
    mastery_ratio: float | None = 0.5,
    label: str | None = None,
) -> CompetencyState:
    if isinstance(competency_id, str):
        competency_id = CompetencyId(competency_id)
    if isinstance(subject_id, str):
        subject_id = SubjectId(subject_id)
    return CompetencyState(
        competency_id=competency_id,
        subject_id=subject_id,
        band=band,
        mastery_ratio=mastery_ratio,
        label=label,
    )


def make_mastery_summary(
    band: MasteryBand = MasteryBand.DEVELOPING,
    *,
    ratio: float | None = 0.5,
) -> MasterySummary:
    return MasterySummary(
        overall_band=band,
        overall_ratio=ratio,
        developing_count=1,
    )


def make_confidence_summary(
    overall: ConfidenceLevel = ConfidenceLevel.MEDIUM,
    *,
    ratio: float | None = 0.6,
) -> ConfidenceSummary:
    return ConfidenceSummary(overall=overall, overall_ratio=ratio)


def make_educational_health(
    band: EducationalHealthBand = EducationalHealthBand.STABLE,
    *,
    ratio: float | None = 0.7,
    reasons: tuple[str, ...] = (),
) -> EducationalHealth:
    return EducationalHealth(band=band, ratio=ratio, reasons=reasons)


def make_mission_reference(
    mission_id: MissionId | str = "mission-001",
) -> MissionReference:
    if isinstance(mission_id, str):
        mission_id = MissionId(mission_id)
    return MissionReference(mission_id=mission_id)


def make_checkpoint_reference(
    checkpoint_id: CheckpointId | str = "checkpoint-001",
) -> CheckpointReference:
    if isinstance(checkpoint_id, str):
        checkpoint_id = CheckpointId(checkpoint_id)
    return CheckpointReference(checkpoint_id=checkpoint_id)


def make_timeline_reference(
    timeline_id: EducationalTimelineId | str = "timeline-001",
) -> EducationalTimelineReference:
    if isinstance(timeline_id, str):
        timeline_id = EducationalTimelineId(timeline_id)
    return EducationalTimelineReference(timeline_id=timeline_id)


def make_episode_id(value: str = "episode-001") -> LearningEpisodeId:
    return LearningEpisodeId(value)


def make_state(
    *,
    state_id: StudentEducationalStateId | str = STATE_001,
    student_id: str = "student-ada",
) -> StudentEducationalState:
    if isinstance(state_id, str):
        state_id = StudentEducationalStateId(state_id)
    return StudentEducationalState.create(state_id=state_id, student_id=student_id)
