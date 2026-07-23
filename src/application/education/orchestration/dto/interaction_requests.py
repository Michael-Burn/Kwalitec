"""Application request DTOs for student interaction workflows.

Primitives only. Domain factories are invoked by the orchestrator at the
application → domain boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class InteractionKind(StrEnum):
    """Supported student interaction kinds for orchestration."""

    QUESTION_ANSWER = "question_answer"
    REFLECTION = "reflection"
    CHECKPOINT = "checkpoint"
    SESSION_COMPLETION = "session_completion"


@dataclass(frozen=True, slots=True)
class QuestionAnswerRequest:
    """Record a single answered question as educational evidence."""

    student_id: str
    competency_id: str
    is_correct: bool
    occurred_at: datetime
    learning_environment: str
    subject_id: str | None = None
    mission_id: str | None = None
    learning_episode_id: str | None = None
    source_origin: str = "orchestration"
    evidence_id: str | None = None

    def __post_init__(self) -> None:
        _require_non_empty(self.student_id, "student_id")
        _require_non_empty(self.competency_id, "competency_id")
        _require_datetime(self.occurred_at, "occurred_at")
        _require_non_empty(self.learning_environment, "learning_environment")
        if not isinstance(self.is_correct, bool):
            raise ValueError("is_correct must be a bool")


@dataclass(frozen=True, slots=True)
class ReflectionRequest:
    """Record a student reflection as educational evidence."""

    student_id: str
    reflection_text: str
    occurred_at: datetime
    learning_environment: str
    subject_id: str | None = None
    competency_id: str | None = None
    mission_id: str | None = None
    learning_episode_id: str | None = None
    source_origin: str = "orchestration"
    evidence_id: str | None = None

    def __post_init__(self) -> None:
        _require_non_empty(self.student_id, "student_id")
        _require_non_empty(self.reflection_text, "reflection_text")
        _require_datetime(self.occurred_at, "occurred_at")
        _require_non_empty(self.learning_environment, "learning_environment")


@dataclass(frozen=True, slots=True)
class CheckpointRequest:
    """Record a reached checkpoint as educational evidence."""

    student_id: str
    checkpoint_id: str
    occurred_at: datetime
    learning_environment: str
    subject_id: str | None = None
    source_origin: str = "orchestration"
    evidence_id: str | None = None

    def __post_init__(self) -> None:
        _require_non_empty(self.student_id, "student_id")
        _require_non_empty(self.checkpoint_id, "checkpoint_id")
        _require_datetime(self.occurred_at, "occurred_at")
        _require_non_empty(self.learning_environment, "learning_environment")


@dataclass(frozen=True, slots=True)
class SessionCompletionRequest:
    """Record study-session completion as educational evidence."""

    student_id: str
    learning_episode_id: str
    occurred_at: datetime
    learning_environment: str
    subject_id: str | None = None
    source_origin: str = "orchestration"
    evidence_id: str | None = None

    def __post_init__(self) -> None:
        _require_non_empty(self.student_id, "student_id")
        _require_non_empty(self.learning_episode_id, "learning_episode_id")
        _require_datetime(self.occurred_at, "occurred_at")
        _require_non_empty(self.learning_environment, "learning_environment")


@dataclass(frozen=True, slots=True)
class StudentInteractionRequest:
    """Generic interaction envelope dispatched by ``process_student_interaction``.

    Exactly one specialised payload must be present, matching ``kind``.
    """

    kind: InteractionKind
    question_answer: QuestionAnswerRequest | None = None
    reflection: ReflectionRequest | None = None
    checkpoint: CheckpointRequest | None = None
    session_completion: SessionCompletionRequest | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.kind, InteractionKind):
            raise ValueError("kind must be an InteractionKind")
        payload = self._payload_for_kind()
        if payload is None:
            raise ValueError(
                f"StudentInteractionRequest of kind {self.kind!r} "
                "requires the matching payload"
            )
        extras = [
            name
            for name, value in (
                ("question_answer", self.question_answer),
                ("reflection", self.reflection),
                ("checkpoint", self.checkpoint),
                ("session_completion", self.session_completion),
            )
            if value is not None and name != self._payload_field_name()
        ]
        if extras:
            raise ValueError(
                "StudentInteractionRequest must carry exactly one payload"
            )

    @property
    def student_id(self) -> str:
        return self._payload_for_kind().student_id  # type: ignore[union-attr]

    @property
    def occurred_at(self) -> datetime:
        return self._payload_for_kind().occurred_at  # type: ignore[union-attr]

    def _payload_field_name(self) -> str:
        return {
            InteractionKind.QUESTION_ANSWER: "question_answer",
            InteractionKind.REFLECTION: "reflection",
            InteractionKind.CHECKPOINT: "checkpoint",
            InteractionKind.SESSION_COMPLETION: "session_completion",
        }[self.kind]

    def _payload_for_kind(
        self,
    ) -> (
        QuestionAnswerRequest
        | ReflectionRequest
        | CheckpointRequest
        | SessionCompletionRequest
        | None
    ):
        return {
            InteractionKind.QUESTION_ANSWER: self.question_answer,
            InteractionKind.REFLECTION: self.reflection,
            InteractionKind.CHECKPOINT: self.checkpoint,
            InteractionKind.SESSION_COMPLETION: self.session_completion,
        }[self.kind]


def _require_non_empty(value: str, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} is required")


def _require_datetime(value: datetime, name: str) -> None:
    if not isinstance(value, datetime):
        raise ValueError(f"{name} must be a datetime")
