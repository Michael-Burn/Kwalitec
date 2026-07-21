"""Study Session Runtime — public lifecycle facade.

Binds a ``StudySessionViewModel`` and advances through fixed guided-session
stages. Deterministic, replayable, and free of educational intelligence.
"""

from __future__ import annotations

from dataclasses import replace

from application.errors import ApplicationError
from application.session_runtime.session_actions import (
    ACTIVE_STAGES,
    SessionAction,
    next_stage,
)
from application.session_runtime.session_checkpoint import SessionCheckpoint
from application.session_runtime.session_event import (
    SessionEvent,
    SessionEventKind,
)
from application.session_runtime.session_state import SessionStage, SessionState
from presentation.study_session.session_view_model import StudySessionViewModel

_ACTION_TO_KIND: dict[SessionAction, SessionEventKind] = {
    SessionAction.START: SessionEventKind.STARTED,
    SessionAction.ADVANCE: SessionEventKind.ADVANCED,
    SessionAction.PAUSE: SessionEventKind.PAUSED,
    SessionAction.RESUME: SessionEventKind.RESUMED,
    SessionAction.COMPLETE: SessionEventKind.COMPLETED,
    SessionAction.CANCEL: SessionEventKind.CANCELLED,
}


class SessionRuntimeError(ApplicationError):
    """Base error for Study Session Runtime failures."""


class InvalidSessionTransitionError(SessionRuntimeError):
    """Raised when a lifecycle operation is unlawful for the current state."""


class SessionRuntime:
    """Execute guided study-session lifecycle for one mission.

    Input: ``StudySessionViewModel`` (presentation; already-decided content).
    Output: ``SessionState`` (lifecycle posture only).

    The runtime never diagnoses, recommends, persists, or calls AI.
    """

    def __init__(
        self,
        view_model: StudySessionViewModel,
        *,
        session_id: str | None = None,
    ) -> None:
        if view_model is None:
            raise SessionRuntimeError("view_model is required")
        mission_title = _mission_title(view_model)
        section_keys = tuple(
            section.key for section in (view_model.sections or ())
        )
        identity = (session_id or "").strip() or _default_session_id(
            mission_title
        )
        self._view_model = view_model
        self._events: list[SessionEvent] = []
        self._state = SessionState(
            session_id=identity,
            mission_title=mission_title,
            stage=SessionStage.NOT_STARTED,
            paused=False,
            cancelled=False,
            sequence=0,
            section_keys=section_keys,
        )

    @property
    def view_model(self) -> StudySessionViewModel:
        """Bound study-session view model (read-only reference)."""
        return self._view_model

    @property
    def state(self) -> SessionState:
        """Current immutable session state."""
        return self._state

    @property
    def events(self) -> tuple[SessionEvent, ...]:
        """Immutable copy of the append-only event log."""
        return tuple(self._events)

    def start(self) -> SessionState:
        """NOT_STARTED → PREPARING."""
        return self._apply(SessionAction.START)

    def advance(self) -> SessionState:
        """Advance one guided stage (PREPARING … → REFLECTION)."""
        return self._apply(SessionAction.ADVANCE)

    def pause(self) -> SessionState:
        """Pause at the current active stage."""
        return self._apply(SessionAction.PAUSE)

    def resume(self) -> SessionState:
        """Resume a paused session at the same stage."""
        return self._apply(SessionAction.RESUME)

    def complete(self) -> SessionState:
        """REFLECTION → COMPLETED."""
        return self._apply(SessionAction.COMPLETE)

    def cancel(self) -> SessionState:
        """Abandon the session and return to NOT_STARTED."""
        return self._apply(SessionAction.CANCEL)

    def checkpoint(self) -> SessionCheckpoint:
        """Capture current state and event log for replay/resume."""
        return SessionCheckpoint(state=self._state, events=self.events)

    def restore(self, checkpoint: SessionCheckpoint) -> SessionState:
        """Replace runtime posture from a checkpoint (same session identity)."""
        if checkpoint is None:
            raise SessionRuntimeError("checkpoint is required")
        if checkpoint.state.session_id != self._state.session_id:
            raise SessionRuntimeError(
                "checkpoint session_id does not match runtime "
                f"({checkpoint.state.session_id!r} != "
                f"{self._state.session_id!r})"
            )
        self._state = checkpoint.state
        self._events = list(checkpoint.events)
        return self._state

    @classmethod
    def replay(
        cls,
        view_model: StudySessionViewModel,
        events: tuple[SessionEvent, ...] | list[SessionEvent],
        *,
        session_id: str | None = None,
    ) -> SessionRuntime:
        """Build a runtime and re-apply events deterministically.

        Events are validated against lawful transitions; corrupt logs raise
        ``InvalidSessionTransitionError``.
        """
        runtime = cls(view_model, session_id=session_id)
        for event in events:
            action = _kind_to_action(event.kind)
            runtime._apply(action)
            applied = runtime._events[-1]
            if (
                applied.kind != event.kind
                or applied.from_stage != event.from_stage
                or applied.to_stage != event.to_stage
                or applied.paused_after != event.paused_after
                or applied.cancelled_after != event.cancelled_after
            ):
                raise InvalidSessionTransitionError(
                    "replay diverged from recorded event "
                    f"at sequence {event.sequence}"
                )
        return runtime

    def _apply(self, action: SessionAction) -> SessionState:
        current = self._state
        kind = _ACTION_TO_KIND[action]
        nxt_stage, paused, cancelled = _transition(current, action)
        event = SessionEvent(
            kind=kind,
            sequence=current.sequence + 1,
            from_stage=current.stage.value,
            to_stage=nxt_stage.value,
            paused_after=paused,
            cancelled_after=cancelled,
        )
        self._events.append(event)
        self._state = replace(
            current,
            stage=nxt_stage,
            paused=paused,
            cancelled=cancelled,
            sequence=event.sequence,
        )
        return self._state


