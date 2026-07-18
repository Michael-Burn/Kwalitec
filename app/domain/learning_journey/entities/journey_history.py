"""Immutable chronological record of Learning Journey events.

Append-only spine for audit, explainability, and deterministic replay of
derived progress. Not a student-editable diary (reflections are separate).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum


class JourneyHistoryEventType(StrEnum):
    """Material journey events recorded in history."""

    JOURNEY_CREATED = "journey_created"
    JOURNEY_STATE_CHANGED = "journey_state_changed"
    SESSION_ADDED = "session_added"
    SESSION_STATE_CHANGED = "session_state_changed"
    EVIDENCE_RECORDED = "evidence_recorded"
    REFLECTION_CAPTURED = "reflection_captured"
    RECOMMENDATION_PROPOSED = "recommendation_proposed"
    RECOMMENDATION_LIFECYCLE_CHANGED = "recommendation_lifecycle_changed"
    PROGRESS_RECALCULATED = "progress_recalculated"
    COMPLETION_CRITERIA_EVALUATED = "completion_criteria_evaluated"


@dataclass(frozen=True)
class JourneyHistoryEntry:
    """One immutable history event.

    Attributes:
        event_id: Stable identity for the history row.
        event_type: Catalogue event type.
        occurred_at: When the event occurred.
        detail_tags: Short structural tags (from/to state, entity ids, …).
        session_id: Optional related session.
        evidence_id: Optional related evidence correlation id.
        recommendation_id: Optional related recommendation.
    """

    event_id: str
    event_type: JourneyHistoryEventType
    occurred_at: datetime
    detail_tags: tuple[str, ...] = ()
    session_id: str | None = None
    evidence_id: str | None = None
    recommendation_id: str | None = None

    @classmethod
    def create(
        cls,
        event_id: str,
        event_type: JourneyHistoryEventType | str,
        occurred_at: datetime,
        *,
        detail_tags: list[str] | tuple[str, ...] | None = None,
        session_id: str | None = None,
        evidence_id: str | None = None,
        recommendation_id: str | None = None,
    ) -> JourneyHistoryEntry:
        """Construct a JourneyHistoryEntry."""
        etype = (
            event_type
            if isinstance(event_type, JourneyHistoryEventType)
            else JourneyHistoryEventType(event_type)
        )
        tags = tuple(t.strip() for t in (detail_tags or ()) if t and t.strip())
        return cls(
            event_id=_require_non_empty(event_id, "event_id"),
            event_type=etype,
            occurred_at=occurred_at,
            detail_tags=tags,
            session_id=_optional_id(session_id),
            evidence_id=_optional_id(evidence_id),
            recommendation_id=_optional_id(recommendation_id),
        )


@dataclass(frozen=True)
class JourneyHistory:
    """Append-only chronological log for one Learning Journey.

    Attributes:
        entries: Ordered events (oldest first by convention).
    """

    entries: tuple[JourneyHistoryEntry, ...] = field(default_factory=tuple)

    @classmethod
    def empty(cls) -> JourneyHistory:
        """Create an empty history."""
        return cls(entries=())

    @classmethod
    def create(
        cls,
        entries: (
            list[JourneyHistoryEntry] | tuple[JourneyHistoryEntry, ...] | None
        ) = None,
    ) -> JourneyHistory:
        """Construct history from an ordered entry sequence."""
        return cls(entries=tuple(entries or ()))

    def append(self, entry: JourneyHistoryEntry) -> JourneyHistory:
        """Return a new history with ``entry`` appended (append-only)."""
        return JourneyHistory(entries=(*self.entries, entry))

    def filter_by_type(
        self, event_type: JourneyHistoryEventType
    ) -> tuple[JourneyHistoryEntry, ...]:
        """Return entries matching ``event_type`` in chronological order."""
        return tuple(e for e in self.entries if e.event_type == event_type)

    @property
    def length(self) -> int:
        """Number of recorded events."""
        return len(self.entries)


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _optional_id(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None
