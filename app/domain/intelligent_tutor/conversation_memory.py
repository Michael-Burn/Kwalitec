"""Conversation memory — lightweight session state only.

Does not store long-term learner state. The Student Digital Twin remains
the system of record for mastery, gaps, confidence, and recommendations.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime


@dataclass(frozen=True)
class ConversationMemory:
    """In-session conversational memory for one TutorSession.

    Remembers the current conversation, referenced concepts, active mission,
    and a short learner-state summary — never Twin inference rows.
    """

    memory_id: str
    session_id: str
    twin_id: str
    referenced_concept_ids: tuple[str, ...] = ()
    active_mission_id: str = ""
    learner_state_summary: str = ""
    turn_count: int = 0
    last_question_kind: str = ""
    last_response_id: str = ""
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        if not (self.memory_id or "").strip():
            raise ValueError("memory_id is required")
        if not (self.session_id or "").strip():
            raise ValueError("session_id is required")
        if not (self.twin_id or "").strip():
            raise ValueError("twin_id is required")
        object.__setattr__(
            self,
            "referenced_concept_ids",
            tuple(dict.fromkeys(self.referenced_concept_ids or ())),
        )
        object.__setattr__(self, "turn_count", max(0, int(self.turn_count)))
        when = self.updated_at
        if when is not None and when.tzinfo is not None:
            object.__setattr__(
                self, "updated_at", when.astimezone(UTC).replace(tzinfo=None)
            )


def update_conversation_memory(
    memory: ConversationMemory,
    *,
    concept_ids: tuple[str, ...] = (),
    active_mission_id: str = "",
    learner_state_summary: str = "",
    question_kind: str = "",
    response_id: str = "",
    updated_at: datetime | None = None,
) -> ConversationMemory:
    """Return an updated memory after one conversational turn."""
    when = updated_at or datetime.now(UTC).replace(tzinfo=None)
    merged = tuple(
        dict.fromkeys(
            list(memory.referenced_concept_ids) + list(concept_ids or ())
        )
    )
    return replace(
        memory,
        referenced_concept_ids=merged,
        active_mission_id=active_mission_id or memory.active_mission_id,
        learner_state_summary=learner_state_summary or memory.learner_state_summary,
        turn_count=memory.turn_count + 1,
        last_question_kind=question_kind or memory.last_question_kind,
        last_response_id=response_id or memory.last_response_id,
        updated_at=when,
    )
