"""Activity validator tests."""

from __future__ import annotations

import pytest

from app.application.learning_activity.dto.activity_sequence import ActivitySequence
from app.application.learning_activity.exceptions import ValidationError
from app.application.learning_activity.validator import ActivityValidator
from app.domain.learning_activity.value_objects.activity_state import (
    ActivityState,
    ActivityTransitionEvent,
)
from app.domain.learning_activity.value_objects.activity_type import ActivityType
from tests.application.learning_activity.helpers import make_activity, make_sequence


class TestActivityValidator:
    def test_valid_sequence(self):
        result = ActivityValidator().validate(make_sequence())
        assert result.is_valid is True
        assert result.issues == ()

    def test_duplicate_ids(self):
        a0 = make_activity("dup", sequence_index=0)
        a1 = make_activity(
            "dup",
            sequence_index=1,
            activity_type=ActivityType.SUMMARY,
        )
        sequence = ActivitySequence(
            session_id="sess-1",
            sequence_id="seq-1",
            activities=(a0, a1),
        )
        result = ActivityValidator().validate(sequence)
        assert result.is_valid is False
        assert "duplicate_id" in result.codes

    def test_duplicate_indices(self):
        a0 = make_activity("a0", sequence_index=0)
        a1 = make_activity(
            "a1",
            sequence_index=0,
            activity_type=ActivityType.SUMMARY,
        )
        sequence = ActivitySequence(
            session_id="sess-1",
            sequence_id="seq-1",
            activities=(a0, a1),
        )
        result = ActivityValidator().validate(sequence)
        assert "duplicate_index" in result.codes

    def test_multiple_active(self):
        sequence = make_sequence(
            states=(
                ActivityState.ACTIVE,
                ActivityState.ACTIVE,
                ActivityState.NOT_STARTED,
            )
        )
        result = ActivityValidator().validate(sequence)
        assert "multiple_active" in result.codes

    def test_allow_multiple_active(self):
        sequence = make_sequence(
            states=(
                ActivityState.ACTIVE,
                ActivityState.ACTIVE,
                ActivityState.NOT_STARTED,
            )
        )
        result = ActivityValidator().validate(
            sequence, allow_multiple_active=True
        )
        assert "multiple_active" not in result.codes

    def test_session_mismatch(self):
        a0 = make_activity("a0", session_id="other")
        sequence = ActivitySequence(
            session_id="sess-1",
            sequence_id="seq-1",
            activities=(a0,),
        )
        result = ActivityValidator().validate(sequence)
        assert "session_mismatch" in result.codes

    def test_empty_session_id(self):
        sequence = ActivitySequence(
            session_id="",
            sequence_id="seq-1",
            activities=(make_activity(),),
        )
        result = ActivityValidator().validate(sequence)
        assert "empty_session_id" in result.codes

    def test_empty_sequence_id(self):
        sequence = ActivitySequence(
            session_id="sess-1",
            sequence_id="  ",
            activities=(make_activity(),),
        )
        result = ActivityValidator().validate(sequence)
        assert "empty_sequence_id" in result.codes

    def test_index_gap(self):
        a0 = make_activity("a0", sequence_index=0)
        a1 = make_activity(
            "a1",
            sequence_index=2,
            activity_type=ActivityType.SUMMARY,
        )
        sequence = ActivitySequence(
            session_id="sess-1",
            sequence_id="seq-1",
            activities=(a0, a1),
        )
        result = ActivityValidator().validate(sequence)
        assert "index_gap" in result.codes

    def test_order_mismatch(self):
        a0 = make_activity("a0", sequence_index=1)
        a1 = make_activity(
            "a1",
            sequence_index=0,
            activity_type=ActivityType.SUMMARY,
        )
        sequence = ActivitySequence(
            session_id="sess-1",
            sequence_id="seq-1",
            activities=(a0, a1),
        )
        result = ActivityValidator().validate(sequence)
        assert "order_mismatch" in result.codes

    def test_assert_valid_raises(self):
        sequence = make_sequence(
            states=(
                ActivityState.ACTIVE,
                ActivityState.ACTIVE,
                ActivityState.NOT_STARTED,
            )
        )
        with pytest.raises(ValidationError, match="multiple_active"):
            ActivityValidator().assert_valid(sequence)

    def test_assert_transition_lawful(self):
        ActivityValidator().assert_transition_lawful(
            ActivityState.NOT_STARTED, ActivityTransitionEvent.START
        )
        with pytest.raises(ValidationError, match="Invalid transition"):
            ActivityValidator().assert_transition_lawful(
                ActivityState.NOT_STARTED, ActivityTransitionEvent.PAUSE
            )

    @pytest.mark.parametrize(
        "event",
        [
            ActivityTransitionEvent.START,
            ActivityTransitionEvent.SKIP,
        ],
    )
    def test_lawful_from_not_started(self, event):
        ActivityValidator().assert_transition_lawful(
            ActivityState.NOT_STARTED, event
        )
