"""Orchestrates milestone detection from read-only ports."""

from __future__ import annotations

from datetime import date

from app.application.learner_progress.milestones import (
    EarnedMilestone,
    SectionProgressSpec,
    detect_ek_mastered_milestones,
    detect_section_complete_milestones,
    detect_streak_milestones,
)
from app.application.learner_progress.query import QualifyingStudyDayQueryPort
from app.application.student_twin.query import LearnerTwinQueryPort


class LearnerProgressMilestoneDetector:
    """Detect newly earned milestones from Twin, Study Progress, and streak data."""

    def __init__(
        self,
        *,
        twin_query: LearnerTwinQueryPort,
        study_day_query: QualifyingStudyDayQueryPort,
    ) -> None:
        self._twin_query = twin_query
        self._study_day_query = study_day_query

    def detect_new_milestones(
        self,
        *,
        user_id: int,
        subject_code: str,
        sections: tuple[SectionProgressSpec, ...],
        completed_topic_ids: frozenset[str],
        previously_earned: frozenset[str],
        as_of: date,
        topic_titles: dict[str, str] | None = None,
    ) -> tuple[EarnedMilestone, ...]:
        """Return milestones earned since ``previously_earned`` was recorded."""
        facts = self._twin_query.topics_with_estimated_knowledge(
            user_id=user_id,
            subject_code=subject_code,
        )
        streak = self._study_day_query.streak_stats(user_id=user_id, as_of=as_of)
        earned: list[EarnedMilestone] = []
        earned.extend(
            detect_ek_mastered_milestones(
                facts,
                previously_earned=previously_earned,
                topic_titles=topic_titles,
            )
        )
        earned.extend(
            detect_section_complete_milestones(
                sections,
                completed_topic_ids=completed_topic_ids,
                previously_earned=previously_earned,
            )
        )
        earned.extend(
            detect_streak_milestones(
                longest_streak_days=streak.longest_streak_days,
                previously_earned=previously_earned,
            )
        )
        return tuple(earned)
