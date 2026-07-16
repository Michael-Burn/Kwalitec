"""IAHF-001 Study Session active-time timer (pure state machine).

Measures ACTIVE STUDY TIME as the sum of RUNNING intervals — not wall-clock
time since session open. Pause freezes elapsed; resume continues without
adding paused duration.

This module has no Flask / DB dependencies. Version 1 persists timer state
in the browser (localStorage); this Python model is the authoritative
algorithm for regression tests and a shared contract for the JS mirror.
"""

from __future__ import annotations

from dataclasses import dataclass

STATUS_NOT_STARTED = "NOT_STARTED"
STATUS_RUNNING = "RUNNING"
STATUS_PAUSED = "PAUSED"
STATUS_COMPLETED = "COMPLETED"

VALID_STATUSES = frozenset(
    {
        STATUS_NOT_STARTED,
        STATUS_RUNNING,
        STATUS_PAUSED,
        STATUS_COMPLETED,
    }
)


@dataclass(frozen=True)
class TimerState:
    """Immutable Study Session timer snapshot.

    Attributes:
        status: NOT_STARTED | RUNNING | PAUSED | COMPLETED.
        accumulated_seconds: Closed RUNNING intervals only.
        running_since_ms: Epoch ms when the current RUNNING segment began;
            None when not RUNNING.
    """

    status: str
    accumulated_seconds: int = 0
    running_since_ms: int | None = None

    def __post_init__(self) -> None:
        if self.status not in VALID_STATUSES:
            raise ValueError(f"Invalid timer status: {self.status}")
        if self.accumulated_seconds < 0:
            raise ValueError("accumulated_seconds must be >= 0")
        if self.status == STATUS_RUNNING and self.running_since_ms is None:
            raise ValueError("RUNNING requires running_since_ms")
        if self.status != STATUS_RUNNING and self.running_since_ms is not None:
            raise ValueError("running_since_ms only valid while RUNNING")


def new_timer() -> TimerState:
    """Return a NOT_STARTED timer."""
    return TimerState(status=STATUS_NOT_STARTED)


def start(state: TimerState, *, now_ms: int) -> TimerState:
    """Transition NOT_STARTED → RUNNING (idempotent if already RUNNING)."""
    if state.status == STATUS_COMPLETED:
        raise ValueError("Cannot start a COMPLETED timer")
    if state.status == STATUS_RUNNING:
        return state
    if state.status == STATUS_PAUSED:
        raise ValueError("Paused timer must resume, not start")
    return TimerState(
        status=STATUS_RUNNING,
        accumulated_seconds=0,
        running_since_ms=now_ms,
    )


def pause(state: TimerState, *, now_ms: int) -> TimerState:
    """Fold the open RUNNING segment and enter PAUSED."""
    if state.status == STATUS_PAUSED:
        return state
    if state.status != STATUS_RUNNING:
        raise ValueError(f"Cannot pause from {state.status}")
    assert state.running_since_ms is not None
    segment = max(0, (now_ms - state.running_since_ms) // 1000)
    return TimerState(
        status=STATUS_PAUSED,
        accumulated_seconds=state.accumulated_seconds + segment,
        running_since_ms=None,
    )


def resume(state: TimerState, *, now_ms: int) -> TimerState:
    """Resume a PAUSED timer without adding paused wall time."""
    if state.status == STATUS_RUNNING:
        return state
    if state.status != STATUS_PAUSED:
        raise ValueError(f"Cannot resume from {state.status}")
    return TimerState(
        status=STATUS_RUNNING,
        accumulated_seconds=state.accumulated_seconds,
        running_since_ms=now_ms,
    )


def elapsed_seconds(state: TimerState, *, now_ms: int) -> int:
    """Active study seconds at ``now_ms`` (excludes paused wall time)."""
    if state.status == STATUS_RUNNING:
        assert state.running_since_ms is not None
        open_segment = max(0, (now_ms - state.running_since_ms) // 1000)
        return state.accumulated_seconds + open_segment
    return state.accumulated_seconds


def finalize(state: TimerState, *, now_ms: int) -> TimerState:
    """Fold any open RUNNING segment and mark COMPLETED."""
    if state.status == STATUS_COMPLETED:
        return state
    if state.status == STATUS_NOT_STARTED:
        return TimerState(status=STATUS_COMPLETED, accumulated_seconds=0)
    if state.status == STATUS_RUNNING:
        paused = pause(state, now_ms=now_ms)
        return TimerState(
            status=STATUS_COMPLETED,
            accumulated_seconds=paused.accumulated_seconds,
        )
    return TimerState(
        status=STATUS_COMPLETED,
        accumulated_seconds=state.accumulated_seconds,
    )


def active_minutes_for_prefill(active_seconds: int) -> int | None:
    """Convert active seconds to optional practice duration minutes.

    Returns None when no active time was recorded; otherwise at least 1.
    """
    if active_seconds <= 0:
        return None
    minutes = (active_seconds + 59) // 60  # ceil
    return max(1, minutes)


def to_dict(state: TimerState) -> dict[str, int | str | None]:
    """Serialize timer state for localStorage / refresh restore."""
    return {
        "status": state.status,
        "accumulated_seconds": state.accumulated_seconds,
        "running_since_ms": state.running_since_ms,
    }


def from_dict(payload: dict) -> TimerState:
    """Restore timer state after page refresh (paused or running)."""
    status = str(payload.get("status") or STATUS_NOT_STARTED)
    accumulated = int(payload.get("accumulated_seconds") or 0)
    raw_since = payload.get("running_since_ms")
    running_since = int(raw_since) if raw_since is not None else None
    return TimerState(
        status=status,
        accumulated_seconds=accumulated,
        running_since_ms=running_since,
    )
