"""Activity completion manager and policy tests."""

from __future__ import annotations

import pytest

from app.application.learning_activity.completion_manager import CompletionManager
from app.application.learning_activity.policies.completion_policy import (
    CompletionPolicy,
)
from app.domain.learning_activity.value_objects.activity_state import ActivityState
from app.domain.learning_activity.value_objects.activity_type import ActivityType
from tests.application.learning_activity.helpers import (
    make_activity,
    make_engine,
    make_sequence,
)


class TestCompletionPolicy:
    def test_rejects_session_and_journey_completion(self):
        assert CompletionPolicy.rejects_session_completion() is True
        assert CompletionPolicy.rejects_journey_completion() is True

    def test_activity_complete_only_when_completed(self):
        assert (
            CompletionPolicy.is_activity_complete(
                make_activity(state=ActivityState.COMPLETED)
            )
            is True
        )
        assert (
            CompletionPolicy.is_activity_complete(
                make_activity(state=ActivityState.SKIPPED)
            )
            is False
        )
        assert (
            CompletionPolicy.is_activity_complete(
                make_activity(state=ActivityState.ACTIVE)
            )
            is False
        )

    def test_sequence_complete_requires_all_terminal(self):
        incomplete = make_sequence(
            states=(
                ActivityState.COMPLETED,
                ActivityState.ACTIVE,
                ActivityState.NOT_STARTED,
            )
        )
        assert CompletionPolicy.is_sequence_complete(incomplete) is False

        complete = make_sequence(
            states=(
                ActivityState.COMPLETED,
                ActivityState.SKIPPED,
                ActivityState.COMPLETED,
            )
        )
        assert CompletionPolicy.is_sequence_complete(complete) is True

    def test_empty_sequence_not_complete(self):
        from app.application.learning_activity.dto.activity_sequence import (
            ActivitySequence,
        )

        empty = ActivitySequence(
            session_id="s", sequence_id="seq", activities=()
        )
        assert CompletionPolicy.is_sequence_complete(empty) is False
        assert CompletionPolicy.ready_for_session_completion(empty) is False

    def test_all_skipped_not_session_ready(self):
        sequence = make_sequence(
            states=(
                ActivityState.SKIPPED,
                ActivityState.SKIPPED,
                ActivityState.SKIPPED,
            )
        )
        assert CompletionPolicy.is_sequence_complete(sequence) is True
        assert CompletionPolicy.ready_for_session_completion(sequence) is False

    def test_ready_when_at_least_one_completed(self):
        sequence = make_sequence(
            states=(
                ActivityState.COMPLETED,
                ActivityState.SKIPPED,
                ActivityState.COMPLETED,
            )
        )
        assert CompletionPolicy.ready_for_session_completion(sequence) is True

    def test_evaluate_blockers_incomplete(self):
        sequence = make_sequence()
        result = CompletionPolicy.evaluate(sequence)
        assert result.sequence_complete is False
        assert result.ready_for_session_completion is False
        assert "sequence_incomplete" in result.blockers

    def test_evaluate_blockers_all_skipped(self):
        sequence = make_sequence(
            states=(
                ActivityState.SKIPPED,
                ActivityState.SKIPPED,
                ActivityState.SKIPPED,
            )
        )
        result = CompletionPolicy.evaluate(sequence)
        assert result.sequence_complete is True
        assert result.ready_for_session_completion is False
        assert "no_completed_activity" in result.blockers

    def test_evaluate_with_activity(self):
        sequence = make_sequence(
            states=(
                ActivityState.COMPLETED,
                ActivityState.NOT_STARTED,
                ActivityState.NOT_STARTED,
            )
        )
        result = CompletionPolicy.evaluate(
            sequence, activity=sequence.activities[0]
        )
        assert result.activity_complete is True
        assert result.activity_id == sequence.activities[0].activity_id

    def test_evaluate_activity_skipped_blocker(self):
        sequence = make_sequence(
            states=(
                ActivityState.SKIPPED,
                ActivityState.NOT_STARTED,
                ActivityState.NOT_STARTED,
            )
        )
        result = CompletionPolicy.evaluate(
            sequence, activity=sequence.activities[0]
        )
        assert "activity_skipped" in result.blockers


class TestCompletionManager:
    def test_manager_ready_signal(self):
        mgr = CompletionManager()
        sequence = make_sequence(
            states=(
                ActivityState.COMPLETED,
                ActivityState.COMPLETED,
                ActivityState.COMPLETED,
            )
        )
        assert mgr.ready_for_session_completion(sequence) is True
        result = mgr.evaluate_sequence(sequence)
        assert result.ready_for_session_completion is True
        assert result.remaining_count == 0

    def test_engine_never_completes_session(self):
        engine = make_engine()
        handle = engine.create_sequence(
            session_id="sess-1",
            activity_types=(ActivityType.INTRODUCTION, ActivityType.SUMMARY),
        )
        # Complete all activities
        handle, _ = engine.start_activity(handle)
        handle, _, _ = engine.complete_activity(handle, start_next=True)
        handle, _, result = engine.complete_activity(handle)
        assert result.sequence_complete is True
        assert engine.ready_for_session_completion(handle) is True
        # Signal only — engine has no complete_session method
        assert not hasattr(engine, "complete_session")
        assert not hasattr(engine, "complete_journey")

    def test_snapshot_includes_ready_flag(self):
        engine = make_engine()
        handle = engine.create_sequence(
            session_id="sess-1",
            activity_types=(ActivityType.INTRODUCTION,),
        )
        handle, _ = engine.start_activity(handle)
        handle, _, _ = engine.complete_activity(handle)
        snap = engine.snapshot(handle)
        assert snap.ready_for_session_completion is True
        assert snap.result is not None
        assert snap.result.ready_for_session_completion is True

    @pytest.mark.parametrize(
        "activity_type",
        [
            ActivityType.INTRODUCTION,
            ActivityType.CONCEPT_LEARNING,
            ActivityType.WORKED_EXAMPLE,
            ActivityType.GUIDED_PRACTICE,
            ActivityType.INDEPENDENT_PRACTICE,
            ActivityType.KNOWLEDGE_CHECK,
            ActivityType.REFLECTION,
            ActivityType.SUMMARY,
            ActivityType.SPACED_RECALL,
            ActivityType.NEXT_INTENTION,
            ActivityType.REVIEW,
            ActivityType.CUSTOM,
        ],
    )
    def test_all_activity_types_can_complete(self, activity_type):
        engine = make_engine()
        handle = engine.create_sequence(
            session_id="sess-1",
            activity_types=(activity_type,),
        )
        handle, _ = engine.start_activity(handle)
        handle, transition, result = engine.complete_activity(handle)
        assert transition.to_state is ActivityState.COMPLETED
        assert result.activity_complete is True
        assert result.ready_for_session_completion is True
