"""Milestone detection for Honest Progress (data foundation only).

Milestones fire only when criteria are genuinely met. Streak thresholds use
7 / 30 / 100 days: one week (habit formation), one month (sustained practice),
and one hundred days (major commitment marker) without punitive framing.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.application.adaptive_decision.types import POLICY_V1_MIN_EVIDENCE
from app.application.student_twin.cutover import ek_display_0_100
from app.application.student_twin.query import TopicKnowledgeFact

EK_MASTERED_THRESHOLD = 90.0
DEFAULT_STREAK_MILESTONE_THRESHOLDS: tuple[int, ...] = (7, 30, 100)


class MilestoneKind(StrEnum):
    """Earned milestone categories."""

    TOPIC_EK_MASTERED = "topic_ek_mastered"
    SECTION_STUDY_COMPLETE = "section_study_complete"
    STREAK_DAYS = "streak_days"


@dataclass(frozen=True)
class SectionProgressSpec:
    """One syllabus section and its leaf topic ids for completion checks."""

    section_id: str
    title: str
    topic_ids: frozenset[str]


@dataclass(frozen=True)
class EarnedMilestone:
    """A milestone genuinely earned at detection time."""

    kind: MilestoneKind
    milestone_id: str
    label: str


def is_ek_mastered(fact: TopicKnowledgeFact | None) -> bool:
    """True when Twin EK meets evidence floor and mastery threshold (S3 fix)."""
    if fact is None or not fact.has_estimated_knowledge:
        return False
    if int(fact.evidence_count or 0) < POLICY_V1_MIN_EVIDENCE:
        return False
    score = ek_display_0_100(fact)
    return score is not None and score >= EK_MASTERED_THRESHOLD


def section_study_complete(
    *,
    section: SectionProgressSpec,
    completed_topic_ids: frozenset[str],
) -> bool:
    """True when every leaf topic in the section is Study Progress complete."""
    if not section.topic_ids:
        return False
    return all(tid in completed_topic_ids for tid in section.topic_ids)


def detect_ek_mastered_milestones(
    facts: tuple[TopicKnowledgeFact, ...],
    *,
    previously_earned: frozenset[str],
    topic_titles: dict[str, str] | None = None,
) -> tuple[EarnedMilestone, ...]:
    """New per-topic EK mastery milestones not previously recorded."""
    titles = topic_titles or {}
    earned: list[EarnedMilestone] = []
    for fact in facts:
        if not is_ek_mastered(fact):
            continue
        milestone_id = f"topic_ek_{fact.topic_id}"
        if milestone_id in previously_earned:
            continue
        title = titles.get(fact.topic_id) or fact.topic_id
        earned.append(
            EarnedMilestone(
                kind=MilestoneKind.TOPIC_EK_MASTERED,
                milestone_id=milestone_id,
                label=f"Estimated knowledge mastered for {title}",
            )
        )
    return tuple(earned)


def detect_section_complete_milestones(
    sections: tuple[SectionProgressSpec, ...],
    *,
    completed_topic_ids: frozenset[str],
    previously_earned: frozenset[str],
) -> tuple[EarnedMilestone, ...]:
    """New full-section Study Progress completion milestones."""
    earned: list[EarnedMilestone] = []
    for section in sections:
        if not section_study_complete(
            section=section,
            completed_topic_ids=completed_topic_ids,
        ):
            continue
        milestone_id = f"section_{section.section_id}"
        if milestone_id in previously_earned:
            continue
        earned.append(
            EarnedMilestone(
                kind=MilestoneKind.SECTION_STUDY_COMPLETE,
                milestone_id=milestone_id,
                label=f"Section complete: {section.title}",
            )
        )
    return tuple(earned)


def detect_streak_milestones(
    *,
    longest_streak_days: int,
    previously_earned: frozenset[str],
    thresholds: tuple[int, ...] = DEFAULT_STREAK_MILESTONE_THRESHOLDS,
) -> tuple[EarnedMilestone, ...]:
    """New streak-length milestones based on peak qualifying-day streak."""
    earned: list[EarnedMilestone] = []
    for threshold in thresholds:
        if longest_streak_days < threshold:
            continue
        milestone_id = f"streak_{threshold}"
        if milestone_id in previously_earned:
            continue
        earned.append(
            EarnedMilestone(
                kind=MilestoneKind.STREAK_DAYS,
                milestone_id=milestone_id,
                label=f"{threshold}-day study streak reached",
            )
        )
    return tuple(earned)
