"""AI Learning Coach enumerations.

Presentation vocabulary only — never mastery bands, recommendation
categories, or educational reasoning codes exposed as domain types.
"""

from __future__ import annotations

from enum import StrEnum


class SuggestedQuestionKind(StrEnum):
    """Deterministic suggested coaching questions — never LLM-authored."""

    WHY_NEXT_MISSION = "why_next_mission"
    WHAT_IMPROVED = "what_improved"
    WHY_READINESS = "why_readiness"
    FOCUS_TODAY = "focus_today"
    MISS_SESSION = "miss_session"


class ExplanationCardKind(StrEnum):
    """Deterministic explanation card kinds."""

    MISSION_PURPOSE = "mission_purpose"
    RECOMMENDATION_RATIONALE = "recommendation_rationale"
    PROGRESS_SUMMARY = "progress_summary"
    READINESS_REASONING = "readiness_reasoning"
    JOURNEY_HIGHLIGHTS = "journey_highlights"


class ReflectionPromptKind(StrEnum):
    """Post-study reflection prompt kinds — never AI generation."""

    MOST_DIFFICULT = "most_difficult"
    BECAME_CLEARER = "became_clearer"
    STILL_UNCERTAIN = "still_uncertain"
    CONFIDENCE = "confidence"


class CelebrationKind(StrEnum):
    """Deterministic celebration moment kinds."""

    STUDY_STREAK = "study_streak"
    MASTERY_IMPROVED = "mastery_improved"
    FIRST_REVISION_CYCLE = "first_revision_cycle"
    MISSION_STREAK = "mission_streak"
    CONSISTENCY = "consistency"


class ContextSectionKind(StrEnum):
    """Structured coach context section kinds."""

    CURRENT_FOCUS = "current_focus"
    LEARNING_JOURNEY = "learning_journey"
    READINESS = "readiness"
    CURRENT_MISSION = "current_mission"
    RECENT_IMPROVEMENTS = "recent_improvements"
    CURRENT_RISKS = "current_risks"
    UPCOMING_MILESTONES = "upcoming_milestones"
