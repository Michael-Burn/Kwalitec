"""Valid state transitions for Learning Session Runtime lifecycle.

Runtime phases: PLANNED → READY → ACTIVE → PAUSED → COMPLETED → ARCHIVED.

Domain ``SessionState`` transitions are applied in lockstep. Never mutates
Journey state and never completes a journey.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.learning_session.exceptions import (
    InvalidSessionState,
    SessionAlreadyArchived,
    SessionAlreadyCompleted,
)
from app.application.learning_session.runtime_phase import (
    RuntimePhase,
    RuntimeTransitionEvent,
    next_runtime_phase,
    phase_from_session_state,
)
from app.domain.learning_journey.entities.learning_session import LearningSession
from app.domain.learning_journey.value_objects.session_state import (
    SessionState,
    SessionTransitionEvent,
)


@dataclass(frozen=True)
class LifecycleResult:
    """Outcome of a lawful lifecycle transition."""

    session: LearningSession
    phase: RuntimePhase
    event: RuntimeTransitionEvent


class LifecycleManager:
    """Enforce lawful Learning Session Runtime phase transitions."""

    def prepare(
        self,
        session: LearningSession,
        *,
        phase: RuntimePhase,
    ) -> LifecycleResult:
        """PLANNED → READY (domain remains NOT_STARTED)."""
        self._reject_terminal(session, phase)
        nxt = next_runtime_phase(phase, RuntimeTransitionEvent.PREPARE)
        if nxt is None:
            raise InvalidSessionState(
                f"Cannot prepare session in phase {phase.value}"
            )
        if session.state != SessionState.NOT_STARTED:
            raise InvalidSessionState(
                "Prepare requires domain NOT_STARTED session"
            )
        return LifecycleResult(
            session=session,
            phase=nxt,
            event=RuntimeTransitionEvent.PREPARE,
        )

    def start(
        self,
        session: LearningSession,
        *,
        phase: RuntimePhase,
    ) -> LifecycleResult:
        """PLANNED/READY → ACTIVE (domain NOT_STARTED → ACTIVE)."""
        self._reject_terminal(session, phase)
        nxt = next_runtime_phase(phase, RuntimeTransitionEvent.START)
        if nxt is None:
            raise InvalidSessionState(
                f"Cannot start session in phase {phase.value}"
            )
        try:
            started = session.apply_transition(SessionTransitionEvent.START_SESSION)
        except ValueError as exc:
            raise InvalidSessionState(str(exc)) from exc
        return LifecycleResult(
            session=started,
            phase=nxt,
            event=RuntimeTransitionEvent.START,
        )

    def pause(
        self,
        session: LearningSession,
        *,
        phase: RuntimePhase,
    ) -> LifecycleResult:
        """ACTIVE → PAUSED."""
        self._reject_terminal(session, phase)
        nxt = next_runtime_phase(phase, RuntimeTransitionEvent.PAUSE)
        if nxt is None:
            raise InvalidSessionState(
                f"Cannot pause session in phase {phase.value}"
            )
        try:
            paused = session.apply_transition(SessionTransitionEvent.PAUSE_SESSION)
        except ValueError as exc:
            raise InvalidSessionState(str(exc)) from exc
        return LifecycleResult(
            session=paused,
            phase=nxt,
            event=RuntimeTransitionEvent.PAUSE,
        )

    def resume(
        self,
        session: LearningSession,
        *,
        phase: RuntimePhase,
    ) -> LifecycleResult:
        """PAUSED → ACTIVE."""
        self._reject_terminal(session, phase)
        nxt = next_runtime_phase(phase, RuntimeTransitionEvent.RESUME)
        if nxt is None:
            raise InvalidSessionState(
                f"Cannot resume session in phase {phase.value}"
            )
        try:
            resumed = session.apply_transition(SessionTransitionEvent.RESUME_SESSION)
        except ValueError as exc:
            raise InvalidSessionState(str(exc)) from exc
        return LifecycleResult(
            session=resumed,
            phase=nxt,
            event=RuntimeTransitionEvent.RESUME,
        )

    def complete(
        self,
        session: LearningSession,
        *,
        phase: RuntimePhase,
        actual_duration_minutes: int | None = None,
    ) -> LifecycleResult:
        """ACTIVE/PAUSED → COMPLETED (domain finish_session)."""
        self._reject_terminal(session, phase)
        nxt = next_runtime_phase(phase, RuntimeTransitionEvent.COMPLETE)
        if nxt is None:
            raise InvalidSessionState(
                f"Cannot complete session in phase {phase.value}"
            )
        try:
            finished = session.apply_transition(SessionTransitionEvent.FINISH_SESSION)
        except ValueError as exc:
            raise InvalidSessionState(str(exc)) from exc
        if actual_duration_minutes is not None:
            if actual_duration_minutes < 0:
                raise InvalidSessionState(
                    "actual_duration_minutes must be non-negative"
                )
            finished = LearningSession.create(
                finished.session_id,
                finished.journey_id,
                sequence_index=finished.sequence_index,
                state=finished.state,
                estimated_effort=finished.estimated_effort,
                objective_id=finished.objective_id,
                actual_duration_minutes=actual_duration_minutes,
                reflection=finished.reflection,
                evidence=list(finished.evidence),
            )
        return LifecycleResult(
            session=finished,
            phase=nxt,
            event=RuntimeTransitionEvent.COMPLETE,
        )

    def archive(
        self,
        session: LearningSession,
        *,
        phase: RuntimePhase,
    ) -> LifecycleResult:
        """COMPLETED → ARCHIVED (domain remains COMPLETED)."""
        if phase == RuntimePhase.ARCHIVED:
            raise SessionAlreadyArchived(
                f"Session {session.session_id} is already archived"
            )
        nxt = next_runtime_phase(phase, RuntimeTransitionEvent.ARCHIVE)
        if nxt is None:
            raise InvalidSessionState(
                f"Cannot archive session in phase {phase.value}"
            )
        if session.state != SessionState.COMPLETED:
            raise InvalidSessionState(
                "Archive requires a COMPLETED domain session"
            )
        return LifecycleResult(
            session=session,
            phase=nxt,
            event=RuntimeTransitionEvent.ARCHIVE,
        )

    @staticmethod
    def initial_phase() -> RuntimePhase:
        """Phase assigned to a newly created session."""
        return RuntimePhase.PLANNED

    @staticmethod
    def derive_phase(
        session: LearningSession,
        *,
        prepared: bool = False,
        archived: bool = False,
    ) -> RuntimePhase:
        """Derive runtime phase from domain state and runtime flags."""
        return phase_from_session_state(
            session.state,
            prepared=prepared,
            archived=archived,
        )

    @staticmethod
    def _reject_terminal(session: LearningSession, phase: RuntimePhase) -> None:
        if phase == RuntimePhase.ARCHIVED:
            raise SessionAlreadyArchived(
                f"Session {session.session_id} is archived"
            )
        if phase == RuntimePhase.COMPLETED or session.state == SessionState.COMPLETED:
            raise SessionAlreadyCompleted(
                f"Session {session.session_id} is already completed"
            )
        if session.state in {SessionState.ABANDONED, SessionState.SKIPPED}:
            raise InvalidSessionState(
                f"Session is {session.state.value}; lifecycle work is closed"
            )
