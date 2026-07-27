"""Feedback source taxonomy for learning feedback provenance."""

from __future__ import annotations

from enum import StrEnum


class FeedbackSource(StrEnum):
    """Where structured learning feedback originated."""

    ASSESSMENT_PIPELINE = "assessment_pipeline"
    MISSION_COMPLETION = "mission_completion"
    MISSION_STEP = "mission_step"
    QUIZ = "quiz"
    QUESTION = "question"
    REVISION = "revision"
    STUDY_SESSION = "study_session"
    REFLECTION = "reflection"
    WORKED_EXAMPLE = "worked_example"
    FORMULA_RECALL = "formula_recall"
