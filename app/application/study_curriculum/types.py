"""Read-side DTOs for the Study Curriculum learning-state join."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.application.study_curriculum.states import TopicLearningState


@dataclass(frozen=True)
class TopicCurriculumState:
    """Minimal per-topic row for Study's Curriculum view."""

    topic_id: str
    topic_code: str
    title: str
    section_id: str | None
    section_title: str | None
    state: TopicLearningState
    last_practised_at: datetime | None


@dataclass(frozen=True)
class CurriculumLearningSnapshot:
    """One honest learning state per published syllabus topic."""

    user_id: int
    subject_code: str
    curriculum_identity: str
    topics: tuple[TopicCurriculumState, ...]
