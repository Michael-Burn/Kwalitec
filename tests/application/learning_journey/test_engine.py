"""Tests for Learning Journey Engine facade and lifecycle operations."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from app.application.learning_journey import (
    InvalidJourneyState,
    JourneyAlreadyCompleted,
    JourneyNotFound,
    LearningJourneyEngine,
    SessionOrderingViolation,
)
from app.domain.learning_journey.entities.journey_history import JourneyHistoryEventType
from app.domain.learning_journey.value_objects.journey_state import JourneyState
from app.domain.learning_journey.value_objects.session_state import SessionState
from tests.application.learning_journey.helpers import (
    NOW,
    InMemoryJourneyRepository,
    make_journey,
    make_objective,
    make_session,
    ready_journey,
)

APP_ROOT = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "application"
    / "learning_journey"
)
FORBIDDEN_ROOT_MODULES = frozenset(
    {
        "flask",
        "flask_login",
        "flask_sqlalchemy",
        "flask_wtf",
        "sqlalchemy",
        "wtforms",
    }
)
FORBIDDEN_PREFIXES = (
    "app.services",
    "app.models",
    "app.auth",
    "app.dashboard",
    "app.mission",
    "app.analytics",
    "app.study_plan",
)


class TestFrameworkIndependence:
    def test_package_avoids_flask_and_orm_imports(self) -> None:
        offenders: list[str] = []
        for path in APP_ROOT.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        root = alias.name.split(".", 1)[0]
                        if root in FORBIDDEN_ROOT_MODULES or any(
                            alias.name.startswith(p) for p in FORBIDDEN_PREFIXES
                        ):
                            offenders.append(f"{path.name}:{alias.name}")
                elif isinstance(node, ast.ImportFrom) and node.module:
                    root = node.module.split(".", 1)[0]
                    if root in FORBIDDEN_ROOT_MODULES or any(
                        node.module.startswith(p) for p in FORBIDDEN_PREFIXES
                    ):
                        offenders.append(f"{path.name}:{node.module}")
        assert offenders == []


class TestEngineCreation:
    def test_create_journey_not_started(self) -> None:
        engine = LearningJourneyEngine(clock=lambda: NOW, id_factory=lambda: "abc")
        journey = engine.create_journey(
            learner_id="learner-1",
            topic_id="topic-a",
            curriculum_id="curr-1",
            objectives=[make_objective()],
        )
        assert journey.state == JourneyState.NOT_STARTED
        assert journey.journey_id == "journey-abc"
        assert len(journey.objectives) == 1

    def test_create_journey_records_history(self) -> None:
        engine = LearningJourneyEngine(clock=lambda: NOW, id_factory=lambda: "x1")
        journey = engine.create_journey(
            learner_id="l1",
            topic_id="t1",
            curriculum_id="c1",
        )
        types = [e.event_type for e in journey.history.entries]
        assert JourneyHistoryEventType.JOURNEY_CREATED in types

    def test_create_with_explicit_id(self) -> None:
        engine = LearningJourneyEngine()
        journey = engine.create_journey(
            learner_id="l1",
            topic_id="t1",
            curriculum_id="c1",
            journey_id="custom-id",
        )
        assert journey.journey_id == "custom-id"

    def test_create_with_sessions(self) -> None:
        engine = LearningJourneyEngine()
        session = make_session("s1", journey_id="j-fixed")
        journey = engine.create_journey(
            learner_id="l1",
            topic_id="topic-a",
            curriculum_id="c1",
            journey_id="j-fixed",
            sessions=[session],
        )
        assert len(journey.sessions) == 1


class TestEngineLifecycle:
    def test_start_journey(self) -> None:
        engine = LearningJourneyEngine()
        journey = make_journey()
        started = engine.start_journey(journey)
        assert started.state == JourneyState.ACTIVE

    def test_start_already_active_is_idempotent(self) -> None:
        engine = LearningJourneyEngine()
        journey = make_journey(state=JourneyState.ACTIVE)
        assert engine.start_journey(journey).state == JourneyState.ACTIVE

    def test_start_from_paused_raises(self) -> None:
        engine = LearningJourneyEngine()
        journey = make_journey(state=JourneyState.PAUSED)
        with pytest.raises(InvalidJourneyState):
            engine.start_journey(journey)

    def test_pause_and_resume(self) -> None:
        engine = LearningJourneyEngine()
        journey = make_journey(state=JourneyState.ACTIVE)
        paused = engine.pause_journey(journey)
        assert paused.state == JourneyState.PAUSED
        resumed = engine.resume_journey(paused)
        assert resumed.state == JourneyState.ACTIVE

    def test_pause_idempotent(self) -> None:
        engine = LearningJourneyEngine()
        journey = make_journey(state=JourneyState.PAUSED)
        assert engine.pause_journey(journey).state == JourneyState.PAUSED

    def test_pause_not_started_raises(self) -> None:
        engine = LearningJourneyEngine()
        with pytest.raises(InvalidJourneyState):
            engine.pause_journey(make_journey())

    def test_resume_not_paused_raises(self) -> None:
        engine = LearningJourneyEngine()
        with pytest.raises(InvalidJourneyState):
            engine.resume_journey(make_journey(state=JourneyState.ACTIVE))

    def test_defer_and_reactivate(self) -> None:
        engine = LearningJourneyEngine()
        journey = make_journey(state=JourneyState.ACTIVE)
        deferred = engine.defer_journey(journey)
        assert deferred.state == JourneyState.DEFERRED
        active = engine.reactivate_journey(deferred)
        assert active.state == JourneyState.ACTIVE

    def test_abandon_journey(self) -> None:
        engine = LearningJourneyEngine()
        abandoned = engine.abandon_journey(make_journey(state=JourneyState.ACTIVE))
        assert abandoned.state == JourneyState.ABANDONED

    def test_operations_reject_completed(self) -> None:
        engine = LearningJourneyEngine()
        completed = make_journey(state=JourneyState.COMPLETED)
        with pytest.raises(JourneyAlreadyCompleted):
            engine.pause_journey(completed)
        with pytest.raises(JourneyAlreadyCompleted):
            engine.resume_journey(completed)
        with pytest.raises(JourneyAlreadyCompleted):
            engine.start_journey(completed)


class TestEngineLoad:
    def test_load_without_repository_raises(self) -> None:
        engine = LearningJourneyEngine()
        with pytest.raises(JourneyNotFound):
            engine.load_journey("missing")

    def test_load_missing_raises(self) -> None:
        repo = InMemoryJourneyRepository()
        engine = LearningJourneyEngine(repository=repo)
        with pytest.raises(JourneyNotFound):
            engine.load_journey("missing")

    def test_load_existing(self) -> None:
        repo = InMemoryJourneyRepository()
        journey = make_journey()
        repo.save(journey)
        engine = LearningJourneyEngine(repository=repo)
        loaded = engine.load_journey("journey-1")
        assert loaded.journey_id == "journey-1"

    def test_engine_never_calls_save(self) -> None:
        repo = InMemoryJourneyRepository()
        engine = LearningJourneyEngine(repository=repo)
        journey = engine.create_journey(
            learner_id="l1",
            topic_id="t1",
            curriculum_id="c1",
            journey_id="j-new",
        )
        assert repo.get_by_id("j-new") is None
        engine.start_journey(journey)
        assert repo.get_by_id("j-new") is None


class TestEngineQueries:
    def test_current_objective_and_sessions(self) -> None:
        engine = LearningJourneyEngine()
        objectives = [
            make_objective("obj-1", sequence_index=0),
            make_objective("obj-2", sequence_index=1),
        ]
        sessions = [
            make_session(
                "sess-1",
                sequence_index=0,
                state=SessionState.ACTIVE,
                objective_id="obj-1",
            ),
            make_session(
                "sess-2",
                sequence_index=1,
                state=SessionState.NOT_STARTED,
                objective_id="obj-2",
            ),
        ]
        journey = make_journey(
            state=JourneyState.ACTIVE,
            objectives=objectives,
            sessions=sessions,
        )
        assert engine.current_objective(journey).objective_id == "obj-1"
        assert engine.current_learning_session(journey).session_id == "sess-1"
        assert engine.next_learning_session(journey).session_id == "sess-1"

    def test_session_plan(self) -> None:
        engine = LearningJourneyEngine()
        journey = make_journey(
            state=JourneyState.ACTIVE,
            objectives=[make_objective()],
            sessions=[
                make_session(
                    state=SessionState.NOT_STARTED,
                    objective_id="obj-1",
                )
            ],
        )
        plan = engine.session_plan(journey)
        assert plan is not None
        assert plan.session_number == 1
        assert plan.is_existing_session is True

    def test_generate_recommendation(self) -> None:
        engine = LearningJourneyEngine(clock=lambda: NOW, id_factory=lambda: "r1")
        journey = make_journey(
            state=JourneyState.ACTIVE,
            objectives=[make_objective()],
        )
        result = engine.generate_recommendation(journey)
        assert result.kind is not None
        assert "mastery" not in result.confidence_explanation.lower() or (
            "no" in result.confidence_explanation.lower()
            or "not" in result.confidence_explanation.lower()
            or "never" in result.confidence_explanation.lower()
            or "claim" in result.confidence_explanation.lower()
        )

    def test_snapshot(self) -> None:
        engine = LearningJourneyEngine()
        journey = ready_journey()
        snap = engine.generate_journey_snapshot(journey)
        assert snap.journey_id == journey.journey_id
        assert snap.sessions_completed == 2
        assert snap.meets_completion_criteria is True

    def test_orchestrate_marks_ready(self) -> None:
        engine = LearningJourneyEngine(clock=lambda: NOW, id_factory=lambda: "o1")
        journey = ready_journey()
        updated = engine.orchestrate(journey)
        assert updated.state == JourneyState.READY_FOR_COMPLETION
        assert updated.recommendations

    def test_confirm_topic_complete(self) -> None:
        engine = LearningJourneyEngine()
        journey = ready_journey()
        ready = engine.mark_ready_for_completion(journey)
        completed = engine.confirm_topic_complete(ready)
        assert completed.state == JourneyState.COMPLETED

    def test_validate_completion_wrong_state(self) -> None:
        engine = LearningJourneyEngine()
        with pytest.raises(InvalidJourneyState):
            engine.validate_completion(ready_journey())

    def test_apply_session_completed(self) -> None:
        engine = LearningJourneyEngine(clock=lambda: NOW, id_factory=lambda: "p1")
        journey = make_journey(
            state=JourneyState.ACTIVE,
            objectives=[make_objective()],
            sessions=[
                make_session(
                    "sess-1",
                    state=SessionState.ACTIVE,
                    objective_id="obj-1",
                )
            ],
        )
        completed = make_session(
            "sess-1",
            state=SessionState.COMPLETED,
            objective_id="obj-1",
        )
        result = engine.apply_session_completed(journey, completed)
        assert result.progress_recalculated is True
        assert result.journey.progress.sessions_completed == 1

    def test_session_ordering_violation_via_selector(self) -> None:
        from app.domain.learning_journey.entities.learning_journey import (
            LearningJourney,
        )

        engine = LearningJourneyEngine()
        bad = LearningJourney.create(
            "journey-1",
            "learner-1",
            "topic-a",
            "curr-1",
            state=JourneyState.ACTIVE,
            sessions=[
                make_session("s1", sequence_index=0),
                make_session("s2", sequence_index=0),
            ],
        )
        with pytest.raises(SessionOrderingViolation):
            engine.session_plan(bad)
