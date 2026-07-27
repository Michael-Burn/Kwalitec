"""Coaching messages — tone-controlled educational guidance lines."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class CoachingTone(StrEnum):
    EXPLAIN = "explain"
    GUIDE = "guide"
    REFLECT = "reflect"
    RECOVER = "recover"


@dataclass(frozen=True)
class CoachingMessage:
    """One coaching line that explains a platform decision."""

    message_id: str
    text: str
    tone: CoachingTone = CoachingTone.EXPLAIN
    evidence_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not (self.message_id or "").strip():
            raise ValueError("message_id is required")
        if not (self.text or "").strip():
            raise ValueError("coaching message text is required")
        tone = (
            self.tone
            if isinstance(self.tone, CoachingTone)
            else CoachingTone(str(self.tone))
        )
        object.__setattr__(self, "tone", tone)
        object.__setattr__(self, "evidence_ids", tuple(self.evidence_ids or ()))
