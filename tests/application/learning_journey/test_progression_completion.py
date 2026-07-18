"""Tests for progression manager, completion manager, and policies."""

from __future__ import annotations

import pytest

from app.application.learning_journey.completion_manager import CompletionManager
from app.application.learning_journey.exceptions import (
    InvalidJourneyState,
    InvalidProgression,
    JourneyAlreadyCompleted,
)
from app.application.learning_journey.policies.completion_policy import (
    CompletionPolicy,
)
from app.application.learning_journey.policies.progression_policy import (
    ProgressionPolicy,
)
from app.application.learning_journey.progression_manager import ProgressionManager
from app.application.learning_journey.recommendation_builder import (
    RecommendationBuilder,
)
from app.domain.learning_journey.entities.journey_reflection import JourneyReflection
from app.domain.learning_journey.value_objects.journey_state import JourneyState
from app.domain.learning_journey.value_objects.session_state import SessionState
from tests.application.learning_journey.helpers import (
    NOW,
    make_captured_reflection,
    make_evidence,
    make_journey,
    make_objective,
    make_session,
    ready_journey,
)


class TestProgressionPolicy:
    def test_may_start_session_states(self) -> None:
        assert ProgressionPolicy.may_start_session(
            make_journey(state=JourneyState.NOT_STARTED)
        )
        assert ProgressionPolicy.may_start_session(
            make_journey(state=JourneyState.ACTIVE)
        )
        assert not ProgressionPolicy.may_start_session(
            make_journey(state=JourneyState.PAUSED)
        )

    def test_pending_reflection_sessions(self) -> None:
        pending = JourneyReflection.create_pending("r1", "sess-1", "journey-1")
        journey = make_journey(
            sessions=[
                make_session(
                    "sess-1",
                    state=SessionState.COMPLETED,
                    reflection=pending,
                )
            ],
            reflections=[pending],
        )
        pending_sessions = ProgressionPolicy.pending_reflection_sessions(journey)
        assert len(pending_sessions) == 1

    def test_no_pending_when_captured(self) -> None:
        captured = make_captured_reflection("r1", "sess-1")
        journey = make_journey(
            sessions=[
                make_session(
                    "sess-1",
                    state=SessionState.COMPLETED,
                    reflection=captured,
                )
            ],
            reflections=[captured],
        )
        assert ProgressionPolicy.pending_reflection_sessions(journey) == ()

    def test_addressed_objective_ids(self) -> None:
        journey = make_journey(
            objectives=[
                make_objective("obj-1"),
                make_objective("obj-2", sequence_index=1),
            ],
            sessions=[
                make_session(
                    state=SessionState.COMPLETED,
                    objective_id="obj-1",
                )
            ],
            evidence=[make_evidence(objective_id="obj-2", session_id=None)],
        )
        addressed = ProgressionPolicy.addressed_objective_ids(journey)
        assert addressed == frozenset({"obj-1", "obj-2"})

    def test_next_unaddressed_objective(self) -> None:
        journey = make_journey(
            objectives=[
                make_objective("obj-1", sequence_index=0),
                make_objective("obj-2", sequence_index=1),
            ],
            sessions=[
                make_session(state=SessionState.COMPLETED, objective_id="obj-1")
            ],
        )
        nxt = ProgressionPolicy.next_unaddressed_objective(journey)
        assert nxt is not None
        assert nxt.objective_id == "obj-2"

    def test_current_focus_from_active_session(self) -> None:
        journey = make_journey(
            objectives=[make_objective("obj-1")],
            sessions=[
                make_session(
                    state=SessionState.ACTIVE,
                    objective_id="obj-1",
                )
            ],
        )
        focus = ProgressionPolicy.current_focus_objective(journey)
        assert focus is not None
        assert focus.objective_id == "obj-1"

    def test_unlocked_objectives(self) -> None:
        journey = make_journey(
            objectives=[make_objective("obj-1")],
            sessions=[
                make_session(state=SessionState.COMPLETED, objective_id="obj-1")
            ],
        )
        unlocked = ProgressionPolicy.unlocked_objectives(
            journey,
            previously_addressed=frozenset(),
        )
        assert len(unlocked) == 1

    def test_next_actions_include_reflection(self) -> None:
        pending = JourneyReflection.create_pending("r1", "sess-1", "journey-1")
        journey = make_journey(
            state=JourneyState.ACTIVE,
            sessions=[
                make_session(
                    "sess-1",
                    state=SessionState.COMPLETED,
                    reflection=pending,
                )
            ],
            reflections=[pending],
        )
        actions = ProgressionPolicy.next_actions_after_progression(
            journey,
            meets_completion_criteria=False,
        )
        assert "capture_reflection" in actions


