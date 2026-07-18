"""Tests for DTOs, exceptions, coordinator, and package exports."""

from __future__ import annotations

import dataclasses

import pytest

from app.application.learning_journey import (
    CompletionManager,
    CompletionPolicy,
    InvalidJourneyState,
    InvalidProgression,
    JourneyAlreadyCompleted,
    JourneyNotFound,
    JourneySnapshot,
    LearningJourneyCoordinator,
    LearningJourneyEngine,
    LearningJourneyEngineError,
    ProgressionManager,
    ProgressionPolicy,
    ProgressionResult,
    RecommendationBuilder,
    RecommendationPolicy,
    RecommendationResult,
    SessionOrderingViolation,
    SessionPlan,
    SessionSelector,
)
from app.application.learning_journey.dto.journey_snapshot import (
    EvidenceSummary,
    ReflectionSummary,
)
from app.domain.learning_journey.entities.journey_recommendation import (
    RecommendationCertainty,
    RecommendationKind,
)
from app.domain.learning_journey.value_objects.completion_status import CompletionStatus
from app.domain.learning_journey.value_objects.effort_estimate import EffortEstimate
from app.domain.learning_journey.value_objects.journey_state import JourneyState
from app.domain.learning_journey.value_objects.session_state import SessionState
from tests.application.learning_journey.helpers import (
    NOW,
    make_evidence,
    make_journey,
    make_objective,
    make_session,
    ready_journey,
)


class TestDtoImmutability:
    def test_session_plan_frozen(self) -> None:
        plan = SessionPlan(
            session_number=1,
            sequence_index=0,
            session_id="s1",
            objective=make_objective(),
            expected_effort=EffortEstimate.MEDIUM,
            recommended_activities=("focused_study",),
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            plan.session_number = 2  # type: ignore[misc]

    def test_recommendation_result_frozen(self) -> None:
        result = RecommendationResult(
            recommendation=None,
            kind=None,
            reason="none",
            confidence_explanation="n/a",
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            result.reason = "x"  # type: ignore[misc]

    def test_progression_result_frozen(self) -> None:
        journey = make_journey()
        result = ProgressionResult(
            journey=journey,
            previous_state=JourneyState.NOT_STARTED,
            current_state=JourneyState.NOT_STARTED,
            unlocked_objectives=(),
            next_actions=(),
            state_changed=False,
            progress_recalculated=False,
            meets_completion_criteria=False,
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            result.state_changed = True  # type: ignore[misc]

    def test_journey_snapshot_frozen(self) -> None:
        snap = JourneySnapshot(
            journey_id="j1",
            learner_id="l1",
            topic_id="t1",
            curriculum_id="c1",
            state=JourneyState.ACTIVE,
            completion_status=CompletionStatus.IN_PROGRESS,
            meets_completion_criteria=False,
            current_objective=None,
            sessions=(),
            evidence_summary=EvidenceSummary(0, "unknown", 0),
            reflection_summary=ReflectionSummary(0, 0, 0),
            recommendation=None,
            objectives_total=0,
            objectives_addressed=0,
            sessions_completed=0,
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            snap.journey_id = "x"  # type: ignore[misc]

    def test_evidence_and_reflection_summaries_frozen(self) -> None:
        with pytest.raises(dataclasses.FrozenInstanceError):
            EvidenceSummary(1, "low", 1).evidence_count = 2  # type: ignore[misc]
        with pytest.raises(dataclasses.FrozenInstanceError):
            ReflectionSummary(1, 0, 0).reflections_captured = 0  # type: ignore[misc]


class TestExceptions:
    def test_hierarchy(self) -> None:
        assert issubclass(JourneyNotFound, LearningJourneyEngineError)
        assert issubclass(InvalidJourneyState, LearningJourneyEngineError)
        assert issubclass(InvalidProgression, LearningJourneyEngineError)
        assert issubclass(JourneyAlreadyCompleted, LearningJourneyEngineError)
        assert issubclass(SessionOrderingViolation, LearningJourneyEngineError)

    def test_raise_and_catch(self) -> None:
        with pytest.raises(LearningJourneyEngineError):
            raise JourneyNotFound("missing")
        with pytest.raises(InvalidJourneyState):
            raise InvalidJourneyState("bad state")
        with pytest.raises(InvalidProgression):
            raise InvalidProgression("bad progression")
        with pytest.raises(JourneyAlreadyCompleted):
            raise JourneyAlreadyCompleted("done")
        with pytest.raises(SessionOrderingViolation):
            raise SessionOrderingViolation("order")


class TestCoordinator:
    def test_orchestrate(self) -> None:
        coordinator = LearningJourneyCoordinator(
            recommendation_builder=RecommendationBuilder(
                clock=lambda: NOW,
                id_factory=lambda: "r1",
            )
        )
        updated = coordinator.orchestrate(ready_journey())
        assert updated.state == JourneyState.READY_FOR_COMPLETION
        assert updated.recommendations

    def test_orchestrate_invalid_raises(self) -> None:
        coordinator = LearningJourneyCoordinator()
        bad = make_journey(
            sessions=[make_session("s1")],
            evidence=[make_evidence(session_id="unknown-session")],
        )
        with pytest.raises(InvalidJourneyState):
            coordinator.orchestrate(bad)

    def test_snapshot_includes_recommendation(self) -> None:
        coordinator = LearningJourneyCoordinator(
            recommendation_builder=RecommendationBuilder(
                clock=lambda: NOW,
                id_factory=lambda: "r1",
            )
        )
        snap = coordinator.snapshot(
            make_journey(
                state=JourneyState.ACTIVE,
                sessions=[make_session(state=SessionState.ACTIVE)],
            )
        )
        assert snap.recommendation is not None
        assert snap.recommendation.kind == RecommendationKind.CONTINUE_CURRENT_SESSION

    def test_generate_recommendation(self) -> None:
        coordinator = LearningJourneyCoordinator()
        result = coordinator.generate_recommendation(
            make_journey(state=JourneyState.COMPLETED)
        )
        assert result.kind is None
        assert result.certainty == RecommendationCertainty.CONDITIONAL

    def test_session_helpers(self) -> None:
        coordinator = LearningJourneyCoordinator()
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
        assert coordinator.next_session(journey).session_id == "sess-1"
        assert coordinator.session_plan(journey) is not None
        assert coordinator.current_objective(journey).objective_id == "obj-1"

    def test_evaluate_completion(self) -> None:
        coordinator = LearningJourneyCoordinator()
        evaluation = coordinator.evaluate_completion(ready_journey())
        assert evaluation.eligible_for_ready is True


class TestPackageExports:
    def test_public_symbols_importable(self) -> None:
        assert LearningJourneyEngine is not None
        assert LearningJourneyCoordinator is not None
        assert SessionSelector is not None
        assert RecommendationBuilder is not None
        assert ProgressionManager is not None
        assert CompletionManager is not None
        assert ProgressionPolicy is not None
        assert CompletionPolicy is not None
        assert RecommendationPolicy is not None
        assert SessionPlan is not None
        assert JourneySnapshot is not None
        assert RecommendationResult is not None
        assert ProgressionResult is not None
