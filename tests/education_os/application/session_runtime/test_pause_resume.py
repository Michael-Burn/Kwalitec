"""Pause / resume coverage for Study Session Runtime (V3-004)."""

from __future__ import annotations

import pytest

from application.session_runtime import (
    InvalidSessionTransitionError,
    SessionRuntime,
    SessionStage,
)
from tests.education_os.application.session_runtime import make_view_model


def test_pause_and_resume_preserve_stage() -> None:
    runtime = SessionRuntime(make_view_model(), session_id="sess-1")
    runtime.start()
    runtime.advance()
    paused = runtime.pause()

    assert paused.stage is SessionStage.LEARNING
    assert paused.paused is True
    assert paused.is_active is False

    resumed = runtime.resume()
    assert resumed.stage is SessionStage.LEARNING
    assert resumed.paused is False
    assert resumed.is_active is True


def test_cannot_advance_while_paused() -> None:
    runtime = SessionRuntime(make_view_model(), session_id="sess-1")
    runtime.start()
    runtime.pause()

    with pytest.raises(InvalidSessionTransitionError, match="paused"):
        runtime.advance()


def test_cannot_complete_while_paused() -> None:
    runtime = SessionRuntime(make_view_model(), session_id="sess-1")
    runtime.start()
    for _ in range(4):
        runtime.advance()
    runtime.pause()

    with pytest.raises(InvalidSessionTransitionError, match="paused"):
        runtime.complete()


def test_cannot_double_pause_or_resume() -> None:
    runtime = SessionRuntime(make_view_model(), session_id="sess-1")
    runtime.start()
    runtime.pause()

    with pytest.raises(InvalidSessionTransitionError, match="already paused"):
        runtime.pause()

    runtime.resume()
    with pytest.raises(InvalidSessionTransitionError, match="not paused"):
        runtime.resume()


def test_cannot_pause_before_start() -> None:
    runtime = SessionRuntime(make_view_model(), session_id="sess-1")

    with pytest.raises(InvalidSessionTransitionError):
        runtime.pause()