class TestCompletionPolicy:
    def test_single_session_insufficient(self) -> None:
        captured = make_captured_reflection("r1", "sess-1")
        journey = make_journey(
            state=JourneyState.ACTIVE,
            objectives=[make_objective()],
            sessions=[
                make_session(
                    "sess-1",
                    state=SessionState.COMPLETED,
                    objective_id="obj-1",
                    reflection=captured,
                )
            ],
            reflections=[captured],
            evidence=[make_evidence(objective_id="obj-1")],
        )
        evaluation = CompletionPolicy.evaluate(journey)
        assert evaluation.meets_completion_criteria is False
        assert "single_session_insufficient" in evaluation.blockers or (
            "insufficient_completed_sessions" in evaluation.blockers
        )

    def test_ready_journey_eligible(self) -> None:
        evaluation = CompletionPolicy.evaluate(ready_journey())
        assert evaluation.meets_completion_criteria is True
        assert evaluation.eligible_for_ready is True

    def test_ready_state_eligible_for_confirm(self) -> None:
        journey = ready_journey()
        from app.domain.learning_journey.entities.learning_journey import (
            LearningJourney,
        )

        ready = LearningJourney.create(
            journey.journey_id,
            journey.learner_id,
            journey.topic_id,
            journey.curriculum_id,
            state=JourneyState.READY_FOR_COMPLETION,
            objectives=list(journey.objectives),
            sessions=list(journey.sessions),
            evidence=list(journey.evidence),
            reflections=list(journey.reflections),
            progress=journey.progress,
        )
        # Recalculate progress onto ready journey
        from app.domain.learning_journey.services.journey_progress_service import (
            JourneyProgressService,
        )

        ready = ready.with_progress(JourneyProgressService.calculate(ready))
        evaluation = CompletionPolicy.evaluate(ready)
        assert evaluation.eligible_for_confirm is True

    def test_completed_blocks(self) -> None:
        evaluation = CompletionPolicy.evaluate(
            make_journey(state=JourneyState.COMPLETED)
        )
        assert evaluation.eligible_for_confirm is False
        assert "journey_already_completed" in evaluation.blockers

    def test_abandoned_blocks(self) -> None:
        evaluation = CompletionPolicy.evaluate(
            make_journey(state=JourneyState.ABANDONED)
        )
        assert evaluation.meets_completion_criteria is False

    def test_paused_blocks_ready(self) -> None:
        journey = ready_journey()
        from app.domain.learning_journey.entities.learning_journey import (
            LearningJourney,
        )
        from app.domain.learning_journey.services.journey_progress_service import (
            JourneyProgressService,
        )

        paused = LearningJourney.create(
            journey.journey_id,
            journey.learner_id,
            journey.topic_id,
            journey.curriculum_id,
            state=JourneyState.PAUSED,
            objectives=list(journey.objectives),
            sessions=list(journey.sessions),
            evidence=list(journey.evidence),
            reflections=list(journey.reflections),
        )
        paused = paused.with_progress(JourneyProgressService.calculate(paused))
        evaluation = CompletionPolicy.evaluate(paused)
        assert evaluation.eligible_for_ready is False
        assert "journey_paused" in evaluation.blockers

    def test_rejects_session_only(self) -> None:
        journey = make_journey(
            sessions=[make_session(state=SessionState.COMPLETED)]
        )
        assert CompletionPolicy.rejects_session_only_completion(journey) is True

    def test_rejects_time_or_percentage(self) -> None:
        assert CompletionPolicy.rejects_time_or_percentage_alone() is True

    def test_pending_reflections_blocker(self) -> None:
        pending = JourneyReflection.create_pending("r1", "sess-1", "journey-1")
        pending2 = JourneyReflection.create_pending("r2", "sess-2", "journey-1")
        journey = make_journey(
            state=JourneyState.ACTIVE,
            objectives=[
                make_objective("obj-1"),
                make_objective("obj-2", sequence_index=1),
            ],
            sessions=[
                make_session(
                    "sess-1",
                    sequence_index=0,
                    state=SessionState.COMPLETED,
                    objective_id="obj-1",
                    reflection=pending,
                ),
                make_session(
                    "sess-2",
                    sequence_index=1,
                    state=SessionState.COMPLETED,
                    objective_id="obj-2",
                    reflection=pending2,
                ),
            ],
            reflections=[pending, pending2],
            evidence=[
                make_evidence("je-1", session_id="sess-1", objective_id="obj-1"),
                make_evidence(
                    "je-2",
                    evidence_id="ev-2",
                    session_id="sess-2",
                    objective_id="obj-2",
                ),
            ],
        )
        evaluation = CompletionPolicy.evaluate(journey)
        assert evaluation.meets_completion_criteria is False
        assert "pending_reflections" in evaluation.blockers


