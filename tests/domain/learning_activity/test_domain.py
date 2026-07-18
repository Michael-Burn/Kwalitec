"""Tests for Learning Activity domain value objects and entities."""

from __future__ import annotations

import pytest

from app.domain.learning_activity.entities.activity_progress import ActivityProgress
from app.domain.learning_activity.entities.learning_activity import LearningActivity
from app.domain.learning_activity.value_objects.activity_state import (
    ActivityState,
    ActivityTransitionEvent,
    is_open_activity_state,
    is_terminal_activity_state,
    next_activity_state,
)
from app.domain.learning_activity.value_objects.activity_type import ActivityType
from tests.application.learning_activity.helpers import make_activity


class TestActivityType:
    @pytest.mark.parametrize(
        "member",
        list(ActivityType),
    )
    def test_all_catalogue_members_are_snake_case(self, member):
        assert member.value == member.value.lower()
        assert " " not in member.value

    def test_known_values_stable_count(self):
        assert len(ActivityType.known_values()) == 12

    def test_resolve_enum_passthrough(self):
        assert ActivityType.resolve(ActivityType.REVIEW) is ActivityType.REVIEW

    @pytest.mark.parametrize(
        ("raw", "expected"),
        [
            ("introduction", ActivityType.INTRODUCTION),
            ("CONCEPT_LEARNING", ActivityType.CONCEPT_LEARNING),
            ("worked-example", ActivityType.WORKED_EXAMPLE),
            ("Guided Practice", ActivityType.GUIDED_PRACTICE),
            ("future_unknown_kind", ActivityType.CUSTOM),
            ("", ActivityType.CUSTOM),
            ("  ", ActivityType.CUSTOM),
        ],
    )
    def test_resolve_maps_tokens(self, raw, expected):
        assert ActivityType.resolve(raw) is expected

    def test_unknown_future_type_does_not_raise(self):
        assert ActivityType.resolve("adaptive_simulation_v3") is ActivityType.CUSTOM


class TestActivityStateMachine:
    @pytest.mark.parametrize(
        ("state", "event", "expected"),
        [
            (
                ActivityState.NOT_STARTED,
                ActivityTransitionEvent.START,
                ActivityState.ACTIVE,
            ),
            (
                ActivityState.NOT_STARTED,
                ActivityTransitionEvent.SKIP,
                ActivityState.SKIPPED,
            ),
            (
                ActivityState.ACTIVE,
                ActivityTransitionEvent.PAUSE,
                ActivityState.PAUSED,
            ),
            (
                ActivityState.ACTIVE,
                ActivityTransitionEvent.COMPLETE,
                ActivityState.COMPLETED,
            ),
            (
                ActivityState.ACTIVE,
                ActivityTransitionEvent.SKIP,
                ActivityState.SKIPPED,
            ),
            (
                ActivityState.PAUSED,
                ActivityTransitionEvent.RESUME,
                ActivityState.ACTIVE,
            ),
            (
                ActivityState.PAUSED,
                ActivityTransitionEvent.COMPLETE,
                ActivityState.COMPLETED,
            ),
            (
                ActivityState.PAUSED,
                ActivityTransitionEvent.SKIP,
                ActivityState.SKIPPED,
            ),
        ],
    )
    def test_lawful_transitions(self, state, event, expected):
        assert next_activity_state(state, event) is expected

    @pytest.mark.parametrize(
        ("state", "event"),
        [
            (ActivityState.NOT_STARTED, ActivityTransitionEvent.PAUSE),
            (ActivityState.NOT_STARTED, ActivityTransitionEvent.RESUME),
            (ActivityState.NOT_STARTED, ActivityTransitionEvent.COMPLETE),
            (ActivityState.ACTIVE, ActivityTransitionEvent.START),
            (ActivityState.ACTIVE, ActivityTransitionEvent.RESUME),
            (ActivityState.PAUSED, ActivityTransitionEvent.START),
            (ActivityState.PAUSED, ActivityTransitionEvent.PAUSE),
            (ActivityState.COMPLETED, ActivityTransitionEvent.START),
            (ActivityState.COMPLETED, ActivityTransitionEvent.COMPLETE),
            (ActivityState.SKIPPED, ActivityTransitionEvent.SKIP),
            (ActivityState.SKIPPED, ActivityTransitionEvent.RESUME),
        ],
    )
    def test_unlawful_transitions_return_none(self, state, event):
        assert next_activity_state(state, event) is None

    @pytest.mark.parametrize(
        "state",
        [ActivityState.COMPLETED, ActivityState.SKIPPED],
    )
    def test_terminal_states(self, state):
        assert is_terminal_activity_state(state) is True
        assert is_open_activity_state(state) is False

    @pytest.mark.parametrize(
        "state",
        [
            ActivityState.NOT_STARTED,
            ActivityState.ACTIVE,
            ActivityState.PAUSED,
        ],
    )
    def test_open_states(self, state):
        assert is_open_activity_state(state) is True
        assert is_terminal_activity_state(state) is False


