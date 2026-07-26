"""Unit tests — Journey Coordinator (P2-MS001)."""

from __future__ import annotations

import pytest

from app.application.unified_journey import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_PLACEHOLDER,
    SOURCE_ADAPTIVE,
    SOURCE_RUNTIME_A,
    SOURCE_STRATEGY,
    HomePrimaryMission,
    JourneyContext,
    JourneyContextAssembler,
    JourneyCoordinator,
    JourneyProgress,
    JourneyStage,
    JourneySubsystemInputs,
    NextBestAction,
)


@pytest.fixture
def coordinator() -> JourneyCoordinator:
    return JourneyCoordinator()


def test_current_stage_defaults_to_daily_mission(coordinator):
    assert coordinator.current_stage("42") is JourneyStage.DAILY_MISSION


def test_current_stage_prefers_explicit_hint(coordinator):
    inputs = JourneySubsystemInputs(stage_hint=JourneyStage.REVISION_MODE)
    assert (
        coordinator.current_stage("42", inputs=inputs)
        is JourneyStage.REVISION_MODE
    )


def test_current_stage_passes_through_subsystem_field(coordinator):
    inputs = JourneySubsystemInputs(
        strategy={"journey_stage": "exam_readiness"},
        adaptive={"journey_stage": "revision_mode"},
    )
    # Strategy has priority over Adaptive — pass-through, no recalculation.
    assert (
        coordinator.current_stage("42", inputs=inputs)
        is JourneyStage.EXAM_READINESS
    )


def test_next_action_placeholder_when_no_inputs(coordinator):
    action = coordinator.next_action("42")
    assert action.availability == AVAILABILITY_PLACEHOLDER
    assert action.source == "placeholder"
    assert action.stage is JourneyStage.DAILY_MISSION
    assert action.endpoint == "student.home"


def test_next_action_passes_through_explicit_action(coordinator):
    provided = NextBestAction(
        action_id="strategy.1",
        stage=JourneyStage.PLANNING,
        title="Complete your study plan",
        cta_label="Open plan",
        endpoint="study_plan.index",
        source=SOURCE_STRATEGY,
        availability=AVAILABILITY_AVAILABLE,
    )
    inputs = JourneySubsystemInputs(
        stage_hint=JourneyStage.PLANNING,
        next_action=provided,
    )
    assert coordinator.next_action("42", inputs=inputs) is provided


def test_orchestration_stage_context_next_action(coordinator):
    """Stage → Context → NextBestAction sequence."""
    inputs = JourneySubsystemInputs(
        runtime_a={
            "title": "Practice differentials",
            "why_it_matters": "Builds fluency",
            "expected_outcome": "Higher readiness",
            "estimated_minutes": 30,
            "endpoint": "student.start_session",
            "cta_label": "Start",
        },
        stage_hint=JourneyStage.DAILY_MISSION,
    )
    stage = coordinator.current_stage("42", inputs=inputs)
    context = coordinator.journey_context("42", inputs=inputs)
    action = coordinator.next_action("42", inputs=inputs)
    assert stage is JourneyStage.DAILY_MISSION
    assert context.stage is stage
    assert context.mission_title == "Practice differentials"
    assert context.source == SOURCE_RUNTIME_A
    assert action.title == context.mission_title
    assert action.why_it_matters == context.mission_reason
    assert action.availability == AVAILABILITY_AVAILABLE


def test_next_action_from_opaque_projection_via_context(coordinator):
    inputs = JourneySubsystemInputs(
        adaptive={
            "next_action": {
                "action_id": "adaptive.rev",
                "stage": "revision_mode",
                "title": "Revise Topic A",
                "why_it_matters": "Spaced review window",
                "expected_outcome": "Stronger retention",
                "estimated_minutes": 25,
                "cta_label": "Begin Revision",
            }
        }
    )
    action = coordinator.next_action("42", inputs=inputs)
    assert action.source == SOURCE_ADAPTIVE
    assert action.title == "Revise Topic A"
    assert action.estimated_minutes == 25
    assert action.availability == AVAILABILITY_AVAILABLE
    assert action.stage is JourneyStage.REVISION_MODE
    assert coordinator.current_stage("42", inputs=inputs) is JourneyStage.REVISION_MODE


def test_journey_context_uses_injected_assembler():
    class StubAssembler(JourneyContextAssembler):
        def assemble(self, *, student_id, stage, inputs=None):
            return JourneyContext(
                stage=stage,
                mission_title="stubbed",
                source=SOURCE_RUNTIME_A,
                availability=AVAILABILITY_AVAILABLE,
                unavailable_reason="",
            )

    coordinator = JourneyCoordinator(assembler=StubAssembler())
    context = coordinator.journey_context("42")
    assert context.mission_title == "stubbed"


