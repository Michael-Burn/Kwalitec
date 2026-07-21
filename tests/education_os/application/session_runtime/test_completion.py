"""Completion coverage for Study Session Runtime (V3-004)."""

from __future__ import annotations

import pytest

from application.session_runtime import (
    InvalidSessionTransitionError,
    SessionRuntime,
    SessionStage,
)
from tests.education_os.application.session_runtime import make_view_model


def _to_reflection(runtime: SessionRuntime) -> None:
    runtime.start()
    for _ in range(4):
        runtime.advance()
    assert runtime.state.stage is SessionStage.REFLECTION


def test_complete_from_reflection() -> None:
    runtime = SessionRuntime(make_view_model(), session_id="sess-1")
    _to_reflection(runtime)
    state = runtime.complete()

    assert state.stage is SessionStage.COMPLETED
    assert state.is_terminal is True
    assert state.paused is False
    assert state.cancelled is False


def test_complete_rejects_earlier_stages() -> None:
    runtime = SessionRuntime(make_view_model(), session_id="sess-1")
    runtime.start()

    with pytest.raises(InvalidSessionTransitionError, match="reflection"):
        runtime.complete()


def test_cannot_complete_twice() -> None:
    runtime = SessionRuntime(make_view_model(), session_id="sess-1")
    _to_reflection(runtime)
    runtime.complete()

    with pytest.raises(InvalidSessionTransitionError, match="completed"):
        runtime.complete()


def test_cannot_cancel_completed_session() -> None:
    runtime = SessionRuntime(make_view_model(), session_id="sess-1")
    _to_reflection(runtime)
    runtime.complete()

    with pytest.raises(InvalidSessionTransitionError, match="completed"):
        runtime.cancel()


def test_cannot_advance_from_reflection() -> None:
    runtime = SessionRuntime(make_view_model(), session_id="sess-1")
    _to_reflection(runtime)

    with pytest.raises(InvalidSessionTransitionError, match="complete"):
        runtime.advance()
