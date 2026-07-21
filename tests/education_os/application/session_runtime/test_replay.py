"""Replay and checkpoint correctness for Study Session Runtime (V3-004)."""

from __future__ import annotations

import pytest

from application.session_runtime import (
    InvalidSessionTransitionError,
    SessionCheckpoint,
    SessionEvent,
    SessionEventKind,
    SessionRuntime,
    SessionStage,
    SessionState,
)
from tests.education_os.application.session_runtime import make_view_model


def _walk_to_notes(runtime: SessionRuntime) -> None:
    runtime.start()
    runtime.advance()
    runtime.advance()
    runtime.advance()
    assert runtime.state.stage is SessionStage.NOTES


def test_replay_rebuilds_identical_state() -> None:
    view = make_view_model()
    original = SessionRuntime(view, session_id="sess-replay")
    original.start()
    original.advance()
    original.pause()
    original.resume()
    original.advance()
    events = original.events

    replayed = SessionRuntime.replay(view, events, session_id="sess-replay")

    assert replayed.state == original.state
    assert replayed.events == original.events
    assert replayed.state.stage is SessionStage.WORKED_EXAMPLE
    assert replayed.state.paused is False


def test_replay_full_completion() -> None:
    view = make_view_model()
    original = SessionRuntime(view, session_id="sess-done")
    original.start()
    for _ in range(4):
        original.advance()
    original.complete()

    replayed = SessionRuntime.replay(
        view, original.events, session_id="sess-done"
    )
    assert replayed.state.stage is SessionStage.COMPLETED
    assert replayed.state.sequence == original.state.sequence


def test_checkpoint_round_trip() -> None:
    runtime = SessionRuntime(make_view_model(), session_id="sess-1")
    _walk_to_notes(runtime)
    runtime.pause()
    checkpoint = runtime.checkpoint()

    assert isinstance(checkpoint, SessionCheckpoint)
    assert checkpoint.state.paused is True
    assert len(checkpoint.events) == checkpoint.state.sequence

    other = SessionRuntime(make_view_model(), session_id="sess-1")
    restored = other.restore(checkpoint)

    assert restored == checkpoint.state
    assert other.events == checkpoint.events
    other.resume()
    other.advance()
    assert other.state.stage is SessionStage.REFLECTION


def test_replay_detects_corrupt_event_log() -> None:
    view = make_view_model()
    runtime = SessionRuntime(view, session_id="sess-1")
    runtime.start()
    events = list(runtime.events)
    corrupt = SessionEvent(
        kind=SessionEventKind.ADVANCED,
        sequence=2,
        from_stage=SessionStage.PREPARING.value,
        to_stage=SessionStage.NOTES.value,  # wrong target
        paused_after=False,
        cancelled_after=False,
    )
    events.append(corrupt)

    with pytest.raises(InvalidSessionTransitionError, match="diverged"):
        SessionRuntime.replay(view, events, session_id="sess-1")


def test_checkpoint_invariant_on_event_length() -> None:
    state = SessionState(
        session_id="x",
        mission_title="Mission",
        stage=SessionStage.PREPARING,
        sequence=1,
    )
    with pytest.raises(ValueError, match="sequence"):
        SessionCheckpoint(state=state, events=())
