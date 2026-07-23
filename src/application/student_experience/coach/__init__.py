"""AI Learning Coach — XP-005.

Application-layer composition of Education OS and Student Experience
outputs into deterministic coaching context.

Responsibilities
    Prepare structured context explaining Education OS decisions.
    Compose suggested questions, explanation cards, reflections, and
    celebration moments.

Non-responsibilities
    Estimate mastery, generate recommendations, generate missions,
    persist data, call GPT/Claude/Gemini, or implement UI.
"""

from __future__ import annotations

from application.student_experience.coach.coach_inputs import CoachInputs
from application.student_experience.coach.enums import (
    CelebrationKind,
    ContextSectionKind,
    ExplanationCardKind,
    ReflectionPromptKind,
    SuggestedQuestionKind,
)
from application.student_experience.coach.errors import (
    CoachExperienceError,
    CoachInvariantViolation,
)
from application.student_experience.coach.ids import (
    CoachId,
    CoachSnapshotId,
    ConversationId,
)
from application.student_experience.coach.learning_coach_service import (
    LearningCoachService,
)
from application.student_experience.coach.models import (
    CelebrationMoment,
    CelebrationMoments,
    CoachContext,
    CoachSnapshot,
    ConversationContext,
    ExplanationCard,
    ExplanationCards,
    FocusContext,
    ImprovementItem,
    JourneyContext,
    MilestoneItem,
    MissionContext,
    ReadinessContext,
    ReflectionPrompt,
    ReflectionPrompts,
    RiskItem,
    SuggestedQuestion,
    SuggestedQuestions,
)
from application.student_experience.coach.ports import (
    CoachContextPublisher,
    CoachPublisher,
)

__all__ = [
    # Service
    "LearningCoachService",
    # Inputs
    "CoachInputs",
    # Identity
    "CoachId",
    "ConversationId",
    "CoachSnapshotId",
    # View models
    "CoachContext",
    "ConversationContext",
    "SuggestedQuestions",
    "SuggestedQuestion",
    "ExplanationCards",
    "ExplanationCard",
    "ReflectionPrompts",
    "ReflectionPrompt",
    "CelebrationMoments",
    "CelebrationMoment",
    "CoachSnapshot",
    "FocusContext",
    "JourneyContext",
    "ReadinessContext",
    "MissionContext",
    "ImprovementItem",
    "RiskItem",
    "MilestoneItem",
    # Enums
    "SuggestedQuestionKind",
    "ExplanationCardKind",
    "ReflectionPromptKind",
    "CelebrationKind",
    "ContextSectionKind",
    # Errors
    "CoachExperienceError",
    "CoachInvariantViolation",
    # Ports
    "CoachPublisher",
    "CoachContextPublisher",
]
