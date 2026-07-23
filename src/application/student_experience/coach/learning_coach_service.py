"""LearningCoachService — compose coaching context from Education OS outputs.

Projection only. Never estimates mastery, generates recommendations,
generates missions, persists data, or invokes an LLM.
"""

from __future__ import annotations

from application.student_experience.coach.coach_composer import (
    compose_context,
    compose_conversation,
    compose_reflection,
    compose_snapshot,
)
from application.student_experience.coach.coach_inputs import CoachInputs
from application.student_experience.coach.ids import (
    CoachId,
    CoachSnapshotId,
    ConversationId,
)
from application.student_experience.coach.models.coach_context import CoachContext
from application.student_experience.coach.models.coach_snapshot import CoachSnapshot
from application.student_experience.coach.models.conversation_context import (
    ConversationContext,
)
from application.student_experience.coach.models.reflection_prompts import (
    ReflectionPrompts,
)
from application.student_experience.coach.ports.coach_context_publisher import (
    CoachContextPublisher,
)
from application.student_experience.coach.ports.coach_publisher import CoachPublisher


class LearningCoachService:
    """Application service composing the AI Learning Coach experience.

    Explains Education OS decisions. Never replaces them. Returns immutable
    view models suitable for UI binding or downstream narration adapters.
    """

    def __init__(
        self,
        *,
        coach_publisher: CoachPublisher | None = None,
        coach_context_publisher: CoachContextPublisher | None = None,
    ) -> None:
        self._publisher = coach_publisher
        self._context_publisher = coach_context_publisher

    def build_context(
        self,
        inputs: CoachInputs,
        *,
        coach_id: CoachId | str | None = None,
    ) -> CoachContext:
        """Compose structured coaching context explaining current decisions.

        Args:
            inputs: Caller-supplied Student Experience + Education OS artefacts.
            coach_id: Optional identity for the composed context. Defaults to a
                deterministic id derived from student and composition time.

        Returns:
            Immutable ``CoachContext``.
        """
        resolved_id = self._resolve_coach_id(inputs, coach_id)
        return compose_context(inputs, coach_id=resolved_id)

    def build_conversation(
        self,
        inputs: CoachInputs,
        *,
        conversation_id: ConversationId | str | None = None,
        context: CoachContext | None = None,
    ) -> ConversationContext:
        """Compose conversation scaffolding with deterministic suggested questions.

        Args:
            inputs: Caller-supplied artefacts and ``as_of`` time.
            conversation_id: Optional identity for the conversation.
            context: Optional pre-composed ``CoachContext`` to avoid recomputation.

        Returns:
            Immutable ``ConversationContext``.
        """
        resolved_id = self._resolve_conversation_id(inputs, conversation_id)
        return compose_conversation(
            inputs,
            conversation_id=resolved_id,
            context=context,
        )

    def build_reflection(self, inputs: CoachInputs) -> ReflectionPrompts:
        """Compose post-study reflection prompts.

        Args:
            inputs: Caller-supplied artefacts.

        Returns:
            Immutable ``ReflectionPrompts``.
        """
        return compose_reflection(inputs)

    def build_snapshot(
        self,
        context: CoachContext,
        *,
        snapshot_id: CoachSnapshotId | str | None = None,
        suggested_question_count: int = 0,
        reflection_prompt_count: int = 0,
    ) -> CoachSnapshot:
        """Project a composed coach context into a compact snapshot.

        Args:
            context: Previously composed ``CoachContext``.
            snapshot_id: Optional snapshot identity.
            suggested_question_count: Optional count from a conversation build.
            reflection_prompt_count: Optional count from a reflection build.

        Returns:
            Immutable ``CoachSnapshot``.
        """
        resolved = self._resolve_snapshot_id(context, snapshot_id)
        return compose_snapshot(
            context,
            snapshot_id=resolved,
            suggested_question_count=suggested_question_count,
            reflection_prompt_count=reflection_prompt_count,
        )

    def refresh_coach(
        self,
        inputs: CoachInputs,
        *,
        coach_id: CoachId | str | None = None,
    ) -> CoachContext:
        """Rebuild coaching artefacts and publish when publishers are configured.

        Args:
            inputs: Caller-supplied artefacts and ``as_of`` time.
            coach_id: Optional identity for the composed context.

        Returns:
            Freshly composed ``CoachContext``.
        """
        context = self.build_context(inputs, coach_id=coach_id)
        conversation = self.build_conversation(inputs, context=context)
        reflection = self.build_reflection(inputs)
        snapshot = self.build_snapshot(
            context,
            suggested_question_count=len(conversation.suggested_questions.questions),
            reflection_prompt_count=len(reflection.prompts),
        )

        if self._context_publisher is not None:
            self._context_publisher.publish_context(context)
            self._context_publisher.publish_snapshot(snapshot)

        if self._publisher is not None:
            self._publisher.publish_conversation(conversation)
            self._publisher.publish_reflection(reflection)
            self._publisher.publish_snapshot(snapshot)

        return context

    @staticmethod
    def _resolve_coach_id(
        inputs: CoachInputs, coach_id: CoachId | str | None
    ) -> CoachId:
        if isinstance(coach_id, CoachId):
            return coach_id
        if isinstance(coach_id, str) and coach_id.strip():
            return CoachId(coach_id.strip())
        stamp = inputs.as_of.strftime("%Y%m%dT%H%M%S")
        return CoachId(f"coach:{inputs.student_id}:{stamp}")

    @staticmethod
    def _resolve_conversation_id(
        inputs: CoachInputs, conversation_id: ConversationId | str | None
    ) -> ConversationId:
        if isinstance(conversation_id, ConversationId):
            return conversation_id
        if isinstance(conversation_id, str) and conversation_id.strip():
            return ConversationId(conversation_id.strip())
        stamp = inputs.as_of.strftime("%Y%m%dT%H%M%S")
        return ConversationId(f"conv:{inputs.student_id}:{stamp}")

    @staticmethod
    def _resolve_snapshot_id(
        context: CoachContext, snapshot_id: CoachSnapshotId | str | None
    ) -> CoachSnapshotId:
        if isinstance(snapshot_id, CoachSnapshotId):
            return snapshot_id
        if isinstance(snapshot_id, str) and snapshot_id.strip():
            return CoachSnapshotId(snapshot_id.strip())
        stamp = context.composed_at.strftime("%Y%m%dT%H%M%S")
        return CoachSnapshotId(f"csnap:{context.coach_id.value}:{stamp}")
