"""Learning Activity Engine facade integration tests."""

from __future__ import annotations

import pytest

from app.application.learning_activity.exceptions import (
    ActivityNotFound,
    InvalidActivityState,
)
from app.domain.learning_activity.value_objects.activity_state import ActivityState
from app.domain.learning_activity.value_objects.activity_type import ActivityType
from tests.application.learning_activity.helpers import make_engine, make_handle


class TestEngineCreateAndAdvance:
    def test_create_sequence_default(self):
        engine = make_engine()
        handle = engine.create_sequence(session_id="sess-1")
        assert handle.sequence.length > 0
        assert handle.plan is not None
        assert all(
            a.state is ActivityState.NOT_STARTED for a in handle.sequence.activities
        )

    def test_plan_without_sequence(self):
        engine = make_engine()
        plan = engine.plan_activities(
            session_id="sess-1",
            activity_types=(ActivityType.REVIEW,),
        )
        assert len(plan.items) == 1

    def test_advance_starts_first(self):
        engine = make_engine()
        handle = make_handle(engine)
        handle = engine.advance_activity(handle)
        current = engine.current_activity(handle)
        assert current is not None
        assert current.state is ActivityState.ACTIVE
        assert current.sequence_index == 0

    def test_advance_completes_and_starts_next(self):
        engine = make_engine()
        handle = make_handle(engine, start_first=True)
        handle = engine.advance_activity(handle)
        current = engine.current_activity(handle)
        assert current is not None
        assert current.sequence_index == 1
        assert handle.sequence.activities[0].state is ActivityState.COMPLETED

    def test_advance_at_end_leaves_completed(self):
        engine = make_engine()
        handle = engine.create_sequence(
            session_id="sess-1",
            activity_types=(ActivityType.INTRODUCTION,),
        )
        handle = engine.advance_activity(handle)
        handle = engine.advance_activity(handle)
        assert engine.current_activity(handle) is None
        assert engine.ready_for_session_completion(handle) is True

    def test_complete_all_via_loop(self):
        engine = make_engine()
        handle = make_handle(
            engine,
            types=(
                ActivityType.INTRODUCTION,
                ActivityType.CONCEPT_LEARNING,
                ActivityType.SUMMARY,
            ),
        )
        for _ in range(3):
            handle = engine.advance_activity(handle)
        # After three advances from not-started: start, complete+start, complete+start
        # Need one more to complete last
        handle = engine.advance_activity(handle)
        result = engine.evaluate_completion(handle)
        assert result.sequence_complete is True
        assert result.ready_for_session_completion is True

    def test_snapshot_fields(self):
        engine = make_engine()
        handle = make_handle(engine, start_first=True)
        snap = engine.snapshot(handle)
        assert snap.session_id == "sess-1"
        assert snap.current_state is ActivityState.ACTIVE
        assert snap.progress.total_count == 5
        assert snap.next_activity is not None
        assert snap.previous_activity is None

    def test_rehydrate(self):
        engine = make_engine()
        handle = make_handle(engine, start_first=True)
        rebuilt = engine.rehydrate(handle.sequence, plan=handle.plan)
        assert rebuilt.sequence.sequence_id == handle.sequence.sequence_id
        assert engine.current_activity(rebuilt).state is ActivityState.ACTIVE

    def test_validate_ok(self):
        engine = make_engine()
        handle = make_handle(engine)
        engine.validate(handle)

    def test_start_named_activity(self):
        engine = make_engine()
        handle = make_handle(engine)
        second = handle.sequence.activities[1]
        # Must not start second while... actually first isn't active, so OK
        # But starting second while first is not_started is fine for single-active
        handle, transition = engine.start_activity(
            handle, activity_id=second.activity_id
        )
        assert transition.to_state is ActivityState.ACTIVE
        assert engine.current_activity(handle).activity_id == second.activity_id

    def test_operations_require_current_when_no_id(self):
        engine = make_engine()
        handle = engine.create_sequence(
            session_id="sess-1",
            activity_types=(ActivityType.INTRODUCTION,),
        )
        handle, _ = engine.start_activity(handle)
        handle, _, _ = engine.complete_activity(handle)
        with pytest.raises(InvalidActivityState, match="No current activity"):
            engine.pause_activity(handle)

    def test_unknown_activity_id(self):
        engine = make_engine()
        handle = make_handle(engine)
        with pytest.raises(ActivityNotFound):
            engine.start_activity(handle, activity_id="nope")

    def test_skip_without_start_next(self):
        engine = make_engine()
        handle = make_handle(engine)
        handle, _ = engine.start_activity(handle)
        handle, _ = engine.skip_activity(handle, start_next=False)
        current = engine.current_activity(handle)
        # Next NOT_STARTED becomes current focus
        assert current is not None
        assert current.state is ActivityState.NOT_STARTED

    def test_complete_without_start_next(self):
        engine = make_engine()
        handle = make_handle(engine, start_first=True)
        handle, _, result = engine.complete_activity(handle, start_next=False)
        assert result.activity_complete is True
        current = engine.current_activity(handle)
        assert current is not None
        assert current.state is ActivityState.NOT_STARTED

    @pytest.mark.parametrize(
        "types",
        [
            (ActivityType.INTRODUCTION, ActivityType.SUMMARY),
            (ActivityType.SPACED_RECALL, ActivityType.REVIEW, ActivityType.CUSTOM),
            (
                ActivityType.WORKED_EXAMPLE,
                ActivityType.GUIDED_PRACTICE,
                ActivityType.INDEPENDENT_PRACTICE,
                ActivityType.KNOWLEDGE_CHECK,
            ),
            (ActivityType.NEXT_INTENTION,),
        ],
    )
    def test_full_happy_path_various_sequences(self, types):
        engine = make_engine()
        handle = engine.create_sequence(
            session_id="sess-1", activity_types=types
        )
        handle, _ = engine.start_activity(handle)
        while True:
            current = engine.current_activity(handle)
            if current is None:
                break
            if current.state is ActivityState.NOT_STARTED:
                handle, _ = engine.start_activity(handle)
            handle = engine.route_evidence(
                handle, evidence_id=f"ev-{current.sequence_index}"
            )
            handle, _, _ = engine.complete_activity(handle, start_next=True)
        assert engine.ready_for_session_completion(handle) is True
        snap = engine.snapshot(handle)
        assert snap.progress.progress_percentage == 100.0
