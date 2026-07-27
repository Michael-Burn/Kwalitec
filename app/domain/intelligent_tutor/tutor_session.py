"""TutorSession aggregate — conversation container for one tutoring thread."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum

from app.domain.intelligent_tutor.conversation_memory import ConversationMemory
from app.domain.intelligent_tutor.explanation import Explanation
from app.domain.intelligent_tutor.tutor_question import TutorQuestion
from app.domain.intelligent_tutor.tutor_response import TutorResponse


class TutorSessionStatus(StrEnum):
    ACTIVE = "active"
    CLOSED = "closed"
    ARCHIVED = "archived"


@dataclass(frozen=True)
class TutorSession:
    """Conversation session for the Evidence-Backed Intelligent Tutor.

    Stores conversation turns only. Learner educational state remains on the
    Student Digital Twin.
    """

    session_id: str
    twin_id: str
    student_id: str
    status: TutorSessionStatus = TutorSessionStatus.ACTIVE
    title: str = ""
    active_mission_id: str = ""
    memory: ConversationMemory | None = None
    questions: tuple[TutorQuestion, ...] = ()
    responses: tuple[TutorResponse, ...] = ()
    explanations: tuple[Explanation, ...] = ()
    created_at: datetime | None = None
    updated_at: datetime | None = None
    version: int = 1

    def __post_init__(self) -> None:
        if not (self.session_id or "").strip():
            raise ValueError("session_id is required")
        if not (self.twin_id or "").strip():
            raise ValueError("twin_id is required")
        status = (
            self.status
            if isinstance(self.status, TutorSessionStatus)
            else TutorSessionStatus(str(self.status))
        )
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "questions", tuple(self.questions or ()))
        object.__setattr__(self, "responses", tuple(self.responses or ()))
        object.__setattr__(self, "explanations", tuple(self.explanations or ()))
        for when_attr in ("created_at", "updated_at"):
            when = getattr(self, when_attr)
            if when is not None and when.tzinfo is not None:
                object.__setattr__(
                    self, when_attr, when.astimezone(UTC).replace(tzinfo=None)
                )

    @property
    def turn_count(self) -> int:
        return len(self.responses)

    def with_turn(
        self,
        *,
        question: TutorQuestion,
        response: TutorResponse,
        memory: ConversationMemory,
        updated_at: datetime | None = None,
    ) -> TutorSession:
        """Append one question/response turn immutably."""
        when = updated_at or datetime.now(UTC).replace(tzinfo=None)
        return replace(
            self,
            questions=(*self.questions, question),
            responses=(*self.responses, response),
            explanations=(*self.explanations, response.explanation),
            memory=memory,
            active_mission_id=memory.active_mission_id or self.active_mission_id,
            updated_at=when,
            version=self.version + 1,
            title=self.title or question.text[:80],
        )

    def close(self, *, updated_at: datetime | None = None) -> TutorSession:
        when = updated_at or datetime.now(UTC).replace(tzinfo=None)
        return replace(
            self,
            status=TutorSessionStatus.CLOSED,
            updated_at=when,
            version=self.version + 1,
        )
