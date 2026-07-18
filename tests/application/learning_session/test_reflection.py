"""Tests for ReflectionManager."""

from __future__ import annotations

import pytest

from app.application.learning_session.exceptions import (
    InvalidSessionState,
    ReflectionRequired,
)
from app.application.learning_session.reflection_manager import ReflectionManager
from app.domain.learning_journey.entities.journey_reflection import (
    ReflectionConfidence,
    ReflectionPosture,
)
from app.domain.learning_journey.value_objects.session_state import SessionState
from tests.application.learning_session.helpers import NOW, make_session


class TestReflectionManager:
    def setup_method(self):
        self.manager = ReflectionManager(
            clock=lambda: NOW,
            id_factory=lambda: "r1",
        )

    def test_attach_pending(self):
        session = make_session(state=SessionState.COMPLETED)
        updated = self.manager.attach_pending(session)
        assert updated.reflection is not None
        assert updated.reflection.posture == ReflectionPosture.PENDING

    def test_attach_pending_rejects_active(self):
        with pytest.raises(InvalidSessionState):
            self.manager.attach_pending(make_session(state=SessionState.ACTIVE))

    def test_attach_pending_idempotent(self):
        session = make_session(state=SessionState.COMPLETED)
        once = self.manager.attach_pending(session)
        twice = self.manager.attach_pending(once)
        assert once.reflection.reflection_id == twice.reflection.reflection_id

    def test_capture_full_fields(self):
        session = self.manager.attach_pending(
            make_session(state=SessionState.COMPLETED)
        )
        updated, summary = self.manager.capture(
            session,
            summary="Learned limits",
            challenges="Notation confusion",
            questions_remaining=["What about continuity?"],
            confidence=ReflectionConfidence.MEDIUM,
            next_intention="Revise examples",
        )
        assert updated.reflection_captured
        assert summary.is_captured
        assert summary.summary == "Learned limits"
        assert summary.challenges == "Notation confusion"
        assert summary.next_intention == "Revise examples"
        assert "What about continuity?" in summary.questions_remaining

    def test_capture_without_pending_artefact(self):
        updated, summary = self.manager.capture(
            make_session(state=SessionState.COMPLETED),
            summary="Direct capture",
            challenges="None",
            confidence="high",
        )
        assert summary.is_captured
        assert updated.reflection.posture == ReflectionPosture.CAPTURED

    def test_capture_rejects_empty_summary(self):
        session = make_session(state=SessionState.COMPLETED)
        with pytest.raises(ReflectionRequired):
            self.manager.capture(
                session,
                summary="",
                challenges="x",
            )

    def test_capture_rejects_active(self):
        with pytest.raises(InvalidSessionState):
            self.manager.capture(
                make_session(state=SessionState.ACTIVE),
                summary="x",
                challenges="y",
            )

    def test_defer_pending(self):
        session = self.manager.attach_pending(
            make_session(state=SessionState.COMPLETED)
        )
        deferred = self.manager.defer(session)
        assert deferred.reflection.posture == ReflectionPosture.DEFERRED_CAPTURE

    def test_defer_rejects_without_pending(self):
        with pytest.raises(InvalidSessionState):
            self.manager.defer(make_session(state=SessionState.COMPLETED))

    def test_capture_after_defer(self):
        session = self.manager.attach_pending(
            make_session(state=SessionState.COMPLETED)
        )
        session = self.manager.defer(session)
        updated, summary = self.manager.capture(
            session,
            summary="Later",
            challenges="Still tricky",
        )
        assert summary.is_captured

    def test_summarise_without_reflection_active(self):
        summary = self.manager.summarise(make_session(state=SessionState.ACTIVE))
        assert summary.posture == ReflectionPosture.NOT_REQUIRED.value
        assert not summary.is_captured

    def test_summarise_completed_without_artefact_pending(self):
        summary = self.manager.summarise(
            make_session(state=SessionState.COMPLETED)
        )
        assert summary.posture == ReflectionPosture.PENDING.value

    def test_next_intention_round_trip(self):
        session = make_session(state=SessionState.COMPLETED)
        updated, _ = self.manager.capture(
            session,
            summary="s",
            challenges="c",
            next_intention="Practice set 3",
        )
        summary = self.manager.summarise(updated)
        assert summary.next_intention == "Practice set 3"
        assert all(
            not q.startswith("next_intention:") for q in summary.questions_remaining
        )
