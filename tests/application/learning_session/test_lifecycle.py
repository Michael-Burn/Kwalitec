"""Tests for LifecycleManager."""

from __future__ import annotations

import pytest

from app.application.learning_session.exceptions import (
    InvalidSessionState,
    SessionAlreadyArchived,
    SessionAlreadyCompleted,
)
from app.application.learning_session.lifecycle_manager import LifecycleManager
from app.application.learning_session.runtime_phase import RuntimePhase
from app.domain.learning_journey.value_objects.session_state import SessionState
from tests.application.learning_session.helpers import make_session


class TestLifecycleManager:
    def setup_method(self):
        self.lifecycle = LifecycleManager()

    def test_initial_phase_planned(self):
        assert self.lifecycle.initial_phase() == RuntimePhase.PLANNED

    def test_prepare_planned_to_ready(self):
        session = make_session()
        result = self.lifecycle.prepare(session, phase=RuntimePhase.PLANNED)
        assert result.phase == RuntimePhase.READY
        assert result.session.state == SessionState.NOT_STARTED

    def test_prepare_rejects_ready(self):
        with pytest.raises(InvalidSessionState):
            self.lifecycle.prepare(make_session(), phase=RuntimePhase.READY)

    def test_start_from_planned(self):
        result = self.lifecycle.start(make_session(), phase=RuntimePhase.PLANNED)
        assert result.phase == RuntimePhase.ACTIVE
        assert result.session.state == SessionState.ACTIVE

    def test_start_from_ready(self):
        result = self.lifecycle.start(make_session(), phase=RuntimePhase.READY)
        assert result.phase == RuntimePhase.ACTIVE

    def test_start_rejects_active(self):
        with pytest.raises(InvalidSessionState):
            self.lifecycle.start(
                make_session(state=SessionState.ACTIVE),
                phase=RuntimePhase.ACTIVE,
            )

    def test_pause_active(self):
        result = self.lifecycle.pause(
            make_session(state=SessionState.ACTIVE),
            phase=RuntimePhase.ACTIVE,
        )
        assert result.phase == RuntimePhase.PAUSED
        assert result.session.state == SessionState.PAUSED

    def test_pause_rejects_planned(self):
        with pytest.raises(InvalidSessionState):
            self.lifecycle.pause(make_session(), phase=RuntimePhase.PLANNED)

    def test_resume_paused(self):
        result = self.lifecycle.resume(
            make_session(state=SessionState.PAUSED),
            phase=RuntimePhase.PAUSED,
        )
        assert result.phase == RuntimePhase.ACTIVE
        assert result.session.state == SessionState.ACTIVE

    def test_resume_rejects_active(self):
        with pytest.raises(InvalidSessionState):
            self.lifecycle.resume(
                make_session(state=SessionState.ACTIVE),
                phase=RuntimePhase.ACTIVE,
            )

    def test_complete_from_active(self):
        result = self.lifecycle.complete(
            make_session(state=SessionState.ACTIVE),
            phase=RuntimePhase.ACTIVE,
            actual_duration_minutes=30,
        )
        assert result.phase == RuntimePhase.COMPLETED
        assert result.session.state == SessionState.COMPLETED
        assert result.session.actual_duration_minutes == 30

    def test_complete_from_paused(self):
        result = self.lifecycle.complete(
            make_session(state=SessionState.PAUSED),
            phase=RuntimePhase.PAUSED,
        )
        assert result.phase == RuntimePhase.COMPLETED

    def test_complete_rejects_negative_duration(self):
        with pytest.raises(InvalidSessionState):
            self.lifecycle.complete(
                make_session(state=SessionState.ACTIVE),
                phase=RuntimePhase.ACTIVE,
                actual_duration_minutes=-1,
            )

    def test_complete_rejects_planned(self):
        with pytest.raises((InvalidSessionState, SessionAlreadyCompleted)):
            self.lifecycle.complete(make_session(), phase=RuntimePhase.PLANNED)

    def test_archive_completed(self):
        result = self.lifecycle.archive(
            make_session(state=SessionState.COMPLETED),
            phase=RuntimePhase.COMPLETED,
        )
        assert result.phase == RuntimePhase.ARCHIVED
        assert result.session.state == SessionState.COMPLETED

    def test_archive_rejects_active(self):
        with pytest.raises((InvalidSessionState, SessionAlreadyCompleted)):
            self.lifecycle.archive(
                make_session(state=SessionState.ACTIVE),
                phase=RuntimePhase.ACTIVE,
            )

    def test_archive_already_archived(self):
        with pytest.raises(SessionAlreadyArchived):
            self.lifecycle.archive(
                make_session(state=SessionState.COMPLETED),
                phase=RuntimePhase.ARCHIVED,
            )

    def test_completed_rejects_start(self):
        with pytest.raises(SessionAlreadyCompleted):
            self.lifecycle.start(
                make_session(state=SessionState.COMPLETED),
                phase=RuntimePhase.COMPLETED,
            )

    def test_archived_rejects_pause(self):
        with pytest.raises(SessionAlreadyArchived):
            self.lifecycle.pause(
                make_session(state=SessionState.COMPLETED),
                phase=RuntimePhase.ARCHIVED,
            )

    def test_abandoned_rejects_lifecycle(self):
        with pytest.raises((InvalidSessionState, SessionAlreadyArchived)):
            self.lifecycle.start(
                make_session(state=SessionState.ABANDONED),
                phase=RuntimePhase.ARCHIVED,
            )

    def test_derive_phase_prepared(self):
        phase = self.lifecycle.derive_phase(make_session(), prepared=True)
        assert phase == RuntimePhase.READY

    def test_derive_phase_archived_flag(self):
        phase = self.lifecycle.derive_phase(
            make_session(state=SessionState.COMPLETED),
            archived=True,
        )
        assert phase == RuntimePhase.ARCHIVED

    def test_happy_path_sequence(self):
        session = make_session()
        r = self.lifecycle.prepare(session, phase=RuntimePhase.PLANNED)
        r = self.lifecycle.start(r.session, phase=r.phase)
        r = self.lifecycle.pause(r.session, phase=r.phase)
        r = self.lifecycle.resume(r.session, phase=r.phase)
        r = self.lifecycle.complete(r.session, phase=r.phase)
        r = self.lifecycle.archive(r.session, phase=r.phase)
        assert r.phase == RuntimePhase.ARCHIVED
