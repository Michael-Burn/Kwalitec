"""SB-001A Baseline declaration shapes — structural only."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.application.student_baseline.enums import (
    ConfidenceBand,
    ExamHistory,
    LearningObjective,
    PositionMode,
    PreviousExperience,
)


@dataclass(frozen=True)
class BaselineSubjectScope:
    """Subject identity for a Baseline draft / complete row."""

    subject_key: str
    category_code: str
    subject_code: str
    curriculum_version: str | None = None
    exam_name: str | None = None
    exam_sitting: str | None = None
    exam_date: date | None = None
    weekday_study_minutes: int | None = None
    weekend_study_minutes: int | None = None
    preferred_session_minutes: int | None = None
    study_preference: str | None = None
    target_grade: str | None = None


@dataclass(frozen=True)
class BaselineDeclarations:
    """Closed answers required to finalise a Baseline."""

    experience: PreviousExperience
    position_mode: PositionMode
    exam_history: ExamHistory
    learning_objective: LearningObjective
    confidence: ConfidenceBand
    curriculum_topic_code: str | None = None
    highest_mark: str | None = None

    def is_complete(self) -> bool:
        """True when required fields are present and coherent."""
        if self.position_mode is PositionMode.CONTINUE_TOPIC:
            return bool(self.curriculum_topic_code)
        return True