def _transition(
    state: SessionState,
    action: SessionAction,
) -> tuple[SessionStage, bool, bool]:
    """Return (next_stage, paused, cancelled) or raise."""
    stage = state.stage
    paused = state.paused
    cancelled = state.cancelled

    if action is SessionAction.START:
        if stage is not SessionStage.NOT_STARTED:
            raise InvalidSessionTransitionError(
                f"Cannot start session in stage {stage.value}"
            )
        if paused:
            raise InvalidSessionTransitionError("Cannot start a paused session")
        return SessionStage.PREPARING, False, False

    if action is SessionAction.CANCEL:
        if cancelled:
            raise InvalidSessionTransitionError(
                "Session is already cancelled"
            )
        if stage is SessionStage.COMPLETED:
            raise InvalidSessionTransitionError(
                "Cannot cancel a completed session"
            )
        if stage is SessionStage.NOT_STARTED:
            raise InvalidSessionTransitionError(
                "Cannot cancel a session that has not started"
            )
        return SessionStage.NOT_STARTED, False, True

    if cancelled:
        raise InvalidSessionTransitionError(
            "Cannot operate on a cancelled session; call start() to begin again"
        )

    if stage is SessionStage.COMPLETED:
        raise InvalidSessionTransitionError(
            f"Cannot {action.value} a completed session"
        )

    if action is SessionAction.PAUSE:
        if paused:
            raise InvalidSessionTransitionError("Session is already paused")
        if stage not in ACTIVE_STAGES:
            raise InvalidSessionTransitionError(
                f"Cannot pause session in stage {stage.value}"
            )
        return stage, True, False

    if action is SessionAction.RESUME:
        if not paused:
            raise InvalidSessionTransitionError("Session is not paused")
        if stage not in ACTIVE_STAGES:
            raise InvalidSessionTransitionError(
                f"Cannot resume session in stage {stage.value}"
            )
        return stage, False, False

    if paused:
        raise InvalidSessionTransitionError(
            f"Cannot {action.value} while session is paused"
        )

    if action is SessionAction.ADVANCE:
        if stage is SessionStage.REFLECTION:
            raise InvalidSessionTransitionError(
                "Cannot advance from reflection; call complete()"
            )
        nxt = next_stage(stage)
        if nxt is None or nxt is SessionStage.COMPLETED:
            raise InvalidSessionTransitionError(
                f"Cannot advance from stage {stage.value}"
            )
        if stage is SessionStage.NOT_STARTED:
            raise InvalidSessionTransitionError(
                "Cannot advance before start(); call start() first"
            )
        return nxt, False, False

    if action is SessionAction.COMPLETE:
        if stage is not SessionStage.REFLECTION:
            raise InvalidSessionTransitionError(
                "complete() requires reflection stage "
                f"(current: {stage.value})"
            )
        return SessionStage.COMPLETED, False, False

    raise InvalidSessionTransitionError(f"Unknown action {action.value}")


def _kind_to_action(kind: SessionEventKind) -> SessionAction:
    for action, mapped in _ACTION_TO_KIND.items():
        if mapped is kind:
            return action
    raise InvalidSessionTransitionError(f"Unknown event kind {kind.value}")


def _mission_title(view_model: StudySessionViewModel) -> str:
    card = getattr(view_model, "mission_card", None)
    title = (getattr(card, "title", None) or "").strip()
    if title:
        return title
    header = getattr(view_model, "header", None)
    title = (getattr(header, "title", None) or "").strip()
    return title or "Study Session"


def _default_session_id(mission_title: str) -> str:
    slug = "".join(
        ch.lower() if ch.isalnum() else "-" for ch in mission_title
    ).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return f"session:{slug or 'study'}"