class TestCompletionManager:
    def test_mark_ready(self) -> None:
        manager = CompletionManager()
        ready = manager.mark_ready_for_completion(ready_journey())
        assert ready.state == JourneyState.READY_FOR_COMPLETION

    def test_mark_ready_rejects_incomplete(self) -> None:
        manager = CompletionManager()
        with pytest.raises(InvalidProgression):
            manager.mark_ready_for_completion(make_journey(state=JourneyState.ACTIVE))

    def test_confirm(self) -> None:
        manager = CompletionManager()
        ready = manager.mark_ready_for_completion(ready_journey())
        completed = manager.confirm_topic_complete(ready)
        assert completed.state == JourneyState.COMPLETED

    def test_confirm_rejects_already_completed(self) -> None:
        manager = CompletionManager()
        with pytest.raises(JourneyAlreadyCompleted):
            manager.validate_completion(make_journey(state=JourneyState.COMPLETED))

    def test_confirm_rejects_wrong_state(self) -> None:
        manager = CompletionManager()
        with pytest.raises(InvalidJourneyState):
            manager.validate_completion(ready_journey())

    def test_rejects_shallow(self) -> None:
        manager = CompletionManager()
        assert manager.rejects_shallow_completion(make_journey()) is True


class TestProgressionManager:
    def test_recalculate_progress(self) -> None:
        manager = ProgressionManager(
            clock=lambda: NOW,
            history_id_factory=lambda: "h1",
            recommendation_builder=RecommendationBuilder(
                clock=lambda: NOW,
                id_factory=lambda: "r1",
            ),
        )
        journey = ready_journey()
        updated = manager.recalculate_progress(journey)
        assert updated.progress.sessions_completed == 2
        assert updated.progress.meets_completion_criteria is True

    def test_apply_session_completed(self) -> None:
        manager = ProgressionManager(
            clock=lambda: NOW,
            history_id_factory=lambda: "h1",
            recommendation_builder=RecommendationBuilder(
                clock=lambda: NOW,
                id_factory=lambda: "r1",
            ),
        )
        journey = make_journey(
            state=JourneyState.NOT_STARTED,
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
        result = manager.apply_session_completed(journey, completed)
        assert result.journey.state == JourneyState.ACTIVE
        assert result.progress_recalculated is True
        assert result.journey.progress.sessions_completed == 1
        assert "obj-1" in {
            o.objective_id for o in result.unlocked_objectives
        } or result.journey.progress.objectives_addressed >= 1

    def test_apply_session_completed_rejects_non_completed(self) -> None:
        manager = ProgressionManager()
        with pytest.raises(InvalidProgression):
            manager.apply_session_completed(
                make_journey(state=JourneyState.ACTIVE),
                make_session(state=SessionState.ACTIVE),
            )

    def test_apply_session_completed_rejects_paused(self) -> None:
        manager = ProgressionManager()
        with pytest.raises(InvalidJourneyState):
            manager.apply_session_completed(
                make_journey(state=JourneyState.PAUSED),
                make_session(state=SessionState.COMPLETED),
            )

    def test_apply_reflection_captured_may_ready(self) -> None:
        manager = ProgressionManager(
            clock=lambda: NOW,
            history_id_factory=lambda: "h1",
            recommendation_builder=RecommendationBuilder(
                clock=lambda: NOW,
                id_factory=lambda: "r1",
            ),
        )
        journey = ready_journey()
        result = manager.apply_reflection_captured(journey)
        assert result.meets_completion_criteria is True
        assert result.current_state == JourneyState.READY_FOR_COMPLETION

    def test_validate_progression_ok(self) -> None:
        manager = ProgressionManager()
        manager.validate_progression(ready_journey())

    def test_validate_progression_fails_on_mismatch(self) -> None:
        manager = ProgressionManager()
        bad = make_journey(
            sessions=[make_session("s1")],
            evidence=[make_evidence(session_id="unknown-session")],
        )
        with pytest.raises(InvalidProgression):
            manager.validate_progression(bad)

    def test_session_completed_auto_ready(self) -> None:
        manager = ProgressionManager(
            clock=lambda: NOW,
            history_id_factory=lambda: "h1",
            recommendation_builder=RecommendationBuilder(
                clock=lambda: NOW,
                id_factory=lambda: "r1",
            ),
        )
        # Start from ready artefacts but swap last session to ACTIVE then complete
        base = ready_journey()
        sessions = list(base.sessions)
        last = sessions[-1]
        # Re-apply completing the last session against ACTIVE journey with both done
        result = manager.apply_session_completed(base, last)
        assert result.meets_completion_criteria is True
        assert result.current_state == JourneyState.READY_FOR_COMPLETION
