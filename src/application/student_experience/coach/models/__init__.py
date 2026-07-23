"""Immutable view models for AI Learning Coach."""

from __future__ import annotations

from application.student_experience.coach.models.celebration_moments import (
    CelebrationMoment,
    CelebrationMoments,
)
from application.student_experience.coach.models.coach_context import (
    CoachContext,
    FocusContext,
    ImprovementItem,
    JourneyContext,
    MilestoneItem,
    MissionContext,
    ReadinessContext,
    RiskItem,
)
from application.student_experience.coach.models.coach_snapshot import CoachSnapshot
from application.student_experience.coach.models.conversation_context import (
    ConversationContext,
)
from application.student_experience.coach.models.explanation_cards import (
    ExplanationCard,
    ExplanationCards,
)
from application.student_experience.coach.models.reflection_prompts import (
    ReflectionPrompt,
    ReflectionPrompts,
)
from application.student_experience.coach.models.suggested_questions import (
    SuggestedQuestion,
    SuggestedQuestions,
)

__all__ = [
    "CelebrationMoment",
    "CelebrationMoments",
    "CoachContext",
    "CoachSnapshot",
    "ConversationContext",
    "ExplanationCard",
    "ExplanationCards",
    "FocusContext",
    "ImprovementItem",
    "JourneyContext",
    "MilestoneItem",
    "MissionContext",
    "ReadinessContext",
    "ReflectionPrompt",
    "ReflectionPrompts",
    "RiskItem",
    "SuggestedQuestion",
    "SuggestedQuestions",
]
