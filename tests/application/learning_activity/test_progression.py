"""Activity progression manager and policy tests."""

from __future__ import annotations

import pytest

from app.application.learning_activity.policies.progression_policy import (
    ProgressionPolicy,
)
from app.application.learning_activity.progression_manager import ProgressionManager
from app.domain.learning_activity.value_objects.activity_state import ActivityState
from app.domain.learning_activity.value_objects.activity_type import ActivityType
from tests.application.learning_activity.helpers import make_engine, make_sequence


class TestProgressionPolicy:
    def test_current_prefers_active(self):
        sequence = make_sequence(
            states=(
                ActivityState.COMPLETED,
                ActivityState.ACTIVE,
                ActivityState.NOT_STARTED,
            )
        )
        current = ProgressionPolicy.current_activity(sequence)
        assert current is not None
        assert current.sequence_index == 1

    def test_current_prefers_paused_over_not_started(self):
        sequence = make_sequence(
            states=(
                ActivityState.PAUSED,
                ActivityState.NOT_STARTED,
                ActivityState.NOT_STARTED,
            )
        )
        current = ProgressionPolicy.current_activity(sequence)
        assert current is not None
        assert current.state is ActivityState.PAUSED

    def test_current_first_not_started(self):
        sequence = make_sequence()
        current = ProgressionPolicy.current_activity(sequence)
        assert current is not None
        assert current.sequence_index == 0

    def test_current_none_when_all_terminal(self):
        sequence = make_sequence(
            states=(
                ActivityState.COMPLETED,
                ActivityState.SKIPPED,
                ActivityState.COMPLETED,
            )
        )
        assert ProgressionPolicy.current_activity(sequence) is None

    def test_completed_and_skipped(self):
        sequence = make_sequence(
            states=(
                ActivityState.COMPLETED,
                ActivityState.SKIPPED,
                ActivityState.NOT_STARTED,
            )
        )
        assert len(ProgressionPolicy.completed_activities(sequence)) == 1
        assert len(ProgressionPolicy.skipped_activities(sequence)) == 1
        assert len(ProgressionPolicy.remaining_activities(sequence)) == 1

    def test_next_after_current(self):
        sequence = make_sequence(
            states=(
                ActivityState.ACTIVE,
                ActivityState.NOT_STARTED,
                ActivityState.NOT_STARTED,
            )
        )
        nxt = ProgressionPolicy.next_activity(sequence)
        assert nxt is not None
        assert nxt.sequence_index == 1

    def test_next_none_at_end(self):
        sequence = make_sequence(
            states=(
                ActivityState.COMPLETED,
                ActivityState.COMPLETED,
                ActivityState.ACTIVE,
            )
        )
        assert ProgressionPolicy.next_activity(sequence) is None

    def test_previous(self):
        sequence = make_sequence(
            states=(
                ActivityState.COMPLETED,
                ActivityState.ACTIVE,
                ActivityState.NOT_STARTED,
            )
        )
        prev = ProgressionPolicy.previous_activity(sequence)
        assert prev is not None
        assert prev.sequence_index == 0

    def test_previous_none_at_start(self):
        sequence = make_sequence()
        assert ProgressionPolicy.previous_activity(sequence) is None

    @pytest.mark.parametrize(
        ("states", "expected"),
        [
            (
                (
                    ActivityState.NOT_STARTED,
                    ActivityState.NOT_STARTED,
                    ActivityState.NOT_STARTED,
                ),
                0.0,
            ),
            (
                (
                    ActivityState.COMPLETED,
                    ActivityState.NOT_STARTED,
                    ActivityState.NOT_STARTED,
                ),
                33.33,
            ),
            (
                (
                    ActivityState.COMPLETED,
                    ActivityState.SKIPPED,
                    ActivityState.NOT_STARTED,
                ),
                66.67,
            ),
            (
                (
                    ActivityState.COMPLETED,
                    ActivityState.COMPLETED,
                    ActivityState.SKIPPED,
                ),
                100.0,
            ),
        ],
    )
    def test_progress_percentage(self, states, expected):
        sequence = make_sequence(states=states)
        assert ProgressionPolicy.progress_percentage(sequence) == expected

    def test_progress_percentage_empty(self):
        from app.application.learning_activity.dto.activity_sequence import (
            ActivitySequence,
        )

        empty = ActivitySequence(
            session_id="s", sequence_id="seq", activities=()
        )
        assert ProgressionPolicy.progress_percentage(empty) == 0.0

    def test_build_progress(self):
        sequence = make_sequence(
            states=(
                ActivityState.COMPLETED,
                ActivityState.ACTIVE,
                ActivityState.NOT_STARTED,
            )
        )
        progress = ProgressionPolicy.build_progress(sequence)
        assert progress.total_count == 3
        assert progress.completed_count == 1
        assert progress.remaining_count == 2
        assert progress.current_index == 1
        assert progress.progress_percentage == 33.33


class TestProgressionManager:
    def test_manager_delegates(self):
        mgr = ProgressionManager()
        sequence = make_sequence(
            states=(
                ActivityState.COMPLETED,
                ActivityState.ACTIVE,
                ActivityState.NOT_STARTED,
            )
        )
        assert mgr.current(sequence).sequence_index == 1
        assert len(mgr.completed(sequence)) == 1
        assert len(mgr.remaining(sequence)) == 2
        assert mgr.percentage(sequence) == 33.33
        assert mgr.next(sequence).sequence_index == 2
        assert mgr.previous(sequence).sequence_index == 0

    def test_engine_navigation(self):
        engine = make_engine()
        handle = engine.create_sequence(
            session_id="sess-1",
            activity_types=(
                ActivityType.INTRODUCTION,
                ActivityType.CONCEPT_LEARNING,
                ActivityType.SUMMARY,
            ),
        )
        handle, _ = engine.start_activity(handle)
        assert engine.previous_activity(handle) is None
        nxt = engine.next_activity(handle)
        assert nxt is not None
        assert nxt.activity_type is ActivityType.CONCEPT_LEARNING

        handle, _, _ = engine.complete_activity(handle, start_next=True)
        assert engine.current_activity(handle).activity_type is (
            ActivityType.CONCEPT_LEARNING
        )
        assert engine.previous_activity(handle).activity_type is (
            ActivityType.INTRODUCTION
        )
