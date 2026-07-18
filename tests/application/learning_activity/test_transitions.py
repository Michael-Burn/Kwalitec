"""Activity transition manager and policy tests."""

from __future__ import annotations

import pytest

from app.application.learning_activity.exceptions import (
    ActivityAlreadyCompleted,
    ActivityAlreadySkipped,
    ActivityNotFound,
    TransitionError,
)
from app.application.learning_activity.policies.transition_policy import (
    TransitionPolicy,
)
from app.application.learning_activity.transition_manager import TransitionManager
from app.domain.learning_activity.value_objects.activity_state import (
    ActivityState,
    ActivityTransitionEvent,
)
from app.domain.learning_activity.value_objects.activity_type import ActivityType
from tests.application.learning_activity.helpers import make_engine, make_sequence


class TestTransitionPolicy:
    @pytest.mark.parametrize(
        ("state", "event", "ok"),
        [
            (ActivityState.NOT_STARTED, ActivityTransitionEvent.START, True),
            (ActivityState.NOT_STARTED, ActivityTransitionEvent.SKIP, True),
            (ActivityState.NOT_STARTED, ActivityTransitionEvent.COMPLETE, False),
            (ActivityState.ACTIVE, ActivityTransitionEvent.PAUSE, True),
            (ActivityState.ACTIVE, ActivityTransitionEvent.COMPLETE, True),
            (ActivityState.ACTIVE, ActivityTransitionEvent.START, False),
            (ActivityState.PAUSED, ActivityTransitionEvent.RESUME, True),
            (ActivityState.COMPLETED, ActivityTransitionEvent.COMPLETE, False),
            (ActivityState.SKIPPED, ActivityTransitionEvent.START, False),
        ],
    )
    def test_is_lawful(self, state, event, ok):
        assert TransitionPolicy.is_lawful(state, event) is ok

    def test_allowed_events_not_started(self):
        events = TransitionPolicy.allowed_events(ActivityState.NOT_STARTED)
        assert ActivityTransitionEvent.START in events
        assert ActivityTransitionEvent.SKIP in events
        assert ActivityTransitionEvent.PAUSE not in events

    def test_allowed_events_active(self):
        events = TransitionPolicy.allowed_events(ActivityState.ACTIVE)
        assert set(events) == {
            ActivityTransitionEvent.PAUSE,
            ActivityTransitionEvent.COMPLETE,
            ActivityTransitionEvent.SKIP,
        }

    def test_allowed_events_paused(self):
        events = TransitionPolicy.allowed_events(ActivityState.PAUSED)
        assert set(events) == {
            ActivityTransitionEvent.RESUME,
            ActivityTransitionEvent.COMPLETE,
            ActivityTransitionEvent.SKIP,
        }

    def test_allowed_events_terminal_empty(self):
        assert TransitionPolicy.allowed_events(ActivityState.COMPLETED) == ()
        assert TransitionPolicy.allowed_events(ActivityState.SKIPPED) == ()

    def test_rejects_invalid_transitions(self):
        assert TransitionPolicy.rejects_invalid_transitions() is True

    @pytest.mark.parametrize(
        "state",
        [ActivityState.COMPLETED, ActivityState.SKIPPED],
    )
    def test_is_terminal(self, state):
        assert TransitionPolicy.is_terminal(state) is True


