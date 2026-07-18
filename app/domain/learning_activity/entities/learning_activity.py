"""One educational activity step inside a Learning Session.

Activities advance session work; finishing an activity never completes the
session alone. Domain validation only — no persistence or Flask concerns.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.learning_activity.value_objects.activity_state import (
    ActivityState,
    ActivityTransitionEvent,
    is_terminal_activity_state,
    next_activity_state,
)
from app.domain.learning_activity.value_objects.activity_type import ActivityType


@dataclass(frozen=True)
class LearningActivity:
    """Bounded educational step inside a Learning Session activity sequence.

    Attributes:
        activity_id: Stable identity within the session sequence.
        session_id: Parent Learning Session identity.
        activity_type: Structural activity kind (not study content).
        sequence_index: 0-based ordering within the sequence.
        state: Activity lifecycle posture.
        title: Optional human-readable label (structural, not generated content).
        objective_id: Optional objective this activity addresses.
        metadata: Immutable structural tags (never educational AI payloads).
        evidence_ids: Append-only evidence identifiers routed to this activity.
        reflection_ids: Append-only reflection identifiers associated here.
    """

    activity_id: str
    session_id: str
    activity_type: ActivityType
    sequence_index: int
    state: ActivityState
    title: str | None = None
    objective_id: str | None = None
    metadata: tuple[str, ...] = field(default_factory=tuple)
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    reflection_ids: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        activity_id: str,
        session_id: str,
        activity_type: ActivityType | str,
        *,
        sequence_index: int = 0,
        state: ActivityState | str = ActivityState.NOT_STARTED,
        title: str | None = None,
        objective_id: str | None = None,
        metadata: list[str] | tuple[str, ...] | None = None,
        evidence_ids: list[str] | tuple[str, ...] | None = None,
        reflection_ids: list[str] | tuple[str, ...] | None = None,
    ) -> LearningActivity:
        """Construct a LearningActivity after validating invariants.

        Raises:
            ValueError: On empty identities or negative sequence_index.
        """
        aid = _require_non_empty(activity_id, "activity_id")
        sid = _require_non_empty(session_id, "session_id")
        if sequence_index < 0:
            raise ValueError("sequence_index must be non-negative")
        type_value = ActivityType.resolve(activity_type)
        state_value = (
            state if isinstance(state, ActivityState) else ActivityState(state)
        )
        return cls(
            activity_id=aid,
            session_id=sid,
            activity_type=type_value,
            sequence_index=sequence_index,
            state=state_value,
            title=_optional_text(title),
            objective_id=_optional_id(objective_id),
            metadata=tuple(metadata or ()),
            evidence_ids=tuple(evidence_ids or ()),
            reflection_ids=tuple(reflection_ids or ()),
        )

    def apply_transition(
        self, event: ActivityTransitionEvent
    ) -> LearningActivity:
        """Return a new activity after a lawful state transition.

        Raises:
            ValueError: When the transition is not lawful.
        """
        nxt = next_activity_state(self.state, event)
        if nxt is None:
            raise ValueError(
                f"invalid activity transition: {self.state.value} + {event.value}"
            )
        return LearningActivity(
            activity_id=self.activity_id,
            session_id=self.session_id,
            activity_type=self.activity_type,
            sequence_index=self.sequence_index,
            state=nxt,
            title=self.title,
            objective_id=self.objective_id,
            metadata=self.metadata,
            evidence_ids=self.evidence_ids,
            reflection_ids=self.reflection_ids,
        )

    def with_evidence(self, evidence_id: str) -> LearningActivity:
        """Append an evidence identifier (append-only, de-duplicated)."""
        eid = _require_non_empty(evidence_id, "evidence_id")
        if eid in self.evidence_ids:
            return self
        return LearningActivity(
            activity_id=self.activity_id,
            session_id=self.session_id,
            activity_type=self.activity_type,
            sequence_index=self.sequence_index,
            state=self.state,
            title=self.title,
            objective_id=self.objective_id,
            metadata=self.metadata,
            evidence_ids=(*self.evidence_ids, eid),
            reflection_ids=self.reflection_ids,
        )

    def with_reflection(self, reflection_id: str) -> LearningActivity:
        """Append a reflection identifier (append-only, de-duplicated)."""
        rid = _require_non_empty(reflection_id, "reflection_id")
        if rid in self.reflection_ids:
            return self
        return LearningActivity(
            activity_id=self.activity_id,
            session_id=self.session_id,
            activity_type=self.activity_type,
            sequence_index=self.sequence_index,
            state=self.state,
            title=self.title,
            objective_id=self.objective_id,
            metadata=self.metadata,
            evidence_ids=self.evidence_ids,
            reflection_ids=(*self.reflection_ids, rid),
        )

    @property
    def is_terminal(self) -> bool:
        """True when the activity cannot resume educational work."""
        return is_terminal_activity_state(self.state)

    @property
    def is_active(self) -> bool:
        """True when the activity is currently ACTIVE."""
        return self.state == ActivityState.ACTIVE


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


def _optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None
