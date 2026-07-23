"""CoachPublisher — publish composed coaching artefacts outbound."""

from __future__ import annotations

from abc import ABC, abstractmethod

from application.student_experience.coach.models.coach_snapshot import CoachSnapshot
from application.student_experience.coach.models.conversation_context import (
    ConversationContext,
)
from application.student_experience.coach.models.reflection_prompts import (
    ReflectionPrompts,
)


class CoachPublisher(ABC):
    """Outbound port for publishing conversation and reflection artefacts.

    Implementations live in infrastructure. Publishing is notification /
    persistence wiring — never educational reasoning and never LLM calls.
    """

    @abstractmethod
    def publish_conversation(self, conversation: ConversationContext) -> None:
        """Publish a composed ``ConversationContext``."""

    @abstractmethod
    def publish_reflection(self, reflection: ReflectionPrompts) -> None:
        """Publish composed ``ReflectionPrompts``."""

    @abstractmethod
    def publish_snapshot(self, snapshot: CoachSnapshot) -> None:
        """Publish a composed ``CoachSnapshot``."""
