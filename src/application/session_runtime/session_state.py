"""Session lifecycle state for the Study Session Runtime.

``SessionState`` is the sole output of the runtime. It records where the
learner is in the guided session stages. Pause is an overlay flag — not a
separate educational stage.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class SessionStage(StrEnum):
    """Guided study-session progress stages (V3-004).

    Linear runner stages only. Educational content of each stage is decided
    upstream; the runtime never chooses what to study.
    """

    NOT_STARTED = "not_started"
    PREPARING = "preparing"
    LEARNING = "learning"
    WORKED_EXAMPLE = "worked_example"
    NOTES = "notes"
    REFLECTION = "reflection"
    COMPLETED = "completed"


@dataclass(frozen=True, slots=True)
class SessionState:
    """Immutable snapshot of session lifecycle posture.

    Attributes:
        session_id: Stable identity for this runtime instance.
        mission_title: Display title copied from the bound view model.
        stage: Current guided-session stage.
        paused: Whether the session is paused at the current stage.
        cancelled: Whether the session was cancelled (returns to NOT_STARTED).
        sequence: Number of applied lifecycle events (replay cursor).
        section_keys: Ordered section keys from the bound view model (metadata).
    """

    session_id: str
    mission_title: str
    stage: SessionStage
    paused: bool = False
    cancelled: bool = False
    sequence: int = 0
    section_keys: tuple[str, ...] = ()

    @property
    def is_terminal(self) -> bool:
        """True when no further educational lifecycle work is accepted."""
        return self.stage is SessionStage.COMPLETED

    @property
    def is_active(self) -> bool:
        """True when the session is in an in-progress, non-paused stage."""
        return (
            self.stage
            not in {SessionStage.NOT_STARTED, SessionStage.COMPLETED}
            and not self.paused
            and not self.cancelled
        )
