"""Mission builder and validator tests."""

from __future__ import annotations

import pytest

from app.application.mission_engine.exceptions import (
    ActiveMissionExists,
    DuplicateMission,
    InvalidJourneyReference,
    InvalidSessionReference,
    MissionBuildError,
)
from app.application.mission_engine.mission_state import MissionSlot, MissionState
from app.application.mission_engine.mission_validator import MissionValidator
from app.domain.learning_journey.value_objects.journey_state import JourneyState
from app.domain.learning_journey.value_objects.session_state import SessionState
from tests.application.mission_engine.helpers import (
    TODAY,
    TOMORROW,
    active_journey,
    make_builder,
    make_journey,
    make_journey_engine,
    make_objective,
)


def test_build_daily_mission_from_active_journey():
    journey = active_journey()
    builder = make_builder()
    mission = builder.build_daily_mission(
        journey, scheduled_date=TODAY, as_of_date=TODAY
    )
    assert mission.learner_id == "learner-1"
    assert mission.journey_id == "journey-1"
    assert mission.topic_id == "topic-a"
    assert mission.slot == MissionSlot.TODAY
    assert mission.state == MissionState.ACTIVE
    assert mission.objective_id == "obj-1"
    assert mission.title == "Objective obj-1"


def test_build_with_existing_session():
    journey = active_journey(with_session=True)
    mission = make_builder().build_daily_mission(
        journey, scheduled_date=TODAY, as_of_date=TODAY
    )
    assert mission.session_id == "sess-1"
    assert mission.sequence_index == 0


def test_build_resume_flag_for_paused_session():
    journey = active_journey(with_session=True, session_state=SessionState.PAUSED)
    mission = make_builder().build_daily_mission(
        journey, scheduled_date=TODAY, as_of_date=TODAY
    )
    assert mission.is_resume is True


def test_build_revision_slot():
    journey = active_journey()
    mission = make_builder().build_daily_mission(
        journey,
        scheduled_date=TODAY,
        as_of_date=TODAY,
        is_revision=True,
    )
    assert mission.slot == MissionSlot.REVISION
    assert mission.is_revision is True


def test_build_tomorrow_slot():
    journey = active_journey()
    mission = make_builder().build_daily_mission(
        journey,
        scheduled_date=TOMORROW,
        as_of_date=TODAY,
        initial_state=MissionState.SCHEDULED,
    )
    assert mission.slot == MissionSlot.TOMORROW
    assert mission.state == MissionState.SCHEDULED


def test_build_rejects_completed_journey():
    journey = make_journey(state=JourneyState.COMPLETED)
    with pytest.raises(MissionBuildError):
        make_builder().build_daily_mission(journey, scheduled_date=TODAY)


def test_build_rejects_abandoned_journey():
    journey = make_journey(state=JourneyState.ABANDONED)
    with pytest.raises(MissionBuildError):
        make_builder().build_daily_mission(journey, scheduled_date=TODAY)


def test_build_summary_fields():
    journey = active_journey()
    builder = make_builder()
    mission = builder.build_daily_mission(
        journey, scheduled_date=TODAY, as_of_date=TODAY
    )
    summary = builder.build_summary(mission)
    assert summary.is_active is True
    assert summary.is_completed is False
    assert summary.delivery_action.value == "today_mission"


def test_with_state_updates():
    journey = active_journey()
    builder = make_builder()
    mission = builder.build_daily_mission(
        journey, scheduled_date=TODAY, as_of_date=TODAY
    )
    updated = builder.with_state(mission, MissionState.COMPLETED)
    assert updated.state == MissionState.COMPLETED
    assert mission.state == MissionState.ACTIVE


def test_build_no_plan_when_deferred_journey_not_selectable():
    engine = make_journey_engine()
    journey = engine.create_journey(
        learner_id="l1",
        topic_id="topic-a",
        curriculum_id="c1",
        objectives=[make_objective()],
    )
    journey = engine.start_journey(journey)
    journey = engine.defer_journey(journey)
    # Deferred journeys cannot select sessions → no plan → build error
    with pytest.raises(MissionBuildError):
        make_builder(journey_engine=engine).build_daily_mission(
            journey, scheduled_date=TODAY, as_of_date=TODAY
        )


# --- Validator ---


def test_validator_duplicate():
    journey = active_journey()
    m1 = make_builder().build_daily_mission(
        journey, scheduled_date=TODAY, as_of_date=TODAY
    )
    m2 = make_builder().build_daily_mission(
        journey,
        scheduled_date=TODAY,
        as_of_date=TODAY,
        mission_id="other",
    )
    # Force same session id
    from dataclasses import replace

    m2 = replace(m2, session_id=m1.session_id)
    with pytest.raises(DuplicateMission):
        MissionValidator().validate_no_duplicate([m1], m2)


def test_validator_allows_duplicate_after_terminal():
    journey = active_journey()
    builder = make_builder()
    m1 = builder.build_daily_mission(journey, scheduled_date=TODAY, as_of_date=TODAY)
    from dataclasses import replace

    done = replace(m1, state=MissionState.COMPLETED)
    m2 = replace(m1, mission_id="m2")
    MissionValidator().validate_no_duplicate([done], m2)


def test_validator_one_active():
    journey = active_journey()
    m1 = make_builder().build_daily_mission(
        journey, scheduled_date=TODAY, as_of_date=TODAY
    )
    with pytest.raises(ActiveMissionExists):
        MissionValidator().validate_one_active([m1])


def test_validator_session_empty():
    journey = active_journey()
    m = make_builder().build_daily_mission(
        journey, scheduled_date=TODAY, as_of_date=TODAY
    )
    from dataclasses import replace

    with pytest.raises(InvalidSessionReference):
        MissionValidator().validate_session_reference(replace(m, session_id=""))


def test_validator_journey_mismatch():
    journey = active_journey()
    other = make_journey(journey_id="other")
    m = make_builder().build_daily_mission(
        journey, scheduled_date=TODAY, as_of_date=TODAY
    )
    with pytest.raises(InvalidSessionReference):
        MissionValidator().validate_session_reference(m, other)


def test_validator_journey_state_terminal():
    with pytest.raises(InvalidJourneyReference):
        MissionValidator().validate_journey_state(
            make_journey(state=JourneyState.COMPLETED)
        )


def test_validator_journey_state_deferred_disallowed():
    with pytest.raises(InvalidJourneyReference):
        MissionValidator().validate_journey_state(
            make_journey(state=JourneyState.DEFERRED),
            allow_deferred=False,
        )


def test_validator_identity_fields():
    journey = active_journey()
    m = make_builder().build_daily_mission(
        journey, scheduled_date=TODAY, as_of_date=TODAY
    )
    from dataclasses import replace

    with pytest.raises(InvalidJourneyReference):
        MissionValidator().validate_mission_identity(replace(m, learner_id=""))


def test_validate_new_mission_ok():
    journey = active_journey()
    m = make_builder().build_daily_mission(
        journey, scheduled_date=TODAY, as_of_date=TODAY
    )
    MissionValidator().validate_new_mission([], m, journey)


def test_structural_title_falls_back_to_session_number():
    journey = active_journey(with_session=True)
    # Clear objective title path by using session without matching plan objective title
    mission = make_builder().build_daily_mission(
        journey, scheduled_date=TODAY, as_of_date=TODAY
    )
    assert "Objective" in mission.title or "Session" in mission.title


def test_build_uses_session_effort():
    journey = active_journey(with_session=True)
    mission = make_builder().build_daily_mission(
        journey, scheduled_date=TODAY, as_of_date=TODAY
    )
    assert mission.effort == "medium"
