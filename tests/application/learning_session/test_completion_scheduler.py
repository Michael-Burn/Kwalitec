"""Tests for CompletionEvaluator and ActivityScheduler."""

from __future__ import annotations

from datetime import UTC, datetime

from app.application.learning_session.activity_scheduler import ActivityScheduler
from app.application.learning_session.completion_evaluator import CompletionEvaluator
from app.application.learning_session.policies.completion_policy import (
    CompletionPolicy,
)
from app.application.learning_session.policies.scheduling_policy import NextAction
from app.application.learning_session.runtime_phase import RuntimePhase
from app.domain.learning_journey.entities.journey_reflection import JourneyReflection
from app.domain.learning_journey.value_objects.effort_estimate import EffortEstimate
from app.domain.learning_journey.value_objects.session_state import SessionState
from tests.application.learning_session.helpers import make_evidence, make_session


class TestCompletionEvaluator:
    def setup_method(self):
        self.evaluator = CompletionEvaluator()

    def test_active_not_complete(self):
        result = self.evaluator.evaluate(make_session(state=SessionState.ACTIVE))
        assert not result.is_complete
        assert result.journey_complete is False

    def test_completed_with_captured_reflection(self):
        reflection = JourneyReflection.create_captured(
            "r1",
            "sess-1",
            "journey-1",
            what_was_learned="x",
            uncertainty="y",
            captured_at=datetime(2026, 7, 18, tzinfo=UTC),
        )
        result = self.evaluator.evaluate(
            make_session(state=SessionState.COMPLETED, reflection=reflection)
        )
        assert result.is_complete
        assert result.session_finished
        assert result.reflection_satisfied
        assert result.journey_complete is False

    def test_never_journey_complete(self):
        reflection = JourneyReflection.create_captured(
            "r1",
            "sess-1",
            "journey-1",
            what_was_learned="x",
            uncertainty="y",
            captured_at=datetime(2026, 7, 18, tzinfo=UTC),
        )
        result = self.evaluator.evaluate(
            make_session(
                state=SessionState.COMPLETED,
                reflection=reflection,
                evidence=[make_evidence()],
            )
        )
        assert result.journey_complete is False

    def test_asserts_session_not_journey(self):
        assert self.evaluator.asserts_session_not_journey()

    def test_evidence_flag_independent_of_mastery(self):
        result = self.evaluator.evaluate(
            make_session(
                state=SessionState.COMPLETED,
                evidence=[make_evidence()],
            )
        )
        assert result.evidence_recorded
        assert not result.is_complete  # reflection still owed


class TestActivityScheduler:
    def setup_method(self):
        self.scheduler = ActivityScheduler()
        self.evaluator = CompletionEvaluator()

    def test_next_action_prepare(self):
        session = make_session()
        action = self.scheduler.next_action(
            session,
            phase=RuntimePhase.PLANNED,
            completion=self.evaluator.evaluate(session),
        )
        assert action == NextAction.PREPARE

    def test_next_action_start(self):
        session = make_session()
        action = self.scheduler.next_action(
            session,
            phase=RuntimePhase.READY,
            completion=self.evaluator.evaluate(session),
        )
        assert action == NextAction.START

    def test_next_action_continue_active(self):
        session = make_session(state=SessionState.ACTIVE, effort=EffortEstimate.LOW)
        action = self.scheduler.next_action(
            session,
            phase=RuntimePhase.ACTIVE,
            completion=self.evaluator.evaluate(session),
            actual_duration_minutes=5,
        )
        assert action == NextAction.CONTINUE

    def test_next_action_break(self):
        session = make_session(state=SessionState.ACTIVE)
        action = self.scheduler.next_action(
            session,
            phase=RuntimePhase.ACTIVE,
            completion=self.evaluator.evaluate(session),
            actual_duration_minutes=50,
        )
        assert action == NextAction.BREAK

    def test_next_action_reflect(self):
        session = make_session(state=SessionState.COMPLETED)
        action = self.scheduler.next_action(
            session,
            phase=RuntimePhase.COMPLETED,
            completion=self.evaluator.evaluate(session),
        )
        assert action == NextAction.REFLECT

    def test_next_action_revise_when_thin_evidence(self):
        reflection = JourneyReflection.create_captured(
            "r1",
            "sess-1",
            "journey-1",
            what_was_learned="x",
            uncertainty="y",
            captured_at=datetime(2026, 7, 18, tzinfo=UTC),
        )
        session = make_session(
            state=SessionState.COMPLETED,
            reflection=reflection,
            evidence=[],
        )
        action = self.scheduler.next_action(
            session,
            phase=RuntimePhase.COMPLETED,
            completion=self.evaluator.evaluate(session),
        )
        assert action == NextAction.REVISE

    def test_next_action_next_session_with_evidence(self):
        reflection = JourneyReflection.create_captured(
            "r1",
            "sess-1",
            "journey-1",
            what_was_learned="x",
            uncertainty="y",
            captured_at=datetime(2026, 7, 18, tzinfo=UTC),
        )
        session = make_session(
            state=SessionState.COMPLETED,
            reflection=reflection,
            evidence=[make_evidence()],
        )
        action = self.scheduler.next_action(
            session,
            phase=RuntimePhase.COMPLETED,
            completion=self.evaluator.evaluate(session),
        )
        assert action == NextAction.NEXT_SESSION

    def test_next_action_none_archived(self):
        session = make_session(state=SessionState.COMPLETED)
        action = self.scheduler.next_action(
            session,
            phase=RuntimePhase.ARCHIVED,
            completion=CompletionPolicy.evaluate(session),
        )
        assert action == NextAction.NONE

    def test_recommend_break_helper(self):
        session = make_session(state=SessionState.ACTIVE)
        assert self.scheduler.recommend_break(
            session,
            actual_duration_minutes=45,
        )
