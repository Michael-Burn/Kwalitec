"""Shared factories for Educational Evidence domain tests."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from domain.education.educational_evidence import (
    CheckpointId,
    CompetencyId,
    EvidenceContext,
    EvidenceId,
    EvidenceSource,
    LearningContext,
    LearningEnvironment,
    LearningEnvironmentKind,
    MissionId,
    SubjectId,
)
from domain.education.foundation.ids import LearningEpisodeId

OCCURRED_AT = datetime(2026, 7, 21, 12, 0, 0, tzinfo=UTC)
STUDENT_ID = "student-ada"


@pytest.fixture
def occurred_at() -> datetime:
    return OCCURRED_AT


@pytest.fixture
def student_id() -> str:
    return STUDENT_ID


@pytest.fixture
def source() -> EvidenceSource:
    return EvidenceSource.student_action("mission_engine")


@pytest.fixture
def mission_environment() -> LearningEnvironment:
    return LearningEnvironment.of(LearningEnvironmentKind.MISSION)


def make_evidence_id(value: str = "evidence-001") -> EvidenceId:
    return EvidenceId(value)


def make_source(origin: str = "mission_engine") -> EvidenceSource:
    return EvidenceSource.student_action(origin)


def make_environment(
    kind: LearningEnvironmentKind = LearningEnvironmentKind.MISSION,
) -> LearningEnvironment:
    return LearningEnvironment.of(kind)


def make_learning_context(
    *,
    subject_id: str | None = None,
    competency_id: str | None = "competency-algebra",
    mission_id: str | None = None,
    checkpoint_id: str | None = None,
    learning_episode_id: str | None = None,
) -> LearningContext:
    return LearningContext(
        subject_id=SubjectId(subject_id) if subject_id else None,
        competency_id=CompetencyId(competency_id) if competency_id else None,
        mission_id=MissionId(mission_id) if mission_id else None,
        checkpoint_id=CheckpointId(checkpoint_id) if checkpoint_id else None,
        learning_episode_id=(
            LearningEpisodeId(learning_episode_id) if learning_episode_id else None
        ),
    )


def make_context(
    *,
    learning_environment: LearningEnvironment | None = None,
    subject_id: str | None = None,
    competency_id: str | None = "competency-algebra",
    mission_id: str | None = None,
    checkpoint_id: str | None = None,
    learning_episode_id: str | None = None,
) -> EvidenceContext:
    return EvidenceContext(
        learning_context=make_learning_context(
            subject_id=subject_id,
            competency_id=competency_id,
            mission_id=mission_id,
            checkpoint_id=checkpoint_id,
            learning_episode_id=learning_episode_id,
        ),
        learning_environment=learning_environment or make_environment(),
    )
