"""One intentional learning event within a Learning Journey.

Sessions advance the journey; finishing a session never completes the journey
alone. Domain validation only — no persistence or Flask concerns.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.learning_journey.entities.journey_evidence import JourneyEvidence
from app.domain.learning_journey.entities.journey_reflection import (
    JourneyReflection,
    ReflectionPosture,
)
from app.domain.learning_journey.value_objects.effort_estimate import EffortEstimate
from app.domain.learning_journey.value_objects.session_state import (
    SessionState,
    SessionTransitionEvent,
    is_terminal_session_state,
    next_session_state,
)


@dataclass(frozen=True)
class LearningSession:
    """Bounded intentional study work inside a Learning Journey.

    Attributes:
        session_id: Stable identity.
        journey_id: Parent journey.
        sequence_index: Ordering within the journey (0-based).
        state: Session lifecycle posture.
        estimated_effort: Planned educational effort band.
        objective_id: Optional primary objective for this session.
        actual_duration_minutes: Observed duration when known (not effort alone).
        reflection: Reflection artefact (pending or captured).
        evidence: Session-scoped JourneyEvidence attributions.
    """

    session_id: str
    journey_id: str
    sequence_index: int
    state: SessionState
    estimated_effort: EffortEstimate
    objective_id: str | None = None
    actual_duration_minutes: int | None = None
    reflection: JourneyReflection | None = None
    evidence: tuple[JourneyEvidence, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        session_id: str,
        journey_id: str,
        *,
        sequence_index: int = 0,
        state: SessionState | str = SessionState.NOT_STARTED,
        estimated_effort: EffortEstimate | str = EffortEstimate.MEDIUM,
        objective_id: str | None = None,
        actual_duration_minutes: int | None = None,
        reflection: JourneyReflection | None = None,
        evidence: list[JourneyEvidence] | tuple[JourneyEvidence, ...] | None = None,
    ) -> LearningSession:
        """Construct a LearningSession after validating invariants.

        Raises:
            ValueError: On empty identities, negative sequence/duration, or
                reflection/session identity mismatch.
        """
        sid = _require_non_empty(session_id, "session_id")
        jid = _require_non_empty(journey_id, "journey_id")
        if sequence_index < 0:
            raise ValueError("sequence_index must be non-negative")
        if actual_duration_minutes is not None and actual_duration_minutes < 0:
            raise ValueError("actual_duration_minutes must be non-negative")
        state_value = (
            state if isinstance(state, SessionState) else SessionState(state)
        )
        effort = (
            estimated_effort
            if isinstance(estimated_effort, EffortEstimate)
            else EffortEstimate(estimated_effort)
        )
        evidence_tuple = tuple(evidence or ())
        for item in evidence_tuple:
            if item.session_id is not None and item.session_id != sid:
                raise ValueError("evidence session_id must match session")
            if item.journey_id != jid:
                raise ValueError("evidence journey_id must match session journey")
        if reflection is not None:
            if reflection.session_id != sid:
                raise ValueError("reflection session_id must match session")
            if reflection.journey_id != jid:
                raise ValueError("reflection journey_id must match session journey")
        return cls(
            session_id=sid,
            journey_id=jid,
            sequence_index=sequence_index,
            state=state_value,
            estimated_effort=effort,
            objective_id=_optional_id(objective_id),
            actual_duration_minutes=actual_duration_minutes,
            reflection=reflection,
            evidence=evidence_tuple,
        )

    def apply_transition(self, event: SessionTransitionEvent) -> LearningSession:
        """Return a new session after a lawful state transition.

        Raises:
            ValueError: When the transition is not lawful.
        """
        nxt = next_session_state(self.state, event)
        if nxt is None:
            raise ValueError(
                f"invalid session transition: {self.state.value} + {event.value}"
            )
        reflection = self.reflection
        if event == SessionTransitionEvent.FINISH_SESSION and reflection is None:
            # Reflection becomes owed; concrete pending artefact is created by
            # session engines (V2-005). Domain marks educational expectation
            # via absence until a PENDING reflection is attached.
            reflection = None
        return LearningSession(
            session_id=self.session_id,
            journey_id=self.journey_id,
            sequence_index=self.sequence_index,
            state=nxt,
            estimated_effort=self.estimated_effort,
            objective_id=self.objective_id,
            actual_duration_minutes=self.actual_duration_minutes,
            reflection=reflection,
            evidence=self.evidence,
        )

    def with_reflection(self, reflection: JourneyReflection) -> LearningSession:
        """Attach or replace the session reflection.

        Raises:
            ValueError: On identity mismatch, or reflection on non-completed
                session when posture is CAPTURED/PENDING.
        """
        if reflection.session_id != self.session_id:
            raise ValueError("reflection session_id must match session")
        if reflection.journey_id != self.journey_id:
            raise ValueError("reflection journey_id must match session journey")
        if (
            reflection.posture
            in {ReflectionPosture.PENDING, ReflectionPosture.CAPTURED}
            and self.state != SessionState.COMPLETED
        ):
            raise ValueError(
                "pending/captured reflection requires COMPLETED session"
            )
        return LearningSession(
            session_id=self.session_id,
            journey_id=self.journey_id,
            sequence_index=self.sequence_index,
            state=self.state,
            estimated_effort=self.estimated_effort,
            objective_id=self.objective_id,
            actual_duration_minutes=self.actual_duration_minutes,
            reflection=reflection,
            evidence=self.evidence,
        )

    def with_evidence(self, evidence: JourneyEvidence) -> LearningSession:
        """Append session-scoped evidence (append-only)."""
        if evidence.journey_id != self.journey_id:
            raise ValueError("evidence journey_id must match session journey")
        if evidence.session_id is not None and evidence.session_id != self.session_id:
            raise ValueError("evidence session_id must match session")
        return LearningSession(
            session_id=self.session_id,
            journey_id=self.journey_id,
            sequence_index=self.sequence_index,
            state=self.state,
            estimated_effort=self.estimated_effort,
            objective_id=self.objective_id,
            actual_duration_minutes=self.actual_duration_minutes,
            reflection=self.reflection,
            evidence=(*self.evidence, evidence),
        )

    @property
    def is_terminal(self) -> bool:
        """True when the session cannot resume educational work."""
        return is_terminal_session_state(self.state)

    @property
    def reflection_captured(self) -> bool:
        """True when a CAPTURED reflection is attached."""
        return (
            self.reflection is not None
            and self.reflection.posture == ReflectionPosture.CAPTURED
        )


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
