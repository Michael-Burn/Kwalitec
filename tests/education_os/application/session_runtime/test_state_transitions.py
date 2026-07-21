"""State transition coverage for Study Session Runtime (V3-004)."""

from __future__ import annotations

import pytest

from application.session_runtime import (
    SessionRuntime,
    SessionStage,
)
from tests.education_os.application.session_runtime import make_view_model

# Happy-path stage walk after start().
_ADVANCE_PATH: tuple[SessionStage, ...] = (
    SessionStage.PREPARING,
    SessionStage.LEARNING,
    SessionStage.WORKED_EXAMPLE,
    SessionStage.NOTES,
    SessionStage.REFLECTION,
)


def test_initial_state_is_not_started() -> None:
    runtime = SessionRuntime(make_view_model(), session_id="sess-1")
    state = runtime.state

    assert state.session_id == "sess-1"
    assert state.stage is SessionStage.NOT_STARTED
    assert state.paused is False
    assert state.cancelled is False
    assert state.sequence == 0
    assert state.section_keys
    assert state.mission_title


def test_start_moves_to_preparing() -> None:
    runtime = SessionRuntime(make_view_model(), session_id="sess-1")
    state = runtime.start()

    assert state.stage is SessionStage.PREPARING
    assert state.sequence == 1
    assert state.is_active is True


@pytest.mark.parametrize(
    ("advances", "expected"),
    [
        (1, SessionStage.LEARNING),
        (2, SessionStage.WORKED_EXAMPLE),
        (3, SessionStage.NOTES),
        (4, SessionStage.REFLECTION),
    ],
)
def test_advance_walks_stages(advances: int, expected: SessionStage) -> None:
    runtime = SessionRuntime(make_view_model(), session_id="sess-1")
    runtime.start()
    state = runtime.state
    for _ in range(advances):
        state = runtime.advance()

    assert state.stage is expected
    assert state.sequence == advances + 1


def test_full_happy_path_to_completed() -> None:
    runtime = SessionRuntime(make_view_model(), session_id="sess-1")
    runtime.start()
    for expected in _ADVANCE_PATH[1:]:
        state = runtime.advance()
        assert state.stage is expected

    state = runtime.complete()
    assert state.stage is SessionStage.COMPLETED
    assert state.is_terminal is True
    assert state.is_active is False
    assert state.sequence == 6


def test_cancel_returns_to_not_started() -> None:
    runtime = SessionRuntime(make_view_model(), session_id="sess-1")
    runtime.start()
    runtime.advance()
    state = runtime.cancel()

    assert state.stage is SessionStage.NOT_STARTED
    assert state.cancelled is True
    assert state.paused is False


def test_start_after_cancel_clears_cancelled() -> None:
    runtime = SessionRuntime(make_view_model(), session_id="sess-1")
    runtime.start()
    runtime.cancel()
    state = runtime.start()

    assert state.stage is SessionStage.PREPARING
    assert state.cancelled is False


def test_events_are_immutable_and_ordered() -> None:
    runtime = SessionRuntime(make_view_model(), session_id="sess-1")
    runtime.start()
    runtime.advance()
    events = runtime.events

    assert len(events) == 2
    assert events[0].sequence == 1
    assert events[1].sequence == 2
    assert events[0].from_stage == SessionStage.NOT_STARTED.value
    assert events[0].to_stage == SessionStage.PREPARING.value
    assert events[1].to_stage == SessionStage.LEARNING.value
    with pytest.raises(AttributeError):
        events[0].kind = events[0].kind  # type: ignore[misc]