def test_journey_state_assembles_immutable_dto(coordinator):
    state = coordinator.journey_state("learner-9")
    assert state.student_id == "learner-9"
    assert state.current_stage is JourneyStage.DAILY_MISSION
    assert state.next_action is not None
    assert state.progress is not None
    assert state.availability == AVAILABILITY_PLACEHOLDER


def test_progress_pass_through(coordinator):
    progress = JourneyProgress(
        current_stage=JourneyStage.WEEKLY_REVIEW,
        stages_completed=(JourneyStage.ONBOARDING, JourneyStage.PLANNING),
        label="Week in review",
        ratio=0.4,
        availability=AVAILABILITY_AVAILABLE,
    )
    inputs = JourneySubsystemInputs(
        stage_hint=JourneyStage.WEEKLY_REVIEW,
        progress=progress,
    )
    assert coordinator.progress("42", inputs=inputs) is progress


def test_home_primary_mission_placeholder(coordinator):
    mission = coordinator.home_primary_mission("42")
    assert isinstance(mission, HomePrimaryMission)
    assert mission.availability == AVAILABILITY_PLACEHOLDER
    assert mission.title == "Today's primary mission"
    assert mission.cta_enabled is False
    assert mission.why_it_matters == ""
    assert mission.expected_outcome == ""


def test_home_primary_mission_from_context(coordinator):
    inputs = JourneySubsystemInputs(
        runtime_a={
            "title": "Practice differentials",
            "why_it_matters": "Builds exam-critical fluency",
            "estimated_minutes": 30,
            "expected_outcome": "Higher readiness on Topic B",
            "cta_label": "Start Today's Session",
            "endpoint": "student.start_session",
        }
    )
    mission = coordinator.home_primary_mission("42", inputs=inputs)
    assert mission.title == "Practice differentials"
    assert mission.why_it_matters == "Builds exam-critical fluency"
    assert mission.estimated_duration_label == "30 minutes"
    assert mission.availability == AVAILABILITY_AVAILABLE
    assert mission.cta_enabled is True


def test_home_primary_mission_pass_through(coordinator):
    provided = HomePrimaryMission(
        title="Practice differentials",
        why_it_matters="Builds exam-critical fluency",
        estimated_duration_label="30 minutes",
        expected_outcome="Higher readiness on Topic B",
        cta_label="Start Today's Session",
        cta_enabled=True,
        endpoint="student.start_session",
        stage=JourneyStage.DAILY_MISSION,
        availability=AVAILABILITY_AVAILABLE,
        unavailable_reason="",
    )
    inputs = JourneySubsystemInputs(home_mission=provided)
    assert coordinator.home_primary_mission("42", inputs=inputs) is provided


def test_coordinator_rejects_empty_student_id(coordinator):
    with pytest.raises(ValueError):
        coordinator.current_stage("")


def test_subsystem_inputs_are_frozen_mappings():
    inputs = JourneySubsystemInputs(runtime_a={"a": 1})
    with pytest.raises(TypeError):
        inputs.runtime_a["a"] = 2  # type: ignore[index]


def test_coordinator_does_not_mutate_input_projections(coordinator):
    payload = {"journey_stage": "planning", "next_action": {"title": "Plan"}}
    inputs = JourneySubsystemInputs(strategy=payload)
    coordinator.journey_state("42", inputs=inputs)
    assert payload == {
        "journey_stage": "planning",
        "next_action": {"title": "Plan"},
    }


def test_coordinator_day_experience_and_study_session(coordinator):
    """P2-MS004: DayExperience → StudySession orchestration (presentation only)."""
    from app.application.unified_journey import (
        JourneyEventType,
        SessionControl,
        SessionPhase,
    )

    context = JourneyContext(
        stage=JourneyStage.DAILY_MISSION,
        mission_title="Revise equity",
        mission_reason="High return",
        estimated_duration="20 minutes",
        expected_outcome="Build fluency",
        completion_state="not_started",
        cta_label="Start",
        cta_enabled=True,
        endpoint="student.start_session",
        source=SOURCE_RUNTIME_A,
        availability=AVAILABILITY_AVAILABLE,
        unavailable_reason="",
    )
    inputs = JourneySubsystemInputs(journey_context=context)
    day = coordinator.day_experience("42", inputs=inputs)
    assert day.current_phase is SessionPhase.READY
    assert day.mission_active is True

    session = coordinator.study_session("42", inputs=inputs, day=day)
    assert session.mission_title == "Revise equity"
    assert session.learning_objective == "Build fluency"

    started = coordinator.apply_session_control(
        "42", SessionControl.START, day=day
    )
    assert started.applied is True
    assert started.day_experience.current_phase is SessionPhase.STUDYING
    assert started.event is not None
    assert started.event.event_type is JourneyEventType.SESSION_STARTED