class TestLearningActivityEntity:
    def test_create_defaults(self):
        activity = make_activity()
        assert activity.state is ActivityState.NOT_STARTED
        assert activity.activity_type is ActivityType.CONCEPT_LEARNING
        assert activity.is_terminal is False
        assert activity.is_active is False

    def test_create_rejects_empty_id(self):
        with pytest.raises(ValueError, match="activity_id"):
            LearningActivity.create("", "sess-1", ActivityType.REVIEW)

    def test_create_rejects_empty_session(self):
        with pytest.raises(ValueError, match="session_id"):
            LearningActivity.create("a1", "  ", ActivityType.REVIEW)

    def test_create_rejects_negative_index(self):
        with pytest.raises(ValueError, match="sequence_index"):
            LearningActivity.create(
                "a1", "s1", ActivityType.REVIEW, sequence_index=-1
            )

    def test_create_resolves_unknown_type_to_custom(self):
        activity = LearningActivity.create("a1", "s1", "brand_new_type")
        assert activity.activity_type is ActivityType.CUSTOM

    def test_apply_transition_start(self):
        activity = make_activity().apply_transition(ActivityTransitionEvent.START)
        assert activity.state is ActivityState.ACTIVE
        assert activity.is_active is True

    def test_apply_transition_invalid_raises(self):
        activity = make_activity()
        with pytest.raises(ValueError, match="invalid activity transition"):
            activity.apply_transition(ActivityTransitionEvent.PAUSE)

    def test_with_evidence_append_only(self):
        activity = make_activity().with_evidence("e1").with_evidence("e2")
        assert activity.evidence_ids == ("e1", "e2")

    def test_with_evidence_dedupes(self):
        activity = make_activity().with_evidence("e1").with_evidence("e1")
        assert activity.evidence_ids == ("e1",)

    def test_with_reflection_append_only(self):
        activity = make_activity().with_reflection("r1").with_reflection("r2")
        assert activity.reflection_ids == ("r1", "r2")

    def test_with_reflection_dedupes(self):
        activity = make_activity().with_reflection("r1").with_reflection("r1")
        assert activity.reflection_ids == ("r1",)

    def test_with_evidence_rejects_empty(self):
        with pytest.raises(ValueError, match="evidence_id"):
            make_activity().with_evidence("  ")

    def test_terminal_after_complete(self):
        activity = (
            make_activity()
            .apply_transition(ActivityTransitionEvent.START)
            .apply_transition(ActivityTransitionEvent.COMPLETE)
        )
        assert activity.is_terminal is True
        assert activity.state is ActivityState.COMPLETED

    def test_frozen(self):
        activity = make_activity()
        with pytest.raises(Exception):
            activity.state = ActivityState.ACTIVE  # type: ignore[misc]


class TestActivityProgress:
    def test_empty(self):
        progress = ActivityProgress.empty("sess-1")
        assert progress.total_count == 0
        assert progress.progress_percentage == 0.0
        assert progress.current_index == -1

    def test_frozen(self):
        progress = ActivityProgress.empty("sess-1")
        with pytest.raises(Exception):
            progress.total_count = 1  # type: ignore[misc]