class TestTransitionManager:
    def test_start_pause_resume_complete(self):
        mgr = TransitionManager()
        sequence = make_sequence()
        aid = sequence.activities[0].activity_id

        started = mgr.start(sequence, aid)
        assert started.activity.state is ActivityState.ACTIVE
        assert started.transition.event is ActivityTransitionEvent.START

        paused = mgr.pause(started.sequence, aid)
        assert paused.activity.state is ActivityState.PAUSED

        resumed = mgr.resume(paused.sequence, aid)
        assert resumed.activity.state is ActivityState.ACTIVE

        completed = mgr.complete(resumed.sequence, aid)
        assert completed.activity.state is ActivityState.COMPLETED
        assert completed.transition.from_state is ActivityState.ACTIVE
        assert completed.transition.to_state is ActivityState.COMPLETED

    def test_skip_from_not_started(self):
        mgr = TransitionManager()
        sequence = make_sequence()
        aid = sequence.activities[0].activity_id
        result = mgr.skip(sequence, aid)
        assert result.activity.state is ActivityState.SKIPPED

    def test_skip_from_active(self):
        mgr = TransitionManager()
        sequence = make_sequence()
        aid = sequence.activities[0].activity_id
        started = mgr.start(sequence, aid)
        skipped = mgr.skip(started.sequence, aid)
        assert skipped.activity.state is ActivityState.SKIPPED

    def test_complete_from_paused(self):
        mgr = TransitionManager()
        sequence = make_sequence()
        aid = sequence.activities[0].activity_id
        started = mgr.start(sequence, aid)
        paused = mgr.pause(started.sequence, aid)
        completed = mgr.complete(paused.sequence, aid)
        assert completed.activity.state is ActivityState.COMPLETED

    def test_cannot_start_when_another_active(self):
        mgr = TransitionManager()
        sequence = make_sequence()
        a0 = sequence.activities[0].activity_id
        a1 = sequence.activities[1].activity_id
        started = mgr.start(sequence, a0)
        with pytest.raises(TransitionError, match="already ACTIVE"):
            mgr.start(started.sequence, a1)

    def test_allow_multiple_active_flag(self):
        mgr = TransitionManager()
        sequence = make_sequence()
        a0 = sequence.activities[0].activity_id
        a1 = sequence.activities[1].activity_id
        started = mgr.start(sequence, a0)
        second = mgr.start(
            started.sequence, a1, allow_multiple_active=True
        )
        active = [
            a
            for a in second.sequence.activities
            if a.state is ActivityState.ACTIVE
        ]
        assert len(active) == 2

    def test_unknown_activity_raises(self):
        mgr = TransitionManager()
        with pytest.raises(ActivityNotFound):
            mgr.start(make_sequence(), "missing")

    def test_already_completed_raises(self):
        mgr = TransitionManager()
        sequence = make_sequence(
            states=(
                ActivityState.COMPLETED,
                ActivityState.NOT_STARTED,
                ActivityState.NOT_STARTED,
            )
        )
        with pytest.raises(ActivityAlreadyCompleted):
            mgr.start(sequence, sequence.activities[0].activity_id)

    def test_already_skipped_raises(self):
        mgr = TransitionManager()
        sequence = make_sequence(
            states=(
                ActivityState.SKIPPED,
                ActivityState.NOT_STARTED,
                ActivityState.NOT_STARTED,
            )
        )
        with pytest.raises(ActivityAlreadySkipped):
            mgr.skip(sequence, sequence.activities[0].activity_id)

    def test_invalid_pause_raises(self):
        mgr = TransitionManager()
        sequence = make_sequence()
        with pytest.raises(TransitionError):
            mgr.pause(sequence, sequence.activities[0].activity_id)

    def test_engine_pause_resume(self):
        engine = make_engine()
        handle = engine.create_sequence(
            session_id="sess-1",
            activity_types=(ActivityType.INTRODUCTION, ActivityType.SUMMARY),
        )
        handle, _ = engine.start_activity(handle)
        handle, transition = engine.pause_activity(handle)
        assert transition.to_state is ActivityState.PAUSED
        handle, transition = engine.resume_activity(handle)
        assert transition.to_state is ActivityState.ACTIVE

    def test_engine_skip(self):
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
        handle, transition = engine.skip_activity(handle)
        assert transition.to_state is ActivityState.SKIPPED
        current = engine.current_activity(handle)
        assert current is not None
        assert current.state is ActivityState.ACTIVE
