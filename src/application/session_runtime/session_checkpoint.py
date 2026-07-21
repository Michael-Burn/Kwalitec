"""Immutable checkpoints for Study Session Runtime replay and resume.

A checkpoint captures state plus the event log up to a sequence point.
Checkpoints never persist themselves — callers own any storage.
"""

from __future__ import annotations

from dataclasses import dataclass

from application.session_runtime.session_event import SessionEvent
from application.session_runtime.session_state import SessionState


@dataclass(frozen=True, slots=True)
class SessionCheckpoint:
    """Point-in-time capture of runtime state and events.

    Attributes:
        state: Session state at the checkpoint.
        events: Immutable event log up to and including ``state.sequence``.
    """

    state: SessionState
    events: tuple[SessionEvent, ...] = ()

    def __post_init__(self) -> None:
        if len(self.events) != self.state.sequence:
            raise ValueError(
                "checkpoint events length must equal state.sequence "
                f"({len(self.events)} != {self.state.sequence})"
            )
        if self.events and self.events[-1].sequence != self.state.sequence:
            raise ValueError(
                "last event sequence must match state.sequence"
            )
