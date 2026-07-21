"""Invalid transition coverage for Study Session Runtime (V3-004)."""

from __future__ import annotations

import pytest

from application.session_runtime import (
    InvalidSessionTransitionError,
    SessionRuntime,
    SessionStage,
)
from tests.education_os.application.session_runtime import make_view_model


@pytest.mark.parametrize(
    "operation",
    ["advance", "resume", "complete", "cancel"],
)
def test_invalid_ops_from_not_started(operation: str) -> None:
    runtime = SessionRuntime(make_view_model(), session_id="sess-1")
    method = getattr(runtime, operation)

    with pytest.raises(InvalidSessionTransitionError):
        method()


def test_cannot_start_twice() -> None:
    runtime = SessionRuntime(make_view_model(), session_id="sess-1")
    runtime.start()

    with pytest.raises(InvalidSessionTransitionError, match="start"):
        runtime.start()


def test_cannot_operate_on_cancelled_without_restart() -> None:
    runtime = SessionRuntime(make_view_model(), session_id="sess-1")
    runtime.start()
    runtime.cancel()

    with pytest.raises(InvalidSessionTransitionError):
        runtime.advance()
    with pytest.raises(InvalidSessionTransitionError, match="already cancelled"):
        runtime.cancel()


def test_checkpoint_rejects_mismatched_session() -> None:
    first = SessionRuntime(make_view_model(), session_id="a")
    first.start()
    checkpoint = first.checkpoint()

    second = SessionRuntime(make_view_model(), session_id="b")
    with pytest.raises(Exception, match="session_id"):
        second.restore(checkpoint)


def test_state_remains_unchanged_after_invalid_transition() -> None:
    runtime = SessionRuntime(make_view_model(), session_id="sess-1")
    runtime.start()
    before = runtime.state
    before_events = runtime.events

    with pytest.raises(InvalidSessionTransitionError):
        runtime.start()

    assert runtime.state == before
    assert runtime.events == before_events
    assert runtime.state.stage is SessionStage.PREPARING
