"""Tests for session selection and session plans."""

from __future__ import annotations

import pytest

from app.application.learning_journey.exceptions import InvalidJourneyState
from app.application.learning_journey.session_selector import SessionSelector
from app.domain.learning_journey.entities.learning_objective import ObjectiveKind
from app.domain.learning_journey.value_objects.effort_estimate import EffortEstimate
from app.domain.learning_journey.value_objects.journey_state import JourneyState
from app.domain.learning_journey.value_objects.session_state import SessionState
from tests.application.learning_journey.helpers import (
    make_journey,
    make_objective,
    make_session,
)


class TestSessionSelector:
    def test_current_prefers_active(self) -> None:
        selector = SessionSelector()
        journey = make_journey(
            state=JourneyState.ACTIVE,
            sessions=[
                make_session("s1", sequence_index=0, state=SessionState.PAUSED),
                make_session("s2", sequence_index=1, state=SessionState.ACTIVE),
            ],
        )
        assert selector.current_session(journey).session_id == "s2"

    def test_current_falls_back_to_paused(self) -> None:
        selector = SessionSelector()
        journey = make_journey(
            state=JourneyState.ACTIVE,
            sessions=[
                make_session("s1", sequence_index=0, state=SessionState.COMPLETED),
                make_session("s2", sequence_index=1, state=SessionState.PAUSED),
            ],
        )
        assert selector.current_session(journey).session_id == "s2"

    def test_next_returns_first_not_started(self) -> None:
        selector = SessionSelector()
        journey = make_journey(
            state=JourneyState.ACTIVE,
            sessions=[
                make_session("s1", sequence_index=0, state=SessionState.COMPLETED),
                make_session("s2", sequence_index=1, state=SessionState.NOT_STARTED),
                make_session("s3", sequence_index=2, state=SessionState.NOT_STARTED),
            ],
        )
        assert selector.next_session(journey).session_id == "s2"

    def test_next_prefers_active_over_not_started(self) -> None:
        selector = SessionSelector()
        journey = make_journey(
            state=JourneyState.ACTIVE,
            sessions=[
                make_session("s1", sequence_index=0, state=SessionState.ACTIVE),
                make_session("s2", sequence_index=1, state=SessionState.NOT_STARTED),
            ],
        )
        assert selector.next_session(journey).session_id == "s1"

    def test_next_raises_on_completed_journey(self) -> None:
        selector = SessionSelector()
        journey = make_journey(state=JourneyState.COMPLETED)
        with pytest.raises(InvalidJourneyState):
            selector.next_session(journey)

    def test_next_raises_on_deferred(self) -> None:
        selector = SessionSelector()
        with pytest.raises(InvalidJourneyState):
            selector.next_session(make_journey(state=JourneyState.DEFERRED))

    def test_next_raises_on_abandoned(self) -> None:
        selector = SessionSelector()
        with pytest.raises(InvalidJourneyState):
            selector.next_session(make_journey(state=JourneyState.ABANDONED))

    def test_build_plan_for_existing(self) -> None:
        selector = SessionSelector()
        journey = make_journey(
            state=JourneyState.ACTIVE,
            objectives=[make_objective("obj-1")],
            sessions=[
                make_session(
                    "s1",
                    state=SessionState.NOT_STARTED,
                    objective_id="obj-1",
                    effort=EffortEstimate.HIGH,
                )
            ],
        )
        plan = selector.build_session_plan(journey)
        assert plan is not None
        assert plan.session_id == "s1"
        assert plan.expected_effort == EffortEstimate.HIGH
        assert plan.session_number == 1
        assert "read_core_notes" in plan.recommended_activities

    def test_build_plan_activities_by_kind(self) -> None:
        selector = SessionSelector()
        for kind, expected_tag in [
            (ObjectiveKind.APPLY, "worked_example"),
            (ObjectiveKind.ANALYSE, "compare_approaches"),
            (ObjectiveKind.REVIEW, "spaced_review"),
            (ObjectiveKind.REVISE, "targeted_revision"),
        ]:
            journey = make_journey(
                state=JourneyState.ACTIVE,
                objectives=[make_objective("obj-x", kind=kind)],
                sessions=[
                    make_session(
                        "s1",
                        state=SessionState.NOT_STARTED,
                        objective_id="obj-x",
                    )
                ],
            )
            plan = selector.build_session_plan(journey)
            assert expected_tag in plan.recommended_activities

    def test_plan_new_session_when_none_pending(self) -> None:
        selector = SessionSelector()
        journey = make_journey(
            state=JourneyState.ACTIVE,
            objectives=[make_objective("obj-1")],
            sessions=[
                make_session("s1", state=SessionState.COMPLETED, objective_id="obj-1")
            ],
        )
        plan = selector.build_session_plan(journey)
        assert plan is not None
        assert plan.is_existing_session is False
        assert plan.session_id is None
        assert plan.sequence_index == 1

    def test_plan_none_for_terminal(self) -> None:
        selector = SessionSelector()
        assert selector.build_session_plan(
            make_journey(state=JourneyState.COMPLETED)
        ) is None

    def test_paused_journey_plan_only_paused_session(self) -> None:
        selector = SessionSelector()
        journey = make_journey(
            state=JourneyState.PAUSED,
            sessions=[
                make_session("s1", state=SessionState.PAUSED, objective_id="obj-1")
            ],
            objectives=[make_objective()],
        )
        plan = selector.build_session_plan(journey)
        assert plan is not None
        assert plan.session_id == "s1"

    def test_paused_without_session_returns_none(self) -> None:
        selector = SessionSelector()
        journey = make_journey(state=JourneyState.PAUSED)
        assert selector.build_session_plan(journey) is None

    def test_deterministic_ordering(self) -> None:
        selector = SessionSelector()
        journey = make_journey(
            state=JourneyState.ACTIVE,
            sessions=[
                make_session("s3", sequence_index=2, state=SessionState.NOT_STARTED),
                make_session("s1", sequence_index=0, state=SessionState.NOT_STARTED),
                make_session("s2", sequence_index=1, state=SessionState.NOT_STARTED),
            ],
        )
        first = selector.next_session(journey)
        second = selector.next_session(journey)
        assert first.session_id == second.session_id == "s1"

    def test_current_none_when_empty(self) -> None:
        selector = SessionSelector()
        assert selector.current_session(make_journey(state=JourneyState.ACTIVE)) is None
